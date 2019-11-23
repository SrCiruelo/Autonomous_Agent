import pygame
from random import uniform
import math
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
