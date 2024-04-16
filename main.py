# main.py

# Libraries Initialization
import pygame
import random
import time
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
STAR = 5 # Player starts off with 5 hearts
SCORE = 0 # Total number of points player earns

class ItemType(Enum):
    GOOD = 4
    BAD = 6
    BONUS = 1
    
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

    def move_right(self):
        self.rect.x += self.speed
        
    def move_left(self):
        self.rect.x -= self.speed
    
    def move_vertically_down(self):
        self.rect.y -= self.speed
        
    def draw(self, screen, img):
        screen.blit(img, (self.rect.x, self.rect.y))

# Player as Child Class of GameEntity
class Player(GameEntity):
    def __init__(self, position, scale_size, speed):
        super().__init__("assets/graphics/player.png", position, scale_size, speed)
      
    def update_position(self, keys):
        '''Handles player's movement'''
        if keys[pygame.K_LEFT] and self.rect.x > 0: # Check left boundary
            self.move_left()
        if keys[pygame.K_RIGHT] and self.rect.x + self.rect.width < WIDTH: # Check right boundary
            self.move_right()

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
        
    @staticmethod 
    def spawn_item():
        # Spawn a new item with random type, position, and speed
        item_types = [ItemType.GOOD] * 4 + [ItemType.BAD] * 6 + [ItemType.BONUS]
        chosen_type = random.choice(item_types)

        if chosen_type == ItemType.GOOD:
            image_path = f'assets/graphics/{chosen_type.name}/{random.randint(1, 4)}.png'
        elif chosen_type == ItemType.BAD:
            image_path = f'assets/graphics/{chosen_type.name}/{random.randint(1, 6)}.png'
        else:  # ItemType.BONUS
            image_path = f'assets/graphics/{chosen_type.name}/1.png'

        new_item = Item(chosen_type, image_path, 
                       (random.randint(0, WIDTH - WIDTH // 12), 0), 
                       (WIDTH // 12, WIDTH // 12), 
                       (WIDTH * (3 / 400)))

        return new_item   
        
    # def update_position(self):
    #     '''Update item's position'''
    #     self.rect.y += int(self.speed)
        
    #     # If the item reaches the GROUND, reset its position through randomization
    #     if self.rect.y >= GROUND_Y:
    #         print("106")
    #         #self.reset_random_position()
    #         del self.item
    #         self.item = Item.spawn_item()
            
            
    # TO DO: This is supposed to fire off randomize_item
    def reset_random_position(self):
        '''Reset position through randomization'''
        self.rect.y = 0
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
    
    def update_score(self):
        global SCORE, STAR
        '''Update score based on item type'''
        if self.type == ItemType.GOOD:
            SCORE += 1
        elif self.type == ItemType.BAD:
            STAR -= 0.5
        elif self.type == ItemType.BONUS:
            SCORE += 5

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
welcome_img = LoadAssets.load_img('assets/graphics/welcome.png', (WIDTH, HEIGHT))
instruction_img = LoadAssets.load_img('assets/graphics/instruction.png', (WIDTH, HEIGHT))
background_img = LoadAssets.load_img('assets/graphics/background.png', (WIDTH, HEIGHT))
game_over_background = LoadAssets.load_img('assets/graphics/game_over_background.png', (WIDTH, HEIGHT))
game_over_screen = LoadAssets.load_img('assets/graphics/game_over_screen.png', (WIDTH, HEIGHT))

# star Image
# star_img_path = 'assets/graphics/heart.png'
# star_img = LoadAssets.load_img(star_img_path, (WIDTH*0.05, WIDTH*0.05))
# star_big_img = LoadAssets.load_img(star_img_path, (WIDTH*0.08125, WIDTH*0.08125))

# Font
game_over_font = LoadAssets.load_fonts('assets/font/Pixelify_Sans/static/PixelifySans-Bold.ttf', WIDTH / 8)
pixel_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (11 / 80))
pixel_small_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (17 / 160))
pixel_smaller_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (9 / 160))
regular_font = LoadAssets.load_fonts('assets/font/Roboto/Roboto-Medium.ttf', WIDTH / 16)
regular_small_font = LoadAssets.load_fonts('assets/font/Roboto/Roboto-Medium.ttf', WIDTH * (7 / 160))
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
game_over_sound = LoadAssets.load_sound_effects('assets/audio/lose.mp3')
lose_sound = LoadAssets.load_sound_effects('assets/audio/lose_p.mp3')
earn_sound = LoadAssets.load_sound_effects('assets/audio/earn.mp3')
boost_sound = LoadAssets.load_sound_effects('assets/audio/boost.mp3')
LoadAssets.load_songs('assets/audio/background_music.mp3')
pygame.mixer.music.play(-1)  # Play in an infinite loop

# Set the volume (0.0 to 1.0, where 0.0 is silent and 1.0 is full volume)
volume_level = 0.3  # Adjust this value to set the desired volume level
pygame.mixer.music.set_volume(volume_level)

# GameState classes
class GameState:
    def __init__(self, game):
        self.game = game

    def handle_events(self, events):
        pass

    def update(self, events):
        pass

    def render(self, screen):
        pass

class MainMenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.state = GamePlayState(self.game)
                
    def render(self, screen):
        screen.blit(welcome_img, (0, 0))

class GamePlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.remaining_time = 3 * 60 # 3 minutes
        self.start_time = time.time()
        self.player = Player((MID_X, GROUND_Y),          # position
                             (WIDTH // 10, WIDTH // 10), # scale_size
                             (WIDTH // 10))              # speed
        self.items = pygame.sprite.Group()
        self.item = Item.spawn_item()
        self.spawn_timer = 0
        self.spawn_interval = 2000  # Spawn interval in milliseconds
        
        # self.good_item1 = Item("Good", 'assets/graphics/pineapple.png', # image_path
        #                       (random.randint(0, WIDTH - WIDTH // 12), 0),             # position
        #                       (WIDTH // 12, WIDTH // 12),                              # scale_size
        #                       (WIDTH * (3 / 400)) )  
        # self.good_item2 = Item("Good", 'assets/graphics/pineapple.png', 
        #                       (random.randint(0, WIDTH - WIDTH // 12), 0), 
        #                       (WIDTH // 12, WIDTH // 12), 
        #                       (WIDTH * (3 / 400))) 
        # self.bonus_item = Item("Bonus", 'assets/graphics/pineapple.png', 
        #                       (random.randint(0, WIDTH - WIDTH // 12), 0), 
        #                       (WIDTH // 12, WIDTH // 12), 
        #                       (WIDTH * (3 / 400)))
        # self.bad_item1 = Item("Bad", 'assets/graphics/coin.png', 
        #                      (random.randint(0, WIDTH - WIDTH // 12), 0), 
        #                      (WIDTH // 12, WIDTH // 12), 
        #                      (WIDTH * (3 / 400)))
        # self.bad_item2 = Item("Bad", 'assets/graphics/coin.png', 
        #                      (random.randint(0, WIDTH - WIDTH // 12), 0), 
        #                      (WIDTH // 12, WIDTH // 12), 
        #                      (WIDTH * (3 / 400)))
        # self.bad_item3 = Item("Bad", 'assets/graphics/coin.png', 
        #                      (random.randint(0, WIDTH - WIDTH // 12), 0), 
        #                      (WIDTH // 12, WIDTH // 12), 
        #                      (WIDTH * (3 / 400)))
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                
            # Get the keys pressed
            keys = pygame.key.get_pressed()

            # Update player position based on key events
            self.player.update_position(keys)
            
    def update_position(self):
        '''Update item's position'''
        self.item.rect.y += int(self.item.speed)
        
        # If the item reaches the GROUND, reset its position through randomization
        if self.item.rect.y >= GROUND_Y:
            print("106")
            #self.reset_random_position()
            del self.item
            self.item = Item.spawn_item()

    def collision_check_and_reset_position(self, item):
        if CollisionManager.check_collision(self.player, item):
            item.reset_random_position()
            item.update_score()

    def update(self, events):
        self.update_position()
        self.collision_check_and_reset_position(self.item)
        # # Update item positions
        # self.good_item1.update_position()
        # self.good_item2.update_position()
        # self.bonus_item.update_position()
        # self.bad_item1.update_position()
        # self.bad_item2.update_position()
        # self.bad_item3.update_position() 

        # # Collision check between player and items
        # self.collision_check_and_reset_position(self.good_item1)
        # self.collision_check_and_reset_position(self.good_item2)
        # self.collision_check_and_reset_position(self.bonus_item)
        # self.collision_check_and_reset_position(self.bad_item1)
        # self.collision_check_and_reset_position(self.bad_item2)
        # self.collision_check_and_reset_position(self.bad_item3)
        # self.update_items()
        
        # Calculate elapsed time since the start
        elapsed_time = time.time() - self.start_time

        # Decrement remaining time by elapsed time
        self.remaining_time -= elapsed_time

        # Update start time for the next iteration
        self.start_time = time.time()

        # Check if the remaining time is less than or equal to 0
        if self.remaining_time <= 0:
            # End the game if time runs out
            pygame.mixer.music.stop()
            LoadAssets.play_sound(game_over_sound)
            self.game.state = GameOverState(self.game)
            
        # Losing Logic
        if STAR <= 0:
            pygame.mixer.music.stop()
            LoadAssets.play_sound(game_over_sound)
            self.game.state = GameOverState(self.game)
            
    # def update_items(self):
    #     (self.spawn_item()).update_position() 

    #     # Spawn new items based on timer
    #     # TO DO: decide whether we should have this take precedence over reset_random_position()
    #     self.spawn_timer += 1
    #     if self.spawn_timer >= 60:
    #         self.spawn_item()
    #         self.spawn_timer = 0

    # def spawn_item(self):
    #     # Spawn a new item with random type, position, and speed
    #     item_types = [ItemType.GOOD] * 4 + [ItemType.BAD] * 6 + [ItemType.BONUS]
    #     chosen_type = random.choice(item_types)

    #     if chosen_type == ItemType.GOOD:
    #         image_path = f'assets/graphics/{chosen_type.name}/{random.randint(1, 4)}.png'
    #     elif chosen_type == ItemType.BAD:
    #         image_path = f'assets/graphics/{chosen_type.name}/{random.randint(1, 6)}.png'
    #     else:  # ItemType.BONUS
    #         image_path = f'assets/graphics/{chosen_type.name}/1.png'

    #     new_item = Item(chosen_type, image_path, 
    #                    (random.randint(0, WIDTH - WIDTH // 12), 0), 
    #                    (WIDTH // 12, WIDTH // 12), 
    #                    (WIDTH * (3 / 400)))

    #     return new_item

    def render(self, screen):
        screen.blit(background_img, (0, 0))
        (self.item).draw(screen, (self.item).image)
        (self.player).draw(screen, (self.player).image)
        # (self.good_item1).draw(screen, (self.good_item1).image)
        # (self.good_item2).draw(screen, (self.good_item2).image)
        # (self.bonus_item).draw(screen, (self.bonus_item).image)
        # (self.bad_item1).draw(screen, (self.bad_item1).image)
        # (self.bad_item2).draw(screen, (self.bad_item2).image)
        # (self.bad_item3).draw(screen, (self.bad_item3).image)
        
class GameOverState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                
    def render(self, screen):
        screen.blit(game_over_screen, (0, 0))
        over_text = game_over_font.render("GAME OVER", True, (251, 194, 7))
        screen.blit(over_text, (WIDTH / 2 - (WIDTH * (5 / 16)), HEIGHT / 2 - (WIDTH / 8)))
        play_again_text = regular_small_font.render("Press SPACE to Play Again", True, (255, 255, 255))
        screen.blit(play_again_text, (WIDTH / 2 - (WIDTH / 4), HEIGHT / 2 + (WIDTH / 16)))
        next_text = regular_small_font.render("Press 'L' to Accept the L :)", True, (255, 255, 255))
        screen.blit(next_text, (WIDTH / 2 - (WIDTH / 4), HEIGHT / 2 + (WIDTH / 8)))

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
        if isinstance(self.state, GamePlayState):
            self.state = PauseState(self)
        elif isinstance(self.state, PauseState):
            self.state = GamePlayState(self)

    def run(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        
        clock = pygame.time.Clock()

        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
            self.state.handle_events(events)
            self.state.update(events)
            self.state.render(screen)

            pygame.display.flip()
            clock.tick(30)
            
        pygame.quit()

# Main
if __name__ == '__main__':
    game = Game()
    game.run()