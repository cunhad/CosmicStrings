# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 12:30:21 2017

@author: felix
"""

import matplotlib.pyplot as plt
import numpy as np
import cube 
    
data = np.load("../Data/testCoefficients_pos(2).npz")

cA = data['cA']
cD = data['cD']

print np.max(cA)
arg = np.argmax(np.max(cA, axis=1))
print arg

print cube.startl[arg]
print cube.endl[arg]

plt.figure(0)
plt.plot(np.linspace(0,40,len(cA[arg])),cA[arg])   
for i in range(100):
    plt.plot(np.linspace(0,40,len(cA[arg-i])),cA[arg-i])   
    plt.plot(np.linspace(0,40,len(cA[arg+i])),cA[arg+i])   
    plt.pause(0.0001)

#plt.figure(1)
#for i in range(len(cA)):
#    plt.plot(np.linspace(0,100,len(cA[i])), cA[i])
#    plt.pause(0.001)
#    
