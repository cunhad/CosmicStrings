#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:40:12 2017

@author: eloisechakour
"""

import numpy as np
import cube
import density3D as dens
import math


"""
#Data acquisition
default_dataname = "pos(1)"
dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
if dataname == "":
  dataname = default_dataname
dataname = "../Data/" + dataname
dataname +=".npz"

print "Loading %s..." %dataname
xpos = np.load(dataname)['x']
ypos = np.load(dataname)['y']
zpos = np.load(dataname)['z']



#Rearranges into one 2D array
pos = np.zeros((3,len(xpos)))
pos[0,:] = xpos[:]
pos[1,:] = ypos[:]
pos[2,:] = zpos[:]
print "Done!"

density, size = dens.density(pos, speed = 1)
startl, endl = cube.lineParse(size)



numPoints = 93
"""


def formatting(startl, endl):

    
    start = np.zeros((27648, 3), dtype = int)
    for i in range(27648):
        for j in range(3):
            start[i, j] = int(startl[i][0][j])
            
    end = np.zeros((27648, 3), dtype = int)
            
    for i in range(27648):
        for j in range(3):
            end[i, j] = int(endl[i][0][j])
            
    return start, end


def center(start, end, size):
    myCube = []
    
    for i in range(size):
        for j in range(size):
            for k in range(size):
                myCube.append([i, j, k])
                
    if (size/2)%2 == 0:
        half = size/2
    else: 
        half = size/2 - 0.5

    
    for i in range(len(myCube)):
        myCube[i][0] = myCube[i][0] - half
        myCube[i][1] = myCube[i][1] - half
        myCube[i][2] = myCube[i][2] - half
    
    for i in range(len(start)):
        start[i, 0] = start[i, 0] - half 
        start[i, 1] = start[i, 1] - half 
        start[i, 2] = start[i, 2] - half 
        end[i, 0] = end[i, 0] - half
        end[i, 1] = end[i, 1] - half
        end[i, 2] = end[i, 2] - half
    
    return myCube, start, end



#Do this for each line
def normalize(startPoint, endPoint, centeredCube, size, index):
    """
    vector = []
    
    for i in range(3):
        vector.append((endPoint[i] - startPoint[i])/2)
    
    phi1 = math.atan2(vector[1], vector[0])
    theta1 = math.acos(vector[2]/(math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)))
    """
    
    newCube = np.transpose(centeredCube)
    endPoint = np.transpose(endPoint)

    position = -1
    
    for i in range(884736):
        array = []
        array.append(newCube[0, i])
        array.append(newCube[1, i])
        array.append(newCube[2, i])
        
        if np.array_equal(endPoint, array) == True :
            position = i
    
    
    phi = math.atan2(endPoint[1], endPoint[0])
    theta = math.acos(endPoint[2]/(math.sqrt(endPoint[0]**2 + endPoint[1]**2 + endPoint[2]**2)))
    

    Rphi = [[math.cos(phi), - math.sin(phi), 0], [math.sin(phi), math.cos(phi), 0], [0, 0, 1]]
    Rtheta = [[1, 0, 0], [0, math.cos(theta), - math.sin(theta)], [0, math.sin(theta), math.cos(theta)]]

    
    matrix = np.dot(Rphi, newCube, out = None)
    rotated = np.dot(Rtheta, matrix, out = None)

    """    
    vect = np.dot(Rphi, endPoint, out = None)
    rotatedVect = np.dot(Rtheta, vect, out = None)
    """
    
    zArray = []
    for i in range(len(rotated[0])):
        zArray.append(rotated[2, i])
    
    negativeMin = np.min(zArray)
    
    for i in range(len(zArray)):
        zArray[i] = zArray[i] + abs(negativeMin)

    
    length = np.max(zArray)
    
    lowerBound = math.floor(zArray[position])
    upperBound = math.ceil(zArray[position])

    
    counter = 0
    
    for i in range(len(zArray)):
        if zArray[i] < upperBound and zArray[i] >= lowerBound:
            counter += 1
        else: 
            continue
    
    return counter, length



"""
start, end = formatting(startl, endl)


centeredCube, centeredStart, centeredEnd = center(start, end, 96)

normFactors = []

count = 0
#for i in range(len(centeredStart)):
for i in range(10):
    factor, length = normalize(centeredStart[i], centeredEnd[i], centeredCube, 96, i)
    normFactors.append(factor)
    count += 1
    print ("Line %s" %count)


"""















