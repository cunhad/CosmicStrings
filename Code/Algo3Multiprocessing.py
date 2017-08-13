# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:25:14 2017

@author: felix
"""


#import matplotlib.pyplot as plt
#import peakdetection as pd
from contextlib import closing
from multiprocessing import Pool
#from multiprocessing import Process
import numpy as np
import pywt
import density3D as dens
import cube
import BrutForceNorm as bnorm
import lineInterpolation as line
import time

#Data acquisition
#default_dataname = "pos(1)"
#dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
#if dataname == "":
#  dataname = default_dataname
#dataname = "../Data/" + dataname
dataname ="../Data/pos(1).npz"

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

def lineCreate(args):
    nbSteps, start, x, my, mz, lineNumber = args
#    print start
#    print end
#    print "Y and Z arrays..."
    return line.multiprocessLine(nbSteps, start, x, my, mz, lineNumber)

def algorithm3(pos, speed = 1):

    density, size = dens.density(pos, s = speed)

    print "Computing 3D FFT..."
    FFTdensity = np.fft.fftn(density)
    print "Done!"

    print "Selecting lines..."   
    tic1 = time.time()    
    if __name__ == '__main__':
        startl, endl = cube.lineParse(size)
        
        nbSteps, x, my, mz = line.initLineCreation_mp(startl, endl)
        
        nbSteps_mp = np.linspace(nbSteps, nbSteps, len(startl), dtype = np.int)
#        print len(x)
#        print len(my)
#        print len(mz)
#        print len(np.linspace(nbSteps, nbSteps, len(startl)))
        
        args = zip(nbSteps_mp, startl, x, my, mz, range(len(startl)))
        
    #    lines = line.lineCreation(startl,endl)
    #    start_end = []
    #    for i in range(len(startl)):
    #        start_end.append([startl[i],endl[i]])    
        print "Y and Z arrays..."
        with closing(Pool(processes = 4)) as p:
            lines = p.map(lineCreate, args)
            p.terminate()        
            
    tic2 = time.time()

    toc1 = time.time()    
    lines = line.lineCreation(startl,endl)
    toc2 = time.time()
    
    if toc2-toc1 < tic2-tic1:
        print "MP wins!"
        print toc2-toc1
        print tic2-tic1
    else:
        print "Normal wins!"
        print toc2-toc1
        print tic2-tic1        
#        p = Pool()
#        print p.map(lineCreate, args, chunksize=50)
#    lines = p.map(lineCreate, args)
    
#    print np.shape(lines)
    
#    if __name__ == '__main__':
#        start = startl
#        end = endl
#        
#        start_end = []
#        
#        for i in range(len(start)):
#            start_end.append([start[i],end[i]])
#        print np.shape(start_end)
##        p = Process(target=lineCreate, args=(start_end,))
##        p.start()
##        p.join()
#        with closing(Pool(processes = 4)) as p:
#            print p.map(lineCreate, start_end, chunksize = 2)
#            p.terminate()
##            lines = p.map(lineCreate, start_end)
##        pool = Pool()
##        lines = pool.map(lineCreate, start_end)

    print "FFTLines..."
    fftLines = []
    for i in range(len(lines)):
        for j in range(len(lines[0][0])):
            fftLines.append(FFTdensity[lines[i][0][j],lines[i][1][j],lines[i][2][j]])

    print "Done!"

    #Apply inverse 1D FFT for each line
    ifftLines = np.hypot(np.real(np.fft.ifft(fftLines)), np.imag(np.fft.ifft(fftLines)))
    
    #Density contrast    
    for i in range(len(ifftLines)):
        ifftLines[i] = (ifftLines[i]-np.mean(ifftLines[i]))/np.mean(ifftLines[i])

#    print "Normalization of dataset..."
#    #Need normalization later
#    start, end = bnorm.formatting(startl, endl)
#    cCube, cStart, cEnd = bnorm.center(start, end, size)
#    normFactors = []
#    lengths = []
#    count = 0
#    for i in range(len(cStart)):
#        factor, length = bnorm.normalize(cStart[i], cEnd[i], cCube, 96, i)
#        normFactors.append(factor)
#        lengths.append(length)
#        count += 1
#        print ("Line %s" %count)
#    
#    
#    normalizedLines = []
#    for i in range(len(ifftLines)):
#        normalizedLine = ifftLines[i]/normFactors[i]
#        normalizedLines.append(normalizedLine)
#    
#    print "Done!"
        
    cA = []
    cD = []

    print "Wavelet Transform..."
    # Appply 1D Wavelet to find coefficients
    for i in range(len(ifftLines)):
        cA.append(pywt.dwt(ifftLines[i], 'haar')[0])
        cD.append(pywt.dwt(ifftLines[i], 'haar')[1])
#        cA.append(pywt.dwt(normalizedLines[i], 'haar')[0])
#        cD.append(pywt.dwt(normalizedLines[i], 'haar')[1])
    print "Done!"


    return cA, cD
    
cA, cD = algorithm3(pos, speed = 100)
#
#for i in range(len(cA)):
#    cA[i] = cA[i][10:40]
#
#cA = cA[25::50]
#
#max_cA = np.max(cA)
#print max_cA
#
#plt.figure()
#for i in range(len(cA)):
#    plt.plot(np.linspace(0,96,len(cA[i])), cA[i])
#    plt.pause(0.0005)


############old bits of code#############
"""
pointNormalization = []
lineNormalization = 0
totalNormalization = []
for i in range(len(ifftLines)):
    ifftLines[i] = (ifftLines[i]-np.mean(ifftLines[i]))/np.mean(ifftLines[i])
    pointNormalization = norm.pointNorm(weightedCube, lines[i], dim)
    lineNormalization = norm.lineNorm(pointNormalization)
    totalNormalization.append(norm.normalizeLine(pointNormalization, ifftLines[i], lineNormalization))
"""
    
##Cutoff value
#cutoff = 2
#for i in range(np.shape(density)[0]):
#    for j in range(np.shape(density)[1]):
#        for k in range(np.shape(density)[2]):
#            if density[i,j,k] > cutoff:
#                density[i,j,k] = cutoff
#
##Plotting the 2D compressions
#for i in range(3):
#    data = np.sum(density, i)
#
#    heatmap_size = (8,5)
#
#    fig = plt.figure(i, figsize=heatmap_size)
#
#    ax = fig.add_subplot(111)#2D heatmap of compressed data
#    plt.imshow(data, aspect='auto', interpolation='none', origin='lower')#, extent=(0,40,0,40))
#
#    ax.set_aspect('equal')
#    cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
#    cax.get_xaxis().set_visible(False)
#    cax.get_yaxis().set_visible(False)
#    cax.patch.set_alpha(0)
#    cax.set_frame_on(False)
#    plt.colorbar(orientation='vertical')
#        return
