import pygame
from random import uniform
from math import cos
from math import sin

class Entity:
    
    def __init__(self,x,y,mass,max_wander_angle,max_speed,max_force):
        self.pos = pygame.math.Vector2(x,y)
        self.vel = pygame.math.Vector2(0,0)
        self.mass = mass
        self.max_speed = max_speed
        self.max_force = max_force
        self.max_wander_angle = max_wander_angle
        
    def add_force(self,acc,time_deltaTime):
        acc = acc/self.mass
        if acc.x == 0 and acc.y == 0:
            return
        if(acc.magnitude() > self.max_force):
            self.vel += acc.normalize() * self.max_force * time_deltaTime
        else:
            self.vel += acc * time_deltaTime
            
            
    def move_on_tick(self,time_deltaTime):
        self.pos = self.pos + self.vel * time_deltaTime
        

    def move(self,desire_speed,time_deltaTime):
        if(time_deltaTime == 0):
            return
        desire_speed = desire_speed.normalize() * self.max_speed
        steering_speed = desire_speed - self.vel
        self.add_force(steering_speed/time_deltaTime,time_deltaTime)
        self.move_on_tick(time_deltaTime)

    #wander angle hace que cambie el ángulo speed un poquito
    def wander(self,time_deltaTime):
        if(self.vel.x == 0 and self.vel.y==0 or time_deltaTime==0):
            return
        displacement_dir = self.vel
        random_angle = uniform(-self.max_wander_angle/2,self.max_wander_angle/2)
        cos_angle = cos(random_angle)
        sin_angle = sin(random_angle)
        displacement_dir = pygame.math.Vector2(cos_angle*self.vel.x - sin_angle*self.vel.y,sin_angle*self.vel.x + cos_angle*self.vel.y)
        self.move(displacement_dir,time_deltaTime)
        #self.move(desire_speed,time_deltaTime)
        
               
        
            
        
        
