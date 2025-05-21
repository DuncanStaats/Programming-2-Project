import pygame 
from sys import exit
import os
import random

GAME_WIDTH = 512  #Change Later, to file size if you want the full background
GAME_HEIGHT = 512
TILE_SIZE = 32

PLAYERX = GAME_WIDTH / 2
PLAYERY = GAME_HEIGHT / 2
PLAYER_WIDTH = 42 #change later to fit sprite image
PLAYER_HEIGHT = 48 #maintain ratio of sprite image
PLAYER_JUMP_WIDTH = 52
PLAYER_JUMP_HEIGHT = 60
PLAYER_DISTANCE = 5

GRAVITY = 0.5
FRICTION = 0.4
PLAYER_VELOCITY_X = 5
PLAYER_VELOCITY_Y = -11

FRUIT_GRAVITY = 0.05
FRUIT_GRAVITY_INCREASE = 0
FRUIT_WIDTH = 36 #change to ratio
FRUIT_HEIGHT = 30
FRUIT_COUNT = 0

def load_image(image_name, scale=None):
    image = pygame.image.load(os.path.join("image", image_name))
    if scale is not None:
        image = pygame.transform.scale(image, scale)
    return image

background_image = load_image("Tree_background.webp") #("FILE_NAME")
player_image_right = load_image("Sprite_image_test.png", (PLAYER_WIDTH, PLAYER_HEIGHT))#(""FILE") #image draws from the top right, still a rectangle
player_image_left = load_image("Sprite_image_test1.png", (PLAYER_WIDTH, PLAYER_HEIGHT))
player_image_jump_right = load_image("Sprite_image_test2.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
player_image_jump_left = load_image("Sprite_image_test3.png", (PLAYER_JUMP_WIDTH, PLAYER_JUMP_HEIGHT))
floor_tile_image = load_image("Lava Tile.png", (TILE_SIZE, TILE_SIZE))
fruit_image = load_image("Fruit.png", (FRUIT_WIDTH, FRUIT_HEIGHT))


pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Duncan's Catching Fruit - Pygame")
clock = pygame.time.Clock()

class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, PLAYERX, PLAYERY, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_x = 0
        self.velocity_y = 0
        self.direction ="right"
        self.jumping = False

    def update_image(self):
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
    def __init__(self, x, y):
        pygame.Rect.__init__(self, x, y, FRUIT_WIDTH, FRUIT_HEIGHT)
        self.image = fruit_image
        self.velocity_y = 0

class Tile(pygame.Rect):
    def __init__(self, x, y, image):
        pygame.Rect.__init__(self, x, y, TILE_SIZE, TILE_SIZE)
        self.image = image

def create_map():
    for i in range(13):
        tile = Tile((i+3)*TILE_SIZE, player.y + TILE_SIZE*6, floor_tile_image)
        tiles.append(tile)

    for i in range(3):
        tile = Tile(i*TILE_SIZE, 11.5*TILE_SIZE, floor_tile_image)
        tiles.append(tile)

    spawn_fruit()

def check_tile_collision(character):
    for tile in tiles:
        if character.colliderect(tile):
            return tile
    return None
    
def check_tile_collisionx(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_x < 0:
            character.x = tile.x + tile.width
        elif character.velocity_x > 0:
            character.x = tile.x - character.width
        character.velocity_x = 0

def check_tile_collisiony(character):
    tile = check_tile_collision(character)
    if tile is not None:
        if character.velocity_y < 0:
            character.y = tile.y + tile.height
        elif character.velocity_y > 0:
            character.y = tile.y - character.height
            character.jumping = False
        character.velocity_y = 0

def move():
    global FRUIT_COUNT

    if player.direction == "left" and player.velocity_x < 0:
        player.velocity_x += FRICTION
    elif player.direction == "right" and player.velocity_x > 0:
        player.velocity_x -= FRICTION
    else:
        player.velocity_x = 0

    player.x += player.velocity_x
    if player.x < 0:
        player.x = 0
    elif player.x + player.width > GAME_WIDTH:
        player.x = GAME_WIDTH - player.width

    check_tile_collisionx(player)

    player.velocity_y += GRAVITY
    player.y += player.velocity_y

    check_tile_collisiony(player)
    for fruit in fruits: 
        fruit.velocity_y += FRUIT_GRAVITY
        fruit.y += fruit.velocity_y
        check_tile_collisiony(fruit)
        
        if player.colliderect(fruit): 
            fruits.remove(fruit)
            FRUIT_COUNT += 1
            spawn_fruit() 
            break 

    gravity_increase()

    return FRUIT_COUNT

def gravity_increase():
    global FRUIT_GRAVITY, FRUIT_GRAVITY_INCREASE

    if FRUIT_COUNT // 15 > FRUIT_GRAVITY_INCREASE:
        FRUIT_GRAVITY += 0.025
        FRUIT_GRAVITY_INCREASE = FRUIT_COUNT // 15
        print(FRUIT_GRAVITY)

    return FRUIT_GRAVITY, FRUIT_GRAVITY_INCREASE

def spawn_fruit():
    random_x = random.randint(0, (GAME_WIDTH // TILE_SIZE) - 1) * TILE_SIZE
    fruit = Fruit(random_x, 0)
    fruits.append(fruit)

def draw():
    window.fill("blue") #can use rgb colors tuple (())
    window.blit(background_image, (0,0)) #Order matters, image after #change position by changing numbers'

    for tile in tiles:
        window.blit(tile.image, tile)

    player.update_image()
    window.blit(player.image, player)
    
    for fruit in fruits:
        window.blit(fruit.image, fruit)

player = Player()
fruits = []
tiles = []
create_map()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
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