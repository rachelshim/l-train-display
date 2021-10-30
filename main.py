#!/usr/bin/python3

import time, sys
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from TrainUpdater import get_next_trains

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
ont_color = graphics.Color(250, 200, 50)


canvas = matrix.CreateFrameCanvas()

# drawing 10x10 L train logo
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

def run():
    print("Press CTRL-C to stop.")
    while True:

    	manhattan_in, brooklyn_in = get_next_trains()

        draw_l_train_logo(2, 3)
        draw_l_train_logo(2, 18)
        graphics.DrawText(canvas, dir_font, 14, 12, font_color, "MANH")
        graphics.DrawText(canvas, dir_font, 14, 27, font_color, "BKLN")
        graphics.DrawText(canvas, time_font, 37, 12, font_color, manhattan_in)
        graphics.DrawText(canvas, time_font, 42, 27, font_color, brooklyn_in)
        canvas = matrix.SwapOnVSync(canvas)

        time.sleep(15)


if __name__ == "__main__":
	try:
		run()
	except KeyboardInterrupt:
		print("Exiting l-train-display\n")
		sys.exit(0)