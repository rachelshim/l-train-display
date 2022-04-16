#!/usr/bin/python3

import time, sys
from train_updater import TrainUpdater, Trip
from train_displayer import TrainDisplayer
import mta_api_key
import constants

if __name__ == "__main__":
	# TODO set up a decent logger
	print("Starting l-train-display...")
	displayer = TrainDisplayer("5x8.bdf")

	try:
		while True:
			displayer.update_display(constants.L_STOPS["L01"], constants.L_STOPS["L29"], 3, 15)
			time.sleep(constants.DISPLAY_SCROLL_SPEED)
		
		except KeyboardInterrupt:
			print("Exiting l-train-display...")
			sys.exit(0)