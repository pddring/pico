# import modules
from machine import Pin, PWM
import picoexplorer as display
import utime
import random

# set up screen
buf = bytearray(display.get_width() * display.get_height() * 2)
display.init(buf)

# set up servos
servo1 = PWM(Pin(0))
servo1.freq(50)

servo2 = PWM(Pin(1))
servo2.freq(50)

angle1 = 90
angle2 = 90

# move servo
def setServo (servo, angle):
    position = int(2000+(angle / 180) * 6000)
    servo.duty_u16(position)
    utime.sleep(0.01)

# loop forever
while True:
    
    # fill the screen yellow
    display.set_pen(255, 255, 0)
    display.clear()         

    # draw title
    display.set_pen(0, 0, 0)
    display.text("Sunflower", 0, 0, 240, 5)
    
    # move the servos if the button is pressed
    if display.is_pressed(display.BUTTON_A):
        display.text("A", 0, 50, 240, 8)
        if angle1<180:
            angle1+=2
    elif display.is_pressed(display.BUTTON_B):
        display.text("B", 0, 150, 240, 8)
        if angle1>0:
            angle1-=2
        
    if display.is_pressed(display.BUTTON_X):
        display.text("X", 200, 50, 240, 8)
        if angle2<180:
            angle2+=2
    elif display.is_pressed(display.BUTTON_Y):
        display.text("Y", 200, 150, 240, 8)
        if angle2>0:
            angle2-=2
    display.text("S1: {} S2: {}".format(angle1, angle2), 0, 200, 240, 2)
    display.update()
    setServo(servo1, angle1)
    setServo(servo2, angle2)
    utime.sleep(0.1)

