import picoexplorer as display
import utime

SHOT_WIDTH = 2
SHOT_HEIGHT = 20

ALIEN_WIDTH = 10
ALIEN_HEIGHT = 5

RELOAD_TIME_MS = 500

WIDTH = display.get_width()
HEIGHT = display.get_height()
display_buffer = bytearray(WIDTH * HEIGHT * 2)
display.init(display_buffer)

display.set_pen(0,0,0)
display.clear()
display.set_pen(255, 0, 0)
display.text("Space Invaders", 0, 0, 0, 4)
display.update()
utime.sleep(1)

joystick = [machine.ADC(0), machine.ADC(1)]
print("Width: {}, Height: {}".format(WIDTH, HEIGHT))

# store list of bullets from player going upwards
# each bullet is a list of [x, y]
shots = []
last_fired = 0

# store list of aliens invading the screen
# each alien is a list of [x, y, direction]
aliens = []

for i in range(10):
    aliens.append([i * 20, 0, 1])


while len(aliens) > 0:
    # read coordinates from joystick
    x = int(joystick[1].read_u16() / 65536 * WIDTH)
    y = int(joystick[0].read_u16() / 65536 * 8)
    print(x, y)
    
    # pull joystick down to shoot
    if y < 2 and last_fired + RELOAD_TIME_MS < utime.ticks_ms():
        shots.append([x, HEIGHT])
        last_fired = utime.ticks_ms()
        print("Fire", shots)
    
    # clear screen
    display.set_pen(0,0,0)
    display.clear()
    
    # draw all aliens
    display.set_pen(0,255,0)
    for alien in aliens:
        # move right
        if alien[2] == 1:
            if alien[0] < WIDTH:
                alien[0] += 1
            else:
                alien[1] += 10
                alien[2] = 0
        # move left
        else:
            if alien[0] > 0:
                alien[0] -= 1
            else:
                alien[1] += 10
                alien[2] = 1
            
        display.rectangle(alien[0], alien[1], ALIEN_WIDTH, ALIEN_HEIGHT)
        
        # check if hit
        for s in shots:
            if s[0] > alien[0] and s[0] - SHOT_WIDTH < alien[0] + ALIEN_WIDTH:
                if s[1] > alien[1] and s[1] - SHOT_HEIGHT < alien[1] + ALIEN_HEIGHT:
                    try:
                        aliens.remove(alien)
                    except:
                        pass
    
    # draw all shots
    display.set_pen(255,0,0)
    for s in shots:
        s[1] -= 2
        if s[1] > 0:
            display.rectangle(s[0], s[1], SHOT_WIDTH, SHOT_HEIGHT)
        else:
            shots.remove(s)
    
    # draw player
    display.set_pen(0,0,255)
    display.rectangle(x, HEIGHT - 10, 10, 10)
    
    # update screen
    display.update()

# all aliens destroyed! Show winning message
display.set_pen(0,0,0)
display.clear()
display.set_pen(255,255,255)
display.text("You win!", 0, 0, 0, 4)
display.update()