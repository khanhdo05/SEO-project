# main.py

# Libraries Initialization
import pygame
import random
from sys import exit
pygame.init()

# Game Window
WIDTH = 1600
HEIGHT = WIDTH * 0.75
TITLE = "Catch Me If You Can"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Background Image
welcome_img = pygame.image.load('graphics/welcome.png')
welcome_img = pygame.transform.scale(welcome_img, (WIDTH, HEIGHT))
instruction_img = pygame.image.load('graphics/instruction.png')
instruction_img = pygame.transform.scale(instruction_img, (WIDTH, HEIGHT))
background_img = pygame.image.load('graphics/background.png')
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
game_over_background = pygame.image.load('graphics/game_over_background.png')
game_over_background = pygame.transform.scale(game_over_background, (WIDTH, HEIGHT))
game_over_screen = pygame.image.load('graphics/game_over_screen.png')
game_over_screen = pygame.transform.scale(game_over_screen, (WIDTH, HEIGHT))

# Heart Image
heart_img = pygame.image.load('graphics/heart.png')
heart_img = pygame.transform.scale(heart_img, (WIDTH*0.05, WIDTH*0.05))
heart_big_img = pygame.transform.scale(heart_img, (WIDTH*0.08125, WIDTH*0.08125))

# Falling object's properties

## Main Object
object_img = pygame.image.load('graphics/coin.png')
object_size = WIDTH // 12
object_img = pygame.transform.scale(object_img, (object_size, object_size))
object_x = random.randint(0, WIDTH - object_size)
object_y = 0 # top of the screen
object_speed = WIDTH * (3 / 400)

## Foul Object 1
foul1_img = pygame.image.load('graphics/object.png')
foul1_size = WIDTH // 12
foul1_img = pygame.transform.scale(foul1_img, (foul1_size, foul1_size))
foul1_speed = WIDTH // 200
foul1_x = random.randint(0, WIDTH - foul1_size)
foul1_y = 0
foul1_falling = False
foul1_score = -1  # Negative score for strawberry

## Foul Object 2
foul2_img = pygame.image.load('graphics/pineapple.png')
foul2_size = WIDTH // 12
foul2_img = pygame.transform.scale(foul2_img, (foul2_size, foul2_size))
foul2_speed = WIDTH // 320
foul2_x = random.randint(0, WIDTH - foul2_size)
foul2_y = 0
foul2_falling = False
foul2_score = -2  # More negative score for pineapple

# Power Up
power_img = pygame.image.load('graphics/power.png')
power_size = WIDTH // 15
power_img = pygame.transform.scale(power_img, (power_size, power_size))
power_speed = WIDTH * (3 / 320)
power_x = random.randint(0, WIDTH - power_size)
power_y = 0
power_falling = False
power_score = -2  # More negative score for pineapple

# Player's properties
player_img = pygame.image.load('graphics/player.png')
player_size = WIDTH // 10
player_img = pygame.transform.scale(player_img, (player_size, player_size))
player_x = WIDTH // 2                 # middle
player_y = HEIGHT - player_size - (WIDTH * (83/800)) # ground
player_speed = player_size

# Other
clock = pygame.time.Clock()
score = 0
heart = 3

# Font
game_over_font = pygame.font.Font('font/Pixelify_Sans/static/PixelifySans-Bold.ttf', int(WIDTH / 8))
pixel_font = pygame.font.Font('font/VT323/VT323-Regular.ttf', int(WIDTH * (11 / 80)))
pixel_small_font = pygame.font.Font('font/VT323/VT323-Regular.ttf', int(WIDTH * (17 / 160)))
pixel_smaller_font = pygame.font.Font('font/VT323/VT323-Regular.ttf', int(WIDTH * (9 / 160)))
regular_font = pygame.font.Font('font/Roboto/Roboto-Medium.ttf', int(WIDTH / 16))
regular_small_font = pygame.font.Font('font/Roboto/Roboto-Medium.ttf', int(WIDTH * (7 / 160)))

# Load the music file
background_music = pygame.mixer.music.load('audio/background_music.mp3')
hehe_music = pygame.mixer.Sound('audio/hehe.mp3')
game_over_sound = pygame.mixer.Sound('audio/lose.mp3')
lose_p_sound = pygame.mixer.Sound('audio/lose_p.mp3')
earn_sound = pygame.mixer.Sound('audio/earn.mp3')
boost_sound = pygame.mixer.Sound('audio/boost.mp3')

# Play the boost sound:
def play_boost_sound():
    boost_sound.play()

# Play the earn sound
def play_earn_sound():
    earn_sound.play()

#Play lose point sound
def play_lose_sound():
    lose_p_sound.play()

# Play the lose sound when lose
def play_go_sound():
    game_over_sound.play()

# Play the sound for hehe screen
def play_hehe_sound():
    hehe_music.play()

background_music
pygame.mixer.music.play(-1)  # Play in an infinite loop

# Set the volume (0.0 to 1.0, where 0.0 is silent and 1.0 is full volume)
volume_level = 0.3  # Adjust this value to set the desired volume level
pygame.mixer.music.set_volume(volume_level)

def reset_game():
    global score, heart, object_speed, player_speed, object_y, foul1_falling, foul1_y, foul2_falling, foul2_y, power_falling, power_y
    score = 0
    heart = 3
    object_speed = WIDTH * (3/ 320)
    player_speed = player_size
    object_y = 0
    foul1_falling = False
    foul1_y = 0
    foul1_x = random.randint(0, WIDTH - foul1_size)
    foul2_falling = False
    foul2_y = 0
    foul2_x = random.randint(0, WIDTH - foul2_size)
    power_falling = False
    power_y = 0
    power_x = random.randint(0, WIDTH - power_size)

# States
WELCOME_STATE = 0
INSTRUCTION_STATE = 1
PLAY_STATE = 2
GAME_OVER_STATE = 3
HEHE = 4

# Initial state
current_state = WELCOME_STATE

# Welcome Screen
while current_state == WELCOME_STATE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            current_state = INSTRUCTION_STATE
    screen.blit(welcome_img, (0, 0))
   
    pygame.display.flip()
    clock.tick(30)

# Instruction Screen
while current_state == INSTRUCTION_STATE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            current_state = PLAY_STATE
    screen.blit(instruction_img, (0, 0))
   
    pygame.display.flip()
    clock.tick(30)
            
# Main Game Loop
is_paused = False # Pause Flag
while current_state == PLAY_STATE:

    for event in pygame.event.get():
        # Quit action
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        # Game logic when pressed keys
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()
            if event.key == pygame.K_SPACE:
                if is_paused:
                    is_paused = False
                else:
                    is_paused = True
            if event.key == pygame.K_LEFT:
                player_x -= player_speed
            if event.key == pygame.K_RIGHT:
                player_x += player_speed
    
    # Draws a new screen
    screen.blit(background_img, (0, 0))

    # Update object's position
    if is_paused == False:
        object_y += object_speed
        if object_y >= HEIGHT - player_size:
            heart -= 1
            object_y = 0
            object_x = random.randint(0, WIDTH - object_size)  
            object_speed += WIDTH // 800
    
    # Randomly drop foul1
    if (score >= 20) and random.randint(0, 8000) == 0 and not foul1_falling:
        foul1_falling = True
        foul1_x = random.randint(0, WIDTH - foul1_size)

    # Update foul1's position
    if is_paused == False:
        foul1_y += foul1_speed
        if foul1_y >= HEIGHT - player_size:
            foul1_falling = False
            foul1_y = 0
            foul1_x = random.randint(0, WIDTH - foul1_size)

    # Randomly drop foul2
    if (score >= 25) and random.randint(0, 8000) == 0 and not foul2_falling:
        foul2_falling = True
        foul2_x = random.randint(0, WIDTH - foul2_size)

    # Update foul2's position
    if is_paused == False:
        foul2_y += foul2_speed
        if foul2_y >= HEIGHT - player_size:
            foul2_falling = False
            foul2_y = 0
            foul2_x = random.randint(0, WIDTH - foul2_size)
    
    # Randomly drop power
    if (score % 5 == 0) and (score >= 10) and random.randint(0, 8000) == 0 and not power_falling:
        power_falling = True
        power_x = random.randint(0, WIDTH - power_size)

    # Update power's position
    if is_paused == False:
        power_y += power_speed
        if power_y >= HEIGHT - player_size:
            power_falling = False
            power_y = 0
            power_x = random.randint(0, WIDTH - power_size)
    
    # Collision Check
    if player_y + (WIDTH * (83 / 800)) < object_y + object_size and object_x < player_x + player_size and player_x < object_x + object_size:
        score += 1
        play_earn_sound()
        object_y = 0
        object_x = random.randint(0, WIDTH - object_size)  
        object_speed += 1

    # Collision Check for Foul1
    if player_y + (WIDTH * (83 / 800)) < foul1_y + foul1_size and foul1_x < player_x + player_size and player_x < foul1_x + foul1_size:
        score += foul1_score
        play_lose_sound()
        foul1_falling = False
        foul1_y = 0

    # Collision Check for Foul2
    if player_y + (WIDTH * (83 / 800)) < foul2_y + foul2_size and foul2_x < player_x + player_size and player_x < foul2_x + foul2_size:
        score += foul2_score
        play_lose_sound()
        foul2_falling = False
        foul2_y = 0

    # Collision Check for Power
    if player_y + (WIDTH * (83 / 800)) < power_y + power_size and power_x < player_x + player_size and player_x < power_x + power_size:
        player_speed += WIDTH // 320
        play_boost_sound()
        power_falling = False
        power_y = 0

    # Boundaries Check
    if player_x < 0:
        player_x = 0
    elif player_x + player_size > WIDTH - player_size:
        player_x = WIDTH - player_size

    # Text
    if is_paused == False:
        screen.blit(heart_img, (WIDTH - (WIDTH / 8), WIDTH * (11 / 320)))
        text = regular_font.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(text, (70, 30))
        heart_count = regular_font.render(":"+ str(heart), True, (0, 0, 0))
        screen.blit(heart_count, (WIDTH - (WIDTH * (23 / 320)), WIDTH * (19 / 800)))
    else:
        text_paused = regular_font.render("Paused. Press Space to Resume", True, (0, 0, 0))
        screen.blit(text_paused, (WIDTH / 2 - (WIDTH / 2.2), HEIGHT / 2.5))

    # Lose!
    if heart == 0:
        play_go_sound()
        current_state = GAME_OVER_STATE

    # Drawing
    screen.blit(object_img, (object_x, object_y))
    screen.blit(player_img, (player_x, player_y))
    screen.blit(foul1_img, (foul1_x, foul1_y))
    screen.blit(foul2_img, (foul2_x, foul2_y))
    screen.blit(power_img, (power_x, power_y))

    # Renew screen
    pygame.display.flip()

    # Frames per sec
    clock.tick(30)

pygame.mixer.music.stop()

# Game Over Screen
while current_state == GAME_OVER_STATE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                reset_game()
                current_state = PLAY_STATE
            elif event.key == pygame.K_l:
                current_state = HEHE
                pygame.mixer.music.stop()
                play_hehe_sound()

    screen.blit(game_over_screen, (0, 0))
    over_text = game_over_font.render("GAME OVER", True, (251, 194, 7))
    screen.blit(over_text, (WIDTH / 2 - (WIDTH * (5 / 16)), HEIGHT / 2 - (WIDTH / 8)))
    play_again_text = regular_small_font.render("Press SPACE to Play Again", True, (255, 255, 255))
    screen.blit(play_again_text, (WIDTH / 2 - (WIDTH / 4), HEIGHT / 2 + (WIDTH / 16)))
    next_text = regular_small_font.render("Press 'L' to Accept the L :)", True, (255, 255, 255))
    screen.blit(next_text, (WIDTH / 2 - (WIDTH / 4), HEIGHT / 2 + (WIDTH / 8)))

    pygame.display.flip()
    clock.tick(30)

# Wait a minute!
while current_state == HEHE:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                exit()

    game_over_text = pixel_font.render("HAPPY BIRTHDAT", True, (252, 43, 113))
    press_to_quit = pixel_font.render("YAYYYYYY?", True, (252, 43, 113))
    dear = pixel_small_font.render("TO:____", True, (251, 194, 7))
    happy = pixel_smaller_font.render("Happy birthday lol lol lol lol True, (251, 194, 7))
    score_final = pixel_smaller_font.render("X" + str(score), True, (252, 43, 113))
    screen.blit(game_over_background, (0, 0))
    screen.blit(game_over_text, (WIDTH / 2 - (WIDTH * (3 / 8)), HEIGHT / 2 - (WIDTH / 8)))
    screen.blit(press_to_quit, (WIDTH / 2 - (WIDTH * (21 / 80)), HEIGHT / 2))
    screen.blit(dear, (WIDTH / 2 - (WIDTH * (3 / 20)), (WIDTH * (13 / 160))))
    screen.blit(happy, (WIDTH / 2 - (WIDTH * (3 / 8)), HEIGHT - (WIDTH * (11 / 80))))
    screen.blit(score_final, (WIDTH * (7 / 32), WIDTH * (9 / 80)))
    screen.blit(heart_big_img, (WIDTH / 8, WIDTH / 10))
    screen.blit(player_img, (WIDTH * 0.75, (WIDTH *  (29/320))))
    pygame.display.flip()
