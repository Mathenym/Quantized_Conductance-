#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 13:25:46 2018

@author: Mitch
"""


from matplotlib.pyplot import figure, subplot, plot, grid, show 
import u3
from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from pyqtgraph.ptime import time

app = QtGui.QApplication([])

p = pg.plot()
p.setWindowTitle('live plot from serial')
curve = p.plot()


 
d = u3.U3() #initialize interface 
 
d.configU3()
d.getCalibrationData() #calibrate Labjack
 
d.configIO(FIOAnalog = 31) # set all channels to analog
AIN_REGISTER = 0 # sets imput to 0 default value 
FIOO_STATE_REGISTER = 6000 # configure the Flexible input number as 3 as an analog input 
 
#sim_time = 10
#start_time = time.time()
data = []

def update():
    
    line = d.getAIN(AIN_REGISTER)  #is the function that reads the input and registers this value in the variable data
    data.append(int(line))
    xdata = np.array(data, dtype='float64')
    curve.setData(xdata)
    app.processEvents()
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()    