# -*- coding: utf-8 -*-
"""
Created on Thu May 11 09:09:55 2017

@author: felix

"""

import numpy as np
import spinmob as s

print "Converting data..."
data = s.data.load(path='RawData.csv').columns['RawData'][12:]
#data = s.data.load(path='RawData.csv').columns['RawData'][12:]

#data = data[12:]#Cuts the first 12 values (as instructed)
print "Done!"

pos = []#initiate the arrays
vel = []

print "Organizing data..."
i=0  
while i < len(data):
#for i in range(len(data)):#Runs through the array
    
    if i+6 > len(data):
        break

    for j in range(3):
        pos.append(data[i+j])#retrieves the appropriate index
        vel.append(data[i+j+3])#same for velocity (3 indexes further)

    i+=6#we increase the data array index by 6 (3 pos, 3 vel) 
    
print "Done!"

import csv

#for i in range(10):
#    with open(('Positions%d_10.csv') %i, 'w') as csvfile:
#        csvwriter = csv.writer(csvfile, delimiter=',')
#        csvwriter.writerow(['Position'])
#        for j in range(len(pos)/100):
#            csvwriter.writerow([pos[j]])

print "Creating CSV position file..."
with open('Positions.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(['Position'])
    for i in range(len(pos)):
        csvwriter.writerow([pos[i]])
print "Done!"

#with open('Velocities.csv', 'wb') as csvfile:
#    csvwriter = csv.writer(csvfile, delimiter=',')
#    csvwriter.writerow(['Velocity'])
#    for i in range(len(vel)):
#        csvwriter.writerow([vel[i]])

##Keeps first and last data points into csv file
#with open('FirstLast10PosVel.csv', 'w') as csvfile:
#    csvwriter = csv.writer(csvfile, delimiter=',')
#    csvwriter.writerow(['First Pos', 'First Vel', 'Last Pos', 'Last Vel'])
#    for i in range(10):
#        csvwriter.writerow([pos[i], vel[i], pos[len(pos)-11+i], vel[len(pos)-11+i]])   
  