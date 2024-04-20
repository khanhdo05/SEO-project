# main.py

# Libraries Initialization
import pygame
import random
from enum import Enum
from sys import exit
pygame.init()

# Define Constants
TITLE = "Name of our game"
WIDTH = 800
HEIGHT = WIDTH * 0.75
MID_X = WIDTH / 2
MID_Y = WIDTH / 2
GROUND_Y = HEIGHT - (WIDTH // 10) - (WIDTH * (83/800)) # For the current graphic
STAR = 5 # Player starts off with 5 stars
SCORE = 0 # Total number of points player earns

class ItemType(Enum):
    GOOD = 4
    BAD = 6
    BONUS = 1
    SLOWDOWN = 1

# GameEntity as Parent Class
class GameEntity(pygame.sprite.Sprite):
    def __init__(self, image_path, position, scale_size, speed):
        ''' Notes:
            + image_path should follow the form: "assets/graphics/FILE_NAME.png"
            + position: (x,y) to place the image on the screen
            + scale_size: (x,y) as desired width and height of the image
            + speed: a number that references the width in scale_size to match screen size 
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
        self.rect.y += self.speed
        
    def draw(self, screen, img):
        screen.blit(img, (self.rect.x, self.rect.y))
    

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
        self.falling = True  

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

    def update_items(self):
    # Update item positions and speeds
        for item in self.items:
            item.update_position()  # Ensure this line is present
            item.move_vertically_down()
            item.speed = random.randint(int(WIDTH * (1 / 200)), int(WIDTH * (3 / 400)))
        self.items.update()
    

    def update_score(self):
        global SCORE, STAR
        '''Update score based on item type'''
        if self.type == "Good":
            SCORE += 1
        elif self.type == "Bad":
            STAR -= 0.5
        elif self.type == "Bonus":
            SCORE += 5

    def update_star_image(self):
        '''Update star image based on STAR count'''
        if STAR >= 1:
            star_img_path = 'assets/graphics/star/fullstar.png'
        elif STAR >= 0.5:
            star_img_path = 'assets/graphics/star/halfstar.png'
        else:
            star_img_path = 'assets/graphics/star/emptystar.png'
        
        self.image = pygame.image.load(star_img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (WIDTH*0.05, WIDTH*0.05))

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

# Star Image
star_img_path = 'assets/graphics/star/fullstar.png'
star_img = LoadAssets.load_img(star_img_path, (WIDTH*0.05, WIDTH*0.05))
star_big_img = LoadAssets.load_img(star_img_path, (WIDTH*0.08125, WIDTH*0.08125))

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

# GameState classes
class GameState:
    def __init__(self, game):
        self.game = game
        self.running = True

    def handle_events(self, events):
        pass

    def update(self, events):
        pass

    def render(self, screen):
        pass

class MainMenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def update(self, events):
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
        # Initialize player and item group
        self.player = Player((MID_X, GROUND_Y), (WIDTH // 10, WIDTH // 10), (WIDTH // 10))
        self.items = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_interval = 2000  # Spawn interval in milliseconds

    def update(self, events):
        # Update items, check collisions, and loss condition
        self.update_items()
        self.check_loss_condition()

    def update_items(self):
        # Update item positions
        for item in self.items:
            print("Hello") 
            item.move_vertically_down()   

        # Spawn new items based on timer
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_item()
            self.spawn_timer = 0

            if pygame.sprite.collide_rect(item, self.player):
                if item.item_type == ItemType.SLOWDOWN:
                    self.player.decrease_speed()  
        self.items.update()

    def spawn_item(self):
        # Spawn a new item with random type, position, and speed
        item_types = [ItemType.GOOD] * 4 + [ItemType.BAD] * 6 + [ItemType.BONUS] + [ItemType.SLOWDOWN]
        chosen_type = random.choice(item_types)

        if chosen_type == ItemType.GOOD:
            image_path = f'assets/graphics/{chosen_type.name.lower()}/{random.randint(1, 4)}.png'
        elif chosen_type == ItemType.BAD:
            image_path = f'assets/graphics/{chosen_type.name.lower()}/{random.randint(1, 6)}.png'
        elif chosen_type == ItemType.BONUS:
            image_path = f'assets/graphics/{chosen_type.name.lower()}/1.png'
        else: 
            image_path = f'assets/graphics/{chosen_type.name.lower()}/1.png'

        new_item = Item(chosen_type.name, image_path, 
                        (random.randint(0, WIDTH - WIDTH // 12), 0), 
                        (WIDTH // 12, WIDTH // 12), 
                        (WIDTH * (3 / 400)))
        self.items.add(new_item)

    def check_loss_condition(self):
        # Check if player lost the game
        if STAR <= 0:
            pygame.mixer.music.stop()
            LoadAssets.play_sound(game_over_sound)
            self.game.state = GameOverState(self.game)

    def handle_events(self, events):
        # Handle player input events
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move_horizontally(-self.player.speed)
                elif event.key == pygame.K_RIGHT:
                    self.player.move_horizontally(self.player.speed)
    
    def render(self, screen):
        # Render background, items, and player
        screen.blit(background_img, (0, 0))
        self.items.draw(screen, self.items)
        self.player.draw(screen, self.player.image)


class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 64)  # Choose a font and font size for the game over message
        self.game_over_text = self.font.render("Game Over", True, (255, 0, 0))  # Render the game over message
        self.restart_text = self.font.render("Press R to Restart", True, (255, 255, 255))  # Render the restart message
        self.quit_text = self.font.render("Press Q to Quit", True, (255, 255, 255))  # Render the quit message

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # If 'R' is pressed, restart the game
                    self.game.restart()
                elif event.key == pygame.K_q:  # If 'Q' is pressed, quit the game
                    pygame.quit()

    def render(self, screen):
        screen.blit(self.game_over_text, (WIDTH // 2 - self.game_over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(self.restart_text, (WIDTH // 2 - self.restart_text.get_width() // 2, HEIGHT // 2))
        screen.blit(self.quit_text, (WIDTH // 2 - self.quit_text.get_width() // 2, HEIGHT // 2 + 50))


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
        self.player_img_path = 'assets/graphics/player.png'

    def toggle_pause(self):
        if isinstance(self.state, GamePlayState):
            self.state = PauseState(self)
        elif isinstance(self.state, PauseState):
            self.state = GamePlayState(self)

    def run(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

    
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    
            keys = pygame.key.get_pressed()
            

            self.state.update(events)
            self.state.render(screen)
            

            pygame.display.flip()
            pygame.time.Clock().tick(30)
            
        pygame.quit()

# Main
if __name__ == '__main__':
    game = Game()
    game.run()