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
import angles as ang
import normalization_array as na
#import density as den


#Data acquisition
default_dataname = "pos(1)"
dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
if dataname == "":
  dataname = default_dataname
dataname +=".npz"
print "Loading %s..." %dataname
#xpos = list(np.load(dataname)['x'])
#ypos = list(np.load(dataname)['y'])
#zpos = list(np.load(dataname)['z'])
xpos = np.load(dataname)['x']
ypos = np.load(dataname)['y']
zpos = np.load(dataname)['z']
pos = []
for i in range(len(xpos)):
    pos.append((xpos[i], ypos[i], zpos[i]))
print "Done!" 




    
def algorithm3(pos):
    
    
    #Find the weight
    size = 120
    weightedCube = na.twins3d(na.octant_assignment(size))
    
    print "Computing 3D FFT..."
    FFTpos = np.fft.fftn(pos)
#    print len(FFTpos)
    FFTposABS = np.hypot(np.real(FFTpos),np.imag(FFTpos))
#    print len(FFTposABS)
    print "Done!"
   
    startl = np.load("startEndPts2D.npz")['startl']
    endl = np.load('startEndPts2D.npz')['endl']
    
    
    #Finding the lines associated with the bresenham lines
#    newStart = ang.startf(start2D)
#    newEnd = ang.endf(end2D)
#    dirVector = ang.dirVector(newStart, newEnd)
#    theta = ang.findTheta(dirVector)
#    phi = ang.findPhi(dirVector)
    
    lines = []
    for i in range(len(startl)):
        lines.append(bnd.bresenhamline(startl[i], endl[i], max_iter=-1) )   
    print lines
    #Apply 1D FFT for each line
    for i in range(size):
        #apply 1D FFT for each line theta[i], phi[i]
#        print("Just for format")
        return
    
    coeffs = []
    
    # Appply 1D Wavelet to find coefficients
    for i in range(size):
        #Apply wavelet
        print("Just for format")
        
    
    
    
    
    return lines
  

arrayOfWaveletCoeffs = algorithm3(pos)





















#r, theta, phi = algorithm3(pos)
