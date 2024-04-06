# main.py

# Libraries Initialization
import pygame
import random
from enum import Enum
from sys import exit
pygame.init()

# Define Constants
TITLE = "Name of our game"
WIDTH = 1600
HEIGHT = WIDTH * 0.75
MID_X = WIDTH / 2
MID_Y = WIDTH / 2
GROUND_Y = HEIGHT - (WIDTH // 10) - (WIDTH * (83/800)) # For the current graphic
HEART_COUNT = 3 # Player starts off with 3 hearts
SCORE = 0 # Total number of points player earns

# Type of item enum
class ItemType(Enum):
    GOOD = "Good" 
    BAD = "Bad"
    BONUS = "Bonus"

# GameEntity as Parent Class
class GameEntity(pygame.sprite.Sprite):
    def __init__(self, image_path, position, scale_size, speed):
        ''' Notes:
            + image_path should follow the form: "assets/graphics/FILE_NAME.png"
            + position: (x,y) to place the image on the screen
            + scale_size: (x,y) as desired width and height of the image
            + speed: a number that references the width in scale_size
        '''
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, scale_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.speed = speed

    def move_horizontally(self):
        self.rect.x += self.speed
    
    def move_vertically_down(self):
        self.rect.y -= self.speed
        
    def draw(self, screen, img):
        screen.blit(img, (self.x, self.y))

# Player as Child Class of GameEntity
class Player(GameEntity):
    def __init__(self, position, scale_size, speed):
        super().__init__("assets/graphics/player.png", position, scale_size, speed)
      
    def update_position(self, keys):
        '''Handles player's movement'''
        if keys[pygame.K_LEFT] and self.rect.x > 0: # Check left boundary
            self.move_horizontally(-self.speed)
        if keys[pygame.K_RIGHT] and self.rect.x + self.rect.width < WIDTH: # Check right boundary
            self.move_horizontally(self.speed)

# CollisionManager class to handle collision checks
class CollisionManager:
    @staticmethod
    def check_collision(sprite1, sprite2):
        '''Check collision between two sprites'''
        return pygame.sprite.collide_rect(sprite1, sprite2)
    
# Item as Child Class of GameEntity
class Item(GameEntity):
    def __init__(self, type, image_path, position, scale_size, speed):
        super().__init__(image_path, position, scale_size, speed)
        self.type = type
        self.falling = True # True or False
    
    def update_position(self):
        '''Update item's position'''
        self.rect.y += self.speed
        
        # If the item reaches the GROUND, reset its position through randomization
        if self.rect.y >= GROUND_Y:
            self.reset_random_position()

    def reset_random_position(self):
        '''Reset position through randomization'''
        self.rect.y = 0
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
    
    def update_score(self):
        '''Update score based on item type'''
        if self.type == ItemType.GOOD:
            SCORE += 1
        elif self.type == ItemType.BAD:
            SCORE -= 1
        elif self.type == ItemType.BONUS:
            SCORE += 5
            
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)

# Load assets
class LoadAssets:
    @staticmethod
    def load_img(image_path, scale_size):
        return pygame.transform.scale(pygame.image.load(image_path), scale_size)
    
    @staticmethod
    def load_fonts(font_path, font_size):
        return pygame.font.Font(font_path, int(font_size))
    
    @staticmethod
    def load_songs(sound_path):
        return pygame.mixer.music.load(sound_path)
    
    @staticmethod
    def load_sound_effects(sound_path):
        return pygame.mixer.Sound(sound_path)
    
    @staticmethod
    def play_sound(sound):
        sound.play()

# Loads images
welcome_img = LoadAssets.load_img('assets/graphics/welcome.png', (WIDTH, HEIGHT))
instruction_img = LoadAssets.load_img('assets/graphics/instruction.png', (WIDTH, HEIGHT))
background_img = LoadAssets.load_img('assets/graphics/background.png', (WIDTH, HEIGHT))
game_over_background = LoadAssets.load_img('assets/graphics/game_over_background.png', (WIDTH, HEIGHT))
game_over_screen = LoadAssets.load_img('assets/graphics/game_over_screen.png', (WIDTH, HEIGHT))

# Heart Image
heart_img_path = 'assets/graphics/heart.png'
heart_img = LoadAssets.load_img(heart_img_path, (WIDTH*0.05, WIDTH*0.05))
heart_big_img = LoadAssets.load_img(heart_img_path, (WIDTH*0.08125, WIDTH*0.08125))

# Font
game_over_font = LoadAssets.load_fonts('assets/font/Pixelify_Sans/static/PixelifySans-Bold.ttf', WIDTH / 8)
pixel_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (11 / 80))
pixel_small_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (17 / 160))
pixel_smaller_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (9 / 160))
regular_font = LoadAssets.load_fonts('assets/font/Roboto/Roboto-Medium.ttf', WIDTH / 16)
regular_small_font = LoadAssets.load_fonts('assets/font/Roboto/Roboto-Medium.ttf', WIDTH * (7 / 160))

# Load the music file
game_over_sound = LoadAssets.load_sound_effects('assets/audio/lose.mp3')
lose_sound = LoadAssets.load_sound_effects('assets/audio/lose_p.mp3')
earn_sound = LoadAssets.load_sound_effects('assets/audio/earn.mp3')
boost_sound = LoadAssets.load_sound_effects('assets/audio/boost.mp3')
LoadAssets.load_songs('assets/audio/background_music.mp3')
pygame.mixer.music.play(-1)  # Play in an infinite loop

# Set the volume (0.0 to 1.0, where 0.0 is silent and 1.0 is full volume)
volume_level = 0.3  # Adjust this value to set the desired volume level
pygame.mixer.music.set_volume(volume_level)

# Falling object's properties

## Main Object
object_img = pygame.image.load('assets/graphics/coin.png')
object_size = WIDTH // 12
object_img = pygame.transform.scale(object_img, (object_size, object_size))
object_x = random.randint(0, WIDTH - object_size)
object_y = 0 # top of the screen
object_speed = WIDTH * (3 / 400)

## Foul Object 1
foul1_img = pygame.image.load('assets/graphics/object.png')
foul1_size = WIDTH // 12
foul1_img = pygame.transform.scale(foul1_img, (foul1_size, foul1_size))
foul1_speed = WIDTH // 200
foul1_x = random.randint(0, WIDTH - foul1_size)
foul1_y = 0
foul1_falling = False
foul1_score = -1  # Negative score for strawberry

## Foul Object 2
foul2_img = pygame.image.load('assets/graphics/pineapple.png')
foul2_size = WIDTH // 12
foul2_img = pygame.transform.scale(foul2_img, (foul2_size, foul2_size))
foul2_speed = WIDTH // 320
foul2_x = random.randint(0, WIDTH - foul2_size)
foul2_y = 0
foul2_falling = False
foul2_score = -2  # More negative score for pineapple

# Power Up
power_img = pygame.image.load('assets/graphics/power.png')
power_size = WIDTH // 15
power_img = pygame.transform.scale(power_img, (power_size, power_size))
power_speed = WIDTH * (3 / 320)
power_x = random.randint(0, WIDTH - power_size)
power_y = 0
power_falling = False

# Player's properties
player_img = pygame.image.load('assets/graphics/player.png')
player_size = WIDTH // 10
player_img = pygame.transform.scale(player_img, (player_size, player_size))
player_x = WIDTH // 2                 # middle
player_y = HEIGHT - (WIDTH // 10) - (WIDTH * (83/800)) # ground
player_speed = player_size

# Other
clock = pygame.time.Clock()


# States
class GameStates(Enum):
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
            HEART_COUNT -= 1
            object_y = 0
            object_x = random.randint(0, WIDTH - object_size)  
            object_speed += WIDTH // 800
    
    # Randomly drop foul1
    if (SCORE >= 20) and random.randint(0, 8000) == 0 and not foul1_falling:
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
    if (SCORE >= 25) and random.randint(0, 8000) == 0 and not foul2_falling:
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
    if (SCORE % 5 == 0) and (SCORE >= 10) and random.randint(0, 8000) == 0 and not power_falling:
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
        SCORE += 1
        LoadAssets.play_sound(earn_sound)
        object_y = 0
        object_x = random.randint(0, WIDTH - object_size)  
        object_speed += 1

    # Collision Check for Foul1
    if player_y + (WIDTH * (83 / 800)) < foul1_y + foul1_size and foul1_x < player_x + player_size and player_x < foul1_x + foul1_size:
        SCORE += foul1_score
        LoadAssets.play_sound(lose_sound)
        foul1_falling = False
        foul1_y = 0

    # Collision Check for Foul2
    if player_y + (WIDTH * (83 / 800)) < foul2_y + foul2_size and foul2_x < player_x + player_size and player_x < foul2_x + foul2_size:
        SCORE += foul2_score
        LoadAssets.play_sound(lose_sound)
        foul2_falling = False
        foul2_y = 0

    # Collision Check for Power
    if player_y + (WIDTH * (83 / 800)) < power_y + power_size and power_x < player_x + player_size and player_x < power_x + power_size:
        player_speed += WIDTH // 320
        LoadAssets.play_sound(boost_sound)
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
        text = regular_font.render("Score: " + str(SCORE), True, (0, 0, 0))
        screen.blit(text, (70, 30))
        heart_count = regular_font.render(":"+ str(HEART_COUNT), True, (0, 0, 0))
        screen.blit(heart_count, (WIDTH - (WIDTH * (23 / 320)), WIDTH * (19 / 800)))
    else:
        text_paused = regular_font.render("Paused. Press Space to Resume", True, (0, 0, 0))
        screen.blit(text_paused, (WIDTH / 2 - (WIDTH / 2.2), HEIGHT / 2.5))

    # Lose!
    if HEART_COUNT == 0:
        LoadAssets.play_sound(game_over_sound)
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

# GameState classes
class GameState:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self):
        pass

    def render(self, screen):
        pass

class MainMenuState(GameState):
    def render(self, screen):
        screen.fill((0, 0, 0))  # Clear screen
        # Render main menu

class GameplayState(GameState):
    def update(self):
        # Update game logic

    def render(self, screen):
        # Render gameplay

class PauseState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.game.toggle_pause()

# Game class
class Game:
    def __init__(self):
        self.running = True
        self.state = MainMenuState(self)

    def toggle_pause(self):
        if isinstance(self.state, GameplayState):
            self.state = PauseState(self)
        elif isinstance(self.state, PauseState):
            self.state = GameplayState(self)

    def run(self):
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        clock = pygame.time.Clock()

        player = Player('player.png', (SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        enemies = [Enemy('enemy.png', (100, 100), 2)]
        items = [Item('item.png', (200, 200), 'heal')]

        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False

            self.state.handle_events(events)
            self.state.update()
            self.state.render(screen)

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

# Main
if __name__ == '__main__':
    game = Game()
    game.run()


if __name__ == '__main__':
    game = Game()
    game.run()