# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:25:14 2017

@author: felix
"""


#import graph_data as data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import bresenhamND as bnd
#import angles as ang
import normalization_array as na
#import Normalization_Test as normal
import peakdetection as pd
#import density as den
import pywt
import Normalization2DNew as norm

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

#For looping purposes
coordinates = ["X","Y","Z"]

for k in range(3):
  cell_size = 2.0
  max_x = np.max(xpos)
  cells = max_x/cell_size

  print "Counting densities..."
  #This only works for 2D 
  plt.figure(1)
  counts, xedges, yedges, Image = plt.hist2d(pos[k], pos[(k+1)%3], (cells,cells), cmap=plt.cm.jet)
  plt.close(1)
  print "Done!"

  counts = np.transpose(counts)#This is only so that the graph comes out ok

  norm_counts = (counts-np.mean(counts))/np.mean(counts)#Fluctuations
  #Saves fluctuation files 
  np.save(('../Data/norm_counts%d_%s.npy' %(k,default_dataname)), norm_counts)

def algorithm3(pos):
        
    dim = 3
    #Find the weight
    size = 120
    weightedCube = na.twins3d(na.octant_assignment(size))
    
    print "Computing 3D FFT..."
    FFTpos = np.fft.fftn(pos)
#    print len(FFTpos)
    FFTposABS = np.hypot(np.real(FFTpos),np.imag(FFTpos))
#    print len(FFTposABS)
    print "Done!"
   
    startl = np.load('../Data/startEndPts.npz')['startArr']
    endl = np.load('../Data/startEndPts.npz')['endArr']
    
    #Still good: DO NOT ERASE
    #Finding the lines associated with the bresenham lines
#    newStart = ang.startf(start2D)
#    newEnd = ang.endf(end2D)
#    dirVector = ang.dirVector(newStart, newEnd)
#    theta = ang.findTheta(dirVector)
#    phi = ang.findPhi(dirVector)
    
    lines = []
    for i in range(len(startl)):
        lines.append(bnd.bresenhamline(startl[i], endl[i], max_iter=-1) )   
    
    
    
    
    #Apply inverse 1D FFT for each line
#    fftLines = np.zeros((len(startl),3))
    fftLines = []
#    print np.shape(FFTposABS)
    for i in range(len(startl)):
        for j in range(len(lines[i])):
            line = lines[i][j]
            for k in range(len(line)):
#                fftLines.append(FFTposABS[k,line[k]])
                fftLines.append(FFTpos[k,line[j][k]])
#            fftLines.append(FFTposABS[lines[i][j]])

    

#    fftLines_seperated = fftLines[0::len(lines[i])]
    fftLines = np.reshape(fftLines, (43200, 120, 3))
    
    ifftLines = np.hypot(np.real(np.fft.ifft(fftLines)), np.imag(np.fft.ifft(fftLines)))

    #Need normalization later
    pointNormalization = norm.pointNorm(weightedCube, lines, dim)
    lineNormalization = norm.lineNorm(pointNormalization)
    totalNormalization = norm.normalizeLine(pointNormalization, ifftLines, lineNormalization)
    
    
#        return
    
    coeffs = []    
    
    # Appply 1D Wavelet to find coefficients
    for i in range(len(ifftLines)):
        coeffs.append(pywt.dwt(ifftLines[i], 'haar'))
                
    
    
    
    
<<<<<<< HEAD
    return lines, FFTposABS, fftLines, totalNormalization, coeffs,ifftLines
  

lines, FFTposABS, fftLines, totalNormalization, coeffs,ifftLines = algorithm3(pos)
#print(totalNormalization)
print np.shape(coeffs)
=======
    return lines, FFTposABS, fftLines, totalNormalization
  

lines, FFTposABS, fftLines, totalNormalization = algorithm3(pos)
print(totalNormalization)





















#r, theta, phi = algorithm3(pos)
>>>>>>> b3f78f03cb0d3380020a09445234f1b644be0a5d
