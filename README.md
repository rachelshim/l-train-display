# l-train-display
taking the L

This project is Python software for an LED matrix display for the next trains for the L train at Bedford Avenue.
It is is very basic; it just checks the closest trains in each direction (Manhattan-bound and Brooklyn-bound) for the L train at Bedford Avenue.
It uses the [MTA's GTFS Realtime feed](https://api.mta.info/#/landing) and [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library.

I relied heavily on [this tutorial](https://howchoo.com/pi/raspberry-pi-led-matrix-panel) to set up the LED matrix and the Rapberry Pi.

## Notes
When reviewing the code please keep in mind that the vast majority of it was written between the hours of 1am and 3am

### Tests
If it breaks it breaks 😔🤟

### Materials
Here's the stuff I used (and spent too much money on). Everything is from Adafruit:
- 64x32 RGB LED Matrix 5mm pitch
- mini magnet feet for the LED display
- 5V 4A (4000 mA) switching power supply
- 16 GB SD Card (the one I bought has Buster Lite pre-installed)
- Raspberry Pi Zero with headers
- Adafruit RGB Matrix Bonnet for Raspberry Pi

In total it runs about $100-150.

### Setup
If you would like to set up something similar, or if you happen to also live near the Bedford Av stop, here are a few guidelines for setup:
1. Assemble your materials. Setup the board and pi with the [tutorial](https://howchoo.com/pi/raspberry-pi-led-matrix-panel) mentioned above.
2. Request an [MTA API key](https://api.mta.info/#/landing).
3. Clone this repo and the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) repo; install requirements.
4. In the `l_train_display/` directory:
    - `vim mta_api_key`
    - add the line: `key = "<your-mta-api-key-here>"`
5. Set up the pi to run the display on startup. I did so by editing `rc.local`:
    - `sudo vim /etc/rc.local`
    - add this line: `cd /home/pi/l-train-display && make run`

### Future work
- error handling: pretty sure that if wifi is bad the loop blocks on the API call. maybe add timeouts?
- store expected times for the next _n_ trains (as opposed to next train) to fall back on in an error scenario, i.e. when call to API fails or returns empty data
- fix logging (this is mainly due to the fact that i've never used real logging in python)
- the display shows 0 whenever the train is <30 seconds away or `arrival time - current time < 0`. Should show the actual next train time as opposed to "current" train which has left the station. This is because when going through the list of train arrivals, it looks for the earliest one and sometimes (by the time we get the data) the earliest one has already left the station. Storing arrival times for _n_ trains rather than just one should help with this.
- show next 2 trains, as opposed to showing just the next train. might require some thinking on how to display this, the LED board is kind small.
- make L train logo look nicer. right now it's very blocky (and kind of ratch -- uses a loop to color pixels; this probably could've been done with DrawCircle, or something).
- rewrite the whole thing in golang (lmao)
