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

pygame.init()

my_character = Entity(0,0,1,50,300,500)

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')

clock = pygame.time.Clock()

crashed = False
mouse_pos = pygame.math.Vector2()

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos[0] = event.pos[0]
            mouse_pos[1] = event.pos[1]
    my_character.follow(mouse_pos[0],mouse_pos[1],clock.get_time()/1000)
    pygame.draw.circle(gameDisplay,(255,20,20),(int(my_character.pos.x),int(my_character.pos.y)),20)
    pygame.display.update()
    clock.tick(60)
    gameDisplay.fill((0,0,0))



