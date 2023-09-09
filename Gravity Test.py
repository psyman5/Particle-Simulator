import vpython as vp
import numpy as np
import random as r

sphere1 = vp.sphere(pos= vp.vector(0,0,0), radius = 1, make_trail = True)
sphere1.velocity = vp.vector(0,0,0)
sphere1.mass = 5
sphere1.p = vp.vector(sphere1.velocity.x * sphere1.mass, sphere1.velocity.y * sphere1.mass,sphere1.velocity.z * sphere1.mass)

#box = vp.box(pos = vp.vector(0,0,0), size = vp.vector(20,20,20))


boundingShape = False

boundingField = (100,100,100)

if boundingShape is True:
    box = vp.box(pos = vp.vector(0,0,0), size = vp.vector(boundingField[0],boundingField[1],boundingField[2]))

timeList = []
pList = []

rate = 1000

debugMode = False

t = 0
dt = .001

momentumGraph = vp.gcurve(color = vp.color.cyan, fast = True)

g = -9.81

gravity = vp.vector(0, -g ,0)

def sphereMoveMethod1(sphere1, dt):
    sphere1.pos += sphere1.velocity
    sphere1.velocity.y += g * dt**2
    #sphere1.p.y = sphere1.velocity.y * sphere1.mass
    return sphere1.pos, sphere1.velocity.y

def sphereMoveMethod2(sphere1,dt):
    sphere1.pos.x = sphere1.pos.x + (sphere1.velocity.x) * dt

    sphere1.pos.y = sphere1.pos.y + (sphere1.velocity.y) * dt

    sphere1.velocity.y += g * dt**2


    sphere1.pos.z = sphere1.pos.z + (sphere1.velocity.z) * dt


def sphereMoveMethod3(sphere1, dt):
    sphere1.pos += sphere1.velocity * dt
    sphere1.velocity.y += g * dt
    return sphere1.pos, sphere1.velocity.y

while True:
    vp.rate(rate)
    t = t + dt

    sphere1.pos, sphere1.velocity.y = sphereMoveMethod3(sphere1, dt)[0] , sphereMoveMethod3(sphere1, dt)[1]

    #sphere1.p.y = sphere1.velocity.y * sphere1.mass

    if sphere1.pos.x + sphere1.radius >= boundingField[0]/2 or sphere1.pos.x - sphere1.radius <= -boundingField[1]/2:
        if sphere1.pos.x > 0:
            sphere1.velocity.x = -sphere1.velocity.x
        else:
            sphere1.velocity.x = abs(sphere1.velocity.x)

    if sphere1.pos.y + sphere1.radius >= boundingField[1]/2 or sphere1.pos.y - sphere1.radius <= -boundingField[1]/2:
        if sphere1.pos.y > 0:
            sphere1.velocity.y = -sphere1.velocity.y
        else:
            sphere1.velocity.y = abs(sphere1.velocity.y)

    if sphere1.pos.z + sphere1.radius >= boundingField[2]/2 or sphere1.pos.z - sphere1.radius <= -boundingField[1]/2:
        if sphere1.pos.z > 0:
            sphere1.velocity.z = -sphere1.velocity.z
        else:
            sphere1.velocity.z = abs(sphere1.velocity.z)

    









































    '''t += dt
    timeList.append(t)
    vp.rate(rate)

    if sphere1.pos.x + sphere1.radius >= boundingField[0]/2 or sphere1.pos.x - sphere1.radius <= -boundingField[0]/2:
            sphere1.velocity.x = -sphere1.velocity.x
            if debugMode == True:
                print(f'X Collision at: {sphere1.pos.x}')

    if sphere1.pos.y + sphere1.radius >= boundingField[1]/2 or sphere1.pos.y - sphere1.radius <= -boundingField[1]/2:
        sphere1.velocity.y = -sphere1.velocity.y
        if debugMode == True:
                print(f'Y Collision at: {sphere1.pos.y}')
            
    if sphere1.pos.z + sphere1.radius >= boundingField[2]/2 or sphere1.pos.z - sphere1.radius <= -boundingField[2]/2:
        sphere1.velocity.z = -sphere1.velocity.z
        if debugMode == True:
            print(f'Z Collision at: {sphere1.pos.z}')

    elif abs(sphere1.p.y) != 0 or sphere1.pos.y >= boundingField[1]:
        sphere1.pos = (sphere1.pos) + ((sphere1.p) * vp.mag(sphere1.mass)**-1) * dt
        sphere1.velocity.y += -gravity.y
        #if -.1 < sphere1.p.y < .1 and sphere1.pos.y - sphere1.radius <= -10:
            #sphere1.p.y = 0
        #else:
        sphere1.p.y = sphere1.velocity.y * sphere1.mass.y
        sphere1.p.x = sphere1.velocity.x * sphere1.mass.x
        sphere1.p.z = sphere1.velocity.z* sphere1.mass.z
        #pList.append([sphere1.p.y])
    
        #momentumGraph.plot(t, abs(sphere1.p.y)/(rate/10), interval = 20)'''
    

 
