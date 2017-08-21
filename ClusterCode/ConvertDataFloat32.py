# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:12:24 2017

@author: felix
"""

import numpy as np

def getPos(dataFile):
    data = np.fromfile(dataFile, np.float32)
    data = data[12:]
    xpos = data[0::6]
    ypos = data[1::6]
    zpos = data[2::6]
    pos = np.zeros((3,len(xpos)))
    pos[0,:] = xpos[:]
    pos[1,:] = ypos[:]
    pos[2,:] = zpos[:]
    
    return pos

#imports the data file, converts it into float32 values, stores it into an array

#Data acquisition
#default_dataname = "0.000xv0(1)"
#dataname = raw_input("filename w/o '.dat' (default is '%s')?: " %(default_dataname))
#if dataname == "":
#    dataname = default_dataname
#dataname = "../RawData/" + dataname
#dataname +=".dat"
##0.000xv0(2)
#data = np.fromfile(dataname, dtype=np.float32)
#
#data = data[12:]
#
#x=data[0::6]
#y=data[1::6]
#z=data[2::6]
#xvel=data[3::6]
#yvel=data[4::6]
#zvel=data[5::6]
#
#while True:
#    savename = raw_input("Name of saved file w/o .npz?")
#    if savename is not "":
#        break
#    else:
#        print "You did not enter a valid filename!"
#savename = "../Data/" + savename
#savename +=".npz"
#
#np.savez(savename, x=x,y=y,z=z)
#np.savez(savename, x*vel=xvel,yvel=yvel,zvel=zvel)

#import csv
##Rewrites everything into csv file
#with open('RawData.csv', 'w') as csvfile:
#    csvwriter = csv.writer(csvfile, delimiter=',')
#    csvwriter.writerow(['RawData'])
#    for i in range(len(data)):
#        csvwriter.writerow([data[i]])
