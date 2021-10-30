#!/usr/bin/python3

import time, sys
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from PIL import Image

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = "adafruit-hat"

matrix = RGBMatrix(options=options)

dir_font = graphics.Font()
dir_font.LoadFont("6x10.bdf")
time_font = graphics.Font()
time_font.LoadFont("5x8.bdf")

l_train_color = graphics.Color(167, 169, 172)
white = graphics.Color(255, 255, 255)
font_color = graphics.Color(250, 200, 50)
canvas = matrix.CreateFrameCanvas()

# drawing logo 10x10 pixels
def draw_l_train_logo(x, y):
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


try:
    print("Press CTRL-C to stop.")
    while True:
        draw_l_train_logo(2, 3)
        draw_l_train_logo(2, 18)
        graphics.DrawText(canvas, dir_font, 14, 12, font_color, "MANH")
        graphics.DrawText(canvas, dir_font, 14, 27, font_color, "BKLN")
        graphics.DrawText(canvas, time_font, 42, 12, font_color, "3min")
        graphics.DrawText(canvas, time_font, 42, 27, font_color, "5min")
        canvas = matrix.SwapOnVSync(canvas)

except KeyboardInterrupt:
    sys.exit(0)

