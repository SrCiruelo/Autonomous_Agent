import pygame
from random import uniform
from random import randint
import math
import numpy as np
from perlin_noise import perlin_noise


class Flow_field:
    #callback function needs returning a vector and two arguments pos x and pos y
    def __init__(self,width,height,callback_per_pixel):
        self.width = int(width)
        self.height = int(height)
        self.arr = []
        for x in range(0,int(width*height)):
            self.arr.append(callback_per_pixel(x/width,x%width))
            
    def get_vector(self,x,y):
        index = self.width*y + x
        if index>self.width*self.height:
            return
        return self.arr[int(index)]

def random_flow_field(x,y):
    random_angle = uniform(0,math.pi*2)
    x_coor = math.cos(random_angle)
    y_coor = math.sin(random_angle)
    vector = pygame.math.Vector2(x_coor,y_coor)
    return vector

def Angle_fromNoise(x,y):
    noise = perlin_noise(x/800*200,y/600*200)*2-1
    noise *= math.pi 
    vec = pygame.math.Vector2(math.cos(noise),math.sin(noise))
    return vec

class Entity:
    
    def __init__(self,x,y,mass,slow_radius,max_speed,max_force):
        self.pos = pygame.math.Vector2(x,y)
        self.vel = pygame.math.Vector2(0,0)
        self.mass = mass
        self.max_speed = max_speed
        self.max_force = max_force
        self.slow_radius = slow_radius
        
    def add_force(self,acc,time_deltaTime):
        acc = acc/self.mass;
        if acc.x == 0 and acc.y == 0:
            return
        if(acc.magnitude() > self.max_force):
            self.vel += acc.normalize() * self.max_force * time_deltaTime
        else:
            self.vel += acc * time_deltaTime
            
            
    def move_on_tick(self,time_deltaTime):
        self.pos = self.pos + self.vel * time_deltaTime
        
    def follow(self,x, y, time_deltaTime):
        if(time_deltaTime == 0):
            return
        desire_speed = pygame.math.Vector2(x,y)  - self.pos
        if desire_speed.x==0 and desire_speed.y==0:
            return
        max_speed = self.max_speed
        dist_to_obj = desire_speed.magnitude()
        if dist_to_obj<self.slow_radius:
            max_speed = max_speed * dist_to_obj/self.slow_radius
        desire_speed = desire_speed.normalize() * max_speed
        steering_speed = desire_speed - self.vel
        self.add_force(steering_speed/time_deltaTime,time_deltaTime)
        self.move_on_tick(time_deltaTime)

    def move(self,desire_speed,time_deltaTime):
        if(time_deltaTime == 0):
            return
        desire_speed = desire_speed.normalize() * self.max_speed
        steering_speed = desire_speed - self.vel
        self.add_force(steering_speed/time_deltaTime,time_deltaTime)
        self.move_on_tick(time_deltaTime)

    
width = 800
height = 600

pygame.init()

my_characters = []

number_of_characters = 40

for x in range(0,number_of_characters):
    my_characters.append(Entity(randint(0,200),randint(10,500),1,50,0.2,0.001))

gameDisplay = pygame.display.set_mode((width,height))
pygame.display.set_caption('A bit Racey')

clock = pygame.time.Clock()

crashed = False
mouse_pos = pygame.math.Vector2()
flow_width = width/24
flow_height = height/24
flow_field = Flow_field(flow_width,flow_height,Angle_fromNoise)
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




