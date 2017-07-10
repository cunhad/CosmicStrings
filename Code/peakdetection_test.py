# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 12:13:11 2017

@author: felix
"""
from scipy import signal
import numpy as np
import pywt 
import matplotlib.pyplot as plt
import os

def clear():
    os.system('cls' if os.name=='nt' else 'clear')

def max_wavelet_level(data):
    max_level = np.int(np.log2(len(data)))
    return max_level

def multilevel_wavelet(data, level, An = [], Dn = []):#, results = []):
    if level <= 0:
        return []
    else:
#        A, D = pywt.dwt(data, 'haar')
#        results.append(An)
#        results.append(Dn)
#        A,D = pywt.dwt(data,'bior3.1')
        A,D = pywt.dwt(data,'haar')
        An.append(A)
        Dn.append(D)
#        An.append(D)
#        Dn.append(A)
#        multilevel_wavelet(An,level-1, results)
        multilevel_wavelet(A,level-1, An,Dn)
#        return results
        return An,Dn
        
def zero_crossing(data,level):
    crossings = []
    for i in range(len(data)-1):
        if data[i] > 0 and data[i+1] < 0 and np.abs(data[i+1]-data[i]) > np.mean(data) + 3*np.std(data):
#            crossings.append(np.mean((i,i+1))*2**level)
            crossings.append((i+1)*2**level)
        if data[i] < 0 and data[i+1] > 0:
            crossings.append((i+1)*2**level)
#            crossings.append(np.mean((i,i+1))*2**level)
    return np.double(crossings)

def find_max_min(data, level):
    max_min = []
    mean = np.mean(data)
    std = np.mean(data)
    
    for i in range(len(data)-1):
        if np.abs(data[i]) > mean + 10*std:
            max_min.append(i*2**(level))
    
    return np.double(max_min)
    
def find_nearest(array,value):
    index = np.abs(array-value).argmin()
    return array[index]
    
def detect_peak(data, level = 0, current_index = 0):
    if level == -1:
        level = np.int(max_wavelet_level(data))-1
    A,D = multilevel_wavelet(data, level)
    zeros = []
    for i in range(len(D)):
        zeros.append(zero_crossing(D[i],i+1))
#        zeros.append(find_max_min(D[i],i+1))
    max_found = zeros[len(zeros)-1]
    for i in range(len(zeros)):
        for j in range(len(max_found)):
            max_found[j] = find_nearest(zeros[len(zeros)-1-i],max_found[j])  
    return max_found, D
    
def plotting(data, D, max_found):  
    plt.figure()
    plt.plot(np.linspace(0,len(data)-1,len(data)),data, '-')
    plt.pause(0.01)
    for i in range(len(D)):
        plt.plot(np.linspace(0,len(data)-1,len(D[i])),D[i], '-')
        plt.pause(0.01)
    for i in range(len(max_found)):
        plt.plot(np.linspace(max_found[i],max_found[i],25), np.linspace(-1,1,25), 'b-')
        plt.pause(0.01)
    plt.plot(np.arange(0,101),np.linspace(0,0,101), 'k--')
    plt.plot(np.linspace(50,50,25), np.linspace(-1.5,1.5,25), 'k--')
    plt.show()
            

data_lenght = 101

ydata = np.random.normal(0,0.01,data_lenght)
#random_index = np.random.random_integers(25,75)
#if ydata[random_index] > 0:
#    ydata[random_index] *= 100
#else :
#    ydata[random_index] *= -100

#ydata = np.load('peak_test_data.npy')

ydata += signal.gaussian(data_lenght, std=5)

xdata = np.arange(0,data_lenght)

#ydata = np.cos(xdata*0.2)

#Aresults, Dresults = multilevel_wavelet(ydata,max_wavelet_level(ydata))

max_found, D = detect_peak(ydata,5)
print max_found

plotting(ydata,D, max_found)

def accuracy_det(data, level = 5, repetitions = 300):
    accurate = 0
    for i in range(repetitions):
        max_found = 0 
        D = 0
        print "Try %d" %i
        max_found, D = detect_peak(data,level)
        for j in max_found:
            if j == 50.:
                accurate += 1
                print "Worked"
    return (accurate/np.float(repetitions))*100.0

result = accuracy_det(ydata)
print result


#plt.figure(0)
#plt.plot(xdata,ydata)
#for i in range(len(max_found)):
#    plt.plot(np.linspace(max_found[i],max_found[i],100),np.linspace(0,np.max(ydata)+1,100),'b-')
#plt.plot(np.linspace(ydata.argmax(),ydata.argmax(),100),np.linspace(0,np.max(ydata)+1,100),'k-')
#plt.show()
#
#
##mlwavelet = pywt.wavedec(ydata, 'bior3.1', 4)
#
#cA1, cD1 = pywt.dwt(ydata, 'bior3.1')
##cA1, cD1 = pywt.dwt(ydata, 'haar')
#x1data = np.linspace(0,data_lenght, np.int(len(cA1)))
#
#plt.figure(1)
#plt.subplot(1,2,1)
#plt.plot(x1data, cA1)
#plt.subplot(1,2,2)
#plt.plot(x1data, cD1)
#plt.tight_layout()
#plt.show()
#
#cA2, cD2 = pywt.dwt(cA1, 'bior3.1')
##cA2 = rescale_data(cA2,ydata)
##cD2 = rescale_data(cD2,ydata)
#x2data = np.linspace(0,data_lenght, np.int(len(cA2)))
#
#plt.figure(2)
#plt.subplot(1,2,1)
#plt.plot(x2data, cA2)
#plt.subplot(1,2,2)
#plt.plot(x2data, cD2)
#plt.tight_layout()
#plt.show()
#
#cA3, cD3 = pywt.dwt(cA2, 'bior3.1')
##cA2 = rescale_data(cA2,ydata)
##cD2 = rescale_data(cD2,ydata)
#x3data = np.linspace(0,data_lenght, np.int(len(cA3)))
#
#plt.figure(3)
#plt.subplot(1,2,1)
#plt.plot(x3data, cA3)
#plt.subplot(1,2,2)
#plt.plot(x3data, cD3)
#plt.tight_layout()
#plt.show()
#
#peakD = (x3data[np.argmin(cA3)] + x3data[np.argmax(cA3)])/2.0
#peakA = x3data[np.argmax(cD3)]
#
#print peakA
#print peakD
