# -*- coding: utf-8 -*-
"""
Created on Thu May 11 10:12:24 2017

@author: felix
"""

import numpy as np

#imports the data file, converts it into float32 values, stores it into an array

dataname = raw_input("What is the filename (without '.dat')?: ")
dataname += ".dat"

#0.000xv0(2)
data = np.fromfile(dataname, dtype=np.float32)

data = data[12:]

x=data[0::6]
y=data[1::6]
z=data[2::6]
xvel=data[3::6]
yvel=data[4::6]
zvel=data[5::6]

np.savez("pos(1).npz", x=x,y=y,z=z)
np.savez("vel(1).npz", xvel=xvel,yvel=yvel,zvel=zvel)

#import csv
##Rewrites everything into csv file
#with open('RawData.csv', 'w') as csvfile:
#    csvwriter = csv.writer(csvfile, delimiter=',')
#    csvwriter.writerow(['RawData'])
#    for i in range(len(data)):
#        csvwriter.writerow([data[i]])
