#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 12:55:20 2018

@author: Mitch
"""

import time 
from matplotlib.pyplot import figure, subplot, plot, grid, show 
import u3
 
d = u3.U3() #initialize interface 
 
d.configU3()
d.getCalibrationData() #calibrate Labjack
 
d.configIO(FIOAnalog = 31) # set all channels to analog
AIN_REGISTER = 0 # sets imput to 0 default value 
FIOO_STATE_REGISTER = 6000 # configure the Flexible input number as 3 as an analog input 
 
sim_time = 10
start_time = time.time()
X = []

while(time.time() - start_time<sim_time):
    x = d.getAIN(AIN_REGISTER)  #is the function that reads the input and registers this value in the variable x
    X.append(x)
    print(x) 
    time.sleep(0.001)
     
     
     
d.close()




