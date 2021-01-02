import pygame, sys
from pygame.locals import *
import random
from array import *
import math
from tkinter import * 
import keyboard

BLACK = (0,0,0)
WHITE = (255,255,255)

root = Tk() 

window_width = root.winfo_screenwidth()-200
window_height = root.winfo_screenheight()-100
point_thickness = 3
display_surf = pygame.display.set_mode((window_width,window_height))

#Main Function
def main():
    pygame.init()
    global display_surf
    display_surf = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('Moving Particles')

#Draws the black window and divider line. 
def drawArena():
    display_surf.fill((0,0,0))
    #Draw outline of arena
    pygame.draw.rect(display_surf, BLACK, ((0,0),(window_width,window_height)))
    #Draw center line

class Particle:
    def __init__(self, x,y,size):
        self.x = x
        self.y = y
        self.radius = size
        self.thickness = 4
        self.color = (255,255,255)
        self.speed = random.random()* 0.5 #random.randrange(1,2)
        self.direction = random.random()*2*math.pi

    def display(self):
        pygame.draw.circle(display_surf, self.color, (self.x, self.y), self.radius, self.thickness)
    
    def collision(self, Particle):
        dist = math.dist((self.x,self.y),(Particle.x,Particle.y))
        if dist <= self.radius + Particle.radius:
            if self.radius < Particle.radius:
                self.speed = Particle.speed
                self.x = Particle.x
                self.y = Particle.y
            self.direction = ((self.direction + Particle.direction)/2)
            self.radius = math.sqrt(self.radius**2 + Particle.radius**2)
            self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
            return True
        else:
            return False
            
    def move(self):
        change_x = math.cos(self.direction)*self.speed
        change_y= math.sin(self.direction)*self.speed
        bounce = False
        if change_x + self.x >= window_width or change_x + self.x <=0:
            self.x -= change_x
            self.direction = (math.pi)-self.direction
            bounce = True
        else:
            self.x += change_x

        if change_y + self.y >= window_height or change_y +self.y <=0:
            self.y -= change_y
            self.direction *= -1
            bounce = True
        else:
            self.y += change_y
        self.direction %= (math.pi*2)

my_particles = []
num = 15
def create_particles(num):  
    for n in range(num):
        size = random.randint(15, 40)
        x = random.randint(size, window_width-size)
        y = random.randint(size, window_height-size)
        my_particles.append(Particle(x, y, size))

drawArena()
create_particles(num)

#Main Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()  
    pygame.time.delay(10)
    display_surf.fill(BLACK)
    num_particles=len(my_particles)
    index = 0
    while index < num_particles:
        particle = my_particles[index]
        check =0
        while check < num_particles:
            if check != index and particle.collision(my_particles[check]):
                del(my_particles[check])
                num_particles-=1
                break
            check +=1
        particle.move()
        particle.display()
        index +=1
    if keyboard.is_pressed('r'):
        my_particles.clear()
        display_surf.fill(BLACK)

        create_particles(num)

    pygame.display.flip()

if __name__=='__main__':
    main()
