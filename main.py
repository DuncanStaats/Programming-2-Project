import pygame 
from sys import exit
import os

GAME_WIDTH = 512  #Change Later, to file size if you want the full background
GAME_HEIGHT = 512

PLAYERX = GAME_WIDTH / 2
PLAYERY = GAME_HEIGHT / 2
PLAYER_WIDTH = 42 #change later to fit sprite image
PLAYER_HEIGHT = 48 #maintain ratio of sprite image
PLAYER_JUMP_WIDTH = 52
PLAYER_JUMP_HEIGHT = 60
PLAYER_DISTANCE = 5

GRAVITY = 1
PLAYER_VELOCITY_Y = -10
FLOOR_Y = GAME_HEIGHT * 3/4

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


pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Duncan's Catching Fruit - Pygame")
clock = pygame.time.Clock()

class Player(pygame.Rect):
    def __init__(self):
        pygame.Rect.__init__(self, PLAYERX, PLAYERY, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.image = player_image_right
        self.velocity_y = 0
        self.direction ="right"
        self.jumping = False

    def update_image(self):
        if self.jumping:
            self.width = PLAYER_JUMP_WIDTH
            self.height = PLAYER_HEIGHT
            if self.direction == "right":
                self.image = player_image_jump_right
            elif self.direction == "left":
                self.image = player_image_jump_left
        else:
            self.width = PLAYER_WIDTH
            self.height = PLAYER_HEIGHT
            if self.direction == "right":
                self.image = player_image_right
            elif self.direction == "left":
                self.image = player_image_left

player = Player()

def move():
    player.velocity_y += GRAVITY
    player.y += player.velocity_y

    if player.y + player.height > FLOOR_Y:
        player.y = FLOOR_Y - player.height
        player.jumping = False

def draw():
    window.fill("blue") #can use rgb colors tuple (())
    window.blit(background_image, (0,0)) #Order matters, image after #change position by changing numbers'
    player.update_image()
    window.blit(player.image, player)

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
        player.x = max(player.x - PLAYER_DISTANCE, 0)
        player.direction = "left"
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x = min(player.x + PLAYER_DISTANCE, GAME_WIDTH - player.width)
        player.direction = "right"

    move()
    draw()
    pygame.display.update()
    clock.tick(60)