# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:25:14 2017

@author: felix
"""


#import matplotlib.pyplot as plt
#import peakdetection as pd
import numpy as np
#import pywt
import density3D as dens
import cube
import BrutForceNorm as bnorm
import lineInterpolation as line

#Data acquisition
#default_dataname = "pos1"
#dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
#if dataname == "":
#  dataname = default_dataname
#dataname = "../Data/" + dataname
#dataname="../Data/pos1.npz"
#
#print "Loading %s..." %dataname
#xpos = np.load(dataname)['x']
#ypos = np.load(dataname)['y']
#zpos = np.load(dataname)['z']



#Rearranges into one 2D array
#pos = np.zeros((3,len(xpos)))
#pos[0,:] = xpos[:]
#pos[1,:] = ypos[:]
#pos[2,:] = zpos[:]

def preCutLines_Arrays(lines, x, y, z, start, end):
    std = np.std(lines)#, axis=0)
    std_away = 30 
    dev = std_away*std

    cutLines = []
    cutX = []
    cutY = []
    cutZ = []
    cutStart = []
    cutEnd = []
    for i in range(len(lines)):
        line = lines[i]
        for j in range(len(line)):
            value = line[j]
            if value >= dev:
                cutLines.append(line)
                cutX.append(x[i])
                cutY.append(y[i])
                cutZ.append(z[i])
                cutStart.append(start[i])
                cutEnd.append(end[i])

    return cutLines, cutX, cutY, cutZ, cutStart, cutEnd

#This algo does not return ridglet coefficients, but rather the 
#lines that have been created before the wavelet transform should 
#occur
def algorithm3(pos):
    #print np.shape(pos)
    #density, size = dens.density(pos, s = 1)
    #np.savez("density.npz", density=density, size=size)
    density = np.load("density.npz")['density']
    size = np.load("density.npz")['size']
    print "Computing 3D FFT..."
    FFTdensity = np.fft.fftn(density)
    
    startl, endl = cube.lineParse(size)

    print "Creating lines..."
    #lines, xArray, yArray, zArray = line.lineCreation(startl,endl)
    #np.savez("../Data/lines_xArray_yArray_zArray.npz", lines=lines, x=xArray, y=yArray, z=zArray)
    data = np.load("../Data/lines_xArray_yArray_zArray.npz")
    lines = data['lines']
    xArray = data['x']
    yArray = data['y']
    zArray = data['z']

    print "Selecting FFT lines..."
#    fftLines = []
#    for i in range(len(lines)):
#        for j in range(len(lines[0][0])):
#            fftLines.append(FFTdensity[lines[i][0][j],lines[i][1][j],lines[i][2][j]])
#    print np.shape(lines)           
#    fftLines = np.reshape(fftLines, (np.shape(lines)[0], np.shape(lines)[2]))
#    
#    #Apply inverse 1D FFT for each line
#    ifftLines = np.hypot(np.real(np.fft.ifft(fftLines)), np.imag(np.fft.ifft(fftLines)))
#    
#    #Density contrast    
#    print "Density contrast..."
#    for i in range(len(ifftLines)):
#        ifftLines[i] = (ifftLines[i]-np.mean(ifftLines[i]))/np.mean(ifftLines[i])
    ifftLines = np.load("../Data/ifftLines.npy")

    print "Chopping lines..."
    ifftLines, xArray, yArray, zArray, startl, endl = preCutLines_Arrays(ifftLines, xArray, yArray, zArray, startl, endl)

    #print "Normalization of dataset..."
    #normFactors, lengths = bnorm.finalNormalization(xArray, yArray, zArray, size, startl, endl)   
    #print (np.shape(normFactors))
    #ifftLinesN = normFactors
    #for i in range(len(ifftLines)):
    #    for j in range(len(ifftLines[0])):
    ##for i in range(10):
    #    #for j in range(10):
    #        ifftLinesN[i][j] = ifftLines[i][j]/normFactors[i][j]

    return ifftLines#N


#ifftLines = algorithm3(pos)
