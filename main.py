import pygame 
from sys import exit

GAME_WIDTH = 650  #Change Later
GAME_HIEGHT = 650

pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HIEGHT))
pygame.display.set_caption("Duncan's Catching Fruit - Pygame")
clock = pygame.time.Clock()

player = pygame.Rect(150,150,50,50)

def draw():
    window.fill("blue") #can use rgb colors tuple (())
    pygame.draw.rect(window, (2, 239, 238), player)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 5

    draw()
    pygame.display.update()
    clock.tick(60)