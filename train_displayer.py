#!/usr/bin/python3

from math import floor
from typing import NamedTuple
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import constants

class Color(NamedTuple):
    # TODO: use everywhere
    red: int
    green: int
    blue: int

BACKGROUND = Color(red=0, green=0, blue=0)
BORDER = Color(red=0, green=255, blue=0)

class TrainDisplayer:
    def __init__(self, font):

        # set up canvas
        options = RGBMatrixOptions()
        options.rows = 32
        options.cols = 64
        options.chain_length = 1
        options.parallel = 1
        options.hardware_mapping = "adafruit-hat"
        self.matrix = RGBMatrix(options=options)
        self.canvas = self.matrix.CreateFrameCanvas()

        # set up font
        self.font = graphics.Font()
        self.font.LoadFont(font)
        self.font_color = graphics.Color(250, 200, 50)

        # we need to keep track of 4 positions where text is --
        # two positions for the top (Manhattan) text, and two for bottom (Brooklyn).
        # this is so that we can have text wrapping around while scrolling.
        # we also need to keep track of the hold, in refresh rate
        self.top_text_pos = {
            "pos_A": constants.TEXT_MARGIN_LEFT,
            "pos_B": None,
            "hold": constants.TEXT_HOLD_TIME_SECONDS/constants.DISPLAY_SCROLL_SPEED
        }
        self.bottom_text_pos = {
            "pos_A": constants.TEXT_MARGIN_LEFT,
            "pos_B": None,
            "hold": constants.TEXT_HOLD_TIME_SECONDS/constants.DISPLAY_SCROLL_SPEED
        }


    def draw_l_train_logo(self, x, y):
        for j in range(3):
            offset = j + 1
            for i in range(offset, 10 - offset):
                self.canvas.SetPixel(x + i, y + 2 - j, 117, 119, 122)
                self.canvas.SetPixel(x + i, y + 8 + j, 117, 119, 122)
        for j in range(3, 8):
            for i in range(10):
                if i == 4:
                    self.canvas.SetPixel(x + i, y + j, 255, 255, 255)
                elif j == 7 and (i == 5 or i == 6):
                    self.canvas.SetPixel(x + i, y + j, 255, 255, 255)
                else:
                    self.canvas.SetPixel(x + i, y + j, 117, 119, 122)


    # draws black rectangle for a vertical section of the matrix
    # essentially, clearing the board for a subsection.
    def draw_vertical_spacer(self, left, right):
        for y in range(0, 32):
            for x in range(left, right + 1):
                self.canvas.SetPixel(x, y, 0, 0, 0)


    def display_scrolling_text(self, text, pos_map, pos_y):
        len_top_A = graphics.DrawText(self.canvas, self.font, pos_map["pos_A"], pos_y, self.font_color, text)
        len_top_B = graphics.DrawText(self.canvas, self.font, pos_map["pos_B"], pos_y, self.font_color, text)

        if pos_map["hold"] > 0:
            pos_map["hold"] -= 1
        elif pos_map["pos_A"] + len_top_A + constants.TEXT_SPACER < constants.TEXT_MARGIN_LEFT + 2:
            # idk why the offset by 2 is needed but that's for future Rachel to figure out
            pos_map["hold"] = constants.TEXT_HOLD_TIME_SECONDS/constants.DISPLAY_SCROLL_SPEED
            pos_map["pos_B"] -= 1
            pos_map["pos_A"] = pos_map["pos_B"] + constants.TEXT_SPACER + constants.FONT_WIDTH * len(text)
        elif pos_map["pos_B"] + len_top_B + constants.TEXT_SPACER < constants.TEXT_MARGIN_LEFT + 2:
            pos_map["hold"] = constants.TEXT_HOLD_TIME_SECONDS/constants.DISPLAY_SCROLL_SPEED
            pos_map["pos_A"] -= 1
            pos_map["pos_B"] = pos_map["pos_A"] + constants.TEXT_SPACER + constants.FONT_WIDTH * len(text)
        else:
            pos_map["pos_A"] -= 1
            pos_map["pos_B"] -= 1

    def draw_moving_border(self, progress: float, color: Color):
        # TODO proper constants
        WIDTH = 64
        HEIGHT = 32

        # remove two from each column to avoid double counting corners
        total_pixels = 2 * WIDTH + 2 * (HEIGHT - 2)
        pixels_so_far = int(floor(total_pixels * progress))

        for pixel in range(pixels_so_far):
            x = 0
            y = 0
            if pixel < WIDTH:
                # top row
                x = pixel
                y = 0
            elif pixel < WIDTH + HEIGHT - 2:
                # right column
                x = WIDTH - 1
                y = 1 + pixel - WIDTH
            elif pixel < 2 * WIDTH + HEIGHT - 2:
                # bottom row
                offset = pixel - WIDTH - (HEIGHT - 2)
                x = WIDTH - 1 - offset
                y = HEIGHT - 1
            else:
                # left column
                offset = pixel - 2 * WIDTH - (HEIGHT - 2)
                y = (HEIGHT - 2) - offset
            self.canvas.SetPixel(x, y, color.red, color.green, color.blue)

    def update_display(self, top_text, bottom_text, top_min, bottom_min, age_ticks: int):
        self.canvas.Clear()

        # we have to draw the display in order: text, then vertical spacers, then next train time, then logo.
        # this is because the color of each pixel can be overwritten before it's displayed.
        # there's not a way to limit the area of the scrolling text, so we get around this by painting
        # black pixels (which essentially means empty LEDs on the matrix) around the areas we want the text to not be displayed.

        # first check if top/bottom text is long enough to warrant scrolling
        # draw text
        if constants.FONT_WIDTH * len(top_text) > constants.TEXT_MARGIN_RIGHT - constants.TEXT_MARGIN_LEFT:
            if self.top_text_pos["pos_B"] is None:
                self.top_text_pos["pos_B"] = self.top_text_pos["pos_A"] + constants.TEXT_SPACER + constants.FONT_WIDTH * len(top_text)
            self.display_scrolling_text(top_text, self.top_text_pos, constants.TOP_Y_POS)
        else:
            graphics.DrawText(self.canvas, self.font, constants.TEXT_MARGIN_LEFT, constants.TOP_Y_POS, self.font_color, top_text)

        if constants.FONT_WIDTH * len(bottom_text) > constants.TEXT_MARGIN_RIGHT - constants.TEXT_MARGIN_LEFT:
            if self.bottom_text_pos["pos_B"] is None:
                self.bottom_text_pos["pos_B"] = self.bottom_text_pos["pos_A"] + constants.TEXT_SPACER + constants.FONT_WIDTH * len(bottom_text)
            self.display_scrolling_text(bottom_text, self.bottom_text_pos, constants.BOTTOM_Y_POS)
        else:
            graphics.DrawText(self.canvas, self.font, constants.TEXT_MARGIN_LEFT, constants.BOTTOM_Y_POS, self.font_color, bottom_text)

        # draw spacers. for more info, see constants.py
        for spacer in constants.VERTICAL_SPACERS:
            self.draw_vertical_spacer(spacer[0], spacer[1])

        # draw logo
        self.draw_l_train_logo(constants.L_LOGO_X, constants.L_LOGO_Y_TOP)
        self.draw_l_train_logo(constants.L_LOGO_X, constants.L_LOGO_Y_BOTTOM)

        # draw min to next train
        graphics.DrawText(self.canvas, self.font, constants.MIN_X, constants.MIN_Y_TOP, self.font_color, top_min)
        graphics.DrawText(self.canvas, self.font, constants.MIN_X, constants.MIN_Y_BOTTOM, self.font_color, bottom_min)

        progress_toward_update = age_ticks * constants.DISPLAY_SCROLL_SPEED / constants.TRAIN_UPDATE_RATE_SECONDS
        if progress_toward_update * 2.0 < 1.0:
            self.draw_moving_border(progress=progress_toward_update * 2.0, color=BORDER)
        else:
            # draw green border then paint over it
            self.draw_moving_border(progress=1.0, color=BORDER)
            self.draw_moving_border(progress=2.0*(progress_toward_update - 0.5), color=BACKGROUND)

        self.canvas = self.matrix.SwapOnVSync(self.canvas)

