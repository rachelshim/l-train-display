#!/usr/bin/python3

import time, sys, threading, logging
from train_updater import TrainUpdater, Trip, Direction
from train_displayer import TrainDisplayer
import mta_api_key
import constants

updater = TrainUpdater(constants.MTA_API_URL, mta_api_key.key)
displayer = TrainDisplayer("5x8.bdf")

lock = threading.Lock()
next_trains_trip = {
    "North": None,
    "South": None
}

def parse_arrival_time(arrival):
    now = time.time()
    arrival_in_min = round((arrival - now)/60)
    if arrival_in_min < -5:
        return "-"
    else:
        return str(arrival_in_min)

def parse_trips_and_update_display():
    while True:
        lock.acquire()
        trip_north = next_trains_trip["North"]
        trip_south = next_trains_trip["South"]
        lock.release()

        north_stop = "No Trains"
        south_stop = "No Trains"
        north_time = "-"
        south_time = "-"
        if trip_north is not None:
            north_stop = constants.L_STOPS[trip_north.terminus[:-1]]
            north_time = parse_arrival_time(trip_north.next_train)
        if trip_south is not None:
            south_stop = constants.L_STOPS[trip_south.terminus[:-1]]
            south_time = parse_arrival_time(trip_south.next_train)

        displayer.update_display(north_stop, south_stop, north_time, south_time)
        time.sleep(constants.DISPLAY_SCROLL_SPEED)

def update_next_trains():
    while True:
        train_north, train_south = updater.get_next_trains()
        lock.acquire()
        next_trains_trip["North"] = train_north
        next_trains_trip["South"] = train_south
        lock.release()

        time.sleep(constants.TRAIN_UPDATE_RATE_SECONDS)


if __name__ == "__main__":
    # TODO set up a decent logger
    logging.basicConfig(filename='main.log', level=logging.INFO)
    logging.info("Starting l-train-display...")

    try:
        display_thread = threading.Thread(target=parse_trips_and_update_display)
        update_thread = threading.Thread(target=update_next_trains)
        display_thread.setDaemon(True)
        update_thread.setDaemon(True)

        display_thread.start()
        update_thread.start()
        while True:
            pass

    except KeyboardInterrupt:
        display_thread.stop()
        update_thread.stop()
        logging.info("Exiting l-train-display...")
        sys.exit(0)