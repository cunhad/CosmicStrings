"""
@author: eloisechakour

Input Recieved: 
    An array of points that the line goes through
    
    TO NORMALIZE A LINE
    1.normalizeLine(lineNorm(pointNorm(data, pointsInLines)), values, pointNorm(data, pointsInLines))
"""

import normalization_array as na


def pointNorm(data, array):
    pointNorm = 0
    normArray = []
    x = 0
    y = 0
    z = 0

    if dim == 3:
        for i in range(len(array)):
            x = array[i][0]
            y = array[i][1]
            z = array[i][2]
            
            pointNorm = data[x, y, z]
            normArray.append(pointNorm)
    elif dim == 2:
        for i in range(len(array)):
            x = array[i][0]
            y = array[i][1]
            
            pointNorm = data[x, y]
            normArray.append(pointNorm)
    
    return normArray


def lineNorm(normArray):
    lineFactor = 0
    
    
    for i in range(len(normArray)):
        lineFactor += 1/normArray[i]
    
    
    
    return lineFactor



def normalizeLine(normArray, valuesArray, lineFactor):
    normalizaedLine = []
    value = 0
    norm = 0
    normedValue = 0
    
    for i in range(len(normArray)):
        value = valuesArray[i]
        norm = normArray[i]
        normedValue = (value/norm)/lineFactor
        normalizaedLine.append(normedValue)
    
    
    return normalizaedLine
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    






