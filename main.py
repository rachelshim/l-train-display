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

def parse_singular_arrival_time(arrival):
    now = time.time()
    arrival_in_min = round((arrival - now)/60)
    return str(arrival_in_min)

def parse_arrival_times(first_arrival, second_arrival):
    now = time.time()
    first_arrival_in_min = round((first_arrival - now)/60)
    second_arrival_in_min = round((second_arrival - now)/60)
    if first_arrival_in_min > 9 or second_arrival_in_min > 9:
        return str(first_arrival_in_min)
    return str(first_arrival_in_min) + "," + str(second_arrival_in_min)

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
            # TODO clean this up and refactor out so there's no duplication
            # loop to find next most trip that's after current time.
            for x in range(len(trips_north)):
                trip = trips_north[x]
                if trip.next_train > time.time():
                    north_stop = constants.L_STOPS[trip.terminus[:-1]]  # need to strip string: L01N -> L01
                    north_time = parse_arrival_time(trip.next_train)

                    # if north_time is less than 2 characters, we can display two times
                    if len(north_time) < 2 and north_time != "-":
                        if x + 1 < len(trips_north):
                            second_north_time = parse_arrival_time(trips_north[x + 1].next_train)
                            if len(second_north_time) < 2 and second_north_time != "-":
                                north_time = north_time + "," + second_north_time

        if trips_south:
            for trip in trips_south:
                if trip.next_train > time.time():
                    south_stop = constants.L_STOPS[trips_south.terminus[:-1]]   # need to strip string: L01S -> L01
                    south_time = parse_arrival_time(trips_south.next_train)

        displayer.update_display(north_stop, south_stop, north_time, south_time)
        time.sleep(constants.DISPLAY_SCROLL_SPEED)

def update_next_trains():
    while True:
        trains_north, trains_south = updater.get_next_trains()
        with lock:
            if trains_north:
                next_trains_trips["North"] = trains_north
            if trains_south:
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
