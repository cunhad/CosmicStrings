#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 28 18:35:55 2017

@author: eloisechakour
"""

#import normalization_array as na
import numpy as np
import cube as cb

# Make new cube with octant assignment
testSize = 20
#cube = na.twins3d(na.octant_assignment(testSize))
start, end = cb.lineParse(testSize)

#Define useful length
#nbCells = len(cube)

#Find a measure for each cube
def findSteps(start):
    nbCells = np.max(start)+1
    nbSteps = 2*nbCells
    return nbSteps

def lineLen(start, end):
    lengthArray = []
    for line in range(len(start)):
        x = end[line][0] - start[line][0]
#        x = np.abs(end[line][0] - start[line][0])
        lengthArray.append(x)

    return lengthArray

#Define the length of steps necessary to have the apropriate number of steps
#and then find the x value for each point for each step
def xArray(start, end, length, nbSteps):
    stepsArray = np.zeros((len(start),nbSteps), dtype = np.int)
    stepLenArray = []

    for line in range(len(length)):
       # lenSteps = np.divide(length[line], nbSteps, dtype=np.float)
        lenSteps = np.divide(length[line], nbSteps, dtype=np.float)
#        lenSteps = length[line]/nbSteps
        stepLenArray.append(lenSteps)

    for k in range(len(stepLenArray)):
#        print start[k][0]
#        print stepLenArray[k]        
        for l in range(nbSteps):
            #stepsArray[k, l] = np.floor(start[k][0] + l*stepLenArray[k])

            stepsArray[k, l] = np.rint(start[k][0] + l*stepLenArray[k])
    return stepsArray

#Find the y slope of the line (vs x)
def ySlope(start, end):
    #did you know: this script was originally named
    #newBresenham_not_really.py !
    m = 0
    slope = []
    for i in range(len(start)):
        if not end[i][0] == start[i][0]:
            m = np.divide(end[i][1] - start[i][1], end[i][0] - start[i][0], dtype=np.float)
        else:
            m = np.nan
        slope.append(m)

    return slope

#Find the z slope of the line (vs x)
def zSlope(start, end):
    m = 0
    slope = []
    for i in range(len(start)):
        if not end[i][0] == start[i][0]:
            m = np.divide(end[i][2] - start[i][2], end[i][0] - start[i][0], dtype=np.float)
        else:
            m = np.nan
        slope.append(m)

    return slope

#Find the points on the y axis corresponding to the x point
def yArray(increments, start, slope, nbSteps):
    array = np.zeros((len(start),nbSteps), dtype = np.int)
    for i in range(len(start)):
        for j in range(nbSteps):
            if slope[i] is not np.nan:
                array[i, j] = np.rint((increments[i, j]-start[i][0])*slope[i] + start[i][1])
            else:
                array[i, j] = np.rint((increments[i, j]-start[i][0])*i + start[i][1])

    return array

def yArray_mp(increments, start, slope, nbSteps, lineNumber):
    array = np.zeros((nbSteps,1), dtype = np.int)
    for i in range(nbSteps):
        if slope is not np.nan:
            array[i] = np.rint((increments[i]-start[0])*slope + start[1])
        else:
            array[i] = np.rint((increments[i]-start[0])*lineNumber + start[1])
        
    return array

#Find the points on the z axis corresponding to the x point
def zArray(increments, start, slope, nbSteps):
    array = np.zeros((len(start),nbSteps), dtype = np.int)
#    zArray = np.zeros((nbCells, nbSteps), dtype = np.float)
    for i in range(len(start)):
        for j in range(nbSteps):
            if slope[i] is not np.nan:
                array[i, j] = np.rint((increments[i, j]-start[i][0])*slope[i] + start[i][2])
            else:
                array[i, j] = np.rint((increments[i, j]-start[i][0])*i + start[i][2])

    return array
    
def zArray_mp(increments, start, slope, nbSteps, lineNumber):
    array = np.zeros((nbSteps,1), dtype = np.int)
    for i in range(nbSteps):
        if slope is not np.nan:
            array[i] = np.rint((increments[i]-start[0])*slope + start[1])
        else:
            array[i] = np.rint((increments[i]-start[0])*lineNumber + start[1])
            
    return array

def lineCreation(start, end):
#    print "Length..."
    nbSteps = findSteps(start)
    length = lineLen(start,end)
#    print "X array..."    
    arrayx = xArray(start,end,length, nbSteps)
#    print "Slopes..."    
    slopey = ySlope(start, end)
    slopez = zSlope(start, end)
#    print "Y array..."
    arrayy = yArray(arrayx, start, slopey, nbSteps)
#    print "Z array..."
    arrayz = zArray(arrayx, start, slopez, nbSteps)
#    print "Making lines..."
#    lines = np.array([arrayx[:],arrayy[:],arrayz[:]])
    lines = []
    for i in range(len(arrayx)):
        lines.append(np.array([arrayx[i][:],arrayy[i][:], arrayz[i][:]]))
#    lines = np.zeros((np.size(arrayx, axis=0), np.size(arrayx, axis=1),3), dtype=np.int)
#    for line in range(len(arrayx)):
#        for cell in range(len(arrayx[line])):
#            lines[line,cell] = np.array([arrayx[line][cell],arrayy[line][cell],arrayz[line][cell]])

    return lines#, arrayx, arrayy, arrayz, slopey, slopez, length

def initLineCreation_mp(start, end):
    print "Steps..."
    nbSteps = findSteps(start)
    length = lineLen(start,end)
    print "X array..."    
    x = xArray(start,end,length, nbSteps)
    print "Slopes..."    
    my = ySlope(start, end)
    mz = zSlope(start, end)
    
    return nbSteps, x, my, mz
    
def lineCreation_mp(nbSteps, start, x, slopey, slopez, lineNumber):
#    print "Y Array..."
    arrayy = yArray_mp(x, start, slopey, nbSteps, lineNumber)
#    print "Z Array..."    
    arrayz = zArray_mp(x, start, slopez, nbSteps, lineNumber)
    
    return arrayy, arrayz
    
def multiprocessLine(nbSteps, start, x, my, mz, lineNumber):
    y,z = lineCreation_mp(nbSteps, start, x, my, mz, lineNumber)
    
    lines = []
    for i in range(len(x)):
        lines.append(np.array([x[i],y[i], z[i]]))
    
    return lines
    
#lines = lineCreation(start,end)
#lines, arrayx, arrayy, arrayz, slopey, slopez, length = lineCreation(start,end)
#print np.shape(lines)
#print lines
































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

"""




























