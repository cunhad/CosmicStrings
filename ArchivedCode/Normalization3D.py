#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 18:35:55 2017

@author: eloisechakour
"""

import normalization_array as na
import numpy as np
import math

# Make new cube with octant assignment
cube = na.twins3d(na.octant_assignment(9))


#Define useful length
nbCells = len(cube)


"""
for x in range(nbCells):
    for y in range(nbCells):
        for z in range(nbCells):
            count += 1
            cubeNb[x][y][z] = count
"""

"""
# Define a line by its start and end points

startPt = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
endPt = [[8, 8, 8], [8, 8, 8], [8, 8, 8]]
slope = 0

dirVect = np.zeros((nbCells,len(startPt)), dtype = np.float)

for h in range(nbCells):
    for i in range(len(startPt)):
        #slope = (endPt[h][i] - startPt[h][i])
        dirVect[h, i] = slope

"""


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

# Define the length of a line in number of cells
def lineLen(start, end):
    lengthArray = []
    for line in range(nbCells):
        x = end[line][0] - start[line][0]
        y = end[line][1] - start[line][1]
        z = end[line][2] - start[line][2]
        lineLength = math.sqrt(x**2 + y**2 + z**2)
        lengthArray.append(lineLength)


    return lengthArray

#Define the length of steps necessary to have the apropriate number of steps and then find the x value for each point for each step
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

#Find the y slope of the line (vs x)  
def ySlope(start, end):
    my = 0
    slopeYArray = []
    for i in range(len(start)):
        my = (end[i][1] - start[i][1])/(end[i][0] - start[i][0])
        slopeYArray.append(my)
    
    return slopeYArray

#Find the z slope of the line (vs x) 
def zSlope(start, end):
    mz = 0
    slopeZArray = []
    for i in range(len(start)):
        mz = (end[i][2] - start[i][2])/(end[i][0] - start[i][0])
        slopeZArray.append(mz)
    
    return slopeZArray
    
#Find the points on the y axis corresponding to the x point
def yArray(xIncrements, start, ySlope):
    yArray = np.zeros((nbCells, nbSteps), dtype = np.float)
    for i in range(nbCells):
        for j in range(nbSteps):
            yArray[i, j] = xIncrements[i, j]*ySlope[i][j] + start[i][1]
    
    return yArray
  
    
#Find the points on the z axis corresponding to the x point
def zArray(xIncrements, start, zSlope):
    zArray = np.zeros((nbCells, nbSteps), dtype = np.float)
    for i in range(nbCells):
        for j in range(nbSteps):
            zArray[i, j] = xIncrements[i, j]*zSlope[i][j] + start[i][2]
    
    return zArray
    
"""
def normPerLine(xArray, yArray, zArrays):
    cubeIdx = np.zeros((nbCells, nbSteps), dtype = np.float)
    cubeIdy = np.zeros((nbCells, nbSteps), dtype = np.float)
    cubeIdz = np.zeros((nbCells, nbSteps), dtype = np.float)
    
    for i in range(nbSteps):
        for j in range(nbCells):
            for k in range(nbCells):
                if (xArray[i][j] <= (k+1)*20) and  (xArray[i][j] >= k*20):
                    cubeIdx[i, j] = k
                if (yArray[i][j] <= (k+1)*20) and  (yArray[i][j] >= k*20):
                    cubeIdy[i, j] = k
                if (zArray[i][j] <= (k+1)*20) and  (zArray[i][j] >= k*20):
                    cubeIdz[i, j] = k
            
    
    coordinate = [0, 0, 0]
    coordinateSave = [-1, -1, -1]
    lineNorm = []
    normFact = 0
    for line in range(nbCells):
        for step in range(nbSteps):
            coordinate[0] = cubeIdx[step, line]
            coordinate[1] = cubeIdy[step, line]
            coordinate[2] = cubeIdz[step, line]
    
            if (coordinate[0] != coordinateSave[0]) or (coordinate[1] != coordinateSave[1]) or (coordinate[2] != coordinateSave[2]):
                normFact += cube[coordinate[0], coordinate[1], coordinate[2]]
            
            for counter in range(3):
                coordinateSave[counter] = coordinate[counter]
        
        lineNorm.append(normFact)
        normFact = 0
        
    return lineNorm
"""

#Find the normalization factor for each distinct square the line passes through
#We will need to divide by this number
def normAtPoint(xArray, yArray, zArray):
    
    cubeIdx = np.zeros((nbCells, nbSteps), dtype = np.float)
    cubeIdy = np.zeros((nbCells, nbSteps), dtype = np.float)
    cubeIdz = np.zeros((nbCells, nbSteps), dtype = np.float)
    
    for i in range(nbSteps):
        for j in range(nbCells):
            for k in range(nbCells):
                if (xArray[i][j] <= (k+1)*20) and  (xArray[i][j] >= k*20):
                    cubeIdx[i, j] = k
                if (yArray[i][j] <= (k+1)*20) and  (yArray[i][j] >= k*20):
                    cubeIdy[i, j] = k
                if (zArray[i][j] <= (k+1)*20) and  (zArray[i][j] >= k*20):
                    cubeIdz[i, j] = k
            
    
    coordinate = [0, 0, 0]
    normPtNum = np.zeros((nbCells, nbCells), dType = float)
    coordinateSave = [-1, -1, -1]
    positionCounter = 0
    for line in range(nbCells):
        for step in range(nbSteps):
            coordinate[0] = cubeIdx[step, line]
            coordinate[1] = cubeIdy[step, line]
            coordinate[2] = cubeIdz[step, line]
        
            if (coordinate[0] != coordinateSave[0]) or (coordinate[1] != coordinateSave[1]) or (coordinate[2] != coordinateSave[2]):
                normPtNum[positionCounter, line] = cube[coordinate[0], coordinate[1], coordinate[2]]
                positionCounter +=1 
                
            for counter in range(3):
                coordinateSave[counter] = coordinate[counter]
        
    
    
    return normPtNum
    

#Find the total normalization factor for each line that we will need to divide by at each point

def totalNormFact(normPtNum):
    lineNorm = []
    normFact = 0
    
    for line in range(nbCells):
        for i in range(nbCells):
            if normPtNum[i, line] != 0.0:
                normFact += 1.0/normPtNum[i, line]
                
        lineNorm.append(normFact)
        normFact = 0
    
    
    return lineNorm
        
        
        
                
            
        
        
    






















