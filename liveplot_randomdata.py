from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import random

app = QtGui.QApplication([])
p = pg.plot()
curve = p.plot()
data = [0]

def updater():

    data.append(random.random())
    curve.setData(data) #xdata is not necessary


timer = QtCore.QTimer()
timer.timeout.connect(updater)
timer.start(0)

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
