# main.py

# Libraries Initialization
import pygame
import random
import time
from enum import Enum
from sys import exit
pygame.init()

# Define Constants
TITLE = "Build The Cake"
WIDTH = 1200
HEIGHT = WIDTH * 0.75
MID_X = WIDTH / 2
MID_Y = WIDTH / 2
GROUND_Y = HEIGHT - (WIDTH // 10) - (WIDTH * (83/800)) # For the current graphic

STAR = 5 # Player starts off with 5 hearts
SCORE = 0 # Total number of points player earns
TIMER = 60*2 # seconds
COUNT_DOWN_TIMER = 10 # seconds
ITEM_SPEED = WIDTH * (3 / 350)
WINNING_SCORE = 50
WINNING_STARS = 3

paused = False

class ItemType(Enum):
    GOOD = 4
    BAD = 6
    BONUS = 2
    SLOWDOWN = 1
    SPEEDUP = 3

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
welcome_img = LoadAssets.load_img('assets/graphics/welcome2.png', (WIDTH, HEIGHT))
instruct1_img = LoadAssets.load_img('assets/graphics/instruct1.png', (WIDTH, HEIGHT))
instruct2_img = LoadAssets.load_img('assets/graphics/instruct2.png', (WIDTH, HEIGHT))
instruct3_img = LoadAssets.load_img('assets/graphics/instruct3.png', (WIDTH, HEIGHT))
instruct4_img = LoadAssets.load_img('assets/graphics/instruct4.png', (WIDTH, HEIGHT))
instruct5_img = LoadAssets.load_img('assets/graphics/instruct5.png', (WIDTH, HEIGHT))
background_img = LoadAssets.load_img('assets/graphics/play_screen_maybe.png', (WIDTH, HEIGHT))
game_over_background = LoadAssets.load_img('assets/graphics/game_over_background.png', (WIDTH, HEIGHT))
game_over_screen = LoadAssets.load_img('assets/graphics/game_over_screen2.png', (WIDTH, HEIGHT))
game_win_screen = LoadAssets.load_img('assets/graphics/win_screen.png', (WIDTH, HEIGHT))
# Font
game_over_font = LoadAssets.load_fonts('assets/font/Pixelify_Sans/static/PixelifySans-Bold.ttf', WIDTH / 8)
game_win_font = LoadAssets.load_fonts('assets/font/Pixelify_Sans/static/PixelifySans-Bold.ttf', WIDTH / 8)
pixel_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (11 / 80))
pixel_small_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (17 / 160))
pixel_smaller_font = LoadAssets.load_fonts('assets/font/VT323/VT323-Regular.ttf', WIDTH * (9 / 160))
regular_font = LoadAssets.load_fonts('assets/font/Roboto/Roboto-Medium.ttf', WIDTH / 20)
regular_big_font = LoadAssets.load_fonts('assets/font/Roboto/Roboto-Medium.ttf', WIDTH / 3)
regular_small_font = LoadAssets.load_fonts('assets/font/Roboto/Roboto-Medium.ttf', WIDTH * (7 / 160))
press_font = LoadAssets.load_fonts('assets/font/Press/press.ttf', WIDTH * (1 / 40))

# Load the music file
game_over_sound = LoadAssets.load_sound_effects('assets/audio/over.mp3')
game_win_sound = LoadAssets.load_sound_effects('assets/audio/win2.mp3')
earn_sound = LoadAssets.load_sound_effects('assets/audio/earn.mp3')
bad_sound = LoadAssets.load_sound_effects('assets/audio/trash.mp3')
slow_item_sound = LoadAssets.load_sound_effects('assets/audio/slow_item.mp3')
boost_sound = LoadAssets.load_sound_effects('assets/audio/soda.mp3')
bonus_sound = LoadAssets.load_sound_effects('assets/audio/yay-6120.mp3')
ten_sec_count_down_sound = LoadAssets.load_sound_effects('assets/audio/tensec.mp3')
LoadAssets.load_songs('assets/audio/background_music.mp3')
pygame.mixer.music.play(-1)  # Play in an infinite loop

# Set the volume (0.0 to 1.0, where 0.0 is silent and 1.0 is full volume)
volume_level = 0.3  # Adjust this value to set the desired volume level
pygame.mixer.music.set_volume(volume_level)

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
        super().__init__("assets/graphics/player3.png", position, scale_size, speed)
    
    def update_position(self, keys):
        if not paused:
            '''Handles player's movement'''
            if keys[pygame.K_LEFT] and self.rect.left > 0: # Check left boundary
                self.move_left()
            if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: # Check right boundary
                self.move_right()
            if self.rect.left < 0:
                self.rect.x = 0
            if self.rect.right > WIDTH:
                self.rect.x = WIDTH - self.rect.width
            
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
        
    @staticmethod 
    def spawn_item():
        # Spawn a new item with random type, position, and speed
        item_types = [ItemType.GOOD] * 4 + [ItemType.BAD] * 4 + [ItemType.BONUS] * 1 + [ItemType.SLOWDOWN] * 1 + [ItemType.SPEEDUP] * 1
        chosen_type = random.choice(item_types)
        if chosen_type == ItemType.GOOD:
            image_path = f'assets/graphics/{chosen_type.name}/{random.randint(1, ItemType.GOOD.value)}.png'
        elif chosen_type == ItemType.BAD:
            image_path = f'assets/graphics/{chosen_type.name}/{random.randint(1, ItemType.BAD.value)}.png'
        elif chosen_type == ItemType.BONUS:
            image_path = f'assets/graphics/{chosen_type.name}/{random.randint(1, ItemType.BONUS.value)}.png'
        elif chosen_type == ItemType.SLOWDOWN:
            image_path = f'assets/graphics/{chosen_type.name}/1.png'
        elif chosen_type == ItemType.SPEEDUP:
            image_path = f'assets/graphics/{chosen_type.name}/1.png'
            
        new_item = Item(chosen_type, image_path, 
                       (random.randint(0, WIDTH - WIDTH // 12), 0), 
                       (WIDTH // 12, WIDTH // 12), 
                       (ITEM_SPEED))
        
        if new_item.type == ItemType.BAD:
            new_item.speed -= 0.3
            
        return new_item  
    
    def update_score_and_play_sound_effects(self):
        global SCORE, STAR
        '''Update score based on item type'''
        if self.type == ItemType.GOOD:
            earn_sound.play()
            SCORE += 1
        elif self.type == ItemType.BONUS:
            bonus_sound.play()
            SCORE += 3
        elif self.type == ItemType.BAD:
            bad_sound.play()
            STAR -= 0.5
        elif self.type == ItemType.SLOWDOWN:
            slow_item_sound.play()
            STAR -= 1
        elif self.type == ItemType.SPEEDUP:
            boost_sound.play()

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
    def render_paused(self, screen):
        pass
    
class MainMenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.state = Instruction1(self.game)
                
    def render(self, screen):
        screen.blit(welcome_img, (0, 0))

class Instruction1(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.state = Instruction2(self.game)
                
    def render(self, screen):
        screen.blit(instruct1_img, (0, 0))

class Instruction2(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.state = Instruction3(self.game)
                
    def render(self, screen):
        screen.blit(instruct2_img, (0, 0))

class Instruction3(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.state = Instruction4(self.game)
                
    def render(self, screen):
        screen.blit(instruct3_img, (0, 0))
        
class Instruction4(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.state = Instruction5(self.game)
                
    def render(self, screen):
        screen.blit(instruct4_img, (0, 0))
        
class Instruction5(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.game.state = GamePlayState(self.game)
                
    def render(self, screen):
        screen.blit(instruct5_img, (0, 0))
        
class GamePlayState(GameState):
    def __init__(self, game):
        super().__init__(game)
        # Times
        self.remaining_time = TIMER # 3 minutes
        self.start_time = time.time()
        self.countdown_time = COUNT_DOWN_TIMER  # Countdown timer for the last 10 seconds
        self.last_countdown_value = None

        player_x = MID_X - (WIDTH // 10)  
        player_y = GROUND_Y - (WIDTH // 16)  

        # Player and Items
        self.player = Player((player_x, player_y),  # position
                             (WIDTH // 6, WIDTH // 6),  # scale_size
                             (WIDTH // 16))  # speed
        self.num_items_to_spawn = 1
        self.spawn_timer = 0
        self.spawn_interval = 30000  # Spawn interval in milliseconds
        self.falling_items = [] #initializing list to keep track of falling items
        self.slowdown_active = False  
        self.boost_active = False
        self.slowdown_duration = 5  
        self.boost_duration = 5 
        self.slowdown_timer = 0  
        self.boost_timer = 0 
        self.star_images = {
            0: LoadAssets.load_img('assets/graphics/star/star_empty.png', (WIDTH * 0.08, WIDTH * 0.08)),
            0.5: LoadAssets.load_img('assets/graphics/star/star_half.png', (WIDTH * 0.08, WIDTH * 0.08)),
            1: LoadAssets.load_img('assets/graphics/star/star_full.png', (WIDTH * 0.08, WIDTH * 0.08))
        }
        
        self.speed_threshold = 10
        self.spawn_threshold = 30
        
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
        if SCORE >= self.spawn_threshold and self.num_items_to_spawn < 4:
            self.num_items_to_spawn += 1
            self.spawn_threshold += 20
                    
        self.spawn_timer += 1000
        if self.spawn_timer >= self.spawn_interval:
            for _ in range(self.num_items_to_spawn):
                new_item = Item.spawn_item()
                self.falling_items.append(new_item)
            self.spawn_timer = 0

        for item in self.falling_items:
            if not paused:
                item.rect.y += int(item.speed)
            if item.rect.y >= GROUND_Y:
                self.falling_items.remove(item)  
            elif CollisionManager.check_collision(self.player, item):
                if item.type == ItemType.SLOWDOWN and self.player.speed > 40:
                    self.player.speed -= 40
                    self.activate_slowdown()
                if item.type == ItemType.SPEEDUP:
                    self.player.speed += 50
                    self.activate_boost()
                item.update_score_and_play_sound_effects()
                self.falling_items.remove(item)    
    

    def activate_slowdown(self):
        self.slowdown_active = True
       # self.slowdown_timer = pygame.time.get_ticks()
        self.slowdown_timer = time.time()

    def activate_boost(self):
        self.boost_active = True
        #self.boost_timer = pygame.time.get_ticks()
        self.boost_timer = time.time()

                     
    def update(self, events):
        global ITEM_SPEED
        self.update_position()
        
        # Calculate elapsed time since the start
        elapsed_time = time.time() - self.start_time
        # Decrement remaining time by elapsed time
        self.remaining_time -= elapsed_time
        # Update start time for the next iteration
        self.start_time = time.time()
        # Check if the remaining time is less than or equal to 0
        if self.remaining_time <= 0:
            pygame.mixer.music.stop()
            # End the game if time runs out
            self.game.state = GameOverState(self.game)
            LoadAssets.play_sound(game_over_sound)
        
        if self.slowdown_active:
            if self.start_time - self.slowdown_timer >= self.slowdown_duration:
                self.player.speed = (WIDTH // 16)
                self.slowdown_active = False
        if self.boost_active:
            if self.start_time - self.boost_timer >= self.boost_duration:
                self.player.speed = (WIDTH // 16)
                self.boost_active = False

        # Speed up item over time logic
        if SCORE >= self.speed_threshold:  # Check if the score exceeds the current threshold
            ITEM_SPEED += 0.5
            self.speed_threshold += 5
            
        # Losing Logic
        if STAR <= 0:
            pygame.mixer.music.stop()
            self.game.state = GameOverState(self.game)
            LoadAssets.play_sound(game_over_sound)
        
        # Winning Logic
        if SCORE >= WINNING_SCORE and STAR > WINNING_STARS:
            pygame.mixer.music.stop()
            self.game.state = GameOverState(self.game)
            LoadAssets.play_sound(game_win_sound)
            
        # Countdown timer logic
        if self.remaining_time <= self.countdown_time:
            pygame.mixer.music.stop()
            LoadAssets.play_sound(ten_sec_count_down_sound)
            countdown_value = int(self.remaining_time) + 1  # Add 1 to ensure it goes from 10 to 0
            if countdown_value != self.last_countdown_value:  # Only update if the value changes
                self.last_countdown_value = countdown_value
            
    def render_stars(self, screen):
        x = WIDTH - (WIDTH // 11.428)  # Adjust this value for positioning
        y = WIDTH // 80                # Adjust this value for positioning
        star_count = int(STAR)
        decimal_part = STAR - star_count  # Get the decimal part of STAR
        
        for i in range(5):
            if i < star_count:
                screen.blit(self.star_images[1], (x, y))
            elif i == star_count and decimal_part >= 0.5:
                screen.blit(self.star_images[0.5], (x, y))
            else:
                screen.blit(self.star_images[0], (x, y))
            x -= self.star_images[1].get_width() 
            
    def render(self, screen):
        global paused
        
        screen.blit(background_img, (0, 0))
        
        # Render stars
        self.render_stars(screen)
        
        # Render the list of items
        for item in self.falling_items:
            item.draw(screen, item.image)
        
        # Render player  
        (self.player).draw(screen, (self.player).image)
        
        # Render score
        score_text = regular_font.render("Score: " + str(SCORE), True, (170, 51, 106))
        screen.blit(score_text, (10, 10))  # Adjust the position as needed
        
        # Render countdown timer
        if isinstance(self.last_countdown_value, int):
            countdown_text = regular_big_font.render(str(self.last_countdown_value), True, (0, 0, 0))
            text_width, text_height = countdown_text.get_size()
            text_x = (WIDTH - text_width) // 2
            text_y = (HEIGHT - text_height) // 2
            screen.blit(countdown_text, (text_x, text_y))       
    
    def render_paused(self, screen):
        # Dark low-opacity overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(1)
        overlay.fill((1, 0, 1))
        screen.blit(overlay, (0, 0))
        
        # Text: Press SPACE to continue. Press ESC or Q to quit.
        pause_text1 = regular_font.render("Press SPACE to continue.", True, (255, 255, 255))
        pause_text2 = regular_font.render("Press ESC or Q to quit.", True, (255, 255, 255))
        
        # Get the size of the text
        text_width1, text_height1 = pause_text1.get_size()
        text_width2, text_height2 = pause_text2.get_size()
        
        # Calculate the position to center the text horizontally
        text_x1 = (WIDTH - text_width1) // 2
        text_x2 = (WIDTH - text_width2) // 2
        
        # Calculate the position to center the text vertically
        text_y1 = (HEIGHT - text_height1) // 2 - text_height1  # Place the first text above the center
        text_y2 = (HEIGHT + text_height2) // 2             # Place the second text below the center
        
        screen.blit(pause_text1, (text_x1, text_y1))
        screen.blit(pause_text2, (text_x2, text_y2)) 
    
class GameOverState(GameState):
    def __init__(self, game):
        super().__init__(game)
        
    def handle_events(self, events):            
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.game.state = GamePlayState(self.game)
                    global SCORE, STAR, paused, TIMER, COUNT_DOWN_TIMER, ITEM_SPEED
                    SCORE = 0
                    STAR = 5
                    paused = False
                    TIMER = 60*2 # seconds
                    COUNT_DOWN_TIMER = 10 # seconds
                    ITEM_SPEED = WIDTH * (3 / 350)
                    
    def render_stars(self, screen, num_stars):
        star_big = LoadAssets.load_img('assets/graphics/star/star_full.png', (int(WIDTH * 0.3), int(WIDTH * 0.3)))
        star_small = LoadAssets.load_img('assets/graphics/star/star_full.png', (int(WIDTH * 0.25), int(WIDTH * 0.25)))
        center_x = WIDTH // 2
        y = HEIGHT // 2 - 300  # Adjust the vertical position as needed
        spacing = star_big.get_width() * 0.6  # Adjust the spacing between stars as needed

        # Render the center star first
        screen.blit(star_big, (center_x - star_big.get_width() // 2, y - star_big.get_height() // 2))

        # Render stars to the left
        for i in range(num_stars // 2):
            screen.blit(star_small, (center_x - spacing * (i + 1) - star_small.get_width() // 2, y - star_small.get_height() // 2))

        # Render stars to the right
        for i in range(num_stars // 2):
            screen.blit(star_small, (center_x + spacing * (i + 1) - star_small.get_width() // 2, y - star_small.get_height() // 2))

            
    def render(self, screen):
        if SCORE >= WINNING_SCORE and STAR > WINNING_STARS:
            screen.blit(game_win_screen, (0, 0))
            win_text = game_win_font.render("YOU WIN!", True, (230, 62, 168))

            win_text_width, _ = game_win_font.size("YOU WIN!")
            win_text_x = (WIDTH - win_text_width) // 2
            win_text_y = HEIGHT // 4 + 20 # Adjusted y position
            screen.blit(win_text, (win_text_x, win_text_y))

            # Render stars
            self.render_stars(screen, int(STAR))

            # Render other text
            score_text = regular_small_font.render(f"Score: {SCORE}", True, (252, 43, 113))
            next_text = press_font.render("Press ENTER to Play Again", True, (169, 47, 32))

            text_x = (WIDTH - score_text.get_width()) // 2
            text_y = HEIGHT // 2 - score_text.get_height()  # Adjusted y position

            # screen.blit(score_text, (text_x, text_y))
            screen.blit(next_text, (text_x - score_text.get_height() - 200, text_y + score_text.get_height())) 
            
        else:
            screen.blit(game_over_screen, (0, 0))
            over_text = game_over_font.render("GAME OVER", True, (251, 194, 7))

            over_text_width, _ = game_over_font.size("GAME OVER")
            over_text_x = (WIDTH - over_text_width) // 2
            over_text_y = HEIGHT // 4 - (WIDTH / 8)
            screen.blit(over_text, (over_text_x, over_text_y))

            play_again_text = regular_small_font.render("Press ENTER to Play Again", True, (255, 255, 255))
            screen.blit(play_again_text, (WIDTH / 2 - (WIDTH / 4), HEIGHT / 4 + (WIDTH / 16)))
            next_text = regular_small_font.render("Press 'L' to Accept the L :)", True, (255, 255, 255))
            screen.blit(next_text, (WIDTH / 2 - (WIDTH / 4), HEIGHT / 4 + (WIDTH / 8)))

class PauseState(GameState):
    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                self.game.toggle_pause()
                
    def render(self, screen):
        pass
        
# Game class
class Game:
    def __init__(self):
        self.running = True
        self.state = MainMenuState(self)
        
    def toggle_pause(self):
        global paused
        paused = not paused
            
    def run(self):
        global paused
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        
        clock = pygame.time.Clock()
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q or event.key == pygame.K_l:
                        self.running = False
                        break
                    if event.key == pygame.K_SPACE:
                        self.toggle_pause()  # Toggle pause when 'SPACE' key is pressed
            
            if not paused:  # Only update and render the game when not paused
                self.state.handle_events(events)
                self.state.update(events)
                self.state.render(screen)
                       # Render pause screen
            if paused:
                self.state.render_paused(screen)
            
            pygame.display.flip()
            clock.tick(30)
            
        pygame.quit()
        
# Main
if __name__ == '__main__':
    game = Game()
    game.run()