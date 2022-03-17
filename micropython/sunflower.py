# import modules
from machine import Pin, PWM
import picoexplorer as display
import utime
import random

start_time = utime.time()
minutes = int(start_time / 60) % (60)
hours = int(start_time / (60*60)) % 24
seconds = start_time % 60
modes = ["manual 1", "manual 2", "time hour", "time minutes", "clock"]
mode = 4

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

sunrise = [6,14]
sunset = [18,11]

# move servo
def setServo (servo, angle):
    position = int(2000+(angle / 180) * 6000)
    servo.duty_u16(position)
    utime.sleep(0.01)

# loop forever
while True:
    # calculate how far through the day we are
    day_seconds = seconds + (((hours * 60) + minutes) * 60)
    sun_rise_seconds = ((sunrise[0] * 60) + sunrise[1]) * 60
    sun_set_seconds = ((sunset[0] * 60) + sunset[1]) * 60
    
    day_length = sun_set_seconds - sun_rise_seconds
    day_progress = (day_seconds - sun_rise_seconds) / day_length
    if day_progress < 0:
        day_progress = 0
    if day_progress > 1:
        day_progress = 1
    
    
    # fill the screen yellow
    display.set_pen(255, 255, 0)
    display.clear()         

    # draw title
    display.set_pen(0, 0, 0)
    display.text("Sunflower", 0, 0, 240, 5)
    
    # draw bar to show how far through the day we are
    display.set_pen(255,0,0)
    display.rectangle(0, 50, int(240 * day_progress), 10)
    
    display.set_pen(0,0,0)
    
    # manually control servo 1
    if mode == 0:
            
        # move the servos if the button is pressed
        if display.is_pressed(display.BUTTON_A):
            display.text("A", 0, 50, 240, 8)
            if angle1>0:
                angle1-=2
        elif display.is_pressed(display.BUTTON_B):
            display.text("B", 0, 150, 240, 8)
            if angle1<180:
                angle1+=2
            
    
    # manually control servo 2
    elif mode == 1:
        # move the servos if the button is pressed
        if display.is_pressed(display.BUTTON_A):
            display.text("A", 0, 50, 240, 8)
            if angle2 > 0:
                angle2 -= 2
        elif display.is_pressed(display.BUTTON_B):
            display.text("B", 0, 150, 240, 8)
            if angle2<180:
                angle2 += 2
            
    # manually control hours
    elif mode == 2:
        if display.is_pressed(display.BUTTON_A):
            display.text("A", 0, 50, 240, 8)
            hours += 1
            if hours > 23:
                hours = 0
        elif display.is_pressed(display.BUTTON_B):
            display.text("B", 0, 150, 240, 8)
            hours -= 1
            if hours < 0:
                hours = 23
            
    # manually control minutes
    elif mode == 3:
        if display.is_pressed(display.BUTTON_A):
            display.text("A", 0, 50, 240, 8)
            minutes += 1
            if minutes > 59:
                minutes = 0
                hours += 1
                if hours > 23:
                    hours = 0
        elif display.is_pressed(display.BUTTON_B):
            display.text("B", 0, 150, 240, 8)
            minutes -= 1
            if minutes < 0:
                minutes = 59
                hours -= 1
                if hours < 0:
                    hours = 23
    # clock mode
    elif mode == 4:
        time = utime.time()
        minutes = int(time / 60) % 60
        hours = int(time / (60*60)) % 24
        seconds = time % 60
        
    # next control mode
    if display.is_pressed(display.BUTTON_X):
        display.text("X", 200, 50, 240, 8)
        if mode < len(modes) - 1:
            mode += 1
    
    # previous control mode
    elif display.is_pressed(display.BUTTON_Y):
        display.text("Y", 200, 150, 240, 8)
        if mode > 0:
            mode -= 1
            
    # update angles (as long as we're not in manual mode)
    if mode > 1:
        angle1 = day_progress * 180
        angle2 = abs(0.5 - day_progress) * 90
            
    display.text("S1: {:} S2: {:}".format(int(angle1), int(angle2)), 0, 200, 240, 2)
    display.text("{:02d}:{:02d}".format(hours, minutes), 20, 120, 140, 7)
    display.text("{:02d}".format(seconds), 190, 150, 140, 2)
    display.text(modes[mode], 0, 220, 240, 2)
    display.update()
    
    setServo(servo1, angle1)
    setServo(servo2, angle2)
    utime.sleep(0.1)

