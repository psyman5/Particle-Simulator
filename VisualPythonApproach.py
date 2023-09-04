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


scene = vp.canvas(width = 1920, height = 1080)

#firstParticle = vp.sphere(pos = vp.vector(0,0,0), radius = 2, color = vp.color.green)

gravityVector = vp.vector(0, -9.81,0)

particleCount = abs(100)

rate = 3000

boundingField = (6000,6000,6000)

startPosRng = [s for s in range(int(-boundingField[0]/2), int(boundingField[0]/2))]

veloRng = [s for s in range(-2000, 2000) if s != 0]

sizeRng = [s for s in range(90) if s != 0]

#particleList = [SphereParticle(position = (r.choice(rng),r.choice(rng), r.choice(rng)), velocity = (r.choice(rng),r.choice(rng), r.choice(rng)), size = r.randint(0,3), mass = 0) for s in range(0, particleCount)] 

if particleCount < 100:
    sphereList = [vp.sphere(pos = vp.vector(r.choice(startPosRng),r.choice(startPosRng), r.choice(startPosRng)), radius = r.choice(sizeRng), make_trail = False, emissive = False) for p in range(particleCount)]
else:
    sphereList = [vp.simple_sphere(pos = vp.vector(r.choice(startPosRng),r.choice(startPosRng), r.choice(startPosRng)), radius = r.choice(sizeRng), make_trail = False, emissive = False) for p in range(particleCount)]

sphereArray = np.array(sphereList)

curveList = []

'''for s in sphereList:
    place = sphereList.index(s)
    if place < len(sphereList):
        curveList.append(vp.curve(vp.vector(s.pos.x,s.pos.y, s.pos.z), vp.vector(vp.vector(sphereList[sphereList.index(s) + 1].pos.x,sphereList[sphereList.index(s) + 1].pos.y, 
                                                                                          sphereList[sphereList.index(s) + 1].pos.z))))'''


sphereVelocities = [vp.vector(r.choice(veloRng),r.choice(veloRng),r.choice(veloRng)) for s in sphereList]
sphereVeloArray = np.array(sphereVelocities)



'''sphereList = [vp.sphere(pos = vp.vector(-10,0,0), 
                        radius = 1),
              vp.sphere(pos = vp.vector(10,0,0), 
                        radius = 1)]'''


#sphereVelocities = [vp.vector(r.choice(rng),r.choice(rng),r.choice(rng)) for s in sphereList]

boundingShape = False

if boundingShape is True:
    #boundingBox = vp.box(pos = vp.vector(0,0,0), size  = vp.vector(boundingField[0],boundingField[1],boundingField[2]), thickness = 1)
    boundingSphere = vp.sphere(pos = vp.vector(0,0,0), radius = boundingField[0])



#sphereOne = vp.sphere(pos = vp.vector(0,0,0), radius = .5)

#sphereOne.velocity = vp.vector(50,-70,-30)

numberOfCalculations= []



debugMode = False

dt = 1/rate
t = 0

coloringMode = True

simRunning = True

while simRunning is True:
    try:
        vp.rate(rate)
        t = t + dt

        for o in np.nditer(sphereArray, flags=['refs_ok','zerosize_ok']):

            s = o.item()

            otherSphereList = [e for e in sphereList if e != s and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*4]
            otherSphereArray = np.array(otherSphereList)
            '''if debugMode == True:
                numberOfCalculations.append(len(otherSphereList))'''
            
            sphereVelocity = sphereVelocities[sphereList.index(s)-1]

            
            for u in np.nditer(otherSphereArray, flags=['refs_ok','zerosize_ok']):

                e = u.item()

                if abs(e.pos.x-s.pos.x) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                    if sphereVelocity.x > 0:
                        sphereVelocity.x = -sphereVelocity.x
                    else:
                        sphereVelocity.x = abs(sphereVelocity.x)
                    if debugMode is True:
                        print(f'X Collision at: {s.pos.x}')

                elif abs(e.pos.y-s.pos.y) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                    if sphereVelocity.y > 0:
                        sphereVelocity.y = -sphereVelocity.y
                    else:
                        sphereVelocity.y = abs(sphereVelocity.y)
                    if debugMode is True:
                        print(f'X Collision at: {s.pos.y}')
                    
                elif abs(e.pos.z-s.pos.z) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                    if sphereVelocity.z > 0:
                        sphereVelocity.z = -sphereVelocity.z
                    else:
                        sphereVelocity.z = abs(sphereVelocity.z)
                    if debugMode is True:
                        print(f'X Collision at: {s.pos.z}')

            if s.pos.x + s.radius >= boundingField[0]/2 or s.pos.x - s.radius <= -boundingField[0]/2:
                sphereVelocity.x = -sphereVelocity.x
                if debugMode is True:
                    print(f'X Collision at: {s.pos.x}')

            if s.pos.y + s.radius >= boundingField[1]/2 or s.pos.y - s.radius <= -boundingField[1]/2:
                sphereVelocity.y = -sphereVelocity.y
                if debugMode is True:
                    print(f'Y Collision at: {s.pos.y}')
                
            if s.pos.z + s.radius >= boundingField[2]/2 or s.pos.z - s.radius <= -boundingField[2]/2:
                sphereVelocity.z = -sphereVelocity.z
                if debugMode is True:
                    print(f'Z Collision at: {s.pos.z}')

            try:
                s.pos.x += (sphereVelocity.x * dt)
            except AttributeError:
                print('X Attribute Error!')
                print(s.pos, s.color, sphereVelocity, t)
                s.color = vp.vector(255,0,255)
                scene.pause()
                scene.waitfor('keydown') 

            try:
                s.pos.y += (sphereVelocity.y * dt)
            except AttributeError:
                print('Y Attribute Error!')
                print(s.pos, s.color, sphereVelocity, t)
                s.color = vp.vector(255,0,255)
                scene.pause()
                scene.waitfor('keydown') 
                
            try:
                s.pos.z += (sphereVelocity.z * dt)
            except AttributeError:
                print('Z Attribute Error!')
                print(s.pos, s.color, sphereVelocity, t)
                s.color = vp.vector(255,0,255)
                scene.pause()
                scene.waitfor('keydown')
                

            sphereVelocities[sphereList.index(s)-1].y += -9.81* dt

            if sphereVelocities[sphereList.index(s)-1].y < 0:
                s.color = vp.vector(1, 0, 0)
            elif sphereVelocities[sphereList.index(s)-1].y > 0: 
                s.color = vp.vector(0, 0 , 1)
            elif sphereVelocities[sphereList.index(s)-1].y == 0:
                s.color = vp.vector(0, 1 , 0)
            

    except RuntimeError:
        SystemExit()