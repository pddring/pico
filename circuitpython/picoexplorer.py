# pico explorer circuit python compatability module
import os
import board
import time
import terminalio
import displayio
import busio
import digitalio
from adafruit_display_text import label
import adafruit_st7789


# Release any resources currently in use for the displays
displayio.release_displays()

tft_cs = board.GP17
tft_dc = board.GP16
spi_mosi = board.GP19
spi_clk = board.GP18

spi = busio.SPI(spi_clk, MOSI=spi_mosi)

display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
display = adafruit_st7789.ST7789(display_bus,
                    width=240, height=240,
                    rowstart=80, colstart=0)
display.rotation = 180

# Make the display context
splash = displayio.Group()
color_bitmap = displayio.Bitmap(240, 240, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x0000FF
bg_sprite = displayio.TileGrid(color_bitmap,
                               pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)
display.show(splash)

print("test")

# constants
BUTTON_A = 0
BUTTON_B = 1
BUTTON_X = 2
BUTTON_Y = 3

# create buttons
buttons = [ digitalio.DigitalInOut(board.GP12),
            digitalio.DigitalInOut(board.GP13),
            digitalio.DigitalInOut(board.GP14),
            digitalio.DigitalInOut(board.GP15)]

# set buttons to inputs with pullup resistor
for b in buttons:
    b.switch_to_input(pull = digitalio.Pull.UP)

def is_pressed(button):
    return not buttons[button].value


def test():
    while True:
        time.sleep(1)
        print(is_pressed(BUTTON_A))
def get_width():
    return 240

def get_height():
    return 240

def init(buf):
    print("Starting...")

def set_pen(r, g, b):
    print("Set pen not implemented yet")

def clear():
    print("Clear not implemented yet")

def update():
    print("Update not implemented yet")

def text(string, x, y, wrap, scale):
    print("Text not implemented yet")