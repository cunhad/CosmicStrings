# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 20:03:49 2017

@author: felix
"""

#import normalization_array as na
import numpy as np
import matplotlib.pyplot as plt

##Data acquisition
#default_dataname = "pos(1)"
#dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
#if dataname == "":    
#    dataname = default_dataname
#dataname = "../Data/" + dataname
#dataname +=".npz"
#
#print ("Loading '%s'..." %dataname)
#xpos = np.load(dataname)['x']
#ypos = np.load(dataname)['y']
#zpos = np.load(dataname)['z']
#print ("Done!")
#
#pos = np.zeros((3,len(xpos)))
#pos[0,:] = xpos[:]
#pos[1,:] = ypos[:]
#pos[2,:] = zpos[:]

def buffer_adjust(pos, nbCells):
    for i in range(len(pos)):
        if pos[i] >= nbCells:
            pos[i] %= nbCells
        elif pos[i] < 0:
            pos[i] = nbCells + pos[i]
    return pos

#nbCells is determined before the simulation
def density(pos, cellSize = 2.0, s = 1, nbCells = 192):
    
    xpos = buffer_adjust(pos[0,:], nbCells)
    ypos = buffer_adjust(pos[1,:], nbCells)
    zpos = buffer_adjust(pos[2,:], nbCells)

    #For testing purposes --> reduces the amount of data
    if s > 1:
        xpos = xpos[0::s]
        ypos = ypos[0::s]
        zpos = zpos[0::s]
    
    print ("Defining limits...")    
    size = np.int(np.ceil(nbCells/cellSize))    
    density = np.zeros((size,size,size,))
    
    
    print ("Counting densities...")
    for i in range(len(xpos)):
        #This shows the percentage of data counted
#        if i%1000 == 0:
#            print "{0:2.0f}%".format(np.float(i)/len(xpos) * 100)
        #This takes the coordinates --> which cell to count it into
        x = np.floor(xpos[i]/cellSize)
        x = np.int(x)
        
        y = np.floor(ypos[i]/cellSize)
        y = np.int(y)
        
        z = np.floor(zpos[i]/cellSize)
        z = np.int(z)
        #Adds a count to the appropriate cell
        density[x,y,z] += 1
     
    #Transposing for plot
    density = np.transpose(density)
    
    return density, size

#density, size  = density(pos, speed = 10)
##print size