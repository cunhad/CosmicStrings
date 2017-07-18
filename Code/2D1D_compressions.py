# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:58:36 2017

@author: felix
"""


import numpy as np
import matplotlib.pyplot as plt

print "Loading positions..."
xpos = list(np.load('../Data/pos(1).npz')['x'])
ypos = list(np.load('../Data/pos(1).npz')['y'])
zpos = list(np.load('../Data/pos(1).npz')['z'])
print "Done!" 

dataset = [xpos,ypos,zpos]
coordinates = ["x","y","z"]
default_dataname = "InitialTry"

for k in range(3):
    cell_size = 2.0
    max_x = np.max(xpos)
    cells = max_x/cell_size

    print "Counting densities..."
    plt.figure(10)
    #counts, xedges, yedges, Image = plt.hist2d(xpos, ypos, (cells,cells), cmap=plt.cm.jet)
    counts, xedges, yedges, Image = plt.hist2d(dataset[k], dataset[(k+1)%3], (cells,cells), cmap=plt.cm.jet)
    #plt.colorbar()
    #plt.show()
    plt.close(10)
    print "Done!"

    counts = np.transpose(counts)#This is only so that the graph comes out ok

    norm_counts = (counts-np.mean(counts))/np.mean(counts)#Fluctuations
    #Saves fluctuation files 
    np.save(('../Data/norm_counts%d_%s.npy' %(k,default_dataname)), norm_counts)


    for i in range(len(norm_counts)):#Cutoff value
        for j in range(len(norm_counts[i])):
            if norm_counts[i][j]>2:
                norm_counts[i][j] = 2

    heatmap_size = (8,5)

    fig = plt.figure(figsize=heatmap_size)

    ax = fig.add_subplot(111)#2D heatmap of compressed data
    ax.set_title('%s%s plane' %(coordinates[k],coordinates[(k+1)%3]))
    plt.imshow(norm_counts, aspect='auto', interpolation='none', origin='lower', extent=(0,40,0,40))

    ax.set_aspect('equal')
    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
    cax.get_xaxis().set_visible(False)
    cax.get_yaxis().set_visible(False)
    cax.patch.set_alpha(0)
    cax.set_frame_on(False)
    plt.colorbar(orientation='vertical')
    plt.savefig("../Images/%s%s_plane.png" %(coordinates[k],coordinates[(k+1)%3]))
    plt.show()

    linearCounts = (np.sum(counts, axis=0)-np.mean(np.sum(counts, axis=0)))/np.mean(np.sum(counts,axis=0))
    
    np.save(('../Data/compressed1DlinearCounts_nowake_%d_%s.npy' %(k,default_dataname)), linearCounts)
    
    plt.figure("%i" %k)#1D compression of data
    plt.plot(range(np.int(cells)),linearCounts,'k-')
    plt.title('%s-wise compression of %s%s plane' %(coordinates[(k+1)%3],coordinates[k],coordinates[(k+1)%3]))
    plt.xlim(0,np.int(cells-1))
    plt.grid(axis='both')
    plt.savefig("../Images/%s_compression.png" %(coordinates[(k+1)%3]))
    plt.show()


 
