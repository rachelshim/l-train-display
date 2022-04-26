#!/usr/bin/python3

import threading
import time, sys
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from train_updater import TrainUpdater, Trip
import mta_api_key
import logging
import constants

NEXT_TRAINS = {
    "Northbound": Trip(None, None, None),
    "Southbound": Trip(None, None, None)
}
lock = threading.Lock()

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
    else:
        return str(train_in)

# updates dict of train times
def get_updated_trains(train_updater):
    while True:
        manh, bkln = train_updater.get_next_trains()
        lock.acquire()
        NEXT_TRAINS["Northbound"] = manh
        NEXT_TRAINS["Southbound"] = bkln
        lock.release()
    time.sleep(20)

# updates display. reads from dict of train times
def update_display():
    canvas.Clear()

    lock.acquire()
    manh = NEXT_TRAINS["Northbound"]
    bkln = NEXT_TRAINS["Southbound"]
    lock.release()

    # manh_terminus = manh.terminus if manh else "manh"
    # bkln_terminus = bkln.terminus if bkln else "bkln"

    # TODO: check for manh/bkln not being None

    # scratch work for displaying terminus
    manh_stop_id = manh.terminus[:-1]
    manh_terminus = constants.L_STOPS[manh_stop_id]
    bkln_stop_id = bkln.terminus[:-1]
    bkln_terminus = constants.L_STOPS[bkln_stop_id]

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

    time.sleep(1)


if __name__ == "__main__":
    # set up logging
    logging.basicConfig(filename="main.log", level=logging.DEBUG)
    train_updater = TrainUpdater(constants.MTA_API_URL, mta_api_key.key)


    logging.info("Starting l-train-display.")

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

    pos_manh = 14
    pos_bkln = 14

    manh_hold = 50
    bkln_hold = 50

    manh_text = "14 St-Union Sq"
    buffer_text = 15

    pos_A = 14
    pos_B = pos_A + buffer_text + 5*len(manh_text)

    try:
        # display_thread = threading.Thread(target=update_display, name="display_thread")
        while True:
            canvas.Clear()

            len_A = graphics.DrawText(canvas, dir_font, pos_A, 11, font_color, manh_text)
            len_B = graphics.DrawText(canvas, dir_font, pos_B, 11, font_color, manh_text)

            if manh_hold > 0:
                manh_hold -= 1
            elif pos_A + len_A + buffer_text < 15:
                manh_hold = 50
                pos_B -= 1
                pos_A = pos_B + buffer_text + 5*len(manh_text)
            elif pos_B + len_B + buffer_text < 15:
                manh_hold = 50
                pos_A -= 1
                pos_B = pos_A + buffer_text + 5*len(manh_text)
            else:
                pos_A -= 1
                pos_B -= 1
            # manh_len = graphics.DrawText(canvas, dir_font, pos_manh, 11, font_color, "14 St-Union Sq")
            # bkln_len = graphics.DrawText(canvas, dir_font, pos_bkln, 27, font_color, "Canarsie-Rockaway Pkwy")
            

            # if manh_hold > 0:
            #     pos_manh = 14
            #     manh_hold -= 1
            # elif pos_manh + manh_len < 14:
            #     pos_manh = 14
            #     manh_hold = 40
            # else:
            #     pos_manh -= 1

            # if bkln_hold > 0:
            #     pos_bkln = 14
            #     bkln_hold -= 1
            # elif pos_bkln + bkln_len < 14:
            #     pos_bkln = 14
            #     bkln_hold = 40
            # else:
            #     pos_bkln -= 1
            
            for y in range(0, 32):
                for x in range(0, 14):
                    canvas.SetPixel(x, y, 0, 0, 0)

            draw_l_train_logo(2, 3, canvas)
            draw_l_train_logo(2, 18, canvas)
            time.sleep(0.05)
            canvas = matrix.SwapOnVSync(canvas)

    except KeyboardInterrupt:
        logging.info("Exiting l-train-display\n")
        sys.exit(0)
        