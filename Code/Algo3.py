# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:25:14 2017

@author: felix
"""

#Test comment :) 

#import graph_data as data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import misc
import bresenhamND as bnd
import angles as ang

s = np.array([[0, 0, 0]])
e = np.array([[5, 5, 5]])
bnd.bresenhamline(s,e,-1)

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
    print "Computing 3D FFT..."
    FFTpos = np.fft.fftn(pos)
#    print len(FFTpos)
    FFTposABS = np.hypot(np.real(FFTpos),np.imag(FFTpos))
#    print len(FFTposABS)
    print "Done!"

    return 

def new_algo3(image):
    FFTpos = np.fft.fftn(image)
    
#r, theta, phi = algorithm3(pos)
#image = misc.imread('YZ_2d_nocutoff.png', flatten=True).astype('float64')
#FFTpos = np.fft.fftn(image)
#FFTposABS = np.hypot(np.real(FFTpos),np.imag(FFTpos))
#
#plt.subplot(1, 2, 1), plt.imshow(image, cmap='gray')
#plt.xticks([]), plt.yticks([])
#plt.subplot(1, 2, 2), plt.imshow(np.real(FFTpos), cmap='gray')
#plt.xticks([]), plt.yticks([])
#plt.show()

counts = np.load('norm_counts1.npy')
FFTcounts = np.fft.fftn(counts)
FFTcounts
FFTcountsReal = np.real(FFTcounts)
#FFTcountsABS = np.abs(np.real(FFTcounts),np.complex(FFTcounts))
FFTcountsABS = np.abs(FFTcounts)

counts = np.abs(np.fft.ifftn(np.fft.fftn(counts)))

plt.figure(1)
plt.imshow(counts, cmap='gray')
plt.show()
plt.figure(2)
plt.imshow(FFTcountsReal, cmap='gray')
plt.figure(4)
plt.imshow(np.imag(FFTcounts), cmap='gray')
plt.figure(3)
plt.imshow(FFTcountsABS, cmap='gray')
plt.colorbar()
plt.show()


newStart = ang.startf(start)
newEnd = ang.endf(end)
dirVector = ang.dirVector(newStart, newEnd)
theta = ang.findTheta(dirVector)
phi = ang.findPhi(dirVector)

