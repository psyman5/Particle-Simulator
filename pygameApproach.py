import pygame
from pygame.locals import *
from ParticleClass import Particle
import random as r
import math

pygame.init()

class ColouredParticle(Particle): #class for particles with colour
    def __init__(self, x, y, rise, run, size, id, colour):
        super().__init__(x, y, rise, run, size, id)
        self.colour = colour

    def bounceX(self):
        self.run = -1 * self.run

    def bounceY(self):
        self.rise = -1 * self.rise

#random colours, change to fit preference
colour = (255,255,0)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)
#

v = 2

clock = pygame.time.Clock()

fps = 165 #limits the clock

fpsList = []

width = 1920

height = 1080

collisionList = []

screen = pygame.display.set_mode((width, height)) #sets to default fullscreen 1920x1080, change width and height for other resolutions

size = 5 #radius of particle drawings

particleCount = 10 #how many particles

particleAmount = []

boundingBox = (0,0,1280,720) #for bounded areas.

collDebugMode = False #debugger for collisions, ignore

debugMode = False #debugger for optimization, ignore


rng = [s for s in range(-10,10) if s != 0]



particleList = [ColouredParticle(x = r.randint(0 ,width), y = r.randint(0,height), #creation of ColouredParticle Class objects
                                 rise = r.choice(rng), run = r.choice(rng), size = size, 
                                 id = x, colour = (r.randint(0,255),r.randint(0,255),r.randint(0,255))) for x in range(0, particleCount)]

simRunning = True

while simRunning == True:
    i = 1

    keys = pygame.key.get_pressed()

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            simRunning = False
            if debugMode == True:
                print(fpsList,particleCount)
            if collDebugMode == True:
                print(particleAmount,collisionList)
                

        '''if event.type == pygame.KEYDOWN: #this is the code for keys, which is unimplemented.
            if event in keys:
                if keys[pygame.K_4]:
                    pygame.draw.circle(screen, (r.randint(0,255),r.randint(0,255),r.randint(0,255)), (p.x,p.y), p.size)
                    particleList.append(ColouredParticle(x = pygame.mouse.get_pos()[0], y = pygame.mouse.get_pos()[1],
                                                        rise = r.choice(rng), run = r.choice(rng), size = size,
                                                            id = particleCount+i,colour = (r.randint(0,255),r.randint(0,255),r.randint(0,255))))
                    i += 1
                    pygame.display.update()


                elif keys[pygame.K_0]:
                    screen.fill(black)
                    del particleList[:]
                    pygame.display.update()

                elif keys[pygame.K_1]:
                    hwnd = win32gui.GetForegroundWindow()
                    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

                elif keys[pygame.K_2]:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    width, height = 1920, 1080
                    pygame.display.update()

                elif keys[pygame.K_3]:
                    width, height = 1280,720
                    screen = pygame.display.set_mode((width, height))'''

    for p in particleList: #particle movement and collision detection

        otherParticleList = [e for e in particleList if e != p and (math.sqrt((((e.x+size)-(p.x + size))**2)+(((e.y+size)-(p.y+size))**2))) < size] #collision detection on particles
                                                                                                                                                    #within a certain distance

        for e in otherParticleList: #operates on particles in distance specified in list comprehension above

            if abs(e.x-p.x) < (e.size + p.size) and math.sqrt((((e.x+size)-(p.x + size))**2)+(((e.y+size)-(p.y+size))**2)) < size*2: #x axis detection
                p.bounceX()
                e.bounceX()
                if collDebugMode == True:
                    print('Collision at: ' + str([[e.x,e.y,e.id],[p.x,p.y,p.id]]))
                    collisionList.append([[e.x,e.y],[p.x,p.y],pygame.time.get_ticks()])

            if abs(e.y-p.y) < (e.size + p.size) and math.sqrt((((e.x+size)-(p.x + size))**2)+(((e.y+size)-(p.y+size))**2)) < size*2: #y axis detection
                p.bounceY()
                e.bounceY()
                if collDebugMode == True:
                                    print('Collision at: ' + str([[e.x,e.y,e.id],[p.x,p.y,p.id]]))
                                    collisionList.append([[e.x,e.y],[p.x,p.y],pygame.time.get_ticks()])

        if (p.x + p.size >= width) or (p.x - p.size <= width) or (p.y + p.size >= height) or (p.y - p.size <= height): #wall detection section
            if p.x - p.size <= 0 or p.x + p.size >= width:
                p.bounceX()
            elif p.y + p.size <= 0 or p.y + p.size >= height:
                p.bounceY()
            pygame.draw.circle(screen, black, ((p.x+p.run,p.y + p.rise)), p.size* size*.75)
            p.x += p.run 
            p.y += p.rise
            pygame.draw.circle(screen, p.colour, (p.x,p.y), p.size)

        elif ((0) < p.x < width) and ((0) < p.y < height):
            pygame.draw.circle(screen, black, ((p.x+p.run,p.y+p.rise)), p.size* size*.75)
            p.x += p.run
            p.y += p.rise
            pygame.draw.circle(screen, p.colour, (p.x,p.y), p.size)

        pygame.display.update()

    
    if debugMode == True: #debug stuff, ignore
        fpsList.append(int(clock.get_fps()))

pygame.quit()
