
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
#testSize = 20
#cube = na.twins3d(na.octant_assignment(testSize))
#start, end = cb.lineParse(testSize)

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
        lengthArray.append(x)

    return lengthArray

#Define the length of steps necessary to have the apropriate number of steps
#and then find the x value for each point for each step
def xArray(start, end, length, nbSteps):
    stepsArray = np.zeros((len(start),nbSteps), dtype = np.int)
    stepLenArray = []

    for line in range(len(length)):
        lenSteps = np.divide(length[line], nbSteps, dtype=np.float)
        stepLenArray.append(lenSteps)

    for k in range(len(stepLenArray)):
        for l in range(nbSteps):
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
    print "--> Length..."
    nbSteps = findSteps(start)
    length = lineLen(start,end)
    print "--> X array..."    
    arrayx = xArray(start,end,length, nbSteps)
    print "--> Slopes..."    
    slopey = ySlope(start, end)
    slopez = zSlope(start, end)
    print "--> Y array..."
    arrayy = yArray(arrayx, start, slopey, nbSteps)
    print "--> Z array..."
    arrayz = zArray(arrayx, start, slopez, nbSteps)
    print "--> Making lines..."
    lines = []
    for i in range(len(arrayx)):
        lines.append(np.array([arrayx[i][:],arrayy[i][:], arrayz[i][:]]))
    return lines, arrayx, arrayy, arrayz#, slopey, slopez, length

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