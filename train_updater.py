#!/usr/bin/python3

import datetime, requests, time
import gtfs_realtime_pb2, nyct_subway_pb2
import logging

URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"
key = "" # add MTA API key here

# set up logging
logging.basicConfig(filename="trains.log", level=logging.DEBUG)

def get_arrival_time_string(arrival):
	now = time.time()
	train_in = round((arrival - now)/60)
	if train_in < -5:
		return "--"
	elif train_in < 1:
		return "Now"
	else:
		return str(train_in) + "min"

def parse_timestamp(timestamp):
	return datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def get_next_trains():
	logging.basicConfig(filename="trains.log", l)
	try:
		resp = requests.get(URL, headers={"x-api-key": key})

		timestamp = time.time()

		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(resp.content)

		next_train = {
			"manhattan": 0,
			"brooklyn": 0
		}
		entities = message.entity
		for entity in entities:
			trip = entity.trip_update
			if trip:
				for time_update in trip.stop_time_update:
					arrival = time_update.arrival.time
					if time_update.stop_id == "L08N":	# Manhattan-bound from Bedford Ave
						next_train["manhattan"] = arrival if next_train["manhattan"] == 0 else min(arrival, next_train["manhattan"])
					elif time_update.stop_id == "L08S":	# Brooklyn-bound from Bedford Ave
						next_train["brooklyn"] = arrival if next_train["brooklyn"] == 0 else min(arrival, next_train["brooklyn"])
			else:
				pass # ignore stopped trains

		manhattan_in = get_arrival_time_string(next_train["manhattan"])
		brooklyn_in = get_arrival_time_string(next_train["brooklyn"])
		
		logging.info("the next manhattan-bound train is due at: ", parse_timestamp(next_train["manhattan"]))
		logging.info("the next brooklyn-bound train is due at: ", parse_timestamp(next_train["brooklyn"]))
		logging.info("next manhattan train in: ", manhattan_in)
		logging.info("next brooklyn train in: ", brooklyn_in)

		return manhattan_in, brooklyn_in

	except Exception as e:
		logging.error(e)
		return "--", "--"
