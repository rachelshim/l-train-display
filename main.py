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

# parse_trips parses all of the trips in a singular direction.
# returns the texts to display: terminus and minutes to next train.
def parse_trips(trips):
    next_stop = "No Trips"
    next_time = "-"
    for x in range(len(trips)):
        trip = trips[x]
        now = time.time()
        if trip.next_train > now:
            next_stop = constants.L_STOPS[trip.terminus[:-1]]   # need to strip string, e.g. L01N -> L01

            if x + 1 < len(trips):
                next_time = parse_arrival_times(trip.next_train, trips[x + 1].next_train)
            else:
                next_time = parse_singular_arrival_time(trip.next_train)

    return next_stop, next_time

# update_display grabs the trip data from the map, parses the trips, and updates the display.
def update_display():
    while True:
        with lock:
            trips_north = next_trains_trips["North"]
            trips_south = next_trains_trips["South"]

        north_stop, north_time = parse_trips(trips_north) if trips_north else ("No Trips", "-")
        south_stop, south_time = parse_trips(trips_south) if trips_south else ("No Trips", "-")

        displayer.update_display(north_stop, south_stop, north_time, south_time)
        time.sleep(constants.DISPLAY_SCROLL_SPEED)


# update_next_trains updates the map with the latest from the API response.
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
        display_thread = threading.Thread(target=update_display)
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
