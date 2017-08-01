#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 14:50:49 2017

@author: donnashimizu
"""

import numpy as np


def cart2sph(x, y, z):
    """conversion of certesian coordinates (x,y,z) to spherical coords, returns r, theta, phi"""
    radius = np.max((np.max(x),np.max(y),np.max(z)))/2.0
    x -= radius
    y -= radius
    z -= radius
    
    x /= radius
    y /= radius
    z /= radius
    
    dx = x*np.sqrt(1-y**2/2.0-z**2/2.0+(y**2*z**2)/3.0)
    dy = y*np.sqrt(1-z**2/2.0-x**2/2.0+(z**2*x**2)/3.0)
    dz = z*np.sqrt(1-x**2/2.0-y**2/2.0+(y**2*x**2)/3.0)
    
    dx*=radius
    dy*=radius
    dz*=radius
    
    
    hxy = []
    r = []
    phi = []
    theta = []
    for i in range(len(dx)):
        hxy.append(np.hypot(dx[i], dy[i]))
        r.append(np.hypot(hxy[i], dz[i]))
        theta.append(np.arctan2(dy[i], dx[i])+np.pi)
        phi.append(np.arctan2(hxy[i], dz[i]))
    return r, theta, phi