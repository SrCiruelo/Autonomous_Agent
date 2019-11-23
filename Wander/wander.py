import pygame
from random import randint
from random import uniform
import math
import numpy as np
import Entity
    
width = 800
height = 600

pygame.init()

my_characters = []

number_of_characters = 1

for x in range(0,number_of_characters):
    my_characters.append(Entity.Entity(randint(0,200),randint(10,500),1,math.pi,100,800))
    my_characters[x].vel = pygame.math.Vector2(uniform(0,0.2),uniform(0,0.2))

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('A bit Racey')

clock = pygame.time.Clock()

crashed = False
mouse_pos = pygame.math.Vector2()
flow_width = width/24
flow_height = height/24
                      
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos[0] = event.pos[0]
            mouse_pos[1] = event.pos[1]
    for x in my_characters:
        x.wander(clock.get_time()/1000)
        pygame.draw.circle(gameDisplay,(255,20,20),(int(x.pos.x),int(x.pos.y)),4)
                
    pygame.display.update()
    clock.tick(60)
    gameDisplay.fill((0,0,0))
