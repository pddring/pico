import picoexplorer as display
import utime
import random

SHOT_WIDTH = 2
SHOT_HEIGHT = 20

NUMBER_OF_ALIENS = 10
ALIEN_WIDTH = 10
ALIEN_HEIGHT = 5

PLAYER_HEIGHT = 10
PLAYER_WIDTH = 10

SHELTER_WIDTH = 15

RELOAD_TIME_MS = 500
MAX_ALIEN_BLASTS = 10
ALIEN_BLAST_SPEED = 2
ALIEN_BLAST_RELOAD_TIME_MS = 500

WIDTH = display.get_width()
HEIGHT = display.get_height()


# delete all items flagged for removal (e.g. an alien that's just been shot)
def cleanup(original_list, items_to_remove):
    for item in items_to_remove:
        if item in original_list:
            original_list.remove(item)

# setup screen
display_buffer = bytearray(WIDTH * HEIGHT * 2)
display.init(display_buffer)

# show startup message
display.set_pen(0,0,0)
display.clear()
display.set_pen(255, 0, 0)
display.text("Space Invaders", 0, 0, 0, 4)
display.update()
utime.sleep(1)

# setup joystick
# plug X into ADC1 and Y into ADC0
# Make sure to also connect ground and 3v3
joystick = [machine.ADC(0), machine.ADC(1)]
print("Width: {}, Height: {}".format(WIDTH, HEIGHT))

# store list of bullets from player going upwards
# each bullet is a list of [x, y]
shots = []
last_fired_player = 0
last_fired_alien = 0

# store list of aliens invading the screen
# each alien is a list of [x, y, direction]
aliens = []

# create aliens at the top of the screen
for i in range(NUMBER_OF_ALIENS):
    aliens.append([i * 20, 0, 1])

# store list of blasts from aliens going down
# each blast is a list of [x, y]
alien_blasts = []

# store list of shelters to hide behind
# each shelter is a list of [x, y, size]
shelters = []

# create shelters at the bottom of the screen
for i in range(6):
    shelters.append([i * 40, HEIGHT - 50, 10])

score = 0

# main game loop (keep looping until you've shot all the aliens)
while len(aliens) > 0:
    # it's not good to remove things from a list whilst iterating through that list
    # these lists keep track of which objects to get rid of at the end of each game loop
    shots_to_remove = []
    aliens_to_remove = []
    alien_blasts_to_remove = []
    shelters_to_remove = []
    
    # read coordinates from joystick
    x = int(joystick[1].read_u16() / 65536 * WIDTH)
    y = int(joystick[0].read_u16() / 65536 * 8)
    
    # pull joystick down to shoot
    if y < 2 and last_fired_player + RELOAD_TIME_MS < utime.ticks_ms():
        shots.append([x, HEIGHT])
        last_fired_player = utime.ticks_ms()
        print("Fire", shots)
    
    # clear screen
    display.set_pen(0,0,0)
    display.clear()
    
    # draw all shelters
    display.set_pen(255, 255, 0)
    for shelter in shelters:
        display.rectangle(shelter[0], shelter[1], SHELTER_WIDTH, shelter[2])
    
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
            
        # draw the alien
        display.rectangle(alien[0], alien[1], ALIEN_WIDTH, ALIEN_HEIGHT)
        
        # check if shot has hit an alien
        for s in shots:
            if s[0] > alien[0] and s[0] - SHOT_WIDTH < alien[0] + ALIEN_WIDTH:
                if s[1] > alien[1] and s[1] - SHOT_HEIGHT < alien[1] + ALIEN_HEIGHT:
                    if s not in shots_to_remove:
                        shots_to_remove.append(s)
                    if alien not in aliens_to_remove:
                        aliens_to_remove.append(alien)
                    score += 1
    
    # draw all shots
    display.set_pen(255,0,0)
    for s in shots:
        s[1] -= 2
        if s[1] > 0:
            display.rectangle(s[0], s[1], SHOT_WIDTH, SHOT_HEIGHT)
        else:
            if s not in shots_to_remove:
                shots_to_remove.append(s)
    
    # make one alien shoot
    shooting_alien = random.choice(aliens)
    if len(alien_blasts) < MAX_ALIEN_BLASTS and last_fired_alien + RELOAD_TIME_MS < utime.ticks_ms():
        alien_blasts.append([shooting_alien[0], shooting_alien[1]])
        last_fired_alien = utime.ticks_ms()
    
    # draw all alien blasts
    display.set_pen(0, 255, 0)
    for blast in alien_blasts:
        display.rectangle(blast[0], blast[1], SHOT_WIDTH, SHOT_HEIGHT)
        
        # check if alien has shot a shelter
        for shelter in shelters:
            if blast[0] + SHOT_WIDTH > shelter[0] and blast[0] < shelter[0] + SHELTER_WIDTH:
                if blast[1] + SHOT_HEIGHT > shelter[1] and blast[1] < shelter[1] + shelter[2]:
                    print("Shelter hit:", blast, shelter)
                    alien_blasts.remove(blast)
                    if shelter[2] > 0:
                        shelter[2] -= 1
                    else:
                        if shelter not in shelters_to_remove:
                            shelters_to_remove.append(shelter)
        
        # check if alien has shot the player
        if blast[0] + SHOT_WIDTH > x and blast[0] < x + PLAYER_WIDTH:
            if blast[1] + SHOT_HEIGHT > y and blast[1] < y + PLAYER_HEIGHT:
                print("Game Over!")
                while True:
                    # End game
                    display.set_pen(0,0,0)
                    display.clear()
                    display.set_pen(255,255,255)
                    display.text("Game Over!", 0, 0, 0, 4)
                    display.update() 
                    utime.sleep(10)
        
        # move player blast up or remove it if it's gone off screen
        if blast[1] < HEIGHT:
            blast[1] += ALIEN_BLAST_SPEED
        else:
            if blast not in alien_blasts_to_remove:
                alien_blasts_to_remove.append(blast)
    
    # draw player and score
    display.set_pen(0,0,255)
    display.rectangle(x, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)    
    display.text("Score: {}".format(score), 0, 0, 0, 2)
    
    # update screen
    display.update()
    
    # remove all objects flagged for removal
    cleanup(shots, shots_to_remove)
    cleanup(aliens, aliens_to_remove)
    cleanup(alien_blasts, alien_blasts_to_remove)
    cleanup(shelters, shelters_to_remove)

# all aliens destroyed! Show winning message
display.set_pen(0,0,0)
display.clear()
display.set_pen(255,255,255)
display.text("You win!", 0, 0, 0, 4)
display.update()