from PyQt5.QtGui import *
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import * 
import pyqtgraph as pg
import random
import u3
import sys

d = u3.U3() #initialize interface

d.configU3() #configure labjack 
d.getCalibrationData() #calibrate Labjack
'''
d.configIO(FIOAnalog = 31) # set all channels to analog
d.streamConfig(NumChannels=1,PChannels=[30],NChannels=[31],Resolution=1,\
               ScanFrequency=10000,SamplesPerPacket=25)
AIN_REGISTER = 30 # sets input to 0 default value
FIOO_STATE_REGISTER = 6000 #open the port of flexible input output.
'''


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("Temperture")
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginWidget(self)
        self.login_widget.button.clicked.connect(self.plotter)
        self.login_widget.button1.clicked.connect(self.stop)
        self.login_widget.button2.clicked.connect(self.clear)
        self.central_widget.addWidget(self.login_widget)
       

    def plotter(self):
        self.data =[0]
        self.temperature = [0]
        self.curve = self.login_widget.plot.getPlotItem().plot()

        self.timer = QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(100)

    def updater(self):

       # self.data.append(self.data[-1]+0.2*(0.5-random.random()) )
        self.temp1 = d.getTemperature()
        self.temp = (self.temp1-273.15)*1.8 +32
        self.temperature.append( self.temp )
        self.curve.setData(self.temperature)    

        #self.curve.setData(self.data)
    def stop(self):
        #d.streamStop()
        self.timer.stop()
        #d.close()
   
    def clear(self):
        self.curve.clear()


class LoginWidget(QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        
        self.plot = pg.PlotWidget()
        self.button = QPushButton('Start Plotting')
        self.button1 = QPushButton('Stop Plotting')
        self.button2 = QPushButton("Clear Plot")
        
        layout = QHBoxLayout()
        layout2 = QVBoxLayout()
      
        
        layout2.addWidget(self.button)
        layout2.addWidget(self.button1)
        layout2.addWidget(self.button2)
        layout.addWidget(self.plot)

        layout.addLayout(layout2)
    
        self.setLayout(layout)
        

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()