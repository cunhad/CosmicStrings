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
    my = 0
    slopeYArray = []
    for i in range(len(start)):
        if not end[i][0] == start[i][0]:
            my = np.divide(end[i][1] - start[i][1], end[i][0] - start[i][0], dtype=np.float)
        else:
            my = np.nan
        slopeYArray.append(my)

    return slopeYArray

#Find the z slope of the line (vs x)
def zSlope(start, end):
    mz = 0
    slopeZArray = []
    for i in range(len(start)):
        if not end[i][0] == start[i][0]:
            mz = np.divide(end[i][2] - start[i][2], end[i][0] - start[i][0], dtype=np.float)
        else:
            mz = np.nan
        slopeZArray.append(mz)

    return slopeZArray

#Find the points on the y axis corresponding to the x point
def yArray(xIncrements, start, ySlope, nbSteps):
    yArray = np.zeros((len(start),nbSteps), dtype = np.int)
    for i in range(len(start)):
        for j in range(nbSteps):
            if ySlope[i] is not np.nan:
                yArray[i, j] = np.rint((xIncrements[i, j]-start[i][0])*ySlope[i] + start[i][1])
            else:
                yArray[i, j] = np.rint((xIncrements[i, j]-start[i][0])*i + start[i][1])

    return yArray

#Find the points on the z axis corresponding to the x point
def zArray(xIncrements, start, zSlope, nbSteps):
    zArray = np.zeros((len(start),nbSteps), dtype = np.int)
#    zArray = np.zeros((nbCells, nbSteps), dtype = np.float)
    for i in range(len(start)):
        for j in range(nbSteps):
            if zSlope[i] is not np.nan:
                zArray[i, j] = np.rint((xIncrements[i, j]-start[i][0])*zSlope[i] + start[i][2])
            else:
                zArray[i, j] = np.rint((xIncrements[i, j]-start[i][0])*i + start[i][2])

    return zArray

def lineCreation(start, end):
    print "Length..."
    nbSteps = findSteps(start)
    length = lineLen(start,end)
    print "X array..."    
    arrayx = xArray(start,end,length, nbSteps)
    print "Slopes..."    
    slopey = ySlope(start, end)
    slopez = zSlope(start, end)
    print "Y array..."
    arrayy = yArray(arrayx, start, slopey, nbSteps)
    print "Z array..."
    arrayz = zArray(arrayx, start, slopez, nbSteps)
    print "Making lines..."
#    lines = np.array([arrayx[:],arrayy[:],arrayz[:]])
    lines = []
    for i in range(len(arrayx)):
        lines.append(np.array([arrayx[i][:],arrayy[i][:], arrayz[i][:]]))
#    lines = np.zeros((np.size(arrayx, axis=0), np.size(arrayx, axis=1),3), dtype=np.int)
#    for line in range(len(arrayx)):
#        for cell in range(len(arrayx[line])):
#            lines[line,cell] = np.array([arrayx[line][cell],arrayy[line][cell],arrayz[line][cell]])

    return lines#, arrayx, arrayy, arrayz, slopey, slopez, length


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




























