#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 11:55:52 2017

@author: donnashimizu
"""
import numpy as np 


def line2D(side):
    """2D endpoint creation for square of side length side"""
    startCell = []
    endCell = [] 
    for i in range(side):
            startCell.append([i,0])
            endCell.append([side - i,side])
    for j in range(side):
            startCell.append([0,j])
            endCell.append([side,side - j]) 
    return startCell , endCell
    
    
def lineParse(cubeLen):
    """3D endpoint creation for cube of length cubeLen"""
    startArr = []
    endArr = []
    for i in range(cubeLen):
        for j in range(cubeLen):
                start = [i,j,0]
                end = [cubeLen-i-1, cubeLen-j-1, cubeLen-1]
                startArr.append(start)
                endArr.append(end)
    for i in range(cubeLen):
        for j in range(cubeLen):
                start = [i,0,j]
                end = [cubeLen-i-1, cubeLen-1, cubeLen-j-1]
                startArr.append(start)
                endArr.append(end)
    for i in range(cubeLen):
        for j in range(cubeLen):
                start = [0,i,j]
                end = [cubeLen-1, cubeLen-i-1, cubeLen-j-1]
                startArr.append(start)
                endArr.append(end)
    return startArr, endArr

def to2DFloat(start, end):
    """To convert to float 2D array instead of 3D int"""
    startf = []
    endf = []
    for i in range(len(start)):
            temps = []
            temps.append(float(start[i][0,0]))
            temps.append(float(start[i][0,1]))
            temps.append(float(start[i][0,2]))
            startf.append(temps)
            tempe = []
            tempe.append(float(end[i][0,0]))
            tempe.append(float(end[i][0,1]))
            tempe.append(float(end[i][0,2]))
            endf.append(tempe)
    return startf, endf
    
"""start and end points for each line in the 120x120x120 cube"""
#startArr, endArr = lineParse(120)
#np.savez("startEndPts.npz",startArr=startArr, endArr=endArr )

#start = list(np.load("startEndPts.npz")['startArr'])
#end = list(np.load('startEndPts.npz')['endArr'])

startl , endl = lineParse(192)
#np.savez("startEndPts2D.npz",startl=startl, endl=endl )
#start2D = list(np.load("startEndPts2D.npz")['startl'])
#end2D = list(np.load('startEndPts2D.npz')['endl'])

        
        
        
