from vpython import *
import math
import cupy as cp
import numpy as np
import random as r

tickRate = 100
particleCount = 20
t = 0
dt = .001


boundingField = (100,100,100)

sphereList = [sphere(pos = vector(r.randint(-75,75), r.randint(-75,75), r.randint(-75,75)), radius = 1, make_trail = False) for s in range(particleCount)]
sphereArray = cp.asarray([s.pos.x,s.pos.y,s.pos.z] for s in sphereList) #TODO Fix this array transmutation magic.


sphereVelocities = [vector(r.randint(-100, 100), r.randint(-100, 100), r.randint(-100, 100)) for s in sphereList]
sphereVelocityArray = cp.asarray([v.x,v.y,v.z] for v in sphereVelocities)

def sphereMove(sphereVelocityArray, sphereList):
    for s in sphereArray:
        velo = sphereVelocityArray.__getitem__(sphereArray.where(sphereArray == s))
        s.pos += velo * dt

def sphereCollision(sphereList, sphereVelocities):

    for s in sphereList:

        otherSphereList = [e for e in sphereList if e != s and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*4]

        sphereVelocity = sphereVelocities[sphereList.index(s)-1]

        for e in otherSphereList:
            if abs(e.pos.x-s.pos.x) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                    if sphereVelocity.x > 0:
                        sphereVelocity.x = -sphereVelocity.x
                    else:
                        sphereVelocity.x = abs(sphereVelocity.x)


            elif abs(e.pos.y-s.pos.y) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                if sphereVelocity.y > 0:
                    sphereVelocity.y = -sphereVelocity.y
                else:
                    sphereVelocity.y = abs(sphereVelocity.y)

                    
            elif abs(e.pos.z-s.pos.z) < (e.radius + s.radius) and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*2:
                if sphereVelocity.z > 0:
                    sphereVelocity.z = -sphereVelocity.z
                else:
                    sphereVelocity.z = abs(sphereVelocity.z)

        if s.pos.x + s.radius >= boundingField[0]/2 or s.pos.x - s.radius <= -boundingField[0]/2:
            sphereVelocity.x = -sphereVelocity.x

        if s.pos.y + s.radius >= boundingField[1]/2 or s.pos.y - s.radius <= -boundingField[1]/2:
            sphereVelocity.y = -sphereVelocity.y
                
        if s.pos.z + s.radius >= boundingField[2]/2 or s.pos.z - s.radius <= -boundingField[2]/2:
            sphereVelocity.z = -sphereVelocity.z


while True:
    rate(tickRate)
    t += dt

    sphereMove(sphereVelocities,sphereList)

    sphereCollision(sphereList, sphereVelocities)