from vpython import *
import math
import cupy as cp
import numpy as np
import random as r
from cupyx.profiler import benchmark




scene = canvas(width = 1280, height = 720)

speedGraph = graph(title='Speed Graph', xtitle='Particles', ytitle='Speed' )
#curve = gvbars(color=color.red, interval = 10)

tickRate = 1000
particleCount = 25
t = 0
dt = 1/10

boundingField = (1000,1000,1000)

boundingBox = box(pos = vector(0,0,0), size = vector(1000,1000,1000), color = color.blue)

startPosRng = [s for s in range(int(-boundingField[0]/2), int(boundingField[0]/2))]

veloRng = [s for s in range(-1000, 1000) if s != 0]

sizeRng = [s for s in range(10) if s != 0]

gravity = -9.81

#particleList = [SphereParticle(position = (r.choice(rng),r.choice(rng), r.choice(rng)), velocity = (r.choice(rng),r.choice(rng), r.choice(rng)), size = r.randint(0,3), mass = 0) for s in range(0, particleCount)] 

if particleCount <= 100:
    sphereList = [sphere(pos = vector(r.choice(startPosRng),r.choice(startPosRng), r.choice(startPosRng)), 
                                    radius = r.choice(sizeRng), make_trail = False, emissive = False) for p in range(particleCount)]
else:
    sphereList = [simple_sphere(pos = vector(r.choice(startPosRng),r.choice(startPosRng), r.choice(startPosRng)), 
                                           radius = r.choice(sizeRng), make_trail = False, emissive = False) for p in range(particleCount)]



sphereArrayMatrix = cp.asarray([[s.pos.x,s.pos.y,s.pos.z] for s in sphereList])



#sphereVelocitiesVectors = [vector(r.choice(veloRng), r.choice(veloRng), r.choice(veloRng)) for s in sphereList]

sphereVelocitiesVectors = [vector(0,0,0) for s in sphereList]

sphereVelocityMatrix = cp.asarray([[v.x,v.y,v.z] for v in sphereVelocitiesVectors])

gravityMatrix = cp.asarray([[-9.81] for v in sphereVelocityMatrix])


def sphereMove(sphereArrayMatrix, t):

    for index, s in enumerate(sphereArrayMatrix):
        velo = sphereVelocityMatrix[index, :]
        print(sphereVelocityMatrix)
        sphereVelocityMatrix[index, :] += gravity * dt
        print(sphereVelocityMatrix)
        s += velo * dt

        sphereList[index].pos = vector(s[0],s[1],s[2])



def sphereMoveAlternate(sphereArrayMatrix, sphereVelocityMatrix):

    sphereVelocityMatrix[:, 1] += gravityMatrix[:, 0] * dt

    sphereArrayMatrix += sphereVelocityMatrix * dt

    posMatrix = cp.asnumpy(sphereArrayMatrix)

    for index, s in enumerate(posMatrix):
        sphereList[index].pos = vector(s[0],s[1],s[2])


def sphereCollision(sphereList, sphereVelocityMatrix):

    for index, s in enumerate(sphereList):

        otherSphereList = [e for e in sphereList if e != s and math.sqrt(((e.pos.x-s.pos.x)**2)+((e.pos.y-s.pos.y)**2)+(((e.pos.z-s.pos.z)**2))) < s.radius*5]

        sphereVelocity = sphereVelocitiesVectors[index]

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

    sphereArrayMatrix = cp.asarray([[s.pos.x,s.pos.y,s.pos.z] for s in sphereList])

    sphereVelocityMatrix = cp.asarray([[v.x,v.y,v.z] for v in sphereVelocitiesVectors])

    return sphereArrayMatrix, sphereVelocityMatrix

def sphereColouring(sphereVelocityMatrix):
    for index, s in enumerate(sphereVelocityMatrix[:, 1]):
        if s < 0:
            sphereList[index].color = (vector(1,0,0))

        else:
            sphereList[index].color = (vector(0,0,1))


def graphingFunction():
    for index, s in enumerate(sphereVelocityMatrix[:, 1]):
        curve.plot(index, s)


#print(benchmark(sphereMoveAlternate, (sphereArrayMatrix, sphereVelocityMatrix), n_repeat= 10000))

#print(benchmark(sphereMove, args = (sphereArrayMatrix, t), n_repeat= 10000))

#print(benchmark(sphereCollision, (sphereList, sphereVelocityMatrix), n_repeat= 10000))



simRunning = True

while simRunning is True:
    rate(tickRate)
    t += dt


    sphereArrayMatrix, sphereVelocityMatrix = sphereCollision(sphereList, sphereVelocityMatrix)

    sphereMoveAlternate(sphereArrayMatrix, sphereVelocityMatrix)

    sphereColouring(sphereVelocityMatrix)



    

    print("Calculation Done! T = " + str(t) + " Seconds")

