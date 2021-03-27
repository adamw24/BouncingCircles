import pygame, sys
from pygame.locals import *
import random
from array import *
from math import *
from tkinter import * 
import keyboard

BLACK = (0,0,0)
WHITE = (255,255,255)

root = Tk() 

window_width = root.winfo_screenwidth() -100
window_height = root.winfo_screenheight() -100
point_thickness = 3
display_surf = pygame.display.set_mode((window_width,window_height))

#Main Function
def main():
    pygame.init()
    global display_surf
    display_surf = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('Bouncing Circles Screensaver')
    display_surf.fill(BLACK)

#Particle object class.
class Particle:
    def __init__(self, x,y,size):
        self.x = x
        self.y = y
        self.radius = size
        self.thickness = 3
        self.color = (255,255,255)
        self.speed = random.randrange(3,6)
        self.direction = random.random()*2*pi

    #Draws the particle.
    def display(self):
        pygame.draw.circle(display_surf, self.color, (self.x, self.y), self.radius, self.thickness)
    
    #Checks if this particle collides with another particle.
    def collision(self, Particle):
        distance= dist((self.x,self.y),(Particle.x,Particle.y))
        if distance <= self.radius + Particle.radius:
            self_mass = (pi*self.radius**2)
            particle_mass = (pi*Particle.radius**2)
            sum_mass = self_mass + particle_mass
            speedx = self_mass*(self.speed*cos(self.direction)) + particle_mass*(Particle.speed*cos(Particle.direction))
            speedx /= sum_mass
            speedy = self_mass*(self.speed*sin(self.direction)) + particle_mass*(Particle.speed*sin(Particle.direction))
            speedy /= sum_mass
            self.speed = sqrt(speedx**2 + speedy**2)
            self.direction = atan2(speedy,speedx)
            self.x = (self.x*self_mass + Particle.x*particle_mass)/ sum_mass
            self.y = (self.y*self_mass + Particle.y*particle_mass)/ sum_mass
            self.radius = sqrt(self.radius**2 + Particle.radius**2)
            self.color = (random.randint(100,255), random.randint(100,255), random.randint(100,255))
            return True
        else:
            return False
    
    #Changes the position of the particle based on the speed direction. CHecks if it bounces against a wall or not.
    def move(self):
        self.direction %= (pi*2)
        change_x = cos(self.direction)*self.speed
        change_y= sin(self.direction)*self.speed
        if (change_x + self.x + self.radius >= window_width and (self.direction < pi/2 or self.direction > 3*pi/2))\
            or change_x + self.x - self.radius <=0 and (self.direction > pi/2 and self.direction < 3*pi/2):
                self.x -= change_x
                self.direction = (pi)-self.direction
        else:
            self.x += change_x

        if change_y + self.y + self.radius>= window_height and (self.direction > pi and self.direction < 2*pi) \
            or (change_y + self.y - self.radius <=0 and (self.direction < pi and self.direction > 0)):
            self.y += change_y
            self.direction *= -1
        else:
            self.y -= change_y
        self.direction %= (pi*2)

#Stores the displayed particles.
my_particles = []
num = 6
#Generates the particles with random size, speed, and starting positions and adds them to the list of particles.
def create_particles(num):  
    for n in range(num):
        size = random.randint(35, 55)
        x = random.randint(size, window_width-size)
        y = random.randint(size, window_height-size)
        my_particles.append(Particle(x, y, size))


create_particles(num)

#Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()  
    pygame.time.delay(10)
    display_surf.fill(BLACK)
    num_particles=len(my_particles)
    index = 0
    #Iterates through all the particles.
    while index < num_particles:
        particle = my_particles[index]
        check = 0
        #Checks if this particle collides with any other particle and if so, deletes the other particle.
        while check < num_particles:
            if check != index and particle.collision(my_particles[check]):
                del(my_particles[check])
                num_particles-=1
                break
            check +=1
        particle.move()
        particle.display()
        index +=1
    #Resets the demo with new particles.
    if keyboard.is_pressed('r'):
        my_particles.clear()
        display_surf.fill(BLACK)
        create_particles(num)

    pygame.display.flip()

if __name__=='__main__':
    main()
