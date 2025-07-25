# Imports necessary modules
import pygame 
from sys import exit
import os
import random

# Game constants
GAME_WIDTH = 512
GAME_HEIGHT = 512
TILE_SIZE = 32

GAME_RUNNING = True
GAME_OVER = False

PLAYERX = GAME_WIDTH / 2
PLAYERY = GAME_HEIGHT / 2
PLAYER_WIDTH = 42
PLAYER_HEIGHT = 48
PLAYER_JUMP_WIDTH = 52
PLAYER_JUMP_HEIGHT = 60
PLAYER_DISTANCE = 5
PLAYER_LIFE_COUNT = 3

GRAVITY = 0.5
FRICTION = 0.4
DEATH_FLOOR = GAME_HEIGHT - PLAYER_HEIGHT
PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -11

FRUIT_GRAVITY = 0.05
FRUIT_GRAVITY_INCREASE = 0
FRUIT_WIDTH = 36
FRUIT_HEIGHT = 30
FRUIT_COUNT = 0

# Function for loading and Scaleing Images
def load_image(image_name, scale=None):
    """Load an image from the 'image' directory and scale if needed."""
    image = pygame.image.load(os.path.join("image", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

# Load game images
background_image = load_image("Tree_background.webp")
player_image_right = load_image("Sprite_image_test.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_left = load_image("Sprite_image_test1.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_right = load_image("Sprite_image_test2.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_jump_left = load_image("Sprite_image_test3.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
floor_tile_image = load_image("Lava Tile.png", (TILE_SIZE, TILE_SIZE))
fruit_image = load_image("Fruit.png", (FRUIT_WIDTH, FRUIT_HEIGHT))

# Initialize pygame modules
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Duncan's Catching Fruit - Pygame")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 36)

# Game Object Classes
class Player(pygame.Rect):
    """Player class with movement and image stuff."""
    def __init__(self):
        pygame.Rect.__init__(self, PLAYERX, PLAYERY, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction ="right"
        self.jumping = False

    def update_image(self):
        """Updates player image based on jump and direction it moves in."""
        if self.jumping:
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        else:
            if self.direction == "right":
                self.image = player_image_right
            elif self.direction == "left":
                self.image = player_image_left

class Fruit(pygame.Rect):
    """Fruit class representing falling objects you collect."""
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, FRUIT_WIDTH, FRUIT_HEIGHT)
        self.image = fruit_image
        self.velocity_y = 0

class Tile(pygame.Rect):
    """Tile class representing floor blocks."""
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

# Game Utility Functions
def create_map():
    """Create initial game map with floor tiles and spawn first fruit."""
    for i in range(13):
        tile = Tile((i+3)*TILE_SIZE, player.y + TILE_SIZE*6, floor_tile_image)
        tiles.append(tile)

    for i in range(3):
        tile = Tile(i*TILE_SIZE, 11.5*TILE_SIZE, floor_tile_image)
        tiles.append(tile)

    spawn_fruit()

def check_tile_collision(character):
    """Checks for collision between a character and a tile."""
    for tile in tiles:
        if character.colliderect(tile):
            return tile
    return None

def check_tile_collisionx(character):
    """Solves horizontal collisions."""
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_x < 0:
            character.x = tile.x + tile.width
        elif character.velocity_x > 0:
            character.x = tile.x - character.width
        character.velocity_x = 0

def check_tile_collisiony(character):
    """Solves vertical collisions and checks death conditions."""
    global PLAYER_LIFE_COUNT, GAME_RUNNING, GAME_OVER
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_y < 0:
            character.y = tile.y + tile.height
        elif character.velocity_y > 0:
            character.y = tile.y - character.height
            character.jumping = False
        character.velocity_y = 0

    # Fall below screen death
    if player.bottom > DEATH_FLOOR:
        player.topleft = (GAME_WIDTH / 2, GAME_HEIGHT - 2*PLAYER_HEIGHT)
        PLAYER_LIFE_COUNT -= 1

    if PLAYER_LIFE_COUNT == 0:
        GAME_RUNNING = False
        GAME_OVER = True

    return PLAYER_LIFE_COUNT, GAME_RUNNING, GAME_OVER

def move():
    """Applys movement, collision checks, and updates the fruit position."""
    global FRUIT_COUNT, PLAYER_LIFE_COUNT

    # Applys horizontal friction
    if player.direction == "left" and player.velocity_x < 0:
        player.velocity_x += FRICTION
    elif player.direction == "right" and player.velocity_x > 0:
        player.velocity_x -= FRICTION
    else:
        player.velocity_x = 0

    # Moves player horizontally
    player.x += player.velocity_x
    if player.x < 0:
        player.x = 0
    elif player.x + player.width > GAME_WIDTH:
        player.x = GAME_WIDTH - player.width

    check_tile_collisionx(player)

    # Applys gravity and vertical movement
    player.velocity_y += GRAVITY
    player.y += player.velocity_y
    check_tile_collisiony(player)

    # Moves fruits and check for collisions
    for fruit in fruits[:]:
        fruit.velocity_y += FRUIT_GRAVITY
        fruit.y += fruit.velocity_y

        for tile in tiles:
            if fruit.colliderect(tile):
                fruits.remove(fruit)
                PLAYER_LIFE_COUNT -= 1
                spawn_fruit()
                break

        if player.colliderect(fruit):
            fruits.remove(fruit)
            FRUIT_COUNT += 1
            spawn_fruit()

    gravity_increase()

    return FRUIT_COUNT, PLAYER_LIFE_COUNT

def gravity_increase():
    """Gradually increase fruit fall speed every 15 caught."""
    global FRUIT_GRAVITY, FRUIT_GRAVITY_INCREASE

    if FRUIT_COUNT // 15 > FRUIT_GRAVITY_INCREASE:
        FRUIT_GRAVITY += 0.025
        FRUIT_GRAVITY_INCREASE = FRUIT_COUNT // 15
        print(FRUIT_GRAVITY)

    return FRUIT_GRAVITY, FRUIT_GRAVITY_INCREASE

def spawn_fruit():
    """Spawn a new fruit at a random position at the top of the screen."""
    random_x = random.randint(0, (GAME_WIDTH // TILE_SIZE) - 1) * TILE_SIZE
    fruit = Fruit(random_x, 0)
    fruits.append(fruit)

def game_over():
    """Display game over screen with final score."""
    game_over_text = FONT.render("GAME OVER", True, (200, 200, 200))
    score_text = FONT.render(f"You Caught {FRUIT_COUNT} Fruits", True, (200, 200, 200))
    window.fill((0, 0, 0))
    window.blit(game_over_text, (GAME_WIDTH / 2 - game_over_text.get_width() / 2, GAME_HEIGHT / 2 - 50))
    window.blit(score_text, (GAME_WIDTH / 2 - score_text.get_width() / 2, GAME_HEIGHT / 2 + 10))
    pygame.display.update()

def display_score(x, y):
    """Render the score text."""
    score_img = font.render(f"Total Score: {str(FRUIT_COUNT)}", True, [0, 0, 0])
    window.blit(score_img, (x, y))

def display_life(x, y):
    """Render the life count text."""
    score_img = font.render(f"Life Count: {str(PLAYER_LIFE_COUNT)}", True, [0, 0, 0])
    window.blit(score_img, (x, y))

def draw():
    """Drawing all elements on the screen."""
    window.fill("blue")
    window.blit(background_image, (0,0))

    for tile in tiles:
        window.blit(tile.image, tile)

    player.update_image()
    window.blit(player.image, player)
    
    for fruit in fruits:
        window.blit(fruit.image, fruit)
    
    display_score(fontX, fontY + 25)
    display_life(fontX, fontY)

# Fonts and Game Stuff
pygame.font.init()
font = pygame.font.Font("freesansbold.ttf", 15)
fontX = 15
fontY = 15

player = Player()
fruits = []
tiles = []
create_map()

# Main Game Loop 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # Keyboard input
    keys = pygame.key.get_pressed()
    if (keys[pygame.K_UP] or keys[pygame.K_w]) and not player.jumping:
        player.velocity_y = PLAYER_VELOCITY_Y
        player.jumping = True
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.velocity_x = -PLAYER_VELOCITY_X
        player.direction = "left"
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.velocity_x = PLAYER_VELOCITY_X
        player.direction = "right"

    move()
    draw()
    pygame.display.update()
    clock.tick(60)

    if GAME_OVER:
        game_over()
        pygame.time.wait(5000)
        pygame.quit()
        exit()