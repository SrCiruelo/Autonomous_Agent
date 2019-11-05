import pygame

class Entity:
    
    def __init__(self,x,y,mass,slow_radius,max_speed,max_force):
        self.pos = pygame.math.Vector2(x,y)
        self.vel = pygame.math.Vector2(0,0)
        self.mass = mass
        self.max_speed = max_speed
        self.max_force = max_force
        self.slow_radius = slow_radius
        
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
