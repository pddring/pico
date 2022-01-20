# pico
This repo holds micropython and circuitpython files for experiements with the Raspberry Pi Pico with the Pico Explorer board

Micropython examples will need the pimoroni uf2 firmware: https://github.com/pimoroni/pimoroni-pico/releases
Circuitpython examples will need the https://circuitpython.org/board/raspberry_pi_pico/ with adafruit_st7789.mpy adafruit_display_text libraries copied 
to the lib folder as described here: https://www.recantha.co.uk/blog/?p=20820

## scope
This displays an oscilloscope trace on the LCD screen for ADC channels 0, 1, 2 and 3 (temperature)

## motors
This lets you steer a robot buggy with two motors using buttons A/B (motor 1) and X/Y (motor 2)

## games

### Space Invaders
If you connect a joystick up to ADC0 (y) and ADC1 (x) then you can move the space invader player left (x) and shoot (pull down y)