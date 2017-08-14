# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import Algo3 as a
import peakDetection as pd
import numpy as np
import ConvertDataFloat32 as conv
import matplotlib.pyplot as plt

def convertData(simulationFile):
    pos = conv.getPos(simulationFile)
    np.save("../TestData/posTest.npy",pos)
    
    return pos
    
def ridgeletLines(pos):
    lines = a.algorithm3(pos)
    np.save("../TestData/linesTest.npy", lines)
    return lines

def preCut(data):
    std = np.std(data)
    std_away = 10
    dev = std*std_away
    preCutLines = []
    for line in range(len(data)):
        for i in data[line]:
            if np.abs(i)>=dev:
                preCutLines.append(data[line])
                break
    return preCutLines
    
def peakDetection(lines):
    results = []
    for line in range(len(lines)):
        if line%50 == 0:
            print "{0:2.0f}%".format(np.float(line)/np.float(len(lines)) * 100)
        results.append(pd.find_max_width(lines[line]))        
    np.save("../TestData/max_widthTest.npy", results)
    return results
    
def plotResults(results):
    plt.figure()
    for lines in range(len(results)):
        line = results[lines]
        for i in range(len(line)):
            peak = line[i][0]
            width = line[i][1]
            plt.plot(np.linspace(peak,peak,2),np.linspace(0,width,2), '-')
            plt.pause(1e-6)
    plt.savefig("../Images/peakResults.png")
    return 
    
def wakeDetection(simulationFile):
     return plotResults(peakDetection(preCut(ridgeletLines(convertData(simulationFile)))))

def ask():
    default_name = "../RawData/0.000xv0(1)"
    simulationFile = raw_input("Name of the file (w/o '.dat') ? ")
    if simulationFile == "":
        simulationFile = default_name+".dat"
    return wakeDetection(simulationFile)
    
ask()
#lines = np.load("../TestData/linesTest.npy")
#results = peakDetection(preCut(lines))
    