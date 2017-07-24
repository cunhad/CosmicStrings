# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 20:03:49 2017

@author: felix
"""

#import normalization_array as na
import numpy as np
import matplotlib.pyplot as plt

#Data acquisition
default_dataname = "pos"
dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
if dataname == "":    
    dataname = default_dataname
dataname = "../Data/" + dataname
dataname +=".npz"

print ("Loading '%s'..." %dataname)
xpos = np.load(dataname)['x']
ypos = np.load(dataname)['y']
zpos = np.load(dataname)['z']
print ("Done!")

pos = np.zeros((3,len(xpos)))
pos[0,:] = xpos[:]
pos[1,:] = ypos[:]
pos[2,:] = zpos[:]

def density(pos, cellSize = 2, speed = 1):
    
    xpos = pos[0,:]
    ypos = pos[1,:]
    zpos = pos[2,:]

    #For testing purposes --> reduces the amount of data
    if speed > 1:
        xpos = xpos[0::speed]
        ypos = ypos[0::speed]
        zpos = zpos[0::speed]
    
    print ("Defining limits...")    
    #Brings the positions to start from (0,0,0)
    print np.int(np.max((np.max(xpos),np.max(ypos),np.max(zpos))))
    
    xMin = np.min(xpos)
    yMin = np.min(ypos)
    zMin = np.min(zpos)
    
    xpos -= xMin
    ypos -= yMin
    zpos -= zMin
    
    #Determines the size of the density array
#    xSize = np.int(np.ceil(np.max(xpos)/cellSize))
#    ySize = np.int(np.ceil(np.max(ypos)/cellSize))
#    zSize = np.int(np.ceil(np.max(zpos)/cellSize))
    print np.int(np.max((np.max(xpos),np.max(ypos),np.max(zpos))))
    size = np.int(np.max((np.max(xpos),np.max(ypos),np.max(zpos))))/cellSize+1
    
#    density = np.zeros((xSize,ySize,zSize))
    
    density = np.zeros((size,size,size,))
    
    print ("Done!")
    
    print ("Counting densities...")
    for i in range(len(xpos)):
        #This shows the percentage of data counted
        if i%1000 == 0:
            print "{0:2.0f}%".format(np.float(i)/len(xpos) * 100)
        #This takes the coordinates --> which cell to count it into
        x = np.round(xpos[i])/cellSize
#        if x >= xSize:
#            x = xSize-1
        if x >= size:
            x = size
        y = np.round(ypos[i])/cellSize
#        if y >= ySize:
#            y = ySize-1   
        if y >= size:
            y = size
        z = np.round(zpos[i])/cellSize
#        if z >= zSize:
#            z = zSize-1
        if z >= size:
            z = size        
        #Adds a count to the appropriate cell
        density[x,y,z] += 1
    print ("Done!")       
    
    #Normalization
    print ("Normalizing...")
    density = (density-np.mean(density))/np.mean(density)+1
    #Transposing for plot
    density = np.transpose(density)
    print ("Done!")

    return density, size

density, size  = density(pos, speed = 10)
print size

##Cutoff value
#cutoff = 2
#for i in range(np.shape(density)[0]):
#    for j in range(np.shape(density)[1]):
#        for k in range(np.shape(density)[2]):
#            if density[i,j,k] > cutoff:
#                density[i,j,k] = cutoff

##Plotting the 2D compressions
#for i in range(3):
#    data = np.sum(density, i)
#    
#    heatmap_size = (8,5)
#
#    fig = plt.figure(i, figsize=heatmap_size)
#    
#    ax = fig.add_subplot(111)#2D heatmap of compressed data
#    plt.imshow(data, aspect='auto', interpolation='none', origin='lower', extent=(0,40,0,40))
#    
#    ax.set_aspect('equal')
#    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
#    cax.get_xaxis().set_visible(False)
#    cax.get_yaxis().set_visible(False)
#    cax.patch.set_alpha(0)
#    cax.set_frame_on(False)
#    plt.colorbar(orientation='vertical')