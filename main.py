#!/usr/bin/python3

import time, sys
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from train_updater import TrainUpdater
import mta_api_key
import logging

URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l"

# set up logging
logging.basicConfig(filename="main.log", level=logging.DEBUG)

# drawing 10x10 L train logo
def draw_l_train_logo(x, y, canvas):
    for j in range(3):
        offset = j + 1
        for i in range(offset, 10 - offset):
            canvas.SetPixel(x + i, y + 2 - j, 117, 119, 122)
            canvas.SetPixel(x + i, y + 8 + j, 117, 119, 122)
    for j in range(3, 8):
        for i in range(10):
            if i == 4:
                canvas.SetPixel(x + i, y + j, 255, 255, 255)
            elif j == 7 and (i == 5 or i == 6):
                canvas.SetPixel(x + i, y + j, 255, 255, 255)
            else:
                canvas.SetPixel(x + i, y + j, 117, 119, 122)

def get_arrival_time_string(arrival):
    now = time.time()
    train_in = round((arrival - now)/60)
    if train_in < -5:
        return "--"
    elif train_in < 1:
        return "Now"
    else:
        return str(train_in)

def run():
    logging.info("Starting l-train-display.")

    train_updater = TrainUpdater(URL, mta_api_key.key)

    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 64
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = "adafruit-hat"

    matrix = RGBMatrix(options=options)

    dir_font = graphics.Font()
    dir_font.LoadFont("5x8.bdf")
    time_font = graphics.Font()
    time_font.LoadFont("5x8.bdf")

    l_train_color = graphics.Color(167, 169, 172)
    font_color = graphics.Color(250, 200, 50)

    canvas = matrix.CreateFrameCanvas()

    while True:
        manh, bkln = train_updater.get_next_trains()
        canvas.Clear()

        # manh_terminus = manh.terminus if manh else "manh"
        # bkln_terminus = bkln.terminus if bkln else "bkln"

        # TODO: check for manh/bkln not being None

        # scratch work for displaying terminus
        manh_stop_id = manh.terminus[:-1]
        manh_terminus = constants.L_STOPS[stop_id]
        bkln_stop_id = bkln.terminus[:-1]
        bkln_terminus = constants.L_STOPS[stop_id]

        manh_next_train = get_arrival_time_string(manh.next_train)
        bkln_next_train = get_arrival_time_string(bkln.next_train)

        draw_l_train_logo(2, 3, canvas)
        draw_l_train_logo(2, 18, canvas)
        graphics.DrawText(canvas, dir_font, 14, 12, font_color, manh_terminus)
        graphics.DrawText(canvas, dir_font, 14, 27, font_color, bkln_terminus)

        manhattan_offset = 62 - len(manh_next_train) * 5
        brooklyn_offset = 62 - len(bkln_next_train) * 5

        graphics.DrawText(canvas, time_font, manhattan_offset, 12, font_color, manh_next_train)
        graphics.DrawText(canvas, time_font, brooklyn_offset, 27, font_color, bkln_next_train)
        canvas = matrix.SwapOnVSync(canvas)

        time.sleep(30)


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        logging.info("Exiting l-train-display\n")
        sys.exit(0)
        
