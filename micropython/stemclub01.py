import picoexplorer as display
import time
import random

buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)

while True:
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    
    display.set_pen(red, green, blue)
    display.clear()         
    
    display.set_pen(0, 0, 0)
    display.text("STEM Club", 25, 20, 240, 6)
    display.text("\\o/ \\o/ \\o/ \\o/ \\o/ \\o/ \\o/ \\o/ \\o/", 25, 120, 240, 4)
    display.update()
    time.sleep(1)
