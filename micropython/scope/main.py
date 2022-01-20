# Simple oscilloscope for a Raspberry Pi Pico
# Press the buttons to toggle the traces
# Designed for use with an pcio explorer board
import picoexplorer as display
import machine
import utime

# set up screen buffer and ADC
WIDTH = display.get_width()
HEIGHT = display.get_height()
display_buffer = bytearray(WIDTH * HEIGHT * 2)
display.init(display_buffer)

# Clear screen and draw title
display.set_pen(0,0,0)
display.clear()
display.set_pen(255, 0, 0)
display.text("PicoScope", 0, 0, 0, 2)

# Get 4 channels of Analogue to Digital converters
adc = []
for i in range(4):
    adc.append(machine.ADC(i))
    
# Colours to display each ADC chanenl
colors = [(255, 0, 0), # Red, channel 0
          (0, 255, 0), # Green, channel 1
          (0, 0, 255), # Blue, channel 2
          (0, 255, 255)] # Cyan channel  3

# button label names to display on screen to toggle traces
button_names = ["A", "B", "X", "Y"]

# button IDs for checking if they're pressed
buttons = [display.BUTTON_A, display.BUTTON_B, display.BUTTON_X, display.BUTTON_Y]

# Only enable ADC0 on startup
enabled = [1,0,0,0]

# needed to draw lines rather than dots
previous_values = [HEIGHT, HEIGHT, HEIGHT, HEIGHT]

# show all channel names
for i in range(4):
    display.set_pen(*colors[i])
    display.text(button_names[i], 128 + (i*22), 0, 1, 1)

# x coordinate of trace goes from 0 (left) to the width of the screen then back to 0
x = 0

# ADC values are stored as 16 bit values (2^16 = 65535). First 20 pixels are used for the title
scale_factor = (HEIGHT - 20) / 65535

# loop forever
while True:
    # clear current x position of screen in black
    display.set_pen(0,0,0)
    display.rectangle(128,20,WIDTH - 128, 10)
    display.rectangle(x, 20, 1, HEIGHT)
    
    # loop through each ADC channel and toggle 
    for i in range(4):
        # toggle ADC channel enabled if button is pressed
        if display.is_pressed(buttons[i]):
            while display.is_pressed(buttons[i]):
                utime.sleep(0.1)
            enabled[i] = not enabled[i]
        
        # draw channel name in black if disabled, or in correct colour if enabled
        if enabled[i]:
            display.set_pen(*colors[i])
            
            # draw trace
            value = adc[i].read_u16()
            y = int(HEIGHT - (value * scale_factor))
            display.rectangle(x, min(previous_values[i],y), 1, abs(y - previous_values[i])+1)
            voltage = "{:.2f}".format(value * 3.3 / 65536)
            display.text(voltage, 128+(i*22), 20, 1, 1)
            previous_values[i] = y 
        else:
            display.set_pen(0,0,0)
        display.text("ADC" + str(i), 128 + (i*22), 10, 1, 1)
    
    # move on to next x coordinate (or back to start)
    x = (x + 1) % WIDTH
    display.update()