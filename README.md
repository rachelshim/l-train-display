# l-train-display
taking the L

This project is Python software for an LED matrix display for the next trains for the L train at Bedford Avenue.
The software is very basic; it just checks the closest trains in each direction (Manhattan-bound and Brooklyn-bound) for the L train at Bedford Avenue.
It uses the [MTA's GTFS Realtime feed](https://api.mta.info/#/landing) and [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.

I relied heavily on [this tutorial](https://howchoo.com/pi/raspberry-pi-led-matrix-panel) to set up the LED matrix and the Rapberry Pi.

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

