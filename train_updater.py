#!/usr/bin/python3
import requests
import gtfs_realtime_pb2, nyct_subway_pb2
from enum import Enum
import constants

class Direction(Enum):
    NORTH = 1
    SOUTH = 3

class Trip(object):
    def __init__(self, terminus, direction, next_train):
        self.terminus = terminus
        self.direction = direction
        self.next_train = next_train

class TrainUpdater:
    def __init__(self, url, key):
        self.URL = url
        self.key = key

    # get_next_trains pings the MTA API for the most up-to-date train arrivals at Bedford Ave
    def get_next_trains(self):
        try:
            resp = requests.get(self.URL, headers={"x-api-key": self.key})

            message = gtfs_realtime_pb2.FeedMessage()
            message.ParseFromString(resp.content)

            trips_to_bedford = []

            # parse through all the trips listed in this message
            entities = message.entity
            for entity in entities:
                trip_update = entity.trip_update
                if trip_update:
                    parsed_trip = self.parse_trip_update(trip_update)
                    if parsed_trip:
                        trips_to_bedford.append(parsed_trip)

            return self.parse_trips_to_bedford(trips_to_bedford)
        except Exception as e:
            print("exception", e)
            return None, None


    # parse_trip_update parses a trip_update entity in the GTFS feed response.
    # if the trip specified in the trip_update stops at Bedford Av, it returns
    # a Trip object. If the trip_update does not stop at Bedford Av, it returns None.
    def parse_trip_update(self, trip_update):
        direction = trip_update.trip.Extensions[nyct_subway_pb2.nyct_trip_descriptor].direction
        final_stop_id = ""
        max_stop_sequence = 0
        next_train_at_bedford = 0

        for stop_time_update in trip_update.stop_time_update:
            if stop_time_update.stop_sequence > max_stop_sequence:
                max_stop_sequence = stop_time_update.stop_sequence
                final_stop_id = stop_time_update.stop_id
            if stop_time_update.stop_id == constants.BEDFORD_AV_NORTH or stop_time_update.stop_id == constants.BEDFORD_AV_SOUTH:
                next_train_at_bedford = stop_time_update.arrival.time

        if next_train_at_bedford == 0:
            return None
        else:
            return Trip(final_stop_id, direction, next_train_at_bedford)


    # parse_trips_to_bedford returns the soonest trips in each direction (North and South)
    # that stops at Bedford Av.
    # if there are no trips to be found for one of the directions, return None for that direction.
    def parse_trips_to_bedford(self, trips_to_bedford):
        northbound_trips = filter(lambda x: x.direction == Direction.NORTH.value, trips_to_bedford)
        southbound_trips = filter(lambda x: x.direction == Direction.SOUTH.value, trips_to_bedford)

        sorted_northbound_trips = sorted(northbound_trips, key=lambda x: x.next_train)
        sorted_southbound_trips = sorted(southbound_trips, key=lambda x: x.next_train)

        next_northbound_train = sorted_northbound_trips[0] if len(sorted_northbound_trips) > 0 else None
        next_southbound_train = sorted_southbound_trips[0] if len(sorted_southbound_trips) > 0 else None

        return (next_northbound_train, next_southbound_train)
