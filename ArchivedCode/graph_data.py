# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:58:36 2017

@author: felix
"""

#print "Importing data..."
import numpy as np
import matplotlib.pyplot as plt

#Default filename -- you can change this if you want!
default_dataname = "pos(1)"
dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
if dataname == "":
  dataname = default_dataname
dataname +=".npz"
print "Loading %s..." %dataname
xpos = list(np.load(dataname)['x'])
ypos = list(np.load(dataname)['y'])
zpos = list(np.load(dataname)['z'])
print "Done!" 

dataset = [xpos,ypos,zpos]
coordinates = ["X","Y","Z"]

for k in range(3):
    cell_size = 2.0
    max_x = np.max(xpos)
    cells = max_x/cell_size
    
    print ("Counting densities for %s%s plane..." %(coordinates[k],coordinates[(k+1)%3]))
    plt.figure(10)
    counts, xedges, yedges, Image = plt.hist2d(xpos, ypos, (cells,cells), cmap=plt.cm.jet)
    counts, xedges, yedges, Image = plt.hist2d(dataset[k], dataset[(k+1)%3], (cells,cells), cmap=plt.cm.jet)
    #plt.colorbar()
    #plt.show()
    plt.close(10)
    print "Done!"
    
    #counts = np.transpose(counts)#This is only so that the graph comes out ok
    
    norm_counts = (counts-np.mean(counts))/np.mean(counts)#Fluctuations

#    for i in range(len(norm_counts)):
#        for j in range(len(norm_counts[i])):
#            if norm_counts[i][j]>2:
#                norm_counts[i][j] = 2
    
    heatmap_size = (8,5)
    
    print "Plotting 2D representation..."
    fig = plt.figure(figsize=heatmap_size)
    
    ax = fig.add_subplot(111)
    ax.set_title('%s%s plane' %(coordinates[k],coordinates[(k+1)%3]))
    plt.imshow(norm_counts, aspect='auto', interpolation='none', origin='lower', extent=(0,40,0,40))
    ax.set_aspect('equal')
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
#    print "DEBUG"
#    plt.show()
    print "Done!"
    
    print "Plotting 1D representation..."
    linearCounts = (np.sum(counts, axis=0)-np.mean(np.sum(counts, axis=0)))/np.mean(np.sum(counts,axis=0))
    plt.figure("%i" %k)
    plt.plot(np.linspace(0,40,np.int(cells)),linearCounts,'k-')
    plt.title('%s-wise compression of %s%s plane' %(coordinates[(k+1)%3],coordinates[k],coordinates[(k+1)%3]))
    plt.xlim(0,40)
    plt.grid(axis='both')
#    plt.show()
    print "Done!"


 
