# This code is the property of Hubert E Coburn II
import os
from time import sleep
from datetime import datetime
import subprocess as sp
import matplotlib.pyplot as plt
import numpy as np


def runDetect():
    """ The following function runs the Kromek supplied detection software and returns the input fie for the 
    Fortran program to run through"""
    try:
        os.system('pyKromek_lib.py')

    except Exception:
        print('error: did not detect')
        
def runSorter():
    """ The following function runs the Fortran program that resorts the data from the Kromek software"""
    try:
        sp.call('sort.exe')
        
    except Exception:
        print('Sorting run process did not work')
        
def readFile(filename):
    """The following program opens and reads the data from the previously created sorting data"""
    try:
        xdata = np.loadtxt(filename, usecols=[1], dtype=float)
        ydata = np.loadtxt(filename, usecols=[3], dtype=float)
        return xdata, ydata
        
    except Exception:
        print('error in file read x')
        
def plotData(x,y):
    """The following function plots the previously pulled data"""
    try:
        plt.plot(x,y,linewidth=0.5)
        plt.title('Radiation Counts', fontsize=18)
        plt.xlabel('Energy [keV]', fontsize=15)
        plt.ylabel('Counts', fontsize=15)
               
        storename  = datetime.now().time().strftime('%H%M%S%f')
        
        plt.savefig('Test_Data/'+str(storename)+'.png')
        
        plt.show(block = False)
        plt.pause(0.5)
        plt.close()
        
    except Exception:
        print('error in file plot')
        
def storeData(livetime,filename):
    """the following function stores the pulled data with a stamp"""
    try:
        data = np.loadtxt(filename, usecols=[1,3], dtype=float)
        np.savetxt('Background_Data/'+str(livetime)+'.txt',data,delimiter ='    ,    ')
        
    except Exception:
        print('error in file save')
        
#### Begin the main program here ####
# This code is the property of Hubert E Coburn II
# The following line runs the initial data aquisition function
timeup = input('Enter live time in minutes:   ')
runDetect()
# The following line runs the Fortran sort program        
runSorter()

# The following line runs the data aquisition functions from the sorted data
energies, counts = readFile('sorted.txt')

# The following line runs the plotting function
#plotData(energies,counts)

# The following line runs the data aquisition tool again for the second sorted data set
#energies, counts = readFile('sortedmod.txt')

# The following line runs the plotting function...again
#plotData(energies,counts)
storeData(timeup,'sorted.txt')

