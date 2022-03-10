# morse code translator for a raspberry pi pico with a pico explorer
# connect the AUDIO speaker to the GP0 pin
import utime
import picoexplorer as explorer

# Set up and initialise Pico Explorer
HEIGHT = explorer.get_height()
WIDTH = explorer.get_width()
buf = bytearray(WIDTH * HEIGHT * 2)
explorer.init(buf)

# tells Pico Explorer which pin you'll be using for noise
explorer.set_audio_pin(0)

TONE_FREQUENCY = 880
DURATION_DOT = 0.1
DURATION_DASH = 0.5
DURATION_SYMBOL = 0.1
DURATION_CHARACTER = 1
DURATION_WORD = 2

SPEED = 2

LINE_SPACING = 20

morse = {
    "a": ".-",
    "b":"-...",
    "c":"-.-.",
    "d":"-..",
    "e":".",
    "f":"..-.",
    "g":"--.",
    "h":"....",
    "i":"..",
    "j":"---.",
    "k":"-.-",
    "l":".-..",
    "m":"--",
    "n":"-.",
    "o":"---",
    "p":".--.",
    "q":"--.-",
    "r":".-.",
    "s":"...",
    "t":"-",
    "u":"..-",
    "v":"...-",
    "w":".--",
    "x":"-..-",
    "y":"-.--",
    "z":"--..",
    }


def clear():                        # this function clears Pico Explorer's screen to black
    explorer.set_pen(0, 0, 0)
    explorer.clear()
    
def send(msg):
    global morse
    y = LINE_SPACING * 2
    for letter in msg:
        letter = letter.lower()
        print(letter)
        if letter in morse:
            symbols = morse[letter]
            
            explorer.text(letter + ": " + symbols, 0, y, 256, 3)
            y += LINE_SPACING
            if y >= HEIGHT:
                clear()
                y = 0
                explorer.set_pen(255,0,0)
            explorer.update()
            
            for symbol in symbols:
                print(symbol, sep="")
                if symbol == ".":
                    explorer.set_tone(TONE_FREQUENCY)
                    utime.sleep(DURATION_DOT / SPEED)
                    explorer.set_tone(-1)
                elif symbol == "-":
                    explorer.set_tone(TONE_FREQUENCY)
                    utime.sleep(DURATION_DASH / SPEED)
                    explorer.set_tone(-1)
                utime.sleep(DURATION_SYMBOL / SPEED)
            utime.sleep(DURATION_CHARACTER / SPEED)
        else:
            print("/")
            utime.sleep(DURATION_WORD / SPEED)

clear()
explorer.set_pen(255,0,0)
explorer.text("Morse Code", 0,0,256,4)
explorer.update()

msg = "Raspberry Pi Pico Morse Code"
send(msg)
