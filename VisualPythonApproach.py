import vpython as vp
import numpy as np
import pandas as pd
import random as r
import math



class SphereParticle():
        def __init__(self, position, velocity, size, mass):
             self.position = position
             self.velocity = velocity
             self.size = size
             self.mass = mass

        def bounceX(self):
            self.velocity[0] = -1 * self.velocity[0]

        def bounceY(self):
            self.velocity[1] = -1 * self.velocity[1]

        def bounceZ(self):
            self.velocity[2] = -1 * self.velocity[2]


class HeavyParticle(vp.vector):
    def __init__(self, mass, radius, position, velocity, *args):
        super().__init__(*args)
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity

#firstParticle = vp.sphere(pos = vp.vector(0,0,0), radius = 2, color = vp.color.green)

gravityVector = vp.vector(0,-4.9,0)

particleCount = 50

boundingField = (500,500,500)

startPosRng = [s for s in range(-20, 20)]

veloRng = [s for s in range(-10, 10) if s != 0]

sizeRng = [s for s in range(2) if s != 0]

#particleList = [SphereParticle(position = (r.choice(rng),r.choice(rng), r.choice(rng)), velocity = (r.choice(rng),r.choice(rng), r.choice(rng)), size = r.randint(0,3), mass = 0) for s in range(0, particleCount)] 

#pointerList = []

sphereList = [vp.sphere(pos = vp.vector(r.choice(startPosRng),r.choice(startPosRng), r.choice(startPosRng)), radius = r.choice(sizeRng)) for p in range(particleCount)]

x = 0
y = 0 
z = 0

#for s in sphereList:
    #pointerList.append(vp.arrow(pos = vp.vector(s.pos.x, s.pos.y, s.pos.z), axis = vp.vector(0,0,0), shaftwidth = 1, headwidth = 1, round = False))


sphereVelocities = [vp.vector(r.choice(veloRng),r.choice(veloRng),r.choice(veloRng)) for s in sphereList]

'''sphereList = [vp.sphere(pos = vp.vector(-10,0,0), 
                        radius = 1),
              vp.sphere(pos = vp.vector(10,0,0), 
                        radius = 1)]'''


#sphereVelocities = [vp.vector(r.choice(rng),r.choice(rng),r.choice(rng)) for s in sphereList]

boundingShape = False

if boundingShape == True:
    boundingBox = vp.box(pos = vp.vector(0,0,0), size  = vp.vector(boundingField[0],boundingField[1],boundingField[2]), thickness = 1)


#sphereOne = vp.sphere(pos = vp.vector(0,0,0), radius = .5)

#sphereOne.velocity = vp.vector(50,-70,-30)

debugMode = False

dt = 0.005
t = 0

simRunning = True

while simRunning == True:

    t = t + dt

    for s in sphereList:

        otherSphereList = [e for e in sphereList if e != s and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < 10]

        '''for p in pointerList:
            p.pos = s.pos

            for e in otherSphereList:
                p.axis = e.pos'''
        
        for e in otherSphereList:
            if abs(e.pos.x-s.pos.x) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                if sphereVelocity.x > 0:
                    sphereVelocity.x = -sphereVelocity.x
                else:
                    sphereVelocity = abs(sphereVelocity.x)
                if debugMode == True:
                    print(f'X Collision at: {s.pos.x}')

            elif abs(e.pos.y-s.pos.y) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                if sphereVelocity.y > 0:
                    sphereVelocity.y = -sphereVelocity.y
                else:
                    sphereVelocity = abs(sphereVelocity.y)
                if debugMode == True:
                    print(f'X Collision at: {s.pos.y}')
                
            elif abs(e.pos.z-s.pos.z) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                if sphereVelocity.z > 0:
                    sphereVelocity.z = -sphereVelocity.z
                else:
                    sphereVelocity = abs(sphereVelocity.z)
                if debugMode == True:
                    print(f'X Collision at: {s.pos.z}')

        sphereVelocity = sphereVelocities[sphereList.index(s)]

        s.pos = s.pos + (sphereVelocity * dt) #+ (gravityVector * dt**2))

        if s.pos.x + s.radius >= boundingField[0]/2 or s.pos.x - s.radius <= -boundingField[0]/2:
            sphereVelocity.x = -sphereVelocity.x
            if debugMode == True:
                print(f'X Collision at: {s.pos.x}')

        if s.pos.y + s.radius >= boundingField[1]/2 or s.pos.y - s.radius <= -boundingField[1]/2:
            sphereVelocity.y = -sphereVelocity.y
            if debugMode == True:
                print(f'Y Collision at: {s.pos.y}')
            
        if s.pos.z + s.radius >= boundingField[2]/2 or s.pos.z - s.radius <= -boundingField[2]/2:
            sphereVelocity.z = -sphereVelocity.z
            if debugMode == True:
                print(f'Z Collision at: {s.pos.z}')






    vp.rate(100)