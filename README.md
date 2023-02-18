# l-train-display
Check it out in action [here](https://photos.app.goo.gl/rtn8anErWDMFe5kMA)!

taking the L

This project is Python software for an LED matrix display for the next trains for the L train at Bedford Avenue.
It just checks the trains in each direction (Manhattan-bound and Brooklyn-bound) for the L train at Bedford Avenue using the [MTA's GTFS Realtime feed](https://api.mta.info/#/landing), and uses the [rpi-rgb-led-matrix](https://github.com/hzeller/rpi-rgb-led-matrix) library to update the LED Matrix.

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
- WIP ~~store expected times for the next _n_ trains (as opposed to next train) to fall back on in an error scenario, i.e. when call to API fails or returns empty data~~
- one thread to grab times from API and one thread to update display doesn't really work. this is because the display update thread is used for scrolling the text, and if there's a blip there can be weird text scrolling for a bit (noticed recently it showed two halves of different station names). really it should be something like:
    * one thread to grab times from API
    * one thread to scroll text display
    * possibly a different thread, definitely a different method at least, that gets the latest updated data from the shared map that's populated by the API thread above. so that the scroll text display thread finishes scrolling (or stops scrolling to show a new terminus).
   
  All of this is probably confusing. what I mean is -- scrolling logic should be separate from deciding what text to display on the screen.
- fix logging (this is mainly due to the fact that i've never used real logging in python)
- WIP ~~the display shows 0 whenever the train is <30 seconds away or `arrival time - current time < 0`. Should show the actual next train time as opposed to "current" train which has left the station. This is because when going through the list of train arrivals, it looks for the earliest one and sometimes (by the time we get the data) the earliest one has already left the station. Storing arrival times for _n_ trains rather than just one should help with this.~~
- WIP ~~show next 2 trains, as opposed to showing just the next train. might require some thinking on how to display this, the LED board is kind small.~~
- make L train logo look nicer. right now it's very blocky (and kind of ratch -- uses a loop to color pixels; this probably could've been done with DrawCircle, or something).
- display issues: space is an issue. Maybe when the terminus station to display in text is longer than the allotted area, use a smaller font? The comma looks ugly af also when displaying two times.
- [anti-flicker mod](https://learn.adafruit.com/adafruit-rgb-matrix-bonnet-for-raspberry-pi/driving-matrices#step-2995409)
- rewrite the whole thing in golang (lmao)
