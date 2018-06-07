from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import random
from PyQt5 import QtCore, QtGui
import u3
import numpy as np

d = u3.U3() #initialize interface

d.configU3()
d.getCalibrationData() #calibrate Labjack

d.configIO(FIOAnalog = 31) # set all channels to analog
d.streamConfig(NumChannels=1,PChannels=[30],NChannels=[31],Resolution=1,\
               ScanFrequency=10000,SamplesPerPacket=25)


AIN_REGISTER = 0 # sets input to 0 default value
FIOO_STATE_REGISTER = 6000 #open the port of flexible input output.

#from PyQt4 import QtCore, QtGui

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.central_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.login_widget = LoginWidget(self)
        self.login_widget.button.clicked.connect(self.plotter)
        #self.login_widget.button.clicked.connect(self.stop_plotting)
        self.central_widget.addWidget(self.login_widget)
       # self.title = 'Quantized Conductance'
    
        self.Quit()

    def plotter(self):
        
        self.data =[0]
        self.curve = self.login_widget.plot.getPlotItem().plot()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updater)
        self.timer.start(0)

    def stop_plotting(self):
        d.streamStop()
       # d.close()

    def Quit(self):
        btn = QtGui.QPushButton("Quit", self)
        btn.clicked.connect(self.stop_plotting)
        btn.resize(50,50)
        #btn.move(100,100)
        self.show()

    def updater(self):

        #self.data.append(self.data[-1]+0.2*(0.5-random.random()) )
       # self.curve.setData(self.data)
        self.line = d.getTemperature() #is the function that reads the input and registers this value in the variable data
        self.data.append(int(self.line))
        #self.xdata = d.streamStart() 
        self.xdata = np.array(self.data, dtype='float64')
        self.curve.setData(self.xdata)

class LoginWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.button = QtGui.QPushButton('Start Plotting')
        #self.button1 = QtGui.QPushButton('Stop Plotting')
        layout.addWidget(self.button)
        #layout.addWidget(self.button1)
        self.plot = pg.PlotWidget()
        layout.addWidget(self.plot)
        self.setLayout(layout)
        self.show()

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
