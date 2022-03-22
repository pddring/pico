# Downloading the firmware
First you need to download the relevant UF2 file on to your pico so that it will run python code.
  
Find the relevant file from https://circuitpython.org/board/raspberry_pi_pico/ 

Hold down the bootsel button on the pico whilst plugging it into your computer. It should appear as a USB drive as RPI-RP2
Copy the UF2 file on to the RPI-RP2 drive. The RPI-RP2 drive will disappear when it's finished and instead you'll see a CIRCUITPY USB drive instead. 

If (like me) you're using the pico explorer board from Pimoroni: https://shop.pimoroni.com/products/pico-explorer-base?variant=32369514315859
then you'll want to install some extra libraries to be able to use the screen:

Download the libaries bundle from https://circuitpython.org/libraries and extract the zip archive.
Copy the adafruit_display_text folder from the lib folder from the extracted archive to the lib folder on your CIRCUITPY drive.

Also copy the adafruit_st7789.py file from the lib folder of the extracte arvhive to the lib folder on your CIRCUITPY drive
