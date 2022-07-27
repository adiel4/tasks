import sys
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSlot, Qt, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog, QCheckBox, QGridLayout, QTabWidget, QApplication, QWidget, QLabel, \
    QPushButton, QMainWindow, QLineEdit, QComboBox, QToolTip
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.basemap import Basemap
from scipy.signal import find_peaks
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1 import make_axes_locatable
import xlwt
from xlwt import Workbook


class plotTemp(FigureCanvas):
    def __init__(self, parent, dates, lineOne, lineTwo, dateTicks, dateLabels, clr1, clr2, w1, w2, name1, name2, latOne,
                 lonOne, dateMin, dateMax):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=True, dpi=120)
        super().__init__(self.fig)
        self.setParent(parent)
        self.l1, = self.ax.plot(dates, lineOne, clr2[0] + '-', linewidth=w2)
        self.l2, = self.ax.plot(dates, lineTwo, clr1[0] + '-', linewidth=w1)
        self.ax.legend([name1 + ' hPa', name2 + ' hPa'], loc='best')
        self.ax.set(xlabel='Дата', ylabel='Температура, К',
                    title='Температура(' + str(lonOne) + '$^\circ$N  ' + str(latOne) + '$^\circ$E)')
        self.ax.set_xticks(dateTicks)
        self.ax.set_xticklabels(dateLabels)
        self.ax.grid()
        self.ax.set_xlim(dates[dateMin], dates[dateMax])

    def col(self, clr):
        self.ax.get_lines()[0].set_color(clr[0])

    def save4(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')

        # fig.tight_layout()


class plotdeltaT(FigureCanvas):
    def __init__(self, parent, dates, dataForPlot, dataForPlot2, dateTicks1, dateLabels1, clr1, clr2, w1, w2, f1, f2,
                 marc1, marc2, name1, name2, latOne, lonOne, dateMin, dateMax):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=True, dpi=120)
        super().__init__(self.fig)
        self.setParent(parent)
        indices, h = find_peaks(dataForPlot, distance=50, height=1)
        indices2, h2 = find_peaks(dataForPlot2, distance=50, height=1)
        self.l1 = self.ax.plot(dates, dataForPlot, clr1[0] + '-', linewidth=w1)
        self.ax.plot(dates, dataForPlot2, clr2[0] + '-', linewidth=w2)
        self.ax.legend([name1 + ' hPa', name2 + ' hPa'], loc='best')
        for m in range(len(indices)):
            # self.ax.text(indices[m], 0.1, dates[indices[m]][4:8])
            self.ax.plot(indices[m], h['peak_heights'][m], marc1[0] + f1[0])
        for n in range(len(indices2)):
            # self.ax.text(indices2[n], 0.2, dates[indices2[n]][4:8])
            self.ax.plot(indices2[n], h2['peak_heights']
            [n], marc2[0] + f2[0])
        self.ax.set(xlabel='Дата', ylabel='STA/LTA',
                    title='STA/LTA(' + str(lonOne) + '$^\circ$N   ' + str(latOne) + '$^\circ$E)')
        self.ax.set_xticks(dateTicks1)
        self.ax.set_xticklabels(dateLabels1)
        self.ax.grid()
        self.ax.set_xlim(dates[dateMin], dates[dateMax])
        # fig.tight_layout()

    def save5(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')

    def lineColor(self, color):

        pass


class plotdeltaTc(FigureCanvas):
    def __init__(self, parent, dates, dataForPlot, dataForPlot2, dateTicks1, dateLabels1, clr1, clr2, w1, w2, f1, f2,
                 mc1, mc2, latOne, lonOne, dateMin, dateMax):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=True, dpi=120)
        super().__init__(self.fig)
        self.setParent(parent)
        indices, h = find_peaks(dataForPlot, distance=50, height=1)
        indices2, h2 = find_peaks(dataForPlot2, distance=50, height=1)
        self.ax.plot(dates, dataForPlot, clr1[0] + '-', linewidth=w1)
        self.ax.plot(dates, dataForPlot2, clr2[0] + '-', linewidth=w2)
        self.ax.legend([r'$\delta$' + 'T', r'$\delta$' + 'Tc'], loc='best')
        for m in range(len(indices)):
            # self.ax.text(indices[m], 0.1, dates[indices[m]][4:8])
            self.ax.plot(indices[m], h['peak_heights'][m], mc1[0] + f1[0])
        for n in range(len(indices2)):
            # self.ax.text(indices2[n], 0.2, dates[indices2[n]][4:8])
            self.ax.plot(indices2[n], h2['peak_heights']
            [n], mc2[0] + f2[0])
        self.ax.set(xlabel='Дата', ylabel=r'$\delta$' + 'T',
                    title='Интегральный параметр(' + str(lonOne) + '$^\circ$N   ' + str(latOne) + '$^\circ$E)')
        self.ax.set_xticks(dateTicks1)
        self.ax.set_xticklabels(dateLabels1)
        self.ax.set_xlim(dates[dateMin], dates[dateMax])
        self.ax.grid()

    def save6(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')


class mapLonLat(FigureCanvas):
    def __init__(self, parent, long, lat, matrix, date, coltop, name, clat, clon, colMap, colBot, crclCol, crclSize,
                 latMinInd, latMaxInd, lonMinInd, lonMaxInd, clat2, clon2, crclCol2, crclSize2, lin_dr):
        plt.close('all')
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
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
        self.ax.set_title(date)
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.15)
        clb = self.fig.colorbar(ac, orientation='vertical', cax=cax)
        clb.ax.set_title(name)
        self.ax.set_xlabel('Долгота, E', labelpad=15)
        self.ax.set_ylabel('Широта, N', labelpad=20)
        coord = m(long[clon], lat[clat])
        self.ax.plot(coord[0], coord[1], color=crclCol[0], marker='*', markersize=float(crclSize[:-2]) * 10)
        if lin_dr:
            coord2 = m(long[clon2], lat[clat2])
            self.ax.plot(coord2[0], coord2[1], color=crclCol2[0], marker='*', markersize=float(crclSize2[:-2]) * 10)

        self.ax.grid(color='w', linewidth=0.1)

    def save1(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')

    def get_figure(self):
        return self.fig


class mapLevLat(FigureCanvas):
    def __init__(self, parent, level, lat, matrix, date, coltop, colMap, colbot, levMin, levMax, latMin,
                 latMax, lines_drawn, lat_epic, lines_drawn2, lat_epic2):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        plt.subplots_adjust(left=0.155, bottom=0.165, right=0.990, top=0.915)
        super().__init__(self.fig)
        self.setParent(parent)
        h_km = []
        for i in level:
            a = round(44.33 * (1 - (i / 1013.25) ** (1 / 5.255)), 2)
            h_km.append(a)
        highColor = round(coltop / 0.2)
        lowColor = round(colbot / 0.2)
        levels = [0.2 * x for x in range(lowColor, highColor + 1)]
        ac = self.ax.contourf(lat, h_km, matrix, levels, cmap=colMap)
        self.ax.set(title=date)
        x, y = [lat[lat_epic], lat[lat_epic]], [h_km[0], h_km[-1]]
        x2, y2 = [lat[lat_epic2], lat[lat_epic2]], [h_km[0], h_km[-1]]
        if lines_drawn:
            plt.plot(x, y, 'r')
        if lines_drawn2:
            plt.plot(x2, y2, 'b')
        clb = self.fig.colorbar(ac, orientation='vertical')
        self.ax.set_xlim(lat[latMin], lat[latMax])
        self.ax.set_ylim(h_km[levMin], h_km[levMax])
        clb.ax.set_title(r'$\delta$' + 'T', fontsize=8)
        self.ax.set(xlabel='Широта, N', ylabel='Высота,км')
        self.ax.grid(linewidth=0.1)

    def save2(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')

    def get_figure(self):
        return self.fig


class mapLevLon(FigureCanvas):
    def __init__(self, parent, lev, long, matrix, date, coltop, colMap, colbot, levMin, levMax, lonMin,
                 lonMax, lines_drawn, lon_epic, lines_drawn2, lon_epic2):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        plt.subplots_adjust(left=0.155, bottom=0.165, right=0.990, top=0.915)
        super().__init__(self.fig)
        self.setParent(parent)
        h_km = []
        for i in lev:
            a = round(44.33 * (1 - (i / 1013.25) ** (1 / 5.255)), 2)
            h_km.append(a)
        highColor = round(coltop / 0.2)
        lowColor = round(colbot / 0.2)
        levels = [0.2 * x for x in range(lowColor, highColor + 1)]
        ac = self.ax.contourf(long, h_km, matrix, levels, cmap=colMap)
        self.ax.set(title=date)
        x, y = [long[lon_epic], long[lon_epic]], [h_km[0], h_km[-1]]
        x2, y2 = [long[lon_epic2], long[lon_epic2]], [h_km[0], h_km[-1]]
        if lines_drawn:
            plt.plot(x, y, 'r')
        if lines_drawn2:
            plt.plot(x2, y2, 'b')
        clb = self.fig.colorbar(ac, orientation='vertical')
        self.ax.set_xlim(long[lonMin], long[lonMax])
        self.ax.set_ylim(h_km[levMin], h_km[levMax])
        clb.ax.set_title(r'$\delta$' + 'T', fontsize=10)
        self.ax.set(xlabel='Долгота, E', ylabel='Высота,км')
        self.ax.grid(linewidth=0.1)

    def save3(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')

    def get_figure(self):
        return self.fig


class plotLatLevDT(FigureCanvas):
    def __init__(self, parent, dtLat, dates, lat, colMap, name, epic_date, epic_lat, lines_drawn,
                 lat_min, lat_max, epic_date2, epic_lat2, lines_drawn2):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        plt.subplots_adjust(left=0.140, bottom=0.245, right=1, top=0.915)
        super().__init__(self.fig)
        self.setParent(parent)
        ac = self.ax.pcolormesh(dates, lat, dtLat, cmap=colMap)
        if lines_drawn:
            x1, y1 = [-0.5, len(dates) - 0.5], [lat[epic_lat] - 0.25, lat[epic_lat] - 0.25]
            x2, y2 = [epic_date - 0.5, epic_date - 0.5], [lat[0] - 0.25, lat[-1]]
            plt.plot(x1, y1, 'r')
            plt.plot(x2, y2, 'r')
        if lines_drawn2:
            x3, y3 = [-0.5, len(dates) - 0.5], [lat[epic_lat2] - 0.25, lat[epic_lat2] - 0.25]
            x4, y4 = [epic_date2 - 0.5, epic_date2 - 0.5], [lat[0] - 0.25, lat[-1]]
            plt.plot(x3, y3, 'b')
            plt.plot(x4, y4, 'b')
        self.ax.set(title='Срез по широте: ' + str(name) + '$^\circ$ E')
        self.ax.autoscale(True)
        self.ax.set_xticks(dates[0:-1:16])
        self.ax.set_xticklabels([xlabel[6:8] for xlabel in dates[0:-1:16]])
        clb = self.fig.colorbar(ac, orientation='vertical')
        clb.ax.set_title(r'$\delta$' + 'T')
        self.ax.set_ylim(lat[lat_min] - 0.25, lat[lat_max] + 0.25)
        self.ax.set(xlabel='Дата', ylabel='Широта')
        self.ax.grid(color='w', linewidth=0.1)

    def save7(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')


class plotLatLevDTc(FigureCanvas):
    def __init__(self, parent, dtLatc, dates, lat, colMap, name, epic_date, epic_lat, lines_drawn,
                 lat_min, lat_max, epic_date2, epic_lat2, lines_drawn2):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        plt.subplots_adjust(left=0.140, bottom=0.245, right=0.960, top=0.915)
        super().__init__(self.fig)
        self.setParent(parent)
        ac = self.ax.pcolormesh(dates, lat, dtLatc, cmap=colMap)
        if lines_drawn:
            x1, y1 = [-0.5, len(dates) - 0.5], [lat[epic_lat] - 0.25, lat[epic_lat] - 0.25]
            x2, y2 = [epic_date - 0.5, epic_date - 0.5], [lat[0] - 0.25, lat[-1]]
            plt.plot(x1, y1, 'r')
            plt.plot(x2, y2, 'r')
        if lines_drawn2:
            x3, y3 = [-0.5, len(dates) - 0.5], [lat[epic_lat2] - 0.25, lat[epic_lat2] - 0.25]
            x4, y4 = [epic_date2 - 0.5, epic_date2 - 0.5], [lat[0] - 0.25, lat[-1]]
            plt.plot(x3, y3, 'b')
            plt.plot(x4, y4, 'b')
        self.ax.set(title='Срез по широте: ' + str(name) + '$^\circ$ E')
        self.ax.autoscale(True)
        self.ax.set_xticks(dates[0:-1:16])
        self.ax.set_xticklabels([xlabel[6:8] for xlabel in dates[0:-1:16]])
        clb = self.fig.colorbar(ac, orientation='vertical')
        clb.ax.set_title(r'$\delta$' + 'Tc')
        self.ax.set_ylim(lat[lat_min] - 0.25, lat[lat_max] + 0.25)
        self.ax.set(xlabel='Дата', ylabel='Широта')
        self.ax.grid(linewidth=0.1)

    def save8(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')


class plotLonLevDT(FigureCanvas):
    def __init__(self, parent, dtLon, dates, lon, colMap, name, epic_date, epic_lon, lines_drawn,
                 lon_min, lon_max, epic_date2, epic_lon2, lines_drawn2):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        plt.subplots_adjust(left=0.140, bottom=0.245, right=1, top=0.915)
        super().__init__(self.fig)
        self.setParent(parent)
        ac = self.ax.pcolormesh(dates, lon, dtLon, cmap=colMap)
        if lines_drawn:
            x1, y1 = [-0.5, len(dates) - 0.5], [lon[epic_lon] - 0.6875, lon[epic_lon] - 0.6875]
            x2, y2 = [epic_date - 0.5, epic_date - 0.5], [lon[0], lon[-1] + 0.3125]
            plt.plot(x1, y1, 'r')
            plt.plot(x2, y2, 'r')
        if lines_drawn2:
            x3, y3 = [-0.5, len(dates) - 0.5], [lon[epic_lon2] - 0.6875, lon[epic_lon2] - 0.6875]
            x4, y4 = [epic_date2 - 0.5, epic_date2 - 0.5], [lon[0], lon[-1] + 0.3125]
            plt.plot(x3, y3, 'b')
            plt.plot(x4, y4, 'b')
        self.ax.set(title='Срез по долготе: ' + str(name) + '$^\circ$ N')
        self.ax.autoscale(True)
        self.ax.set_xticks(dates[0:-1:16])
        self.ax.set_xticklabels([xlabel[6:8] for xlabel in dates[0:-1:16]])
        clb = self.fig.colorbar(ac, orientation='vertical')
        clb.ax.set_title(r'$\delta$' + 'T')
        self.ax.set_ylim(lon[lon_min] - 0.3125, lon[lon_max] + 0.3125)
        self.ax.set(xlabel='Дата', ylabel='Долгота')
        self.ax.grid(linewidth=0.1)

    def save9(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')


class plotLonLevDTc(FigureCanvas):
    def __init__(self, parent, dtLonc, dates, lon, colMap, name, epic_date, epic_lon, lines_drawn,
                 lon_min, lon_max, epic_date2, epic_lon2, lines_drawn2):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        plt.subplots_adjust(left=0.140, bottom=0.245, right=0.960, top=0.915)
        super().__init__(self.fig)
        self.setParent(parent)
        ac = self.ax.pcolormesh(dates, lon, dtLonc, cmap=colMap)
        if lines_drawn:
            x1, y1 = [-0.5, len(dates) - 0.5], [lon[epic_lon] - 0.6875, lon[epic_lon] - 0.6875]
            x2, y2 = [epic_date - 0.5, epic_date - 0.5], [lon[0], lon[-1] + 0.3125]
            plt.plot(x1, y1, 'r')
            plt.plot(x2, y2, 'r')
        if lines_drawn2:
            x3, y3 = [-0.5, len(dates) - 0.5], [lon[epic_lon2] - 0.6875, lon[epic_lon2] - 0.6875]
            x4, y4 = [epic_date2 - 0.5, epic_date2 - 0.5], [lon[0], lon[-1] + 0.3125]
            plt.plot(x3, y3, 'b')
            plt.plot(x4, y4, 'b')
        self.ax.set(title='Срез по долготе: ' + str(name) + '$^\circ$ N')
        self.ax.autoscale(True)
        self.ax.set_xticks(dates[0:-1:16])
        self.ax.set_xticklabels([xlabel[6:8] for xlabel in dates[0:-1:16]])
        clb = self.fig.colorbar(ac, orientation='vertical')
        clb.ax.set_title(r'$\delta$' + 'Tc')
        self.ax.set_ylim(lon[lon_min] - 0.3125, lon[lon_max] + 0.3125)
        self.ax.set(xlabel='Дата', ylabel='Долгота')
        self.ax.grid(linewidth=0.1)

    def save10(self, name, dpi, docFormat):
        plt.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tempArray = []
        self.dates = []
        self.level = []
        self.longtitude = []
        self.latitude = []

        # self.pdf_map_lev_lon = PdfPages('C:/Users/User/Documents/FiguresEh.pdf')

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))

        ## СВОЙСТВА КНОПОК #############################

        self.btnDwnld = QPushButton('Загрузка', self)
        self.btnDwnld.move(40, 230)
        self.btnDwnld.resize(100, 30)
        self.btnDwnld.clicked.connect(self.download)
        self.btnMap = QPushButton('Карта', self)
        self.btnMap.move(150, 250)
        self.btnMap.resize(100, 20)
        self.btnMap.clicked.connect(self.dateMap)
        self.btnMap.clicked.connect(self.dateMap2)
        self.btnMap.clicked.connect(self.dateMap3)
        self.btnGraph = QPushButton('График', self)
        self.btnGraph.move(40, 270)
        self.btnGraph.resize(60, 30)
        self.btnGraph.clicked.connect(self.timePlot)
        self.btnPrevMap = QPushButton('<', self)
        self.btnPrevMap.move(150, 270)
        self.btnPrevMap.resize(30, 30)
        self.btnPrevMap.clicked.connect(self.PrevMap)
        self.btnPrevMap.clicked.connect(self.dateMap)
        self.btnPrevMap.clicked.connect(self.dateMap2)
        self.btnPrevMap.clicked.connect(self.dateMap3)
        self.btnNextMap = QPushButton('>', self)
        self.btnNextMap.move(180, 270)
        self.btnNextMap.resize(30, 30)
        self.btnNextMap.clicked.connect(self.NextMap)
        self.btnNextMap.clicked.connect(self.dateMap)
        self.btnNextMap.clicked.connect(self.dateMap2)
        self.btnNextMap.clicked.connect(self.dateMap3)

        #### СВОЙСТВА ТЕКСТОВ ####################
        self.labVys1 = QLabel('Высота(1), ГПа', self)
        self.labVys1.resize(self.labVys1.sizeHint())
        self.labVys1.move(40, 30)
        self.labVys2 = QLabel('Высота(2), ГПа', self)
        self.labVys2.resize(self.labVys2.sizeHint())
        self.labVys2.move(40, 60)
        self.labShir1 = QLabel('Широта(График)', self)
        self.labShir1.resize(self.labShir1.sizeHint())
        self.labShir1.move(40, 90)
        self.labDolg1 = QLabel('Долгота(График)', self)
        self.labDolg1.resize(self.labDolg1.sizeHint())
        self.labDolg1.move(40, 120)
        self.labShir2 = QLabel('Широта(Карта)', self)
        self.labShir2.resize(self.labShir2.sizeHint())
        self.labShir2.move(40, 150)
        self.labDolg2 = QLabel('Долгота(Карта)', self)
        self.labDolg2.resize(self.labDolg2.sizeHint())
        self.labDolg2.move(40, 180)
        self.labLTA = QLabel('LTA', self)
        self.labLTA.resize(70, 20)
        self.labLTA.move(250, 30)
        self.labSTA = QLabel('STA', self)
        self.labSTA.resize(70, 20)
        self.labSTA.move(250, 90)
        self.lab3hour = QLabel('Усреднение', self)
        self.lab3hour.resize(100, 20)
        self.lab3hour.move(250, 150)
        self.is3hour = QCheckBox(self)
        self.is3hour.move(250, 170)

        ########### СВОЙСТВА  ОКОН ДЛЯ ТЕКСТА ##############
        self.textLTA = QLineEdit(self)
        self.textLTA.move(250, 60)
        self.textLTA.setText('105')
        self.textLTA.resize(50, 20)
        self.textSTA = QLineEdit(self)
        self.textSTA.move(250, 120)
        self.textSTA.setText('21')
        self.textSTA.resize(50, 20)

        ################ СВОЙСТВА ТАБЛИЦ   #####################
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

        ############# ОСНОВНЫЕ СВОЙСТВА ОСНОВНЫХ ВКЛАДОК ###############

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

        self.tabs.addTab(self.tab1, "Карта(N/E)")
        self.tabs.addTab(self.tab4, "Профиль;STA/LTA")
        self.tabs.addTab(self.tab5, "Cрез(N/E)")
        self.tabs.addTab(self.tab6, 'Сохранение Графиков')

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

        ########### ВКЛАДКА: Срез() #################

        self.labDate = QLabel('Даты', self)
        self.tab5.layout.addWidget(self.labDate, 0, 0, 1, 1)
        self.boxDates2 = QComboBox(self)
        self.boxDates2.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tab5.layout.addWidget(self.boxDates2, 0, 1, 1, 4)
        self.boxDates3 = QComboBox(self)
        self.boxDates3.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tab5.layout.addWidget(self.boxDates3, 0, 5, 1, 4)
        self.lablat = QLabel('Широта', self)
        self.tab5.layout.addWidget(self.lablat, 0, 9, 1, 1)
        self.boxLat3 = QComboBox(self)
        self.tab5.layout.addWidget(self.boxLat3, 0, 10, 1, 1)
        self.lablon = QLabel('Долгота', self)
        self.tab5.layout.addWidget(self.lablon, 0, 11, 1, 1)
        self.boxLon3 = QComboBox(self)
        self.tab5.layout.addWidget(self.boxLon3, 0, 12, 1, 1)
        self.btnMap2 = QPushButton('График', self)
        self.tab5.layout.addWidget(self.btnMap2, 0, 13, 1, 2)
        self.btnMap2.clicked.connect(self.latlonMap)
        self.cmapBox2 = QComboBox(self)
        self.tab5.layout.addWidget(self.cmapBox2, 0, 15, 1, 2)

        ########### ВКЛАДКА: Сохранение графиков #################

        self.labSave1 = QLabel('Карта(N/E)', self)
        self.tab6.layout.addWidget(self.labSave1, 0, 0)
        self.textSave1 = QLineEdit(self)
        self.textSave1.setText('file1')
        self.tab6.layout.addWidget(self.textSave1, 0, 1)
        self.boxFormats1 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats1, 0, 2)
        self.textDPI = QLineEdit(self)
        self.textDPI.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI, 0, 3)
        self.btnSaveMap1 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap1, 0, 4)
        self.btnSaveMap1.clicked.connect(self.Save1)
        self.labSave2 = QLabel('Карта(N/h)', self)
        self.tab6.layout.addWidget(self.labSave2, 1, 0)
        self.textSave2 = QLineEdit(self)
        self.textSave2.setText('file2')
        self.tab6.layout.addWidget(self.textSave2, 1, 1)
        self.boxFormats2 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats2, 1, 2)
        self.textDPI2 = QLineEdit(self)
        self.textDPI2.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI2, 1, 3)
        self.btnSaveMap2 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap2, 1, 4)
        self.btnSaveMap2.clicked.connect(self.Save2)

        self.labSave3 = QLabel('Карта(E/h)', self)
        self.tab6.layout.addWidget(self.labSave3, 2, 0)
        self.textSave3 = QLineEdit(self)
        self.textSave3.setText('file3')
        self.tab6.layout.addWidget(self.textSave3, 2, 1)
        self.boxFormats3 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats3, 2, 2)
        self.textDPI3 = QLineEdit(self)
        self.textDPI3.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI3, 2, 3)
        self.btnSaveMap3 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap3, 2, 4)
        self.btnSaveMap3.clicked.connect(self.Save3)

        self.labSave4 = QLabel('Профиль', self)
        self.tab6.layout.addWidget(self.labSave4, 3, 0)
        self.textSave4 = QLineEdit(self)
        self.textSave4.setText('file4')
        self.tab6.layout.addWidget(self.textSave4, 3, 1)
        self.boxFormats4 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats4, 3, 2)
        self.textDPI4 = QLineEdit(self)
        self.textDPI4.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI4, 3, 3)
        self.btnSaveMap4 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap4, 3, 4)
        self.btnSaveMap4.clicked.connect(self.Save4)

        self.labSave5 = QLabel('STA/LTA профиль', self)
        self.tab6.layout.addWidget(self.labSave5, 4, 0)
        self.textSave5 = QLineEdit(self)
        self.textSave5.setText('file5')
        self.tab6.layout.addWidget(self.textSave5, 4, 1)
        self.boxFormats5 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats5, 4, 2)
        self.textDPI5 = QLineEdit(self)
        self.textDPI5.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI5, 4, 3)
        self.btnSaveMap5 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap5, 4, 4)
        self.btnSaveMap5.clicked.connect(self.Save5)

        self.labSave6 = QLabel('Интегральный профиль', self)
        self.tab6.layout.addWidget(self.labSave6, 5, 0)
        self.textSave6 = QLineEdit(self)
        self.textSave6.setText('file6')
        self.tab6.layout.addWidget(self.textSave6, 5, 1)
        self.boxFormats6 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats6, 5, 2)
        self.textDPI6 = QLineEdit(self)
        self.textDPI6.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI6, 5, 3)
        self.btnSaveMap6 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap6, 5, 4)
        self.btnSaveMap6.clicked.connect(self.Save6)

        self.labSave7 = QLabel('Срез по широте: dT', self)
        self.tab6.layout.addWidget(self.labSave7, 6, 0)
        self.textSave7 = QLineEdit(self)
        self.textSave7.setText('file7')
        self.tab6.layout.addWidget(self.textSave7, 6, 1)
        self.boxFormats7 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats7, 6, 2)
        self.textDPI7 = QLineEdit(self)
        self.textDPI7.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI7, 6, 3)
        self.btnSaveMap7 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap7, 6, 4)
        self.btnSaveMap7.clicked.connect(self.Save7)
        self.labSave8 = QLabel('Срез по широте: dT*c', self)
        self.tab6.layout.addWidget(self.labSave8, 7, 0)
        self.textSave8 = QLineEdit(self)
        self.textSave8.setText('file8')
        self.tab6.layout.addWidget(self.textSave8, 7, 1)
        self.boxFormats8 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats8, 7, 2)
        self.textDPI8 = QLineEdit(self)
        self.textDPI8.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI8, 7, 3)
        self.btnSaveMap8 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap8, 7, 4)
        self.btnSaveMap8.clicked.connect(self.Save8)
        self.labSave9 = QLabel('Срез по долготе: dT', self)
        self.tab6.layout.addWidget(self.labSave9, 8, 0)
        self.textSave9 = QLineEdit(self)
        self.textSave9.setText('file9')
        self.tab6.layout.addWidget(self.textSave9, 8, 1)
        self.boxFormats9 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats9, 8, 2)
        self.textDPI9 = QLineEdit(self)
        self.textDPI9.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI9, 8, 3)
        self.btnSaveMap9 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap9, 8, 4)
        self.btnSaveMap9.clicked.connect(self.Save9)
        self.labSave10 = QLabel('Срез по долготе: dT*c', self)
        self.tab6.layout.addWidget(self.labSave10, 9, 0)
        self.textSave10 = QLineEdit(self)
        self.textSave10.setText('file10')
        self.tab6.layout.addWidget(self.textSave10, 9, 1)
        self.boxFormats10 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats10, 9, 2)
        self.textDPI10 = QLineEdit(self)
        self.textDPI10.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI10, 9, 3)
        self.btnSaveMap10 = QPushButton('Сохранить', self)
        self.tab6.layout.addWidget(self.btnSaveMap10, 9, 4)
        self.btnSaveMap10.clicked.connect(self.Save10)

        imgFormats = ['.tiff', '.png', '.eps', '.jpeg', '.ps', '.raw', '.svg']

        box_formats = [self.boxFormats1, self.boxFormats2, self.boxFormats3, self.boxFormats4, self.boxFormats5,
                       self.boxFormats6, self.boxFormats7, self.boxFormats8, self.boxFormats9, self.boxFormats10]
        for form in imgFormats:
            for box in box_formats:
                box.addItem(form)

        ######## ОСНОВНЫЕ СВОЙСТВА ВКЛАДОК НАСТРОЙКИ ################

        self.tabsOptions = QTabWidget(self)
        self.tabsOptions.move(20, 300)
        self.tabsOptions.resize(300, 400)

        self.tab_line_options = QTabWidget(self)
        self.tab4.layout.addWidget(self.tab_line_options, 0, 1, 1, 1)

        self.tab_line_properties = QWidget(self)
        self.tab_line_markers = QWidget(self)
        self.tab_line_options.addTab(self.tab_line_markers, 'Маркеры')
        self.tab_line_options.addTab(self.tab_line_properties, 'Линии')
        self.tab_line_properties.layout = QGridLayout(self.tab_line_properties)
        self.tab_line_properties.setLayout(self.tab_line_properties.layout)
        self.tab_line_markers.layout = QGridLayout(self.tab_line_markers)
        self.tab_line_markers.setLayout(self.tab_line_markers.layout)

        self.tabMap = QWidget(self)
        self.tabLimits = QWidget(self)
        self.tabData = QWidget(self)

        self.tabsOptions.addTab(self.tabMap, 'Карта')
        self.tabsOptions.addTab(self.tabLimits, 'Границы')
        self.tabsOptions.addTab(self.tabData, 'Данные')

        self.tabMap.layout = QGridLayout(self.tabMap)
        self.tabMap.setLayout(self.tabMap.layout)
        self.tabLimits.layout = QGridLayout(self.tabLimits)
        self.tabLimits.setLayout(self.tabLimits.layout)
        self.tabData.layout = QGridLayout(self.tabData)
        self.tabData.setLayout(self.tabData.layout)
        ############### Вкладка: Свойства линий #####################

        self.labPlot1Wid = QLabel('Толщина и цвета линий:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot1Wid, 0, 0)
        self.labPlot2Wid = QLabel('Толщина и цвета линий:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot2Wid, 3, 0)
        self.labPlot3Wid = QLabel('Толщина и цвета линий:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot3Wid, 6, 0)
        self.labPlot1Col = QLabel('Температурный профиль', self)
        self.tab_line_properties.layout.addWidget(self.labPlot1Col, 0, 3)
        self.labPlot2Col = QLabel('STA/LTA профиль', self)
        self.tab_line_properties.layout.addWidget(self.labPlot2Col, 3, 3)
        self.labPlot3Col = QLabel('Интегральный профиль', self)
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

        ############### Вкладка: Свойства маркеров #####################
        self.labMark = QLabel('Размеры маркеров STA/LTA', self)
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
        self.labMark2 = QLabel('Форма маркеров STA/LTA', self)
        self.tab_line_markers.layout.addWidget(self.labMark2, 2, 0, 1, 4)
        self.tab_line_markers.layout.addWidget(self.markW2, 1, 2)
        self.boxMark = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxMark, 3, 0, 1, 2)
        self.boxMark2 = QComboBox(self)
        self.tab_line_markers.layout.addWidget(self.boxMark2, 3, 2, 1, 2)
        self.labMark3 = QLabel('Размеры маркеров интег. проф.', self)
        self.tab_line_markers.layout.addWidget(self.labMark3, 4, 0, 1, 4)
        self.markW3 = QLineEdit(self)
        self.markW3.setText('1')
        self.tab_line_markers.layout.addWidget(self.markW3, 5, 0)
        self.markW4 = QLineEdit(self)
        self.markW4.setText('1')
        self.tab_line_markers.layout.addWidget(self.markW4, 5, 2)
        self.labMark3 = QLabel('Форма маркеров интег. проф.', self)
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
            ' Нет маркеров',
            '.-точка',
            'o-окружность',
            ',-пиксель',
            'v',
            '^',
            '>',
            '<',
            's-квадрат',
            'p-пятиуг.',
            '*-звезда',
            'h-шестиуг.',
            '+',
            'x',
            'd-ромб',
        ]
        for i in markForm:
            self.boxMark.addItem(i)
            self.boxMark2.addItem(i)
            self.boxMark3.addItem(i)
            self.boxMark4.addItem(i)

        ########### Вкладка: Свойства Карты ##############
        self.labisC = QLabel('Коэффициент корреляции', self)
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
        self.labGr = QLabel('Верх. и нижн. граница', self)
        self.tabMap.layout.addWidget(self.labGr, 1, 0, 1, 2)
        self.top1 = QLineEdit(self)
        self.top1.setText('1.5')
        self.tabMap.layout.addWidget(self.top1, 2, 0, 1, 1)
        self.labGr4 = QLabel('Карта(N/E)', self)
        self.tabMap.layout.addWidget(self.labGr4, 1, 2, 1, 3)
        self.bot1 = QLineEdit(self)
        self.bot1.setText('-0.2')
        self.tabMap.layout.addWidget(self.bot1, 2, 2, 1, 1)
        self.labGr2 = QLabel('Верх. и нижн. граница', self)
        self.tabMap.layout.addWidget(self.labGr2, 3, 0, 1, 2)
        self.top2 = QLineEdit(self)
        self.top2.setText('1.8')
        self.tabMap.layout.addWidget(self.top2, 4, 0, 1, 1)
        self.labGr5 = QLabel('Карта(N/h)', self)
        self.tabMap.layout.addWidget(self.labGr5, 3, 2, 1, 3)
        self.bot2 = QLineEdit(self)
        self.bot2.setText('-0.2')
        self.tabMap.layout.addWidget(self.bot2, 4, 2, 1, 1)
        self.labGr3 = QLabel('Верх. и нижн. граница', self)
        self.tabMap.layout.addWidget(self.labGr3, 5, 0, 1, 2)
        self.top3 = QLineEdit(self)
        self.top3.setText('1.8')
        self.tabMap.layout.addWidget(self.top3, 6, 0, 1, 1)
        self.labGr6 = QLabel('Карта(E/h)', self)
        self.tabMap.layout.addWidget(self.labGr6, 5, 2, 1, 3)
        self.bot3 = QLineEdit(self)
        self.bot3.setText('-0.2')
        self.tabMap.layout.addWidget(self.bot3, 6, 2, 1, 1)
        self.crclLabel = QLabel('Эпицентр', self)
        self.crclLabelLon = QLabel('Долгота', self)
        self.crclLabelLat = QLabel('Широта', self)
        self.tabMap.layout.addWidget(self.crclLabelLat, 9, 0)
        self.tabMap.layout.addWidget(self.crclLabelLon, 9, 2)
        self.tabMap.layout.addWidget(self.crclLabel, 8, 0)
        self.crcLat = QComboBox(self)
        self.tabMap.layout.addWidget(self.crcLat, 9, 1)
        self.crcLon = QComboBox(self)
        self.tabMap.layout.addWidget(self.crcLon, 9, 3, 1, 2)
        self.boxcrcDate = QComboBox(self)
        self.tabMap.layout.addWidget(self.boxcrcDate, 8, 1, 1, 2)
        self.crclLabelColor = QLabel('Цвет', self)
        self.tabMap.layout.addWidget(self.crclLabelColor, 10, 0)
        self.crclLabelSize = QLabel('Размер', self)
        self.tabMap.layout.addWidget(self.crclLabelSize, 10, 2)
        self.boxCrclColor = QComboBox(self)
        self.tabMap.layout.addWidget(self.boxCrclColor, 10, 1)
        self.textCrclSize = QLineEdit(self)
        self.textCrclSize.setText('1 см')
        self.tabMap.layout.addWidget(self.textCrclSize, 10, 3)
        self.check_epic = QCheckBox(self)
        self.tabMap.layout.addWidget(self.check_epic, 8, 3)

        self.crclLabel2 = QLabel('Эпицентр', self)
        self.crclLabelLon2 = QLabel('Долгота', self)
        self.crclLabelLat2 = QLabel('Широта', self)
        self.tabMap.layout.addWidget(self.crclLabelLat2, 12, 0)
        self.tabMap.layout.addWidget(self.crclLabelLon2, 12, 2)
        self.tabMap.layout.addWidget(self.crclLabel2, 11, 0)
        self.crcLat2 = QComboBox(self)
        self.tabMap.layout.addWidget(self.crcLat2, 12, 1)
        self.crcLon2 = QComboBox(self)
        self.tabMap.layout.addWidget(self.crcLon2, 12, 3, 1, 2)
        self.boxcrcDate2 = QComboBox(self)
        self.tabMap.layout.addWidget(self.boxcrcDate2, 11, 1, 1, 2)
        self.crclLabelColor2 = QLabel('Цвет', self)
        self.tabMap.layout.addWidget(self.crclLabelColor2, 13, 0)
        self.crclLabelSize2 = QLabel('Размер', self)
        self.tabMap.layout.addWidget(self.crclLabelSize2, 13, 2)
        self.boxCrclColor2 = QComboBox(self)
        self.tabMap.layout.addWidget(self.boxCrclColor2, 13, 1)
        self.textCrclSize2 = QLineEdit(self)
        self.textCrclSize2.setText('1 см')
        self.tabMap.layout.addWidget(self.textCrclSize2, 13, 3)
        self.check_epic2 = QCheckBox(self)
        self.tabMap.layout.addWidget(self.check_epic2, 11, 3)

        colors = ['b-синий', 'g-зеленый', 'r-красный', 'c-голубой', 'm-фиолетовый', 'y-желтый', 'k-черный']
        box_colors = [self.boxPlot1Line1Color, self.boxPlot1Line2Color, self.boxcol, self.boxcol2,
                      self.boxPlot2Line1Color, self.boxPlot2Line2Color, self.boxcol3, self.boxcol4,
                      self.boxPlot3Line1Color, self.boxPlot3Line2Color, self.boxCrclColor, self.boxCrclColor2]
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

        ###############Вкладка: Свойства границ ######################
        self.labLimit1 = QLabel('Границы карты(N/E)', self)
        self.labLimit2 = QLabel('Границы карты(N/h)', self)
        self.labLimit3 = QLabel('Границы карты(h/E)', self)
        self.labLimit4 = QLabel('Границы Темп. профиля', self)
        self.labLimit5 = QLabel('Границы STA/LTA;Интегральный парам.', self)
        self.labLimit6 = QLabel('Границы Пространственного среза', self)

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

        ################### Вкладка: Данные #############################
        self.label_tab_data = QLabel('Данные:', self)
        self.tabData.layout.addWidget(self.label_tab_data, 0, 0, 1, 1)
        self.box_data_type = QComboBox(self)
        self.tabData.layout.addWidget(self.box_data_type, 0, 1, 1, 3)
        datas = ['Карта', "Профиль;STA/LTA", "Срез"]
        for i in datas:
            self.box_data_type.addItem(i)
        self.label_tab_data2 = QLabel('Сохранить как: ', self)
        self.tabData.layout.addWidget(self.label_tab_data2, 1, 0, 1, 1)
        self.txtFileName = QLineEdit(self)
        self.txtFileName.setText('File1')
        self.tabData.layout.addWidget(self.txtFileName, 1, 1, 1, 1)
        self.box_file_type = QComboBox(self)
        self.box_file_type.addItem('.xls')
        self.tabData.layout.addWidget(self.box_file_type, 1, 2, 1, 1)
        self.btn_save_data = QPushButton('Сохранить', self)
        self.tabData.layout.addWidget(self.btn_save_data, 1, 3, 1, 1)
        self.btn_save_data.clicked.connect(self.save_data)

        self.box_date1 = QComboBox(self)
        self.tabData.layout.addWidget(self.box_date1, 2, 0, 1, 2)
        self.box_date2 = QComboBox(self)
        self.tabData.layout.addWidget(self.box_date2, 2, 2, 1, 2)
        self.btnPdfMaker = QPushButton('Сохранить PDF', self)
        self.tabData.layout.addWidget(self.btnPdfMaker, 3, 0, 1, 2)
        # self.btnPdfMaker.clicked.connect(self.pdf_maker)

        self.filedialog = QFileDialog()
        self.setGeometry(0, 0, 1300, 700)
        self.setWindowTitle('Algorithm')
        self.show()

    @pyqtSlot()
    def download(self):
        boxes = [self.boxLat1, self.boxLatMax3, self.boxLatMin3, self.boxLat2, self.crcLat, self.boxLat3,
                 self.boxLatMin1, self.boxLatMin2,
                 self.boxLatMax1, self.boxLatMax2, self.crcLat2, self.boxLevel1, self.boxLevel2, self.boxLevMin1,
                 self.boxLevMin2, self.boxLevMax1, self.boxLevMax2, self.boxLon1, self.boxLon2, self.boxLon3,
                 self.crcLon, self.boxLonMax2, self.boxLonMax1, self.boxLonMax3, self.boxLonMin3, self.boxLonMin1,
                 self.boxLonMin2, self.crcLon2,
                 self.boxDates, self.boxDates2, self.boxDates3, self.boxDatesMaxPlot2, self.boxDatesMaxPlot1,
                 self.boxDatesMinPlot2, self.boxDatesMinPlot1,
                 self.boxcrcDate, self.box_date2, self.box_date1, self.boxcrcDate2]
        for box in boxes:
            box.clear()
        self.level, self.latitude, self.longtitude, self.dates, self.tempArray = [], [], [], [], []
        from netCDF4 import Dataset
        a = self.filedialog.getOpenFileNames()[:-1]
        for i in a:
            for j in i:
                if j[-2:] == 'c4' or j[-2:] == 'nc':
                    ds = Dataset(j)
                    temp = ds['T'][:]
                    if i.index(j) == 0:
                        self.level = list(ds['lev'][:])
                        self.latitude = list(ds['lat'][:])
                        self.longtitude = list(ds['lon'][:])
                        dates = list(ds['time'][:])
                    for m, k in enumerate(dates):
                        a = j.split('.')[2]
                        for boxdates in boxes[-11:]:
                            boxdates.addItem(a + '-' + str(int(k // 60)) + ':00:00')
                        self.dates.append(a + '-' + str(int(k // 60)) + ':00:00')
                        self.tempArray.append(tuple(temp[m][:][:][:]))
                else:
                    continue
        self.tempArray = tuple(self.tempArray)
        for i in self.level:
            for boxlev in boxes[11:17]:
                boxlev.addItem(str(i))
        for j in self.latitude:
            for boxlat in boxes[0:11]:
                boxlat.addItem(str(j))
        for k in self.longtitude:
            for boxlon in boxes[17:28]:
                boxlon.addItem(str(k))
        self.boxDates.adjustSize()
        self.boxDates2.setCurrentIndex(0)
        boxes2 = [self.boxLatMax1, self.boxLatMax2, self.boxLonMax1, self.boxLonMax2, self.boxLevMax1,
                  self.boxLevMax2, self.boxDates3, self.boxDatesMaxPlot1, self.boxDatesMaxPlot2,
                  self.boxLatMax3, self.boxLonMax3, self.box_date2]
        self.boxDatesMinPlot2.setCurrentIndex(int(self.textLTA.text()))
        for box in boxes2:
            box.setCurrentIndex(box.count() - 1)

        self.boxLevel1.setCurrentIndex(self.boxLevel1.count() - 6)
        self.boxLevel2.setCurrentIndex(self.boxLevel2.count() - 2)

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
        crclCol2 = self.boxCrclColor2.currentText()
        crclSize2 = self.textCrclSize2.text().replace(',', '.')
        clat2 = self.latitude.index(float(self.crcLat2.currentText()))
        clon2 = self.longtitude.index(float(self.crcLon2.currentText()))
        lines_drawn = self.check_epic2.isChecked()
        if self.is3hour.isChecked():
            for i in range(len(self.latitude) - 1):
                for j in range(len(self.longtitude) - 1):
                    if i in [0, self.boxLat1.count()] or j in [0, self.boxLon1.count()]:
                        continue
                    else:
                        self.temp_matrix_c[i][j] = np.mean([
                            self.temp_matrix_c[i - 1][j - 1], self.temp_matrix_c[i - 1][j],
                            self.temp_matrix_c[i - 1][j + 1],
                            self.temp_matrix_c[i][j - 1], self.temp_matrix_c[i][j], self.temp_matrix_c[i][j],
                            self.temp_matrix_c[i + 1][j - 1], self.temp_matrix_c[i + 1][j],
                            self.temp_matrix_c[i + 1][j + 1]
                        ])
                        self.temp_matrix[i][j] = np.mean([
                            self.temp_matrix[i - 1][j - 1], self.temp_matrix[i - 1][j],
                            self.temp_matrix[i - 1][j + 1],
                            self.temp_matrix[i][j - 1], self.temp_matrix[i][j], self.temp_matrix[i][j],
                            self.temp_matrix[i + 1][j - 1], self.temp_matrix[i + 1][j],
                            self.temp_matrix[i + 1][j + 1]
                        ])

        for i in range(len(self.latitude) - 1):
            tuple(self.temp_matrix[i])
            tuple(self.temp_matrix_c[i])
        self.temp_matrix = tuple(self.temp_matrix)
        self.temp_matrix_c = tuple(self.temp_matrix_c)
        self.chart4 = mapLonLat(self, self.longtitude,
                                self.latitude, self.temp_matrix_c, date, colTop, r'$\delta$' + 'Tc', clat, clon,
                                self.colMap,
                                colBot, crclCol,
                                crclSize, latMin, latMax, lonMin, lonMax,
                                clat2, clon2, crclCol2, crclSize2, lines_drawn)
        self.chart11 = mapLonLat(self, self.longtitude,
                                 self.latitude, self.temp_matrix, date, colTop, r'$\delta$' + 'T', clat, clon,
                                 self.colMap,
                                 colBot, crclCol,
                                 crclSize, latMin, latMax, lonMin, lonMax,
                                 clat2, clon2, crclCol2, crclSize2, lines_drawn)
        self.tab1.layout.addWidget(self.chart4, 0, 0, 1, 1)
        self.toolbar = NavigationToolbar(self.chart4, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab1.layout.addWidget(self.toolbar, 1, 0, 1, 1)

        self.tab1.layout.addWidget(self.chart11, 0, 1, 1, 1)
        self.toolbar11 = NavigationToolbar(self.chart11, self)
        self.toolbar11.setOrientation(Qt.Horizontal)
        self.tab1.layout.addWidget(self.toolbar11, 1, 1, 1, 1)

    @pyqtSlot()
    def dateMap2(self):
        date = self.boxDates.currentText()
        lattit = float(self.boxLon2.currentText())
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())

        if lta > self.dates.index(date):
            return None

        self.lev_lat_matrix = []
        for i, lev in enumerate(self.level):
            row = []
            for j, lat in enumerate(self.latitude):
                tempLTA = []
                for k in self.tempArray[:self.dates.index(date) + 1][-lta:]:
                    tempLTA.append(k[i][j][self.longtitude.index(lattit)])
                tempSTA = tempLTA[-sta:]
                lS = np.std(tempSTA) / np.std(tempLTA)
                row.append(lS)
            self.lev_lat_matrix.append(row)

        if self.is3hour.isChecked():
            for i in range(len(self.level) - 1):
                for j in range(len(self.latitude) - 1):
                    if i in [0, self.boxLevel2.count()] or j in [0, self.boxLat1.count()]:
                        continue
                    else:
                        self.lev_lat_matrix[i][j] = np.mean([
                            self.lev_lat_matrix[i - 1][j - 1], self.lev_lat_matrix[i - 1][j],
                            self.lev_lat_matrix[i - 1][j + 1],
                            self.lev_lat_matrix[i][j - 1], self.lev_lat_matrix[i][j], self.lev_lat_matrix[i][j + 1],
                            self.lev_lat_matrix[i + 1][j - 1], self.lev_lat_matrix[i + 1][j],
                            self.lev_lat_matrix[i + 1][j + 1]
                        ])
        for i in range(len(self.level) - 1):
            tuple(self.lev_lat_matrix[i])
        self.lev_lat_matrix = tuple(self.lev_lat_matrix)
        levMin = self.boxLevMin1.currentIndex()
        levMax = self.boxLevMax1.currentIndex()
        latMin = self.boxLatMin2.currentIndex()
        latMax = self.boxLatMax2.currentIndex()
        coltop = float(self.top2.text().replace(',', '.'))
        colBot = float(self.bot2.text().replace(',', '.'))
        lines_drawn = self.check_epic.isChecked()
        lat_epic = self.crcLat.currentIndex()
        lines_drawn2 = self.check_epic2.isChecked()
        lat_epic2 = self.crcLat2.currentIndex()

        self.chart5 = mapLevLat(self, self.level,
                                self.latitude, self.lev_lat_matrix, date, coltop, self.colMap, colBot, levMin, levMax,
                                latMin,
                                latMax, lines_drawn, lat_epic, lines_drawn2, lat_epic2)
        self.tab1.layout.addWidget(self.chart5, 2, 1, 1, 1)
        self.toolbar = NavigationToolbar(self.chart5, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab1.layout.addWidget(self.toolbar, 3, 1, 1, 1)

    @pyqtSlot()
    def dateMap3(self):
        date = self.boxDates.currentText()
        long = float(self.boxLat2.currentText())
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())

        if lta > self.dates.index(date):
            return None
        self.lev_lon_matrix = []
        for i, lev in enumerate(self.level):
            row = []
            for j, lon in enumerate(self.longtitude):
                tempLTA = []
                for k in self.tempArray[:self.dates.index(date) + 1][-lta:]:
                    tempLTA.append(k[i][self.latitude.index(long)][j])
                tempSTA = tempLTA[-sta:]
                lS = np.std(tempSTA) / np.std(tempLTA)
                row.append(lS)
            self.lev_lon_matrix.append(row)

        if self.is3hour.isChecked():
            for i in range(len(self.level) - 1):
                for j in range(len(self.longtitude) - 1):
                    if i in [0, self.boxLevel2.count()] or j in [0, self.boxLon1.count()]:
                        continue
                    else:
                        self.lev_lon_matrix[i][j] = np.mean([
                            self.lev_lon_matrix[i - 1][j - 1], self.lev_lon_matrix[i - 1][j],
                            self.lev_lon_matrix[i - 1][j + 1],
                            self.lev_lon_matrix[i][j - 1], self.lev_lon_matrix[i][j], self.lev_lon_matrix[i][j + 1],
                            self.lev_lon_matrix[i + 1][j - 1], self.lev_lon_matrix[i + 1][j],
                            self.lev_lon_matrix[i + 1][j + 1]

                        ])
        levMin = self.boxLevMin2.currentIndex()
        levMax = self.boxLevMax2.currentIndex()
        lonMin = self.boxLonMin2.currentIndex()
        lonMax = self.boxLonMax2.currentIndex()
        coltop = float(self.top3.text().replace(',', '.'))
        colbot = float(self.bot3.text().replace(',', '.'))
        lines_drawn = self.check_epic.isChecked()
        lon_epic = self.crcLon.currentIndex()
        lines_drawn2 = self.check_epic2.isChecked()
        lon_epic2 = self.crcLon2.currentIndex()
        for i in range(len(self.level) - 1):
            tuple(self.lev_lon_matrix[i])
        self.lev_lon_matrix = tuple(self.lev_lon_matrix)
        self.chart6 = mapLevLon(self, self.level,
                                self.longtitude, self.lev_lon_matrix, date, coltop, self.colMap, colbot, levMin, levMax,
                                lonMin,
                                lonMax, lines_drawn, lon_epic, lines_drawn2, lon_epic2)
        self.tab1.layout.addWidget(self.chart6, 2, 0)
        self.toolbar = NavigationToolbar(self.chart6, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab1.layout.addWidget(self.toolbar, 3, 0)

    def save_pdf(self):
        from matplotlib.backends.backend_pdf import PdfPages

        figures = [self.chart4.get_figure(), self.chart11.get_figure(), self.chart5.get_figure(),
                   self.chart6.get_figure()]
        pdf1, pdf2, pdf3, pdf4 = PdfPages('Карта(dTc)(N/E).pdf'), PdfPages('Карта(dT)(N/E).pdf'), PdfPages(
            'Карта(dT)(N/h).pdf'), PdfPages('Карта(dT)(E/h).pdf')
        pdfs = [pdf1, pdf2, pdf3, pdf4]
        for i in range(len(figures)):
            pdfs[i].savefig(figures[i])
            pdfs[i].close()
        print(figures)
        pass

    @pyqtSlot()
    def NextMap(self):
        ind = self.boxDates.currentIndex()
        self.boxDates.setCurrentIndex(ind + 1)

    @pyqtSlot()
    def PrevMap(self):
        ind = self.boxDates.currentIndex()
        self.boxDates.setCurrentIndex(ind - 1)

    @pyqtSlot()
    def timePlot(self):
        if self.boxLevel1.currentText() == '':
            return None
        levOne = float(self.boxLevel1.currentText())
        levTwo = float(self.boxLevel2.currentText())
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())
        latOne = float(self.boxLat1.currentText())
        lonOne = float(self.boxLon1.currentText())

        self.tempLevOneCoorOne = []
        self.tempLevOneCoorTwo = []

        for k in self.tempArray:
            self.tempLevOneCoorOne.append(
                k[self.level.index(levOne)][self.latitude.index(latOne)][self.longtitude.index(lonOne)])
            self.tempLevOneCoorTwo.append(
                k[self.level.index(levTwo)][self.latitude.index(latOne)][self.longtitude.index(lonOne)])
        dateTicks = self.dates[0:-1:50]
        dateLabels = []
        for i in dateTicks:
            dateLabels.append(i[6:8])
        width1 = float(self.textPlot1Line2Width.text().replace(',', '.'))
        width2 = float(self.textPlot1Line1Width.text().replace(',', '.'))
        clr1 = self.boxPlot1Line2Color.currentText()
        clr2 = self.boxPlot1Line1Color.currentText()

        name1 = self.boxLevel1.currentText()
        name2 = self.boxLevel2.currentText()
        dateMin1 = self.boxDatesMinPlot1.currentIndex()
        dateMax1 = self.boxDatesMaxPlot1.currentIndex()
        self.chart = plotTemp(self, self.dates, self.tempLevOneCoorOne, self.tempLevOneCoorTwo, dateTicks, dateLabels,
                              clr1, clr2, width1, width2, name1, name2, latOne, lonOne, dateMin1, dateMax1)
        self.tab4.layout.addWidget(self.chart, 0, 0, 1, 1)
        self.toolbar = NavigationToolbar(self.chart, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab4.layout.addWidget(self.toolbar, 1, 0, 1, 1)

        self.arrayLev1 = []
        self.arrayLev2 = []
        self.integArray = []
        self.integArraywR = []

        for i in range(lta, len(self.tempLevOneCoorTwo)):
            index1 = i - lta
            index2 = i + 1
            lTA = np.std(self.tempLevOneCoorTwo[index1:index2])
            sTA = np.std(self.tempLevOneCoorTwo[:i][-sta:])
            lTA2 = np.std(self.tempLevOneCoorOne[index1:index2])
            sTA2 = np.std(self.tempLevOneCoorOne[:i][-sta:])
            stalta = sTA / lTA
            stalta2 = sTA2 / lTA2
            self.arrayLev1.append(stalta)
            self.arrayLev2.append(stalta2)
            self.integArray.append(stalta * stalta2)
            coef = np.corrcoef(self.tempLevOneCoorTwo[:i][-sta:], self.tempLevOneCoorOne[:i][-sta:])[0][1]

            if stalta * stalta2 * coef >= 0:
                result = 0
                self.integArraywR.append(result)
            else:
                result = stalta * stalta2 * np.abs(coef)
                self.integArraywR.append(result)

        dateTicks = self.dates[lta:][0:-1:50]
        dateLabels = []
        for i in dateTicks:
            dateLabels.append(i[6:8])

        clr1 = self.boxPlot2Line1Color.currentText()
        clr2 = self.boxPlot2Line2Color.currentText()
        clr3 = self.boxPlot3Line1Color.currentText()
        clr4 = self.boxPlot3Line2Color.currentText()

        width1 = float(self.textPlot2Line1Width.text().replace(',', '.'))
        width2 = float(self.textPlot2Line2Width.text().replace(',', '.'))
        width3 = float(self.textPlot3Line1Width.text().replace(',', '.'))
        width4 = float(self.textPlot3Line2Width.text().replace(',', '.'))

        form1, form2 = self.boxMark.currentText(), self.boxMark2.currentText()
        form3, form4 = self.boxMark3.currentText(), self.boxMark4.currentText()
        marCol1, marCol2 = self.boxcol.currentText(), self.boxcol2.currentText()
        marCol3, marCol4 = self.boxcol3.currentText(), self.boxcol4.currentText()
        start = int(self.textLTA.text())
        if self.boxDatesMinPlot2.currentIndex() > lta:
            dateMin2 = self.boxDatesMinPlot2.currentIndex() - lta
        else:
            dateMin2 = 0
        dateMax2 = self.boxDatesMaxPlot2.currentIndex() - start
        self.chart2 = plotdeltaT(
            self, self.dates[lta:], self.arrayLev1, self.arrayLev2, dateTicks, dateLabels, clr1, clr2, width1, width2,
            form1,
            form2, marCol1, marCol2, name1, name2, latOne, lonOne, dateMin2, dateMax2)

        self.toolbar2 = NavigationToolbar(self.chart2, self)
        self.toolbar2.setOrientation(Qt.Horizontal)

        self.chart3 = plotdeltaTc(
            self, self.dates[lta:], self.integArray, self.integArraywR, dateTicks, dateLabels, clr3, clr4, width3,
            width4, form3,
            form4, marCol3, marCol4, latOne, lonOne, dateMin2, dateMax2)
        self.toolbar3 = NavigationToolbar(self.chart3, self)
        self.toolbar3.setOrientation(Qt.Horizontal)

        self.tab4.layout.addWidget(self.chart2, 2, 0, 1, 1)
        self.tab4.layout.addWidget(self.toolbar2, 3, 0, 1, 1)
        self.tab4.layout.addWidget(self.chart3, 2, 1, 1, 1)
        self.tab4.layout.addWidget(self.toolbar3, 3, 1, 1, 1)

    def latlonMap(self):
        index1, index2 = self.boxDates2.currentIndex(), self.boxDates3.currentIndex()
        lta, sta = int(self.textLTA.text()), int(self.textSTA.text())
        latitude, longtitude = self.boxLat3.currentIndex(), self.boxLon3.currentIndex()
        self.latdT, self.londT, self.latdTc, self.londTc = [], [], [], []
        if index1 < lta:
            return
        levOne = self.boxLevel1.currentIndex()
        levTwo = self.boxLevel2.currentIndex()
        for i, lat in enumerate(self.latitude):
            rowdT1 = []
            rowdTc1 = []
            for k in range(index1, index2 + 1, 1):
                array1 = []
                array3 = []
                for temp1 in self.tempArray[:k][-lta:]:
                    a = temp1[levOne][i][longtitude]
                    b = temp1[levTwo][i][longtitude]
                    array1.append(a)
                    array3.append(b)
                ltalat = np.std(array1)
                stalat = np.std(array1[-sta:])
                ltalat2 = np.std(array3)
                stalat2 = np.std(array3[-sta:])
                coef = np.corrcoef(array1[-sta:], array3[-sta:])[0][1]
                sL1 = stalat / ltalat
                sL3 = stalat2 / ltalat2
                if sL1 * sL3 * coef >= 0:
                    result = 0
                    rowdTc1.append(result)
                else:
                    result = sL1 * sL3 * np.abs(coef)
                    rowdTc1.append(result)
                rowdT1.append(sL1)
            self.latdT.append(rowdT1)
            self.latdTc.append(rowdTc1)

        for j, lon in enumerate(self.longtitude):
            rowdT2 = []
            rowdTc2 = []
            for y in range(index1, index2 + 1, 1):
                array2 = []
                array4 = []
                for temp2 in self.tempArray[:y][-lta:]:
                    a1 = temp2[levOne][latitude][j]
                    b1 = temp2[levTwo][latitude][j]
                    array2.append(a1)
                    array4.append(b1)
                ltalon = np.std(array2)
                stalon = np.std(array2[-sta:])
                ltalon2 = np.std(array4)
                stalon2 = np.std(array4[-sta:])
                coef = np.corrcoef(array2[-sta:], array4[-sta:])[0][1]
                sL2 = stalon / ltalon
                sL4 = stalon2 / ltalon2
                if sL2 * sL4 * coef >= 0:
                    result = 0
                    rowdTc2.append(result)
                else:
                    result = sL2 * sL4 * np.abs(coef)
                    rowdTc2.append(result)
                rowdT2.append(sL2 * sL4)
            self.londTc.append(rowdTc2)
            self.londT.append(rowdT2)

        for i in range(len(self.latitude) - 1):
            tuple(self.latdT[i])
            tuple(self.latdTc[i])
        for j in range(len(self.longtitude) - 1):
            tuple(self.londT[i])
            tuple(self.londTc[i])

        self.londT = tuple(self.londT)
        self.londTc = tuple(self.londTc)
        self.latdTc = tuple(self.latdTc)
        self.latdT = tuple(self.latdT)
        epic_lat = self.crcLat.currentIndex()
        epic_lon = self.crcLon.currentIndex()
        epic_date = self.boxcrcDate.currentIndex() - index1
        colmap = self.cmapBox2.currentText()
        lines_drawn = self.check_epic.isChecked()
        epic_lat2 = self.crcLat2.currentIndex()
        epic_lon2 = self.crcLon2.currentIndex()
        epic_date2 = self.boxcrcDate2.currentIndex() - index1
        lines_drawn2 = self.check_epic2.isChecked()

        lat_min, lat_max = self.boxLatMin3.currentIndex(), self.boxLatMax3.currentIndex()
        lon_min, lon_max = self.boxLonMin3.currentIndex(), self.boxLonMax3.currentIndex()
        self.chart7 = plotLatLevDT(self, self.latdT, self.dates[index1:index2 + 1], self.latitude, colmap,
                                   self.longtitude[longtitude], epic_date, epic_lat, lines_drawn,
                                   lat_min, lat_max, epic_date2, epic_lat2, lines_drawn2)
        self.toolbar7 = NavigationToolbar(self.chart7, self)
        self.toolbar7.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chart7, 1, 0, 2, 8)
        self.tab5.layout.addWidget(self.toolbar7, 3, 0, 1, 4)

        self.chart8 = plotLatLevDTc(self, self.latdTc, self.dates[index1:index2 + 1], self.latitude, colmap,
                                    self.longtitude[longtitude], epic_date, epic_lat, lines_drawn,
                                    lat_min, lat_max, epic_date2, epic_lat2, lines_drawn2)
        self.toolbar8 = NavigationToolbar(self.chart8, self)
        self.toolbar8.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chart8, 1, 9, 2, 8)
        self.tab5.layout.addWidget(self.toolbar8, 3, 9, 1, 4)

        self.chart9 = plotLonLevDT(self, self.londT, self.dates[index1:index2 + 1], self.longtitude, colmap,
                                   self.latitude[latitude], epic_date, epic_lon, lines_drawn,
                                   lon_min, lon_max, epic_date2, epic_lon2, lines_drawn2)
        self.toolbar9 = NavigationToolbar(self.chart9, self)
        self.toolbar9.setOrientation(Qt.Horizontal)

        self.tab5.layout.addWidget(self.chart9, 4, 0, 2, 8)
        self.tab5.layout.addWidget(self.toolbar9, 6, 0, 1, 4)

        self.chart10 = plotLonLevDTc(self, self.londTc, self.dates[index1:index2 + 1], self.longtitude, colmap,
                                     self.latitude[latitude], epic_date, epic_lon, lines_drawn,
                                     lon_min, lon_max, epic_date2, epic_lon2, lines_drawn2)
        self.toolbar10 = NavigationToolbar(self.chart10, self)
        self.toolbar10.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chart10, 4, 9, 2, 8)
        self.tab5.layout.addWidget(self.toolbar10, 6, 9, 1, 4)

    def Save1(self):
        form = self.boxFormats1.currentText()
        dpi = int(self.textDPI.text()[:3])
        name = self.textSave1.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart4.save1(directory + '/' + name, dpi, form)
        except:
            return None

    def Save2(self):
        form = self.boxFormats2.currentText()
        dpi = int(self.textDPI2.text()[:3])
        name = self.textSave2.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart5.save2(directory + '/' + name, dpi, form)
        except:
            return None

    def Save3(self):
        form = self.boxFormats3.currentText()
        dpi = int(self.textDPI3.text()[:3])
        name = self.textSave3.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart6.save3(directory + '/' + name, dpi, form)
        except:
            return None

    def Save4(self):
        form = self.boxFormats4.currentText()
        dpi = int(self.textDPI4.text()[:3])
        name = self.textSave4.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart.save4(directory + '/' + name, dpi, form)
        except:
            return None

    def Save5(self):
        form = self.boxFormats5.currentText()
        dpi = int(self.textDPI5.text()[:3])
        name = self.textSave5.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart2.save5(directory + '/' + name, dpi, form)
        except:
            return None

    def Save6(self):
        form = self.boxFormats6.currentText()
        dpi = int(self.textDPI6.text()[:3])
        name = self.textSave6.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart3.save6(directory + '/' + name, dpi, form)
        except:
            return None

    def Save7(self):
        form = self.boxFormats7.currentText()
        dpi = int(self.textDPI7.text()[:3])
        name = self.textSave7.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart7.save7(directory + '/' + name, dpi, form)
        except:
            return None

    def Save8(self):
        form = self.boxFormats8.currentText()
        dpi = int(self.textDPI8.text()[:3])
        name = self.textSave8.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart8.save8(directory + '/' + name, dpi, form)
        except:
            return None

    def Save9(self):
        form = self.boxFormats9.currentText()
        dpi = int(self.textDPI9.text()[:3])
        name = self.textSave9.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart9.save9(directory + '/' + name, dpi, form)
        except:
            return None

    def Save10(self):
        form = self.boxFormats10.currentText()
        dpi = int(self.textDPI10.text()[:3])
        name = self.textSave10.text()
        directory = str(QFileDialog.getExistingDirectory(self, 'Выберите папку для сохранения'))
        if directory == '':
            return None
        try:
            self.chart10.save10(directory + '/' + name, dpi, form)
        except:
            return None

    def save_data(self):

        a = self.box_data_type.currentIndex()

        if a == 0:
            wb = Workbook()
            directory = str(QFileDialog.getExistingDirectory(self, 'Select file'))
            filename = self.txtFileName.text()
            sheet1 = wb.add_sheet('map1')
            sheet1.write(0, 0, '#')
            for k in range(len(self.latitude)):
                sheet1.write(k + 1, 0, self.latitude[k])
            for k in range(len(self.longtitude)):
                sheet1.write(0, k + 1, self.longtitude[k])
            for i in range(len(self.latitude)):
                for j in range(len(self.longtitude)):
                    sheet1.write(i + 1, j + 1, round(float(self.temp_matrix_c[i][j]), 2))
            sheet2 = wb.add_sheet('map2')
            sheet2.write(0, 0, '#')
            for k in range(len(self.latitude)):
                sheet2.write(k + 1, 0, self.latitude[k])
            for k in range(len(self.longtitude)):
                sheet2.write(0, k + 1, self.longtitude[k])
            for i in range(len(self.latitude)):
                for j in range(len(self.longtitude)):
                    sheet2.write(i + 1, j + 1, round(float(self.temp_matrix[i][j]), 2))
            sheet3 = wb.add_sheet('map3')
            sheet3.write(0, 0, '#')
            for k in range(len(self.level)):
                sheet3.write(k + 1, 0, self.level[k])
            for k in range(len(self.latitude)):
                sheet3.write(0, k + 1, self.latitude[k])
            for i in range(len(self.level)):
                for j in range(len(self.latitude)):
                    sheet3.write(i + 1, j + 1, round(float(self.lev_lat_matrix[i][j]), 2))
            sheet4 = wb.add_sheet('map4')
            sheet4.write(0, 0, '#')
            for k in range(len(self.level)):
                sheet4.write(k + 1, 0, self.level[k])
            for k in range(len(self.longtitude)):
                sheet4.write(0, k + 1, self.longtitude[k])
            for i in range(len(self.level)):
                for j in range(len(self.longtitude)):
                    sheet4.write(i + 1, j + 1, round(float(self.lev_lon_matrix[i][j]), 2))
            wb.save(directory + '/' + filename + '.xls')
        elif a == 1:
            wb = Workbook()
            directory = str(QFileDialog.getExistingDirectory(self, 'Select file'))
            filename = self.txtFileName.text()
            table1 = [self.tempLevOneCoorOne, self.tempLevOneCoorTwo, self.arrayLev1, self.arrayLev2,
                      self.integArray, self.integArraywR]
            list1 = ['sta/lta:' + self.boxLevel1.currentText(), 'sta/lta:' + self.boxLevel2.currentText(),
                     'dT', 'dTc']
            sheet1 = wb.add_sheet('Plot1')
            sheet1.write(0, 0, '#')
            for i in range(len(self.level)):
                sheet1.write(0, i + 1, self.level[i])
            for i in range(len(list1)):
                sheet1.write(0, i + 1 + len(self.level), list1[i])
            for j in range(len(self.dates)):
                sheet1.write(j + 1, 0, self.dates[j])
                for k in range(len(self.level)):
                    sheet1.write(j + 1, 1 + k, round(
                        float(self.tempArray[j][k][self.boxLat1.currentIndex()][self.boxLon1.currentIndex()]), 2))
                if j >= int(self.textLTA.text()):
                    sheet1.write(j + 1, 1 + len(self.level),
                                 round(float(self.arrayLev1[int(self.textLTA.text()) - j]), 2))
                    sheet1.write(j + 1, 2 + len(self.level),
                                 round(float(self.arrayLev2[int(self.textLTA.text()) - j]), 2))
                    sheet1.write(j + 1, 3 + len(self.level),
                                 round(float(self.integArray[int(self.textLTA.text()) - j]), 2))
                    sheet1.write(j + 1, 4 + len(self.level),
                                 round(float(self.integArraywR[int(self.textLTA.text()) - j]), 2))
            wb.save(directory + '/' + filename + '.xls')
        elif a == 2:
            wb = Workbook()
            directory = str(QFileDialog.getExistingDirectory(self, 'Select file'))
            filename = self.txtFileName.text()
            index1 = self.boxDates2.currentIndex()
            index2 = self.boxDates3.currentIndex()
            sheet1 = wb.add_sheet('SliceLatdTc')
            for i in range(len(self.dates[index1:index2]) + 1):
                sheet1.write(i + 1, 0, self.dates[index1:index2 + 1][i])
            for i in range(len(self.latitude)):
                sheet1.write(0, i + 1, float(self.latitude[i]))
            for i in range(len(self.dates[index1:index2])+1):
                for j in range(len(self.latitude)):
                    sheet1.write(i + 1, j + 1, round(float(self.latdTc[j][i]), 2))
            sheet2 = wb.add_sheet('SliceLatdT')
            for i in range(len(self.dates[index1:index2]) + 1):
                sheet2.write(i + 1, 0, self.dates[index1:index2 + 1][i])
            for i in range(len(self.latitude)):
                sheet2.write(0, i + 1, float(self.latitude[i]))
            for i in range(len(self.dates[index1:index2])+1):
                for j in range(len(self.latitude)):
                    sheet2.write(i + 1, j + 1, round(float(self.latdT[j][i]), 2))
            sheet3 = wb.add_sheet('SliceLondTc')
            for i in range(len(self.dates[index1:index2]) + 1):
                sheet3.write(i + 1, 0, self.dates[index1:index2 + 1][i])
            for i in range(len(self.longtitude)):
                sheet3.write(0, i + 1, float(self.longtitude[i]))
            for i in range(len(self.dates[index1:index2])+1):
                for j in range(len(self.longtitude)):
                    sheet3.write(i + 1, j + 1, round(float(self.londTc[j][i]), 2))
            sheet4 = wb.add_sheet('SliceLondT')
            for i in range(len(self.dates[index1:index2]) + 1):
                sheet4.write(i + 1, 0, self.dates[index1:index2 + 1][i])
            for i in range(len(self.longtitude)):
                sheet4.write(0, i + 1, float(self.longtitude[i]))
            for i in range(len(self.dates[index1:index2])+1):
                for j in range(len(self.longtitude)):
                    sheet4.write(i + 1, j + 1, round(float(self.londT[j][i]), 2))
            wb.save(directory + '/' + filename + '.xls')


if __name__.endswith('__main__'):
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
