#!/usr/bin/python3

import requests
import gtfs_realtime_pb2
import nyct_subway_pb2
from google.protobuf import text_format
import time
import datetime

URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"
key = "" # add MTA API key here

def main():
	while True:
		resp = requests.get(URL, headers={"x-api-key": key})

		timestamp = time.time()

		message = gtfs_realtime_pb2.FeedMessage()
		message.ParseFromString(resp.content)

		closest_train = {
			"brooklyn": 0,
			"manhattan": 0
		}
		entities = message.entity
		for entity in entities:
			trip = entity.trip_update
			if trip:
				for time_update in trip.stop_time_update:
					arrival_time = time_update.arrival.time
					if time_update.stop_id == "L08S":	# brooklyn-bound bedford
						closest_train["brooklyn"] = arrival_time if closest_train["brooklyn"] == 0 else min(arrival_time, closest_train["brooklyn"])
					elif time_update.stop_id == "L08N":	# manhattan-bound beford
						closest_train["manhattan"] = arrival_time if closest_train["manhattan"] == 0 else min(arrival_time, closest_train["manhattan"])
			else:
				pass #TODO

		next_brooklyn_train = datetime.datetime.fromtimestamp(closest_train["brooklyn"]).strftime("%Y-%m-%d %H:%M:%S")
		next_manhattan_train = datetime.datetime.fromtimestamp(closest_train["manhattan"]).strftime("%Y-%m-%d %H:%M:%S")

		now = time.time()
		brooklyn_time = round((closest_train["brooklyn"] - now)/60)
		manhattan_time = round((closest_train["manhattan"] - now)/60)
		
		if closest_train["brooklyn"] == 0 or brooklyn_time < -5:
			b_min = "--"
		elif brooklyn_time < 1:
			b_min = "Now"
		else:
			b_min = str(brooklyn_time) + "min"

		if closest_train["manhattan"] == 0 or manhattan_time < -5:
			m_min = "--"
		elif manhattan_time < 1:
			m_min = "Now"
		else:
			m_min = str(manhattan_time) + "min"
		
		print("checked at: ", datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S"))
		print("the next brooklyn-bound train is due at: ", next_brooklyn_train)
		print("the next manhattan-bound train is due at: ", next_manhattan_train)
		print("next brooklyn train in: ", b_min)
		print("next manhattan train in: ", m_min)
		print("\n")

		time.sleep(30)


if __name__ == "__main__":
	main()
