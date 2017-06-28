# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 19:25:14 2017

@author: felix
"""

#import graph_data as data
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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

def cart2sph(x, y, z):
#    x=xpos#[:10000]
#    y=ypos#[:10000]
#    z=zpos#[:10000]
    
    radius = np.max((np.max(x),np.max(y),np.max(z)))/2.0
    x -= radius
    y -= radius
    z -= radius
    
    x /= radius
    y /= radius
    z /= radius
    
#    print len(x)
    
    dx = x*np.sqrt(1-y**2/2.0-z**2/2.0+(y**2*z**2)/3.0)
    dy = y*np.sqrt(1-z**2/2.0-x**2/2.0+(z**2*x**2)/3.0)
    dz = z*np.sqrt(1-x**2/2.0-y**2/2.0+(y**2*x**2)/3.0)
    
    dx*=radius
    dy*=radius
    dz*=radius
    
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #for i in range(len(dx)):
    #    ax.scatter(dx[i],dy[i],dz[i], marker='o')
    #    plt.pause(0.00001)    
    #    plt.show()
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(dx,dy,dz, marker='o')
    #plt.show()
    
    #fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    #ax.scatter(x,y,z, marker='o')
    #plt.show()
    hxy = []
    r = []
    phi = []
    theta = []
#    print len(dx)
    for i in range(len(dx)):
        hxy.append(np.hypot(dx[i], dy[i]))
        r.append(np.hypot(hxy[i], dz[i]))
        theta.append(np.arctan2(dy[i], dx[i])+np.pi)
        phi.append(np.arctan2(hxy[i], dz[i]))
    return r, theta, phi
    
def algorithm3(pos):
    print "Computing 3D FFT..."
    FFTpos = np.fft.fftn(pos)
#    print len(FFTpos)
    FFTposABS = np.hypot(np.real(FFTpos),np.imag(FFTpos))
#    print len(FFTposABS)
    print "Done!"
    
    print "Converting coordinates..."
#    print np.shape(FFTposABS[:,0])
    sphFFTpos = cart2sph(FFTposABS[:,0],FFTposABS[:,1],FFTposABS[:,2])

    print "Done!"
    
    return sphFFTpos
    
r, theta, phi = algorithm3(pos)

##R = np.cos(phi**2)
#X = [] 
#Y = []
#Z = []
#
#for i in range(len(r)):
#    X.append(r[i] * np.sin(phi[i]) * np.cos(theta[i]))
#    Y.append(r[i] * np.sin(phi[i]) * np.sin(theta[i]))
#    Z.append(r[i] * np.cos(phi[i]))
#
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#for i in range(len(X)):
#    ax.scatter(X[i],Y[i],Z[i], marker='o')
#    plt.pause(0.000000001)
#    plt.show()
