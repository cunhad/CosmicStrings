#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 17:11:20 2017

@author: eloisechakour
"""
import normalization_array as na
import numpy as np


#Data acquisition
default_dataname = "pos(1)"
dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
if dataname == "":
  dataname = default_dataname
dataname = "../Data/" + dataname
dataname +=".npz"

print ("Loading %s..." %dataname)
xpos = np.load(dataname)['x']
ypos = np.load(dataname)['y']
zpos = np.load(dataname)['z']



#Rearranges into one 2D array
pos = np.zeros((3,len(xpos)))
pos[0,:] = xpos[:]
pos[1,:] = ypos[:]
pos[2,:] = zpos[:]
print ("Done!")

size = 120


# Make new cube with octant assignment
cube = na.twins3d(na.octant_assignment(size))


xpos = xpos[:10000]
ypos = ypos[:10000]
zpos = zpos[:10000]


#Define useful length
nbCells = len(cube)


#Find a measure for each cube

nbSteps = 20.0*nbCells

xMax = xpos[0]
yMax = ypos[0]
zMax = zpos[0]

xMin = xpos[0]
yMin = ypos[0]
zMin = zpos[0]


xCell = []
yCell = []
zCell = []

for i in range(len(xpos)):
    if xpos[i] < xMin:
        xMax = xpos[i]
    if ypos[i] < yMin:
        yMax = ypos[i]
    if zpos[i] < zMin:
        zMax = zpos[i]


for i in range(len(xpos)):
    xpos[i] = xpos[i] + abs(xMin)
    ypos[i] = ypos[i] + abs(yMin)
    zpos[i] = zpos[i] + abs(zMin)


for i in range(len(xpos)):
    if xpos[i] > xMax:
        xMax = xpos[i]
    if ypos[i] > yMax:
        yMax = ypos[i]
    if zpos[i] > zMax:
        zMax = zpos[i]

        



for i in range(len(xpos)):
    xpos[i] = (xpos[i]/xMax)*size
    ypos[i] = (ypos[i]/yMax)*size
    zpos[i] = (zpos[i]/zMax)*size


print ("values normalized")


for i in range(len(xpos)):
    for cell in range(size):
        if xpos[i] < cell+1 and xpos[i] > cell:
            xCell.append(cell)

print ("x done")  

for i in range(len(ypos)):
    for cell in range(size):
        if ypos[i] < cell+1 and ypos[i] > cell:
            yCell.append(cell)

print ("y done")

for i in range(len(zpos)):
    for cell in range(size):
        if zpos[i] < cell+1 and zpos[i] > cell:
            zCell.append(cell)


print ("z done")

density = np.zeros((size, size, size), dtype = float)



for i in range(size):
    print(i)
    for j in range(size):
        for k in range(size):
            for pos in range(len(xCell)):
                if xCell[pos] == i and yCell[pos] == j and zCell[pos] == k:
                   density[i, j, k] += 1.0 




















