import pygame 
import sys

pygame.init()

if len(sys.argv) == 1:
    raise NameError("You have to give a path to the image")

path = str(sys.argv[1])
My_image = pygame.image.load(path)

WIDTH = My_image.get_width()
HEIGHT = My_image.get_height()

gameDisplay = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Flow Field From Image')


gameDisplay.blit(My_image,(0,0))

clock = pygame.time.Clock()
crashed = False

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
    
    pygame.display.update()
    clock.tick(60)
