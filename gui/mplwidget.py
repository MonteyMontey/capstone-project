""" https://stackoverflow.com/questions/43947318/plotting-matplotlib-figure-inside-qwidget-using-qt-designer-form-and
-pyqt5/44029435#44029435 """

import matplotlib

# Ensure using PyQt5 backend
matplotlib.use('QT5Agg')

from PyQt5 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas


class MplCanvas(Canvas):
    """Matplotlib canvas class to create figure"""

    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        self.fig.subplots_adjust(bottom=0.2, left=0.175)
        Canvas.__init__(self, self.fig)


class MplWidget(QtWidgets.QWidget):
    """ Matplotlib widget to embed canvas in GUI"""

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
