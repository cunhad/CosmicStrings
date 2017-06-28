#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:39:14 2017

@author: donnashimizu
"""
import numpy as np
import matplotlib.pyplot as p

newarray = np.fromfile("0.000xv0.dat", dtype=np.float32) 

def separate(newarray):
    newarray =  newarray[12:]
    position = []
    velocity = []
    i = 0 
    while (1):
        if(i == len(newarray)):
            break
        position.append(newarray[i])
        i+=1
        position.append(newarray[i])
        i+=1
        position.append(newarray[i])
        i+=1
        velocity.append(newarray[i])
        i+=1
        velocity.append(newarray[i])
        i+=1 
        velocity.append(newarray[i])
        i+=1
    return position, velocity



pos, velocity = separate(newarray)
x = pos[0::3]
y = pos[1::3]
z = pos[2::3]
xvel = velocity[0::3]
yvel = velocity[1::3]
zvel = velocity[2::3]

#p.scatter(x,y)
#p.xlabel("x-axis")
#p.ylabel("y-axis")
#p.show()
#p.scatter(y,z)
#p.xlabel("y-axis")
#p.ylabel("z-axis")
#p.show()
#p.scatter(z,x)
#p.xlabel("z-axis")
#p.ylabel("x-axis")
#p.show()

p.hist2d(x, y, (50,50), cmap=p.cm.jet)
p.colorbar()
p.show()
p.hist2d(y, z, (50,50), cmap=p.cm.jet)
p.colorbar()
p.show()
p.hist2d(z, x, (50,50), cmap=p.cm.jet)
p.colorbar()
p.show()









