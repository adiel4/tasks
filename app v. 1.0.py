import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog, QCheckBox, QGridLayout, QTabWidget, QApplication, QWidget, QLabel, \
    QPushButton, QMainWindow, QLineEdit, QComboBox, QToolTip
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.basemap import Basemap
from scipy.signal import find_peaks
import traceback

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        tuple (exctype, value, traceback.format_exc() )

    result
        object data returned from processing, anything

    progress
        int indicating % progress

    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread

    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.

    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function

    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress

class mapLonLat(FigureCanvas):
    def __init__(self, parent, long, lat, matrix, date, coltop, name, clat, clon, colMap, colBot, crclCol, crclSize,
                 latMinInd, latMaxInd, lonMinInd, lonMaxInd):
        plt.close('all')
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        plt.subplots_adjust(left=0.155, bottom=0.165, right=0.990, top=0.915)
        super().__init__(self.fig)
        self.setParent(parent)
        m = Basemap(projection='merc', llcrnrlat=lat[latMinInd], urcrnrlat=lat[latMaxInd],
                    llcrnrlon=long[lonMinInd], urcrnrlon=long[lonMaxInd], lat_ts=20, resolution='i')
        m.drawcoastlines(linewidth=0.5)
        xs, ys = np.meshgrid(long, lat)
        x, y = m(xs, ys)
        m.drawparallels(np.arange(lat[4], lat[-1], 5), labels=[1, 0, 0, 0], linewidth=0.1
                        , fmt=(lambda x: (u"%d\N{DEGREE SIGN}") % (x)))
        m.drawmeridians(np.arange(long[0], long[-1], 10), labels=[0, 0, 0, 1], linewidth=0.1
                        , fmt=(lambda x: (u"%d\N{DEGREE SIGN}") % (x)))
        highColor = round(coltop / 0.2)
        lowColor = round(colBot / 0.2)
        self.levels = [0.2 * x for x in range(lowColor, highColor + 1)]
        ac = m.contourf(x, y, matrix, self.levels, cmap=colMap)
        self.ax.set_title(date, )
        clb = self.fig.colorbar(ac, orientation='vertical')
        clb.ax.set_title(name, fontsize=10)
        self.ax.set_xlabel('??????????????, ??E', labelpad=20)
        self.ax.set_ylabel('????????????, ??N', labelpad=30)
        coord = m(long[clon], lat[clat])
        self.ax.plot(coord[0], coord[1], color=crclCol[0], marker='*', markersize=float(crclSize[:-2]) * 10)
        self.ax.grid(color='w', linewidth=0.1)

    def save1(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tempArray = []
        self.dates = []
        self.level = []
        self.longtitude = []
        self.latitude = []

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        ## ???????????????? ???????????? #############################

        self.btnDwnld = QPushButton('????????????????', self)
        self.btnDwnld.move(40, 230)
        self.btnDwnld.resize(100, 30)
        self.btnDwnld.clicked.connect(self.oh_no)
        self.btnExit = QPushButton('??????????', self)
        self.btnExit.move(40, 600)
        self.btnExit.resize(50, 50)
        # self.btnExit.clicked.connect(self.exit)
        self.btnMap = QPushButton('??????????', self)
        self.btnMap.move(150, 250)
        self.btnMap.resize(100, 20)
        self.btnMap.clicked.connect(self.oh_no2)
        # self.btnMap.clicked.connect(self.dateMap2)
        # self.btnMap.clicked.connect(self.dateMap3)
        self.btnGraph = QPushButton('????????????', self)
        self.btnGraph.move(40, 270)
        self.btnGraph.resize(60, 30)
        # self.btnGraph.clicked.connect(self.timePlot)
        self.btnPrevMap = QPushButton('<', self)
        self.btnPrevMap.move(150, 270)
        self.btnPrevMap.resize(30, 30)
        # self.btnPrevMap.clicked.connect(self.PrevMap)
        # self.btnPrevMap.clicked.connect(self.dateMap)
        # self.btnPrevMap.clicked.connect(self.dateMap2)
        # self.btnPrevMap.clicked.connect(self.dateMap3)
        self.btnNextMap = QPushButton('>', self)
        self.btnNextMap.move(180, 270)
        self.btnNextMap.resize(30, 30)
        # self.btnNextMap.clicked.connect(self.NextMap)
        # self.btnNextMap.clicked.connect(self.dateMap)
        # self.btnNextMap.clicked.connect(self.dateMap2)
        # self.btnNextMap.clicked.connect(self.dateMap3)

        #### ???????????????? ?????????????? ####################
        self.labVys1 = QLabel('????????????(1), ??????', self)
        self.labVys1.resize(self.labVys1.sizeHint())
        self.labVys1.move(40, 30)
        self.labVys2 = QLabel('????????????(2), ??????', self)
        self.labVys2.resize(self.labVys2.sizeHint())
        self.labVys2.move(40, 60)
        self.labShir1 = QLabel('????????????(????????????)', self)
        self.labShir1.resize(self.labShir1.sizeHint())
        self.labShir1.move(40, 90)
        self.labDolg1 = QLabel('??????????????(????????????)', self)
        self.labDolg1.resize(self.labDolg1.sizeHint())
        self.labDolg1.move(40, 120)
        self.labShir2 = QLabel('????????????(??????????)', self)
        self.labShir2.resize(self.labShir2.sizeHint())
        self.labShir2.move(40, 150)
        self.labDolg2 = QLabel('??????????????(??????????)', self)
        self.labDolg2.resize(self.labDolg2.sizeHint())
        self.labDolg2.move(40, 180)
        self.labLTA = QLabel('LTA', self)
        self.labLTA.resize(70, 20)
        self.labLTA.move(250, 30)
        self.labSTA = QLabel('STA', self)
        self.labSTA.resize(70, 20)
        self.labSTA.move(250, 90)

        ########### ????????????????  ???????? ?????? ???????????? ##############
        self.textLTA = QLineEdit(self)
        self.textLTA.move(250, 60)
        self.textLTA.setText('105')
        self.textLTA.resize(50, 20)
        self.textSTA = QLineEdit(self)
        self.textSTA.move(250, 120)
        self.textSTA.setText('21')
        self.textSTA.resize(50, 20)

        ################ ???????????????? ????????????   #####################
        self.boxLevel1 = QComboBox(self)
        self.boxLevel1.move(150, 30)
        self.boxLevel1.resize(70, 20)
        self.boxLevel2 = QComboBox(self)
        self.boxLevel2.move(150, 60)
        self.boxLevel2.resize(70, 20)
        self.boxLat1 = QComboBox(self)
        self.boxLat1.move(150, 90)
        self.boxLat1.resize(70, 20)
        self.boxLon1 = QComboBox(self)
        self.boxLon1.move(150, 120)
        self.boxLon1.resize(70, 20)
        self.boxLat2 = QComboBox(self)
        self.boxLat2.move(150, 150)
        self.boxLat2.resize(70, 20)
        self.boxLon2 = QComboBox(self)
        self.boxLon2.move(150, 180)
        self.boxLon2.resize(70, 20)
        self.boxDates = QComboBox(self)
        self.boxDates.move(150, 230)
        self.boxDates.resize(100, 20)
        self.boxDates.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        ############# ???????????????? ???????????????? ???????????????? ?????????????? ###############

        self.tabs = QTabWidget(self)
        self.tabs.resize(950, 700)
        self.tabs.move(320, 0)

        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        self.tab4 = QWidget(self)
        self.tab5 = QWidget(self)
        self.tab6 = QWidget(self)
        self.tab7 = QWidget(self)

        self.tabs.addTab(self.tab1, "??????????(N/E)")
        self.tabs.addTab(self.tab4, "??????????????;STA/LTA")
        self.tabs.addTab(self.tab5, "C??????(N/E)")
        self.tabs.addTab(self.tab6, '???????????????????? ????????????????')

        self.tab1.layout = QGridLayout(self.tab1)
        self.tab1.setLayout(self.tab1.layout)
        self.tab4.layout = QGridLayout(self.tab4)
        self.tab4.setLayout(self.tab4.layout)
        self.tab5.layout = QGridLayout(self.tab5)
        self.tab5.setLayout(self.tab5.layout)
        self.tab6.layout = QGridLayout(self.tab6)
        self.tab6.setLayout(self.tab6.layout)

        self.tab5.layout.setRowStretch(0, 1)
        self.tab5.layout.setRowStretch(1, 4)
        self.tab5.layout.setRowStretch(4, 4)
        self.tab5.layout.setRowStretch(3, 1)
        self.tab5.layout.setRowStretch(6, 1)

        self.tab4.layout.setRowStretch(0, 5)
        self.tab4.layout.setRowStretch(1, 1)
        self.tab4.layout.setRowStretch(2, 5)
        self.tab4.layout.setRowStretch(3, 1)
        self.tab4.layout.setColumnStretch(0, 5)
        self.tab4.layout.setColumnStretch(1, 5)

        ########### ??????????????: ????????() #################

        self.labDate = QLabel('????????', self)
        self.tab5.layout.addWidget(self.labDate, 0, 0, 1, 1)
        self.boxDates2 = QComboBox(self)
        self.boxDates2.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tab5.layout.addWidget(self.boxDates2, 0, 1, 1, 4)
        self.boxDates3 = QComboBox(self)
        self.boxDates3.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tab5.layout.addWidget(self.boxDates3, 0, 5, 1, 4)
        self.lablat = QLabel('????????????', self)
        self.tab5.layout.addWidget(self.lablat, 0, 9, 1, 1)
        self.boxLat3 = QComboBox(self)
        self.tab5.layout.addWidget(self.boxLat3, 0, 10, 1, 1)
        self.lablon = QLabel('??????????????', self)
        self.tab5.layout.addWidget(self.lablon, 0, 11, 1, 1)
        self.boxLon3 = QComboBox(self)
        self.tab5.layout.addWidget(self.boxLon3, 0, 12, 1, 1)
        self.btnMap2 = QPushButton('????????????', self)
        self.tab5.layout.addWidget(self.btnMap2, 0, 13, 1, 2)
        # self.btnMap2.clicked.connect(self.latlonMap)
        self.cmapBox2 = QComboBox(self)
        self.tab5.layout.addWidget(self.cmapBox2, 0, 15, 1, 2)

        ########### ??????????????: ???????????????????? ???????????????? #################

        self.labSave1 = QLabel('??????????(N/E)', self)
        self.tab6.layout.addWidget(self.labSave1, 0, 0)
        self.textSave1 = QLineEdit(self)
        self.textSave1.setText('file1')
        self.tab6.layout.addWidget(self.textSave1, 0, 1)
        self.boxFormats1 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats1, 0, 2)
        self.textDPI = QLineEdit(self)
        self.textDPI.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI, 0, 3)
        self.btnSaveMap1 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap1, 0, 4)
        # self.btnSaveMap1.clicked.connect(self.Save1)
        self.labSave2 = QLabel('??????????(N/h)', self)
        self.tab6.layout.addWidget(self.labSave2, 1, 0)
        self.textSave2 = QLineEdit(self)
        self.textSave2.setText('file2')
        self.tab6.layout.addWidget(self.textSave2, 1, 1)
        self.boxFormats2 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats2, 1, 2)
        self.textDPI2 = QLineEdit(self)
        self.textDPI2.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI2, 1, 3)
        self.btnSaveMap2 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap2, 1, 4)
        # self.btnSaveMap2.clicked.connect(self.Save2)

        self.labSave3 = QLabel('??????????(E/h)', self)
        self.tab6.layout.addWidget(self.labSave3, 2, 0)
        self.textSave3 = QLineEdit(self)
        self.textSave3.setText('file3')
        self.tab6.layout.addWidget(self.textSave3, 2, 1)
        self.boxFormats3 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats3, 2, 2)
        self.textDPI3 = QLineEdit(self)
        self.textDPI3.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI3, 2, 3)
        self.btnSaveMap3 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap3, 2, 4)
        # self.btnSaveMap3.clicked.connect(self.Save3)

        self.labSave4 = QLabel('??????????????', self)
        self.tab6.layout.addWidget(self.labSave4, 3, 0)
        self.textSave4 = QLineEdit(self)
        self.textSave4.setText('file4')
        self.tab6.layout.addWidget(self.textSave4, 3, 1)
        self.boxFormats4 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats4, 3, 2)
        self.textDPI4 = QLineEdit(self)
        self.textDPI4.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI4, 3, 3)
        self.btnSaveMap4 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap4, 3, 4)
        # self.btnSaveMap4.clicked.connect(self.Save4)

        self.labSave5 = QLabel('STA/LTA ??????????????', self)
        self.tab6.layout.addWidget(self.labSave5, 4, 0)
        self.textSave5 = QLineEdit(self)
        self.textSave5.setText('file5')
        self.tab6.layout.addWidget(self.textSave5, 4, 1)
        self.boxFormats5 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats5, 4, 2)
        self.textDPI5 = QLineEdit(self)
        self.textDPI5.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI5, 4, 3)
        self.btnSaveMap5 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap5, 4, 4)
        # self.btnSaveMap5.clicked.connect(self.Save5)

        self.labSave6 = QLabel('???????????????????????? ??????????????', self)
        self.tab6.layout.addWidget(self.labSave6, 5, 0)
        self.textSave6 = QLineEdit(self)
        self.textSave6.setText('file6')
        self.tab6.layout.addWidget(self.textSave6, 5, 1)
        self.boxFormats6 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats6, 5, 2)
        self.textDPI6 = QLineEdit(self)
        self.textDPI6.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI6, 5, 3)
        self.btnSaveMap6 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap6, 5, 4)
        # self.btnSaveMap6.clicked.connect(self.Save6)

        self.labSave7 = QLabel('???????? ???? ????????????: dT', self)
        self.tab6.layout.addWidget(self.labSave7, 6, 0)
        self.textSave7 = QLineEdit(self)
        self.textSave7.setText('file7')
        self.tab6.layout.addWidget(self.textSave7, 6, 1)
        self.boxFormats7 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats7, 6, 2)
        self.textDPI7 = QLineEdit(self)
        self.textDPI7.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI7, 6, 3)
        self.btnSaveMap7 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap7, 6, 4)
        # self.btnSaveMap7.clicked.connect(self.Save7)
        self.labSave8 = QLabel('???????? ???? ????????????: dT*c', self)
        self.tab6.layout.addWidget(self.labSave8, 7, 0)
        self.textSave8 = QLineEdit(self)
        self.textSave8.setText('file8')
        self.tab6.layout.addWidget(self.textSave8, 7, 1)
        self.boxFormats8 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats8, 7, 2)
        self.textDPI8 = QLineEdit(self)
        self.textDPI8.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI8, 7, 3)
        self.btnSaveMap8 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap8, 7, 4)
        # self.btnSaveMap8.clicked.connect(self.Save8)
        self.labSave9 = QLabel('???????? ???? ??????????????: dT', self)
        self.tab6.layout.addWidget(self.labSave9, 8, 0)
        self.textSave9 = QLineEdit(self)
        self.textSave9.setText('file9')
        self.tab6.layout.addWidget(self.textSave9, 8, 1)
        self.boxFormats9 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats9, 8, 2)
        self.textDPI9 = QLineEdit(self)
        self.textDPI9.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI9, 8, 3)
        self.btnSaveMap9 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap9, 8, 4)
        # self.btnSaveMap9.clicked.connect(self.Save9)
        self.labSave10 = QLabel('???????? ???? ??????????????: dT*c', self)
        self.tab6.layout.addWidget(self.labSave10, 9, 0)
        self.textSave10 = QLineEdit(self)
        self.textSave10.setText('file10')
        self.tab6.layout.addWidget(self.textSave10, 9, 1)
        self.boxFormats10 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats10, 9, 2)
        self.textDPI10 = QLineEdit(self)
        self.textDPI10.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI10, 9, 3)
        self.btnSaveMap10 = QPushButton('??????????????????', self)
        self.tab6.layout.addWidget(self.btnSaveMap10, 9, 4)
        # self.btnSaveMap10.clicked.connect(self.Save10)

        imgFormats = ['.tiff', '.png', '.eps', '.jpeg', '.ps', '.raw', '.svg']

        box_formats = [self.boxFormats1, self.boxFormats2, self.boxFormats3, self.boxFormats4, self.boxFormats5,
                       self.boxFormats6, self.boxFormats7, self.boxFormats8, self.boxFormats9, self.boxFormats10]
        for form in imgFormats:
            for box in box_formats:
                box.addItem(form)

        ######## ???????????????? ???????????????? ?????????????? ?????????????????? ################

        self.tabsOptions = QTabWidget(self)
        self.tabsOptions.move(20, 300)
        self.tabsOptions.resize(300, 300)

        self.tab_line_options = QTabWidget(self)
        self.tab4.layout.addWidget(self.tab_line_options, 0, 1, 1, 1)

        self.tab_line_properties = QWidget(self)
        self.tab_line_markers = QWidget(self)
        self.tab_line_options.addTab(self.tab_line_markers, '??????????????')
        self.tab_line_options.addTab(self.tab_line_properties, '??????????')
        self.tab_line_properties.layout = QGridLayout(self.tab_line_properties)
        self.tab_line_properties.setLayout(self.tab_line_properties.layout)
        self.tab_line_markers.layout = QGridLayout(self.tab_line_markers)
        self.tab_line_markers.setLayout(self.tab_line_markers.layout)

        self.tabMap = QWidget(self)
        self.tabLimits = QWidget(self)
        self.tabData = QWidget(self)

        self.tabsOptions.addTab(self.tabMap, '??????????')
        self.tabsOptions.addTab(self.tabLimits, '??????????????')
        self.tabsOptions.addTab(self.tabData, '????????????')

        self.tabMap.layout = QGridLayout(self.tabMap)
        self.tabMap.setLayout(self.tabMap.layout)
        self.tabLimits.layout = QGridLayout(self.tabLimits)
        self.tabLimits.setLayout(self.tabLimits.layout)
        self.tabData.layout = QGridLayout(self.tabData)
        self.tabData.setLayout(self.tabData.layout)
        ############### ??????????????: ???????????????? ?????????? #####################

        self.labPlot1Wid = QLabel('?????????????? ?? ?????????? ??????????:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot1Wid, 0, 0)
        self.labPlot2Wid = QLabel('?????????????? ?? ?????????? ??????????:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot2Wid, 3, 0)
        self.labPlot3Wid = QLabel('?????????????? ?? ?????????? ??????????:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot3Wid, 6, 0)
        self.labPlot1Col = QLabel('?????????????????????????? ??????????????', self)
        self.tab_line_properties.layout.addWidget(self.labPlot1Col, 0, 3)
        self.labPlot2Col = QLabel('STA/LTA ??????????????', self)
        self.tab_line_properties.layout.addWidget(self.labPlot2Col, 3, 3)
        self.labPlot3Col = QLabel('???????????????????????? ??????????????', self)
        self.tab_line_properties.layout.addWidget(self.labPlot3Col, 6, 3)
        self.textPlot1Line1Width = QLineEdit(self)
        self.textPlot1Line1Width.setText('1')
        self.tab_line_properties.layout.addWidget(self.textPlot1Line1Width, 1, 0)
        self.textPlot1Line2Width = QLineEdit(self)
        self.textPlot1Line2Width.setText('1')
        self.tab_line_properties.layout.addWidget(self.textPlot1Line2Width, 2, 0)
        self.textPlot2Line1Width = QLineEdit(self)
        self.textPlot2Line1Width.setText('0.8')
        self.tab_line_properties.layout.addWidget(self.textPlot2Line1Width, 4, 0)
        self.textPlot2Line2Width = QLineEdit(self)
        self.textPlot2Line2Width.setText('0.8')
        self.tab_line_properties.layout.addWidget(self.textPlot2Line2Width, 5, 0)
        self.textPlot3Line1Width = QLineEdit(self)
        self.textPlot3Line1Width.setText('0.8')
        self.tab_line_properties.layout.addWidget(self.textPlot3Line1Width, 7, 0)
        self.textPlot3Line2Width = QLineEdit(self)
        self.textPlot3Line2Width.setText('0.8')
        self.tab_line_properties.layout.addWidget(self.textPlot3Line2Width, 8, 0)
        self.boxPlot1Line1Color = QComboBox(self)
        self.tab_line_properties.layout.addWidget(self.boxPlot1Line1Color, 1, 3)
        self.boxPlot1Line2Color = QComboBox(self)
        self.tab_line_properties.layout.addWidget(self.boxPlot1Line2Color, 2, 3)
        self.boxPlot2Line1Color = QComboBox(self)
        self.tab_line_properties.layout.addWidget(self.boxPlot2Line1Color, 4, 3)
        self.boxPlot2Line2Color = QComboBox(self)
        self.tab_line_properties.layout.addWidget(self.boxPlot2Line2Color, 5, 3)
        self.boxPlot3Line1Color = QComboBox(self)
        self.tab_line_properties.layout.addWidget(self.boxPlot3Line1Color, 7, 3)
        self.boxPlot3Line2Color = QComboBox(self)
        self.tab_line_properties.layout.addWidget(self.boxPlot3Line2Color, 8, 3)

        ############### ??????????????: ???????????????? ???????????????? #####################
        self.labMark = QLabel('?????????????? ???????????????? STA/LTA', self)
        self.tab_line_markers.layout.addWidget(self.labMark, 0, 0, 1, 4)
        self.markW = QLineEdit(self)
        self.markW.setText('1')
        self.tab_line_markers.layout.addWidget(self.markW, 1, 0)
        self.markW2 = QLineEdit(self)
        self.markW2.setText('1')
        self.boxcol = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxcol, 1, 1)
        self.boxcol2 = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxcol2, 1, 3)
        self.labMark2 = QLabel('?????????? ???????????????? STA/LTA', self)
        self.tab_line_markers.layout.addWidget(self.labMark2, 2, 0, 1, 4)
        self.tab_line_markers.layout.addWidget(self.markW2, 1, 2)
        self.boxMark = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxMark, 3, 0, 1, 2)
        self.boxMark2 = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxMark2, 3, 2, 1, 2)
        self.labMark3 = QLabel('?????????????? ???????????????? ??????????. ????????.', self)
        self.tab_line_markers.layout.addWidget(self.labMark3, 4, 0, 1, 4)
        self.markW3 = QLineEdit(self)
        self.markW3.setText('1')
        self.tab_line_markers.layout.addWidget(self.markW3, 5, 0)
        self.markW4 = QLineEdit(self)
        self.markW4.setText('1')
        self.tab_line_markers.layout.addWidget(self.markW4, 5, 2)
        self.labMark3 = QLabel('?????????? ???????????????? ??????????. ????????.', self)
        self.tab_line_markers.layout.addWidget(self.labMark3, 6, 0, 1, 4)
        self.boxcol3 = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxcol3, 5, 1)
        self.boxcol4 = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxcol4, 5, 3)
        self.boxMark3 = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxMark3, 7, 0, 1, 2)
        self.boxMark4 = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxMark4, 7, 2, 1, 2)

        markForm = [
            ' ?????? ????????????????',
            '.-??????????',
            'o-????????????????????',
            ',-??????????????',
            'v',
            '^',
            '>',
            '<',
            's-??????????????',
            'p-????????????.',
            '*-????????????',
            'h-??????????????.',
            '+',
            'x',
            'd-????????',
        ]
        for i in markForm:
            self.boxMark.addItem(i)
            self.boxMark2.addItem(i)
            self.boxMark3.addItem(i)
            self.boxMark4.addItem(i)

        ########### ??????????????: ???????????????? ?????????? ##############
        self.labisC = QLabel('?????????????????????? ????????????????????', self)
        self.tabMap.layout.addWidget(self.labisC, 0, 0, 1, 2)
        self.isC = QCheckBox(self)
        self.isC.setChecked(True)
        self.tabMap.layout.addWidget(self.isC, 0, 2)
        self.cmapBox = QComboBox(self)
        self.tabMap.layout.addWidget(self.cmapBox, 0, 3, 1, 2)
        for cmap_id in plt.colormaps():
            self.cmapBox.addItem(cmap_id)
            self.cmapBox2.addItem(cmap_id)
        self.cmapBox.setCurrentText('coolwarm')
        self.cmapBox2.setCurrentText('coolwarm')
        self.labGr = QLabel('????????. ?? ????????. ??????????????', self)
        self.tabMap.layout.addWidget(self.labGr, 1, 0, 1, 2)
        self.top1 = QLineEdit(self)
        self.top1.setText('1.5')
        self.tabMap.layout.addWidget(self.top1, 2, 0, 1, 1)
        self.labGr4 = QLabel('??????????(N/E)', self)
        self.tabMap.layout.addWidget(self.labGr4, 1, 2, 1, 3)
        self.bot1 = QLineEdit(self)
        self.bot1.setText('-0.2')
        self.tabMap.layout.addWidget(self.bot1, 2, 2, 1, 1)
        self.labGr2 = QLabel('????????. ?? ????????. ??????????????', self)
        self.tabMap.layout.addWidget(self.labGr2, 3, 0, 1, 2)
        self.top2 = QLineEdit(self)
        self.top2.setText('1.8')
        self.tabMap.layout.addWidget(self.top2, 4, 0, 1, 1)
        self.labGr5 = QLabel('??????????(N/h)', self)
        self.tabMap.layout.addWidget(self.labGr5, 3, 2, 1, 3)
        self.bot2 = QLineEdit(self)
        self.bot2.setText('-0.2')
        self.tabMap.layout.addWidget(self.bot2, 4, 2, 1, 1)
        self.labGr3 = QLabel('????????. ?? ????????. ??????????????', self)
        self.tabMap.layout.addWidget(self.labGr3, 5, 0, 1, 2)
        self.top3 = QLineEdit(self)
        self.top3.setText('1.8')
        self.tabMap.layout.addWidget(self.top3, 6, 0, 1, 1)
        self.labGr6 = QLabel('??????????(E/h)', self)
        self.tabMap.layout.addWidget(self.labGr6, 5, 2, 1, 3)
        self.bot3 = QLineEdit(self)
        self.bot3.setText('-0.2')
        self.tabMap.layout.addWidget(self.bot3, 6, 2, 1, 1)
        self.crclLabel = QLabel('????????????????', self)
        self.crclLabelLon = QLabel('??????????????', self)
        self.crclLabelLat = QLabel('????????????', self)
        self.tabMap.layout.addWidget(self.crclLabelLat, 9, 0)
        self.tabMap.layout.addWidget(self.crclLabelLon, 9, 2)
        self.tabMap.layout.addWidget(self.crclLabel, 8, 0)
        self.crcLat = QComboBox(self)
        self.tabMap.layout.addWidget(self.crcLat, 9, 1)
        self.crcLon = QComboBox(self)
        self.tabMap.layout.addWidget(self.crcLon, 9, 3, 1, 2)
        self.boxcrcDate = QComboBox(self)
        self.tabMap.layout.addWidget(self.boxcrcDate, 8, 1, 1, 2)
        self.crclLabelColor = QLabel('????????', self)
        self.tabMap.layout.addWidget(self.crclLabelColor, 10, 0)
        self.crclLabelSize = QLabel('????????????', self)
        self.tabMap.layout.addWidget(self.crclLabelSize, 10, 2)
        self.boxCrclColor = QComboBox(self)
        self.tabMap.layout.addWidget(self.boxCrclColor, 10, 1)
        self.textCrclSize = QLineEdit(self)
        self.textCrclSize.setText('1 ????')
        self.tabMap.layout.addWidget(self.textCrclSize, 10, 3)
        self.check_epic = QCheckBox(self)
        self.tabMap.layout.addWidget(self.check_epic, 8, 3)

        colors = ['b-??????????', 'g-??????????????', 'r-??????????????', 'c-??????????????', 'm-????????????????????', 'y-????????????', 'k-????????????']
        box_colors = [self.boxPlot1Line1Color, self.boxPlot1Line2Color, self.boxcol, self.boxcol2,
                      self.boxPlot2Line1Color, self.boxPlot2Line2Color, self.boxcol3, self.boxcol4,
                      self.boxPlot3Line1Color, self.boxPlot3Line2Color, self.boxCrclColor]
        for color in colors:
            for box in box_colors:
                box.addItem(color)

        self.boxPlot1Line1Color.setCurrentIndex(0)
        self.boxPlot1Line2Color.setCurrentIndex(1)
        self.boxPlot2Line2Color.setCurrentIndex(2)
        self.boxPlot3Line1Color.setCurrentIndex(3)
        self.boxPlot3Line2Color.setCurrentIndex(5)
        self.boxPlot2Line1Color.setCurrentIndex(4)
        self.boxCrclColor.setCurrentIndex(2)
        self.boxDates.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        ###############??????????????: ???????????????? ???????????? ######################
        self.labLimit1 = QLabel('?????????????? ??????????(N/E)', self)
        self.labLimit2 = QLabel('?????????????? ??????????(N/h)', self)
        self.labLimit3 = QLabel('?????????????? ??????????(h/E)', self)
        self.labLimit4 = QLabel('?????????????? ????????. ??????????????', self)
        self.labLimit5 = QLabel('?????????????? STA/LTA;???????????????????????? ??????????.', self)
        self.labLimit6 = QLabel('?????????????? ?????????????????????????????????? ??????????', self)

        self.tabLimits.layout.addWidget(self.labLimit1, 0, 0, 1, 4)
        self.tabLimits.layout.addWidget(self.labLimit2, 2, 0, 1, 4)
        self.tabLimits.layout.addWidget(self.labLimit3, 4, 0, 1, 4)
        self.tabLimits.layout.addWidget(self.labLimit4, 6, 0, 1, 4)
        self.tabLimits.layout.addWidget(self.labLimit5, 8, 0, 1, 4)
        self.tabLimits.layout.addWidget(self.labLimit6, 10, 0, 1, 4)

        self.boxLatMin1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMin1, 1, 0, 1, 1)
        self.boxLatMax1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMax1, 1, 1, 1, 1)
        self.boxLonMin1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMin1, 1, 2, 1, 1)
        self.boxLonMax1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMax1, 1, 3, 1, 1)
        self.boxLatMin2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMin2, 3, 0, 1, 1)
        self.boxLatMax2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMax2, 3, 1, 1, 1)
        self.boxLevMin1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLevMin1, 3, 2, 1, 1)
        self.boxLevMax1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLevMax1, 3, 3, 1, 1)
        self.boxLevMin2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLevMin2, 5, 0, 1, 1)
        self.boxLevMax2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLevMax2, 5, 1, 1, 1)
        self.boxLonMin2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMin2, 5, 2, 1, 1)
        self.boxLonMax2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMax2, 5, 3, 1, 1)

        self.boxDatesMinPlot1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMinPlot1, 7, 0, 1, 2)
        self.boxDatesMaxPlot1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMaxPlot1, 7, 2, 1, 2)
        self.boxDatesMinPlot2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMinPlot2, 9, 0, 1, 2)
        self.boxDatesMaxPlot2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMaxPlot2, 9, 2, 1, 2)
        self.boxLonMin3 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMin3, 11, 0, 1, 1)
        self.boxLonMax3 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMax3, 11, 1, 1, 1)
        self.boxLatMin3 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMin3, 11, 2, 1, 1)
        self.boxLatMax3 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMax3, 11, 3, 1, 1)

        ################### ??????????????: ?????????? #############################
        self.label_tab_data = QLabel('????????????:', self)
        self.tabData.layout.addWidget(self.label_tab_data, 0, 0, 1, 1)
        self.box_data_type = QComboBox(self)
        self.tabData.layout.addWidget(self.box_data_type, 0, 1, 1, 3)
        datas = ['??????????(N/E)', '??????????(N/h)', '??????????(E/h)', '??????????????????????', 'STA/LTA', '???????????????????????? ????????????????'
            , '????????????. ????????(????????????.dT)', '????????????. ????????(????????????.dTc)', '????????????. ????????(??????????????.dT)'
            , '????????????. ????????(dTc)']
        for i in datas:
            self.box_data_type.addItem(i)
        self.label_tab_data2 = QLabel('?????????????????? ??????: ', self)
        self.tabData.layout.addWidget(self.label_tab_data2, 1, 0, 1, 1)
        self.txtFileName = QLineEdit(self)
        self.txtFileName.setText('File1')
        self.tabData.layout.addWidget(self.txtFileName, 1, 1, 1, 1)
        self.box_file_type = QComboBox(self)
        self.box_file_type.addItem('.csv')
        self.tabData.layout.addWidget(self.box_file_type, 1, 2, 1, 1)
        self.btn_save_data = QPushButton('??????????????????', self)
        self.tabData.layout.addWidget(self.btn_save_data, 1, 3, 1, 1)
        # self.btn_save_data.clicked.connect(self.save_data)

        self.filedialog = QFileDialog()
        self.setGeometry(0, 0, 1300, 700)
        self.setWindowTitle('Algorithm')
        self.show()


    def download(self):
        boxes = [self.boxLat1, self.boxLatMax3, self.boxLatMin3, self.boxLat2, self.crcLat, self.boxLat3,
                 self.boxLatMin1, self.boxLatMin2,
                 self.boxLatMax1, self.boxLatMax2, self.boxLevel1, self.boxLevel2, self.boxLevMin1,
                 self.boxLevMin2, self.boxLevMax1, self.boxLevMax2, self.boxLon1, self.boxLon2, self.boxLon3,
                 self.crcLon, self.boxLonMax2, self.boxLonMax1, self.boxLonMax3, self.boxLonMin3, self.boxLonMin1,
                 self.boxLonMin2,
                 self.boxDates, self.boxDates2, self.boxDates3, self.boxDatesMaxPlot2, self.boxDatesMaxPlot1,
                 self.boxDatesMinPlot2, self.boxDatesMinPlot1,
                 self.boxcrcDate]
        for box in boxes:
            box.clear()
        self.level, self.latitude, self.longtitude, self.dates, self.tempArray = [], [], [], [], []
        import netCDF4 as nc
        a = self.filedialog.getOpenFileNames()[:-1]
        for i in a:
            for j in i:
                if j[-2:] == 'c4' or j[-2:] == 'nc':
                    ds = nc.Dataset(j)
                    temp = ds['T'][:]
                    if i.index(j) == 0:
                        self.level = list(ds['lev'][:])
                        self.latitude = list(ds['lat'][:])
                        self.longtitude = list(ds['lon'][:])
                        dates = list(ds['time'][:])
                    for m, k in enumerate(dates):
                        a = j.split('.')[2]
                        for boxdates in boxes[-8:]:
                            boxdates.addItem(a + '-' + str(int(k // 60)) + ':00:00')
                        self.dates.append(a + '-' + str(int(k // 60)) + ':00:00')
                        self.tempArray.append(temp[m][:][:][:])
                else:
                    continue
        for i in self.level:
            for boxlev in boxes[10:16]:
                boxlev.addItem(str(i))
        for j in self.latitude:
            for boxlat in boxes[0:10]:
                boxlat.addItem(str(j))
        for k in self.longtitude:
            for boxlon in boxes[16:26]:
                boxlon.addItem(str(k))
        self.boxDates.adjustSize()
        self.boxDates2.setCurrentIndex(0)
        boxes2 = [self.boxLatMax1, self.boxLatMax2, self.boxLonMax1, self.boxLonMax2, self.boxLevMax1,
                  self.boxLevMax2, self.boxDates3, self.boxDatesMaxPlot1, self.boxDatesMaxPlot2,
                  self.boxLatMax3, self.boxLonMax3]
        self.boxDatesMinPlot2.setCurrentIndex(int(self.textLTA.text()))
        for box in boxes2:
            box.setCurrentIndex(box.count() - 1)

        self.boxLevel1.setCurrentIndex(self.boxLevel1.count() - 6)
        self.boxLevel2.setCurrentIndex(self.boxLevel2.count() - 2)

    def oh_no(self):
        worker = Worker(self.download())

    @pyqtSlot()
    def dateMap(self):
        lev = float(self.boxLevel1.currentText())
        lev2 = float(self.boxLevel2.currentText())
        date = self.boxDates.currentText()
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())
        self.temp_matrix_c = []
        self.temp_matrix = []
        if lta > self.dates.index(date):
            return None

        for i, lat in enumerate(self.latitude):
            row = []
            row2 = []
            for j, lon in enumerate(self.longtitude):
                temp1LTA = []
                temp2LTA = []
                for k in self.tempArray[:self.dates.index(date) + 1][-lta:]:
                    temp1LTA.append(k[self.level.index(lev)][i][j])
                    temp2LTA.append(k[self.level.index(lev2)][i][j])
                temp1STA = temp1LTA[-sta:]
                temp2STA = temp2LTA[-sta:]
                lS1 = np.std(temp1STA) / np.std(temp1LTA)
                lS2 = np.std(temp2STA) / np.std(temp2LTA)
                r = np.corrcoef(temp1STA, temp2STA)[0][1]
                if r < 0:
                    result = (lS1 * lS2) * np.abs(r)
                else:
                    result = 0

                name = r'$\delta$' + 'T'
                result2 = lS1 * lS2
                row2.append(result2)
                row.append(result)
            self.temp_matrix_c.append(row)
            self.temp_matrix.append(row2)

        latMin = self.boxLatMin1.currentIndex()
        latMax = self.boxLatMax1.currentIndex()
        lonMin = self.boxLonMin1.currentIndex()
        lonMax = self.boxLonMax1.currentIndex()
        crclCol = self.boxCrclColor.currentText()
        crclSize = self.textCrclSize.text().replace(',', '.')
        self.colMap = self.cmapBox.currentText()
        colTop = float(self.top1.text().replace(',', '.'))
        colBot = float(self.bot1.text().replace(',', '.'))
        clat = self.latitude.index(float(self.crcLat.currentText()))
        clon = self.longtitude.index(float(self.crcLon.currentText()))
        self.chart4 = mapLonLat(self, self.longtitude,
                                self.latitude, self.temp_matrix_c, date, colTop, r'$\delta$' + 'Tc', clat, clon,
                                self.colMap,
                                colBot, crclCol,
                                crclSize, latMin, latMax, lonMin, lonMax)
        self.chart11 = mapLonLat(self, self.longtitude,
                                 self.latitude, self.temp_matrix, date, colTop, r'$\delta$' + 'T', clat, clon,
                                 self.colMap,
                                 colBot, crclCol,
                                 crclSize, latMin, latMax, lonMin, lonMax)
        self.tab1.layout.addWidget(self.chart4, 0, 0, 1, 1)
        self.toolbar = NavigationToolbar(self.chart4, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab1.layout.addWidget(self.toolbar, 1, 0, 1, 1)

        self.tab1.layout.addWidget(self.chart11, 0, 1, 1, 1)
        self.toolbar11 = NavigationToolbar(self.chart11, self)
        self.toolbar11.setOrientation(Qt.Horizontal)
        self.tab1.layout.addWidget(self.toolbar11, 1, 1, 1, 1)

    def oh_no2(self):
        worker2 = Worker(self.dateMap())

if __name__.endswith('__main__'):
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())