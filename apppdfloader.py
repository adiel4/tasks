import sys
from PyQt5.QtWidgets import QFileDialog, QCheckBox, QGridLayout, QTabWidget, QApplication, QWidget, QLabel, \
    QPushButton, QMainWindow, QLineEdit, QComboBox, QToolTip
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.basemap import Basemap
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QThread, QObject
import matplotlib.pyplot as plt
import numpy as np

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.btn_dwnld = QPushButton('Загрузить', self)
        self.btn_dwnld.move(40, 230)
        self.btn_dwnld.resize(100, 30)
        self.btn_dwnld.clicked.connect(self.fuck_your)
        self.setGeometry(0, 0, 500, 500)
        self.setWindowTitle('PDF loader')
        self.show()
    def fuck_your(self):
        print('fuck you')

if __name__.endswith('__main__'):
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
