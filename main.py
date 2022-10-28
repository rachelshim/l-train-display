#!/usr/bin/python3

import time, sys, threading
from train_updater import TrainUpdater, Trip, Direction
from train_displayer import TrainDisplayer
import mta_api_key
import constants

updater = TrainUpdater(constants.MTA_API_URL, mta_api_key.key)
displayer = TrainDisplayer("5x8.bdf")

lock = threading.Lock()
next_trains_trips = {
    "North": [],
    "South": []
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
        with lock:
            trips_north = next_trains_trips["North"]
            trips_south = next_trains_trips["South"]

        north_stop = "No Trips"
        south_stop = "No Trips"
        north_time = "-"
        south_time = "-"

        if trips_north:
            # loop to find next most trip that's after current time.
            for trip in trips_north:
                if trip.next_train > time.time():
                    north_stop = constants.L_STOPS[trip.terminus[:-1]]
                    north_time = parse_arrival_time(trip.next_train)
        if trips_south:
            for trip in trips_south:
                if trip.next_train > time.time():
                    south_stop = constants.L_STOPS[trips_south.terminus[:-1]]
                    south_time = parse_arrival_time(trips_south.next_train)

        displayer.update_display(north_stop, south_stop, north_time, south_time)
        time.sleep(constants.DISPLAY_SCROLL_SPEED)

def update_next_trains():
    while True:
        trains_north, trains_south = updater.get_next_trains()
        with lock:
            next_trains_trips["North"] = trains_north
            next_trains_trips["South"] = trains_south

        time.sleep(constants.TRAIN_UPDATE_RATE_SECONDS)


if __name__ == "__main__":
    # TODO set up a decent logger
    print("Starting l-train-display...")

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
        print("Exiting l-train-display...")
        sys.exit(1)
