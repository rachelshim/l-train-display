# l-train-display
taking the L

This project is Python software for an LED matrix display for the next trains for the L train at Bedford Avenue.
The software is very basic; it just checks the closest trains in each direction (Manhattan-bound and Brooklyn-bound) for the L train at Bedford Avenue.
It uses the [MTA's GTFS Realtime feed](https://api.mta.info/#/landing) and [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.

I relied heavily on [this tutorial](https://howchoo.com/pi/raspberry-pi-led-matrix-panel) to set up the LED matrix and the Rapberry Pi.

### Notes
The code is rough right now. I'll clean it up sometime later.

### Tests
There are no tests because I am lazy. If it breaks it breaks 😔🤟

### Materials
Here's the stuff I used (and spent too much money on). Everything is from Adafruit:
- 64x32 RGB LED Matrix 5mm pitch
- mini magnet feet for the LED display
- 5V 4A (4000 mA) switching power supply
- 16 GB SD Card (the one I bought has Buster Lite pre-installed)
- Raspberry Pi Zero with headers
- Adafruit RGB Matrix Bonnet for Raspberry Pi
In total it runs about $100-150.

### Future work
- error handling: pretty sure that if wifi is bad the loop blocks on the API call. maybe add timeouts?
- store expected times for the next _n_ trains (as opposed to next train) to fall back on in an error scenario, i.e. when call to API fails or returns empty data
- fix logging (this is mainly due to the fact that i've never used real logging in python)
- the display shows "Now" whenever the train is <30 seconds away or `arrival time - current time < 0`. Should show the actual next train time as opposed to "current" train which has left the station. This is because when going through the list of train arrivals, it looks for the earliest one and sometimes (by the time we get the data) the earliest one has already left the station. Storing arrival times for _n_ trains rather than just one should help with this.
- run updating board and calling API to grab train data on two separate threads, so we can update the board faster (e.g. 10 seconds) than what we're limited by the API (20-30 seconds)
