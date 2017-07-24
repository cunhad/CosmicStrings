# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:25:14 2017

@author: felix
"""


#import graph_data as data
import numpy as np
#import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
import bresenhamND as bnd
#import angles as ang
import normalization_array as na
#import Normalization_Test as normal
#import peakdetection as pd
#import density as den
import pywt
import Normalization2DNew as norm
import density3D as dens
import cube

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

#
##For looping purposes
#coordinates = ["X","Y","Z"]
#
#for k in range(3):
#  cell_size = 2.0
#  max_x = np.max(xpos)
#  cells = max_x/cell_size
#
#  print "Counting densities..."
#  #This only works for 2D 
#  plt.figure(1)
#  counts, xedges, yedges, Image = plt.hist2d(pos[k], pos[(k+1)%3], (cells,cells), cmap=plt.cm.jet)
#  plt.close(1)
#  print "Done!"
#
#  counts = np.transpose(counts)#This is only so that the graph comes out ok
#
#  norm_counts = (counts-np.mean(counts))/np.mean(counts)#Fluctuations
#  #Saves fluctuation files 
#  np.save(('../Data/norm_counts%d_%s.npy' %(k,default_dataname)), norm_counts)

def algorithm3(pos):
    
    density, size = dens.density(pos, speed = 20)
        
    dim = np.shape(pos)[0]
    #Find the weight
#    size = 120
    print ("Computing weighted cube...")
    weightedCube = na.twins3d(na.octant_assignment(size))
    print "Done!"
    
    print "Computing 3D FFT..."
    FFTpos = np.fft.fftn(density)
#    print len(FFTpos)
    FFTposABS = np.hypot(np.real(FFTpos),np.imag(FFTpos))
#    print np.shape(FFTposABS)
#    print len(FFTposABS)
    print "Done!"
    
    startl, endl = cube.lineParse(size)
   
#    startl = np.load('../Data/startEndPts.npz')['startArr']
#    endl = np.load('../Data/startEndPts.npz')['endArr']
        
    #Still good: DO NOT ERASE
    #Finding the lines associated with the bresenham lines
#    newStart = ang.startf(start2D)
#    newEnd = ang.endf(end2D)
#    dirVector = ang.dirVector(newStart, newEnd)
#    theta = ang.findTheta(dirVector)
#    phi = ang.findPhi(dirVector)
    print "Selecting lines..."
    lines = []
    for i in range(len(startl)):
        lines.append(bnd.bresenhamline(startl[i], endl[i], max_iter=-1) )   
    print "Done!" 
#    lines -= 1
#    return FFTposABS, lines
#    
#    
#    
#    
    #Apply inverse 1D FFT for each line
#    fftLines = np.zeros((len(startl),3))
    fftLines = []
#    print np.shape(FFTposABS)
    for i in range(len(lines)):
        for j in range(len(lines[i])):
#            x = []           
#            for k in range(len(lines[i][j])):
###                fftLines.append(FFTposABS[k,line[k]])
#                x.append(lines[i][j][k])
            fftLines.append(FFTposABS[lines[i][j][0],lines[i][j][1],lines[i][j][2]])
#            fftLines.append(FFTposABS[lines[i][j]])
            
#    print lines[i][j]
    
#    return fftLines

    fftLines = np.reshape(fftLines, (len(lines), size))
    
    ifftLines = np.hypot(np.real(np.fft.ifft(fftLines)), np.imag(np.fft.ifft(fftLines)))

    #Need normalization later
    pointNormalization = norm.pointNorm(weightedCube, lines, dim)
    lineNormalization = norm.lineNorm(pointNormalization)
    print np.shape(pointNormalization)
    print np.shape(ifftLines)
    print np.shape(lineNormalization)
    totalNormalization = norm.normalizeLine(pointNormalization, ifftLines, lineNormalization)
    
    
#        return
    
    coeffs = []    
    
    # Appply 1D Wavelet to find coefficients
    for i in range(len(ifftLines)):
        coeffs.append(pywt.dwt(ifftLines[i], 'haar'))
                
    
    
    
    
    return lines, FFTposABS, fftLines, totalNormalization, coeffs,ifftLines
#  
#
#lines, FFTposABS, fftLines, totalNormalization, coeffs,ifftLines = algorithm3(pos)
##print(totalNormalization)
#print np.shape(coeffs)
    
fftLines = algorithm3(pos)






















#r, theta, phi = algorithm3(pos)