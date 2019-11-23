import pygame
from random import randint
import math
import numpy as np
import Entity
import Flow_field
    
width = 800
height = 600

pygame.init()

my_characters = []

number_of_characters = 40

for x in range(0,number_of_characters):
    my_characters.append(Entity.Entity(randint(0,200),randint(10,500),1,50,0.2,0.001))

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('A bit Racey')

clock = pygame.time.Clock()

crashed = False
mouse_pos = pygame.math.Vector2()
flow_width = width/24
flow_height = height/24
flow_field = Flow_field.Flow_field(flow_width,flow_height,Flow_field.Angle_fromNoise)
show_field = False
                      
while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos[0] = event.pos[0]
            mouse_pos[1] = event.pos[1]
        elif event.type == pygame.KEYDOWN:
            if(event.key == pygame.K_SPACE):
                show_field = not show_field
    for x in my_characters:
        loc_x = int(x.pos.x/width*flow_field.width)
        loc_y = int(x.pos.y/height*flow_field.height)
        if loc_x >= flow_width or loc_y >= flow_height:
            x.pos.x = randint(0,200)
            x.pos.y = randint(10,500)
            loc_x = int(x.pos.x/width*flow_field.width)
            loc_y = int(x.pos.y/height*flow_field.height)
        desire_speed = flow_field.get_vector(loc_x,loc_y)
        x.move(desire_speed ,clock.get_time())
        pygame.draw.circle(gameDisplay,(255,20,20),(int(x.pos.x),int(x.pos.y)),2)

    if show_field:
        for x in range(0,int(flow_width)):
            for y in range(0,int(flow_height)):
                flow_pos = pygame.math.Vector2(x/flow_width * width,y/flow_height*height)
                end_line_pos = flow_pos + flow_field.get_vector(x,y) * 13
                pygame.draw.line(gameDisplay,(200,10,80),flow_pos,end_line_pos,1)
                
    pygame.display.update()
    clock.tick(60)
    #ameDisplay.fill((0,0,0))




