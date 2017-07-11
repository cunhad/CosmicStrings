#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:30:02 2017

@author: eloisechakour

Take a start point and an end point and make an array that contains angles 
array[hight][length]
"""

import numpy as np
import math

start = list(np.load("../Data/startEndPts.npz")['startArr'])
end = list(np.load('../Data/startEndPts.npz')['endArr'])

print(start)

def startf(start):
    startf = [[]]
    endf = [[]]
    for i in range(len(start)):
            temps = []
            temps.append(float(start[i][0,0]))
            temps.append(float(start[i][0,1]))
            temps.append(float(start[i][0,2]))
            startf.append(temps)
    return(startf)

    
def endf(end):
    endf = [[]]
    for i in range(len(end)):
        tempe = []
        tempe.append(float(end[i][0,0]))
        tempe.append(float(end[i][0,1]))
        tempe.append(float(end[i][0,2]))
        endf.append(tempe)
    return endf




def dirVector(myArray1, myArray2):
    
    dirVect = []
    
    if(len(myArray1) != len(myArray2)):
        print("The array lengths don't match.")
        return " "
    else:
        hight = len(myArray1)
        length = len(myArray1[0])
        dirVect = [[0 for col in range(length)] for row in range(hight)]
        for j in range(length):
            for i in range (hight):
                diff = myArray2[i][j] - myArray1[i][j]
                dirVect[i][j] = diff
    
    return dirVect
        
 
    

def findTheta(vect):
    hight = len(vect)
    aTheta = [0 for row in range(hight)]
    for i in range(hight):    
        theta = math.atan2(vect[i][1], vect[i][0])
        aTheta[i] = theta
    return aTheta


def findPhi(vect):
    hight = len(vect)
    aPhi = [0 for row in range(hight)]
    for i in range(hight):
        phi = math.atan2(np.sqrt(vect[i][0]**2 + vect[i][1]**2), vect[i][2])
        aPhi[i]  = phi
    return aPhi





"""
vector = dirVector(startf, endf)

aTheta = findTheta(vector)
print(aTheta)

aPhi = findPhi(vector)
print(aPhi)



"""







