# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 12:13:11 2017

@author: felix
"""
from scipy import signal
import numpy as np
import pywt 
import matplotlib.pyplot as plt

#Computes the maximum amount of levels 
def max_wavelet_level(data):
    max_level = np.int(np.log2(len(data)))
    return max_level

#Recurcive wavelet transform depending on the level
def multilevel_wavelet(data, level, An = [], Dn = []):
    if level <= 0:
        return []
    else:
        A,D = pywt.dwt(data,'haar')
#        A,D = pywt.dwt(data,'bior3.1')
        An.append(A)
        Dn.append(D)
        #Recursive call on A 
        multilevel_wavelet(A,level-1, An,Dn)
        return An,Dn

#Checks for zero crossing on selected data and creates
#an array with all appropriate indices (i+1).
def zero_crossing(data,level):
    crossings = []
    std_away = 0
    for i in range(len(data)-1):
        #This checks for 3 sigmas significance
#        if np.abs(data[i+1]-data[i]) >= np.mean(data) + std_away*np.std(data):
            #There are 2 cases for zero crossing
            #Still testing this!!!
            if data[i] > 0 and data[i+1] < 0: 
                crossings.append((2*i+1)*2**(level-1))
#                crossings.append((i+1)*2**level)
            if data[i] < 0 and data[i+1] > 0:
                crossings.append((2*i+1)*2**(level-1))             
#                crossings.append((i+1)*2**level)
    return np.double(crossings)
    
#Returns the nearest value of an array
#that is compared to an original value
def find_nearest(array,value, ret = "value"):
    if len(array) == 0:
        print "Warning: No maxima found!"
        return
    index = np.abs(array-value).argmin()
    if ret == "value":
        return array[index]
    elif ret == "index":
        return index
    
#Main function
#Creates a multilevel wavelet transform on selected data
#and analyses the results to find the maxima of the 
#distribution.
###Only applied to 1D distribution
def detect_peak(data, level = -1, current_index = 0):
    #By default, this goes to maximal level - 1.
    if level == -1:
        level = np.int(max_wavelet_level(data))-2
    A,D = multilevel_wavelet(data, level)
    zeros = []
    #Finds all zeros
    for i in range(len(D)):
        zeros.append(zero_crossing(D[i],i+1))
    #Last zero crossings correspond to local maxima
    max_found = zeros[len(zeros)-1]
    for i in range(len(zeros)):
        for j in range(len(max_found)):
            #Find nearest value to backtrack levels
#            print "Before: %d" %max_found[j]
            max_found[j] = find_nearest(zeros[len(zeros)-1-i],max_found[j]) 
#            print "After: %d" %max_found[j]
    max_found = np.unique(max_found)
    l = len(max_found)-1
#    print max_found
    for i in range(len(max_found)):
        if l-i < 0:
            break        
#        print l
        if np.abs(data[max_found[l-i]])<np.mean(data)+1*np.std(data):
            max_found = np.delete(max_found, l-i)
#            print "Deleted %d" %(l-i)
    return max_found, D

#Very simple function to plot the results of the Multi-Level wavelet
#analysis.
def plotting(data, D, max_found):  
    plt.figure()
    plt.plot(np.linspace(0,len(data)-1,len(data)),data, '-', label = "Original")
    plt.pause(0.01)
    for i in range(len(D)):
        plt.plot(np.linspace(0,len(data)-1,len(D[i])),D[i], '-', label=("Level %d" %(i+1)))
        plt.pause(0.01)
    for i in range(len(max_found)):
        plt.plot(np.linspace(max_found[i],max_found[i],25), np.linspace(data.min(),data.max(),25), 'b-', linewidth=2, label="Max found")
        plt.pause(0.01)
    plt.plot(np.linspace(data.argmax(),data.argmax(),25), np.linspace(data.min(),data.max(),25), 'k--', label = "Max")
    plt.legend(loc=1, fontsize=10)
    plt.xlim(0,len(data)-1)
    plt.savefig("../Images/peakTest.png")
    plt.show()
    
#Runs a 100 times the main algorithm to determine its accuracy
def accuracy_det(data, level = -1, repetitions = 100):
    accurate = 0
    for i in range(repetitions):
        max_found = 0 
        D = 0
        print "Try %d" %i
        max_found, D = detect_peak(data,level)
#        print max_found
        for j in max_found:
            if j == 50.0:
                accurate += 1
                print "Worked"
    return (accurate/np.float(repetitions))*100.0

#Determine the Full Width Half Maximum of the data
#according the found maxima. 
def width_det(data, max_found):
    fwhm = []
    for i in max_found:
        fwhm.append(find_nearest(data[:i], data[i]/2., ret='index'))
        fwhm.append(find_nearest(data[i:], data[i]/2., ret='index')+i)
#    print fwhm
    widths = []
    for i in range(len(fwhm)/2):
        widths.append(fwhm[2*i+1]-fwhm[2*i])
    return widths

            
##Data generation
#data_lenght = 80
#ydata = np.random.normal(0,0.04,data_lenght)
#ydata += signal.gaussian(data_lenght, std=5)
#xdata = np.arange(0,data_lenght)
            
ydata = np.load("../Data/compressed1DlinearCounts2_InitialTry.npy")

#Testing
max_found, D = detect_peak(ydata,4)
plotting(ydata,D, max_found)
widths = width_det(ydata, max_found)
#print widths
#
#result = accuracy_det(ydata)
#print result
#
