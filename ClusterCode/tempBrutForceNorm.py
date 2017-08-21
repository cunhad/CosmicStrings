#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 15:40:12 2017

@author: eloisechakour
"""
import numpy as np
#import cube
#import density3D as dens
import math
import numpy.lib.arraysetops as aso
import time as t

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


def formatting(startArray, endArray):
    nbLines = np.shape(startArray)[0]
    startPoints = np.zeros((nbLines, 3), dtype = int)
    for i in range(nbLines):
        for j in range(3):
            startPoints[i, j] = startArray[i][0][j]
            
    endPoints = np.zeros((nbLines, 3), dtype = int)
            
    for i in range(nbLines):
        for j in range(3):
            endPoints[i, j] = endArray[i][0][j]
            
    return startPoints, endPoints

def reshape(xArray, yArray, zArray, size):
    #Watch out this '2' might be problematic when we change the amount of steps in Algo3
    nbSteps = 2*(size)
    lenght = np.shape(xArray)[1]
    nbLines = np.shape(xArray)[0]
    completeArray = np.zeros((lenght, nbLines, 3), dtype = int)
    for i in range(lenght):
        for j in range(nbSteps):
            tempx = xArray[i][j]
            tempy = yArray[i][j]
            tempz = zArray[i][j]
            completeArray[i, j, 0] = tempx
            completeArray[i, j, 1] = tempy
            completeArray[i, j, 2] = tempz
    
    return completeArray


def center(start, end, completeArray, size):
    lenght = np.shape(start)[1]
    nbLines = np.shape(start)[0]
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
    
    for i in range (lenght):
        for j in range (nbLines):
            completeArray[i, j, 0] = completeArray[i, j, 0] - half
            completeArray[i, j, 1] = completeArray[i, j, 1] - half
            completeArray[i, j, 2] = completeArray[i, j, 2] - half
    
    for i in range(len(start)):
        start[i][0] = start[i][0] - half 
        start[i][1] = start[i][1] - half 
        start[i][2] = start[i][2] - half 
        end[i][0] = end[i][0] - half
        end[i][1] = end[i][1] - half
        end[i][2] = end[i][2] - half
    

    return myCube, start, end, completeArray




#Do this for each point in each line
def normalize(completeArray, start, end, centeredCube, size, index):
    newCube = np.transpose(centeredCube)

    position = []
    
    nbLines = np.shape(start)[0]


    cubeSize = size**3
    print t.time()
    for k in range(nbLines):
        if not k%3 == 0:
            break
    #for k in range(len(completeArray)):
        for j in range(cubeSize):
            #array = []
            #array.append(newCube[:,j])
            #array.append(newCube[0, j])
            #array.append(newCube[1, j])
            #array.append(newCube[2, j])
        
            #if np.array_equal(completeArray[k], array) == True :
            if len(np.setdiff1d(completeArray[k], newCube[:,j])) == 0:
                position.append(j)
                print j
                break

    #####ADDED BY FELIX######
    if len(position) == 0:
        position.append(0)
    #######END#############

    x = end[0] - start[0]
    y = end[1] - start[1]
    z = end[2] - start[2]

    phi = -1*math.atan2(y, x)
    theta =-1* math.acos(z/(math.sqrt(x**2 + y**2 + z**2)))
        
    completeArray = np.transpose(completeArray)
    
    Rphi = [[math.cos(phi), - math.sin(phi), 0], [math.sin(phi), math.cos(phi), 0], [0, 0, 1]]
    Rtheta = [[1, 0, 0], [0, math.cos(theta), - math.sin(theta)], [0, math.sin(theta), math.cos(theta)]]

    completeArray = np.transpose(completeArray)
    matrix = np.dot(Rphi, newCube, out = None)
    rotated = np.dot(Rtheta, matrix, out = None)

    zArray = []
    for j in range(len(position)):
        zArray.append(rotated[2, position[j]])
    
    negativeMin = np.min(zArray)
    
    for j in range(len(zArray)):
        zArray[j] = zArray[j] + abs(negativeMin)

    lowerBound = []
    upperBound = []
    length = np.max(zArray)/size
    
    for j in range(len(zArray)):
        zArray[j] = np.divide(zArray[j],length)
    
    for j in range(len(zArray)):
        number = zArray[j]

        lowerBound.append(math.floor(number))
        upperBound.append(math.ceil(number))

    
    nbCells = []

    for k in range(len(upperBound)):
        counter = 0
        for i in range(len(zArray)): 
        #for i in range(10):
            if rotated[2, i] < upperBound[k] and zArray[i] >= lowerBound[k]:
                counter += 1
                
        nbCells.append(counter)

    
    return nbCells, length



def finalNormalization(xArray, yArray, zArray, size, startl, endl):
    
    newArray = reshape(xArray, yArray, zArray, size)
    cCube, cStart, cEnd, completeArray = center(startl, endl, newArray, size)
    normFactors = []
    lengths = []
    count = 0
    for i in range(len(completeArray)):
        factor, length = normalize(completeArray[i], cStart[i], cEnd[i], cCube, size, i)
        normFactors.append(factor)
        lengths.append(length)
        count += 1
        print ("Line %s" %count)
        #print time.time()
    return normFactors, lengths

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















