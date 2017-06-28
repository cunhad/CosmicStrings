# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 14:43:00 2017

@author: Hyunji
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:58:36 2017

@author: felix
"""


#print "Importing data..."
import numpy as np
import matplotlib.pyplot as plt
import pylab
from mpl_toolkits.mplot3d import Axes3D
from scipy import misc

print "Loading positions..."
default_dataname = "pos(1)"
dataname = raw_input(("filename (without '.npz') (default is '%s')?: " %default_dataname))
if dataname == "":
    dataname = default_dataname
dataname +=".npz"


#xpos = list(np.load(dataname)['x'])
#ypos = list(np.load(dataname)['y'])
#zpos = list(np.load(dataname)['z'])



xpos = list(np.array(np.load(dataname)['x']))
ypos = list(np.load(dataname)['y'])
zpos = list(np.load(dataname)['z'])
pos = []
for i in range(len(xpos)):
    pos.append((xpos[i], ypos[i], zpos[i]))
print "Done!" 

pos = np.zeros((3,len(xpos)))
pos[0,:] = xpos[:]
pos[1,:] = ypos[:]
pos[2,:] = zpos[:]

dataset = [xpos,ypos,zpos]
coordinates = ["X","Y","Z"]

for k in range(3):
  cell_size = 2.0
  max_x = np.max(xpos)
  cells = max_x/cell_size

  print "Counting densities..."
  plt.figure(10)
#  counts, xedges, yedges, Image = plt.hist2d(xpos, ypos, (cells,cells), cmap=plt.cm.jet)
  counts, xedges, yedges, Image = plt.hist2d(dataset[k], dataset[(k+1)%3], (cells,cells), cmap=plt.cm.jet)
#  plt.colorbar()
#  plt.show()
  plt.close(10)
  print "Done!"

  #counts = np.transpose(counts)#This is only so that the graph comes out ok

  norm_counts = (counts-np.mean(counts))/np.mean(counts)#Fluctuations
  np.save(('norm_counts%d.npy' %k), norm_counts)


#  for i in range(len(norm_counts)):
#      for j in range(len(norm_counts[i])):
#          if norm_counts[i][j]>2:
#              norm_counts[i][j] = 2

  heatmap_size = (8,5)

  fig = plt.figure(figsize=heatmap_size)

  ax = fig.add_subplot(111)
  ax.set_title('%s%s plane' %(coordinates[k],coordinates[(k+1)%3]))
  plt.imshow(norm_counts, aspect='auto', interpolation='none', origin='lower', extent=(0,40,0,40))

  ax.set_aspect('equal')
  cax = fig.add_axes([0.12, 0.1, 0.78, 0.8])
  cax.get_xaxis().set_visible(False)
  cax.get_yaxis().set_visible(False)
  cax.patch.set_alpha(0)
  cax.set_frame_on(False)

  plt.show()

  linearCounts = (np.sum(counts, axis=0)-np.mean(np.sum(counts, axis=0)))/np.mean(np.sum(counts,axis=0))

  plt.figure("%i" %k)
  plt.plot(np.linspace(0,40,np.int(cells)),linearCounts,'k-')
  plt.title('%s-wise compression of %s%s plane' %(coordinates[(k+1)%3],coordinates[k],coordinates[(k+1)%3]))
  plt.xlim(0,40)
  plt.grid(axis='both')
  plt.show()
  
FFT
  

FFTdata = np.abs(np.fft.fftn(dataset))

def sphericalcoords(data):
    ptsnew = np.zeros(data.shape)
    xy = data[0,:]**2 + data[1,:]**2
    print ptsnew.shape
    ptsnew[0,:] = np.sqrt(xy + data[2,:]**2)
    ptsnew[1,:] = np.arctan2(np.sqrt(xy), data[2,:]) # for elevation angle defined from Z-axis down
    ptsnew[2,:] = np.arctan2(data[1,:], data[0,:])
    return ptsnew
    
def discrete_radon_transform(image, steps):
    R = np.zeros((steps, len(image)), dtype='float64')
    FFTimage = np.abs(np.fft.fftn(image))
    for s in range(steps):
        rotation = misc.imrotate(image, -s*180/steps).astype('float64')
        R[:,s] = sum(rotation)
    return R

# Read image as 64bit float gray scale
image = misc.imread('wakedensity.png', flatten=True).astype('float64')
radon = discrete_radon_transform(image, 399)

# Plot the original and the radon transformed image
plt.subplot(1, 2, 1), plt.imshow(image, cmap='gray')
plt.xticks([]), plt.yticks([])
plt.subplot(1, 2, 2), plt.imshow(radon, cmap='gray')
plt.xticks([]), plt.yticks([])
plt.show()