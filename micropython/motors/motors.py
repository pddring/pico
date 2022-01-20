import time, random
import picoexplorer as explorer

# set up screem
WIDTH = explorer.get_width()
HEIGHT = explorer.get_height()
display_buffer = bytearray(WIDTH * HEIGHT * 2)  # 2-bytes per pixel (RGB565)
explorer.init(display_buffer)

# main loop (forever)
while True:
    # clear screen and display controle
    explorer.set_pen(0,0,0)
    explorer.rectangle(0, 0, WIDTH, HEIGHT)
    explorer.set_pen(0,0,255)
    explorer.text("A/B Motor 1", 0, 0, WIDTH, 4)
    explorer.text("X/Y Motor 2", 0, 50, WIDTH, 4)

    # Press A/B to control motor 1
    if explorer.is_pressed(explorer.BUTTON_A):
        explorer.set_motor(0, 0, 1)
        explorer.text("Motor 1 Forwards", 0, 100, WIDTH, 2)
    elif explorer.is_pressed(explorer.BUTTON_B):
        explorer.set_motor(0, 1, 1)
        explorer.text("Motor 1 Backwards", 0, 100, WIDTH, 2)
    else:
        explorer.set_motor(0, 0, 0)
    
    
    # Press X/Y to control motor 2
    if explorer.is_pressed(explorer.BUTTON_X):
        explorer.set_motor(1, 0, 1)
        explorer.text("Motor 2 Forwards", 0, 150, WIDTH, 2)
    elif explorer.is_pressed(explorer.BUTTON_Y):
        explorer.set_motor(1, 1, 1)
        explorer.text("Motor 2 Backwards", 0, 150, WIDTH, 2)
    else:
         explorer.set_motor(1, 0, 0)
    
    # update screen and slow down main loop
    time.sleep(0.1)
    explorer.update()

