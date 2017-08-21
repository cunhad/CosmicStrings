# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:25:14 2017

@author: felix
"""


#import graph_data as data
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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
#dataname = raw_input("filename w/o '.npz' (default is '%s')?: " %(default_dataname))
#if dataname == "":
#  dataname = default_dataname
#dataname = "../Data/" + dataname
#dataname +=".npz"
dataname = "pos(1).npz"

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

    density, size = dens.density(pos, speed = 1)

    dim = np.shape(pos)[0]
    #Find the weight
#    size = 120
    print ("Computing weighted cube...")
    weightedCube = na.twins3d(na.octant_assignment(size))
    print "Done!"

    print "Computing 3D FFT..."
    FFTpos = np.fft.fftn(density)
#    print len(FFTpos)
#    FFTposABS = np.hypot(np.real(FFTpos),np.imag(FFTpos))
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
            fftLines.append(FFTpos[lines[i][j][0],lines[i][j][1],lines[i][j][2]])
#            fftLines.append(FFTposABS[lines[i][j][0],lines[i][j][1],lines[i][j][2]])
#            fftLines.append(FFTposABS[lines[i][j]])

#    print lines[i][j]

#    return fftLines
    print "Done!"


    fftLines = np.reshape(fftLines, (len(lines), size))

    ifftLines = np.hypot(np.real(np.fft.ifft(fftLines)), np.imag(np.fft.ifft(fftLines)))

    print "Normalization of dataset..."
    pointNormalization = []
    lineNormalization = 0
    totalNormalization = []
    for i in range(len(ifftLines)):
        ifftLines[i] = (ifftLines[i]-np.mean(ifftLines[i]))/np.mean(ifftLines[i])
        pointNormalization = norm.pointNorm(weightedCube, lines[i], dim)
        lineNormalization = norm.lineNorm(pointNormalization)
        totalNormalization.append(norm.normalizeLine(pointNormalization, ifftLines[i], lineNormalization))
    #density, size  = density(pos, speed = 10)
    print "Done!"
##print size
#
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

    cA = []
    cD = []

    print "Wavelet Transform..."
    # Appply 1D Wavelet to find coefficients
    for i in range(len(ifftLines)):
#        cA.append(pywt.dwt(ifftLines[i], 'haar')[0])
#        cD.append(pywt.dwt(ifftLines[i], 'haar')[1])
        cA.append(pywt.dwt(totalNormalization[i], 'haar')[0])
        cD.append(pywt.dwt(totalNormalization[i], 'haar')[1])
    print "Done!"


    return cA, cD
#
#
#lines, FFTposABS, fftLines, totalNormalization, coeffs,ifftLines = algorithm3(pos)
##print(totalNormalization)
#print np.shape(coeffs)

cA, cD = algorithm3(pos)

np.savez("../testCoefficients_pos(1).npz", cA=cA, cD=cD)

#for i in range(len(cA)):
#    cA[i] = cA[i][10:40]

#cA = cA[0::50]

#max_cA = np.max(cA)
#print max_cA
#
#plt.figure()
for i in range(len(cA)):
    plt.plot(np.linspace(0,120,len(cA[i])), cA[i])
#    plt.pause(0.0005)
plt.savefig("pos1_fig.png")
