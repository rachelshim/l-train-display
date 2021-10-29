#!/usr/bin/python3

import datetime, requests, time
import gtfs_realtime_pb2, nyct_subway_pb2

URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"
key = "" # add MTA API key here

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

def main():
	while True:
		resp = requests.get(URL, headers={"x-api-key": key})

		timestamp = time.time()

		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(resp.content)

		next_train = {
			"brooklyn": 0,
			"manhattan": 0
		}
		entities = message.entity
		for entity in entities:
			trip = entity.trip_update
			if trip:
				for time_update in trip.stop_time_update:
					arrival = time_update.arrival.time
					if time_update.stop_id == "L08S":	# Brooklyn-bound from Bedford Ave
						next_train["brooklyn"] = arrival if next_train["brooklyn"] == 0 else min(arrival, next_train["brooklyn"])
					elif time_update.stop_id == "L08N":	# Manhattan-bound from Bedford Ave
						next_train["manhattan"] = arrival if next_train["manhattan"] == 0 else min(arrival, next_train["manhattan"])
			else:
				pass # ignore stopped trains

		brooklyn_in = get_arrival_time_string(next_train["brooklyn"])
		manhattan_in = get_arrival_time_string(next_train["manhattan"])
		
		print(parse_timestamp(timestamp))
		print("the next brooklyn-bound train is due at: ", parse_timestamp(next_train["brooklyn"]))
		print("the next manhattan-bound train is due at: ", parse_timestamp(next_train["manhattan"]))
		print("next brooklyn train in: ", brooklyn_in)
		print("next manhattan train in: ", manhattan_in)
		print("\n")

		time.sleep(15)


if __name__ == "__main__":
	main()
