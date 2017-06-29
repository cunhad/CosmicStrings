#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 18:35:55 2017

@author: eloisechakour
"""

import normalization_array as na
import numpy as np
import math


cube = na.twins3d(na.octant_assignment(9))

nbCells = len(cube)
count = 0
cubeNb = cube

for x in range(nbCells):
    for y in range(nbCells):
        for z in range(nbCells):
            count += 1
            cube[x][y][z] = count



# Define a line by its start and end points

startPt = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
endPt = [[8, 8, 8], [8, 8, 8], [8, 8, 8]]
slope = 0

dirVect = np.zeros((nbCells,len(startPt)), dtype = np.float)

for h in range(nbCells):
    for i in range(len(startPt)):
        #slope = (endPt[h][i] - startPt[h][i])
        dirVect[h, i] = slope




#Find a measure for each cube

nbSteps = 20.0*nbCells

normFact = 0
point = []
store = [-1, -1, -1]
normFactArray = []

xPos = []
yPos = []
zPos = []
x = 0
y = 0
z = 0


def lineLen(start, end):
    lengthArray = []
    for line in range(nbCells):
        x = end[line][0] - start[line][0]
        y = end[line][1] - start[line][1]
        z = end[line][2] - start[line][2]
        lineLength = math.sqrt(x**2 + y**2 + z**2)
        lengthArray.append(lineLength)


    return lengthArray

def xArray(start, end, length):
    stepsArray = np.zeros((nbCells, len(start)), dtype = np.float)
    stepLenArray = []
    
    for line in range(nbCells):
        xStart = start[line][0]
        xEnd = end[line][0]
        lenSteps = length[line]/nbSteps
        stepLenArray.append(lenSteps)
    
    for k in range(len(stepLenArray)):
        for l in range(nbSteps):
            stepsArray[k, l] = start[k][0] + l*lenSteps
            
    return stepsArray
    
def ySlope(start, end):
    my = 0
    slopeYArray = []
    for i in range(len(start)):
        my = (end[i][1] - start[i][1])/(end[i][0] - start[i][0])
        slopeYArray.append(my)
    
    return slopeYArray

def zSlope(start, end):
    mz = 0
    slopeZArray = []
    for i in range(len(start)):
        mz = (end[i][2] - start[i][2])/(end[i][0] - start[i][0])
        slopeZArray.append(mz)
    
    return slopeZArray
    
    
def yArray(xIncrements, start, ySlope):
    yArray = np.zeros((nbCells, nbSteps), dtype = np.float)
    for i in range(nbCells):
        for j in range(nbSteps):
            yArray[i, j] = xIncrements[i, j]*ySlope[i][j] + start[i][1]
    
    return yArray
    
def yArray(xIncrements, start, zSlope):
    zArray = np.zeros((nbCells, nbSteps), dtype = np.float)
    for i in range(nbCells):
        for j in range(nbSteps):
            zArray[i, j] = xIncrements[i, j]*zSlope[i][j] + start[i][2]
    
    return zArray
    



    
    
    
    
    
    
    #We need to do this for each line 
"""
for line in range(nbCells):
    
    #Make array of x cube ids
    xCount = startPt[line][0]*20
    while xCount*20*dirVect[line][0] <= endPt[line][0]:
        for m in range(length):
            if (xCount*20*dirVect >= m*cubeLength) and (xCount*20*dirVect <= (m+1)*cubeLength):
                xPos.append(m)
        xCount += 1
        
    #Make array of y cube ids
    yCount = startPt[line][1]*20
    while xCount*20*dirVect[line][1] <= endPt[line][1]:
        for n in range(length):
            if (yCount*20*dirVect >= n*cubeLength) and (yCount*20*dirVect <= (n+1)*cubeLength):
                yPos.append(n)
        yCount += 1
      
    #Make array of z cube ids
    zCount = startPt[line][2]*20
    while xCount*20*dirVect[line][2] <= endPt[line][2]:
        for p in range(length):
            if (zCount*20*dirVect >= p*cubeLength) and (zCount*20*dirVect <= (p+1)*cubeLength):
                zPos.append(p)
        zCount += 1
    
    # Find the total cube ids and make sure they are unique
    
    
    
    for counter in range(first, last):
        for x in range(nbCells):
            for y in range(nbCells):
                for z in range(nbCells):
                
    
        
"""      
        
        
        
        
                
            
        
        
    






















