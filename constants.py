#!/usr/bin/python3

MTA_API_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"

BEDFORD_AV_NORTH = "L08N"
BEDFORD_AV_SOUTH = "L08S"

L_STOPS = {
	"L01": "8 Av",
	"L02": "6 Av",
	"L03": "14 St-Union Sq",
	"L05": "3 Av",
	"L06": "1 Av",
	"L08": "Bedford Av",
	"L10": "Lorimer St",
	"L11": "Graham Av",
	"L12": "Grand St",
	"L13": "Montrose Av",
	"L14": "Morgan Av",
	"L15": "Jefferson St",
	"L16": "DeKalb Av",
	"L17": "Myrtle-Wyckoff Avs",
	"L19": "Halsey St",
	"L20": "Wilson Av",
	"L21": "Bushwich Av-Aberdeen St",
	"L22": "Broadway Junction",
	"L24": "Atlantic Av",
	"L25": "Sutter Av",
	"L26": "Livonia Av",
	"L27": "New Lots Av",
	"L28": "East 105 St",
	"L29": "Canarsie-Rockaway Pkwy"
}


# constants for TrainDisplayer

FONT_WIDTH = 5
FONT_HEIGHT = 8

DISPLAY_SCROLL_SPEED = 0.05
TEXT_HOLD_TIME_SECONDS = 2.5 

# the space between the wrap-around for the text, in pixels
TEXT_SPACER = 12

# display is a 64x32 LED board.
# assuming pixels at positions [0, 63], across the x-axis we have the pixels
# set up as follows:
# [0, 1] spacer
# [2, 11] train logo
# [12, 13] spacer
# [14, 49] text
# [50, 51] spacer
# [52, 61] time in min
# [62, 63] spacer

# every section that's not part of the scrolling text must be cleared
VERTICAL_SPACERS = [
	(0, 13),
	(50, 63)
]

L_LOGO_X = 2
L_LOGO_Y_TOP = 3
L_LOGO_Y_BOTTOM = 18

TEXT_MARGIN_LEFT = 14
TEXT_MARGIN_RIGHT = 50

MIN_X = 52
MIN_Y_TOP = 11
MIN_Y_BOTTOM = 27

TOP_Y_POS = 11
BOTTOM_Y_POS = 27
