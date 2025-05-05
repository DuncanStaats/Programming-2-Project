import pygame 
from sys import exit
import os

GAME_WIDTH = 650  #Change Later, to file size if you want the full background
GAME_HIEGHT = 650

PLAYERX = GAME_WIDTH/2
PLAYERY = GAME_HIEGHT/2
PLAYER_WIDTH = 42 #change later to fit sprite image
PLAYER_HEIGHT = 48 #maintain ratio of sprite image
PLAYER_DISTANCE = 5

background_image = pygame.image.load(os.path.join("FOLDER_NAME", "FILE_NAME"))
player_image_right = pygame.image.load(os.path.join("FOLDER", "FILE"))#image draws from the top right, still a rectangle
player_image_right = pygame.transform.scale(player_image_right, (PLAYER_HEIGHT, PLAYER_WIDTH))

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HIEGHT))
pygame.display.set_caption("Duncan's Catching Fruit - Pygame")
clock = pygame.time.Clock()

class Player(pygame.Rect):
    def __init__(self):
        pygame.rect.__inti__(self,PLAYER_WIDTH,PLAYER_HEIGHT,PLAYERX,PLAYERY)
        self.image = player_image_right

player = Player()

def draw():
    window.fill("blue") #can use rgb colors tuple (())
    window.blit(background_image, (0,0)) #Order matters, image after #change position by changing numbers
    window.blit(player.image, player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x = max(player.x - PLAYER_DISTANCE, 0)
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x = min(player.x + PLAYER_DISTANCE, GAME_WIDTH - player.width)

    draw()
    pygame.display.update()
    clock.tick(60)