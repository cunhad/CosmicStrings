#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 17:51:25 2017

@author: eloisechakour
"""

import normalization_array as na
import numpy as np
import math


square = na.twins2d(na.quadrant_assignment(120))

nbCells = len(square)

nbSteps = 20.0*nbCells

def length(start, end):
    
    lineLen = []
    for line in range(nbCells):
        xLen = end[line][0] - start[line][0]
        yLen = end[line][1] - start[line][1]
        leng = math.sqrt(xLen**2 + yLen**2)
        lineLen.append(leng)
        
    return lineLen

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


def slope(start, end):
    slopes = []
    for line in range(nbCells):
        m = (end[line][1] - start[line][1])/(end[line][0] - start[line][0])
        slopes.append(m)
    
    return slopes

def yPositions(start, xArray, slopes):
    y = np.zeros((nbSteps, nbCells), dtype = np.float)
    for line in range(len(slopes)):
        for i in range(nbSteps):
            y[i, line] = slopes[line]*xArray[line][i] + start[line][1]
    
    return y

def normAtPoint(xArray, yArray):
    
    cubeIdx = np.zeros((nbCells, nbSteps), dtype = np.float)
    cubeIdy = np.zeros((nbCells, nbSteps), dtype = np.float)
    
    
    for line in range(nbCells):
        for i in range(nbSteps):
            for count in range(nbCells):
                if (xArray[line][i] <= (count+1)*20) and  (xArray[line][i] >= count*20):
                    cubeIdx[i, line] = count
                if (yArray[line][i] <= (count+1)*20) and  (yArray[line][i] >= count*20):
                    cubeIdy[i, line] = count
    
    coord = [0,0]
    coordSave = [-1, -1]
    normPtNum = np.zeros((nbCells, nbCells), dType = float)
    positionCounter = 0
    
    for line in range(nbCells):
        for step in range(nbSteps):
            coord[0] = cubeIdx[step, line]
            coord[1] = cubeIdy[step, line]
            if (coord[0] != coordSave[0]) or (coord[1] != coordSave[1]):
                normPtNum[positionCounter, line] = square[coord[0], coord[1]]
                positionCounter +=1 
                
            for counter in range(3):
                coordSave[counter] = coord[counter]
    
    return normPtNum


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



    
        
        
        






