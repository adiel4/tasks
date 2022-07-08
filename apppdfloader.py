import time
import sys
import time
import traceback

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject, QRunnable, QThreadPool
from PyQt5.QtWidgets import QFileDialog, QCheckBox, QGridLayout, QTabWidget, QApplication, QWidget, QLabel, \
    QPushButton, QLineEdit, QComboBox, QMessageBox
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from mpl_toolkits.basemap import Basemap



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
        self.ax.set_xlabel('Долгота, °E', labelpad=20)
        self.ax.set_ylabel('Широта, °N', labelpad=30)
        coord = m(long[clon], lat[clat])
        self.ax.plot(coord[0], coord[1], color=crclCol[0], marker='*', markersize=float(crclSize[:-2]) * 10)
        self.ax.grid(color='w', linewidth=0.1)
    def get_figure(self):
        return self.fig


class mapLevLat(FigureCanvas):
    def __init__(self, parent, level, lat, matrix, date, coltop, colMap, colbot, levMin, levMax, latMin,
                 latMax, lines_drawn, lat_epic):
        plt.close('all')
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
        if lines_drawn:
            plt.plot(x, y, 'r')
        clb = self.fig.colorbar(ac, orientation='vertical')
        self.ax.set_xlim(lat[latMin], lat[latMax])
        self.ax.set_ylim(h_km[levMin], h_km[levMax])
        clb.ax.set_title(r'$\delta$' + 'T', fontsize=10)
        self.ax.set(xlabel='Широта, °N', ylabel='Высота,км')
        self.ax.grid(linewidth=0.1)

    def save2(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')

    def get_figure(self):
        return self.fig


class mapLevLon(FigureCanvas):
    def __init__(self, parent, lev, long, matrix, date, coltop, colMap, colbot, levMin, levMax, lonMin,
                 lonMax, lines_drawn, lon_epic):
        plt.close('all')
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
        if lines_drawn:
            plt.plot(x, y, 'r')
        clb = self.fig.colorbar(ac, orientation='vertical')
        self.ax.set_xlim(long[lonMin], long[lonMax])
        self.ax.set_ylim(h_km[levMin], h_km[levMax])
        clb.ax.set_title(r'$\delta$' + 'T', fontsize=10)
        self.ax.set(xlabel='Долгота, °E', ylabel='Высота,км')
        self.ax.grid(linewidth=0.1)

    def save3(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')

    def get_figure(self):
        return self.fig


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.tempArray = []
        self.dates = []
        self.level = []
        self.longtitude = []
        self.latitude = []

    def initUI(self):
        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.btn_dwnld = QPushButton('Загрузить', self)
        self.btn_dwnld.move(40, 150)
        self.btn_dwnld.resize(100, 30)
        self.btn_dwnld.clicked.connect(self.fuck_your)

        #### СВОЙСТВА ТЕКСТОВ ####################
        self.labVys1 = QLabel('Высота(1), ГПа', self)
        self.labVys1.resize(self.labVys1.sizeHint())
        self.labVys1.move(40, 30)
        self.labVys2 = QLabel('Высота(2), ГПа', self)
        self.labVys2.resize(self.labVys2.sizeHint())
        self.labVys2.move(40, 60)
        self.labShir2 = QLabel('Широта(Карта)', self)
        self.labShir2.resize(self.labShir2.sizeHint())
        self.labShir2.move(40, 90)
        self.labDolg2 = QLabel('Долгота(Карта)', self)
        self.labDolg2.resize(self.labDolg2.sizeHint())
        self.labDolg2.move(40, 120)
        self.labLTA = QLabel('LTA', self)
        self.labLTA.resize(70, 20)
        self.labLTA.move(250, 30)
        self.labSTA = QLabel('STA', self)
        self.labSTA.resize(70, 20)
        self.labSTA.move(250, 90)
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

        ########### СВОЙСТВА  ОКОН ДЛЯ ТЕКСТА ##############
        self.textLTA = QLineEdit(self)
        self.textLTA.move(250, 60)
        self.textLTA.setText('105')
        self.textLTA.resize(50, 20)
        self.textSTA = QLineEdit(self)
        self.textSTA.move(250, 120)
        self.textSTA.setText('21')
        self.textSTA.resize(50, 20)

        self.tabsOptions = QTabWidget(self)
        self.tabsOptions.move(20, 200)
        self.tabsOptions.resize(300, 300)

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
        self.cmapBox.setCurrentText('coolwarm')
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
        colors = ['b-синий', 'g-зеленый', 'r-красный', 'c-голубой', 'm-фиолетовый', 'y-желтый', 'k-черный']
        for color in colors:
            self.boxCrclColor.addItem(color)

        ###############Вкладка: Свойства границ ######################
        self.labLimit1 = QLabel('Границы карты(N/E)', self)
        self.labLimit2 = QLabel('Границы карты(N/h)', self)
        self.labLimit3 = QLabel('Границы карты(h/E)', self)

        self.tabLimits.layout.addWidget(self.labLimit1, 0, 0, 1, 4)
        self.tabLimits.layout.addWidget(self.labLimit2, 2, 0, 1, 4)
        self.tabLimits.layout.addWidget(self.labLimit3, 4, 0, 1, 4)

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

        ################### Вкладка: Данные #############################
        self.box_date1 = QComboBox(self)
        self.tabData.layout.addWidget(self.box_date1, 2, 0, 1, 2)
        self.box_date2 = QComboBox(self)
        self.tabData.layout.addWidget(self.box_date2, 2, 2, 1, 2)
        self.btnPdfMaker = QPushButton('Сохранить PDF', self)
        self.tabData.layout.addWidget(self.btnPdfMaker, 3, 0, 1, 2)
        self.btnPdfMaker.clicked.connect(self.pdf_maker)
        self.btnPdfMaker.clicked.connect(self.pdf_maker2)
        self.btnPdfMaker.clicked.connect(self.pdf_maker3)
        self.filedialog = QFileDialog()
        self.setGeometry(0, 0, 350, 500)
        self.setWindowTitle('PDF loader')
        self.show()

    def fuck_your(self):
        boxes = [self.boxLat1, self.boxLatMax2, self.boxLatMax1, self.boxLatMin1, self.boxLatMin2, self.crcLat
            , self.crcLon, self.boxLon1, self.boxLonMax2, self.boxLonMax1, self.boxLonMin2, self.boxLonMin1
            , self.boxLevel1, self.boxLevel2, self.boxLevMax1, self.boxLevMax2, self.boxLevMin2, self.boxLevMin1
            , self.box_date1, self.box_date2, self.boxcrcDate]
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
                        for boxdates in boxes[-3:]:
                            boxdates.addItem(a + '-' + str(int(k // 60)) + ':00:00')
                        self.dates.append(a + '-' + str(int(k // 60)) + ':00:00')
                        self.tempArray.append(temp[m][:][:][:])
                else:
                    continue
        for i in self.level:
            for boxlev in boxes[12:18]:
                boxlev.addItem(str(i))
        for j in self.latitude:
            for boxlat in boxes[0:6]:
                boxlat.addItem(str(j))
        for k in self.longtitude:
            for boxlon in boxes[6:12]:
                boxlon.addItem(str(k))
        boxes2 = [self.boxLatMax1, self.boxLatMax2, self.boxLonMax2, self.boxLonMax1, self.boxLevMax1
                  , self.boxLevMax2, self.box_date2]
        for box in boxes2:
            box.setCurrentIndex(box.count() - 1)
        self.boxLevel1.setCurrentIndex(self.boxLevel1.count() - 6)
        self.boxLevel2.setCurrentIndex(self.boxLevel2.count() - 2)


    def pdf_maker(self):
        start = time.time()
        QApplication.processEvents()
        index1 = self.box_date1.currentIndex()
        index2 = self.box_date2.currentIndex()
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())
        lev = float(self.boxLevel1.currentText())
        lev2 = float(self.boxLevel2.currentText())
        latMin = self.boxLatMin1.currentIndex()
        latMax = self.boxLatMax1.currentIndex()
        lonMin = self.boxLonMin1.currentIndex()
        lonMax = self.boxLonMax1.currentIndex()
        crclCol = self.boxCrclColor.currentText()
        crclSize = self.textCrclSize.text().replace(',', '.')
        colMap = self.cmapBox.currentText()
        colTop = float(self.top1.text().replace(',', '.'))
        colBot = float(self.bot1.text().replace(',', '.'))
        clat = self.latitude.index(float(self.crcLat.currentText()))
        clon = self.longtitude.index(float(self.crcLon.currentText()))
        try:
            pdf_map_lat_lon = PdfPages('C:/Users/User/Documents/FiguresNE.pdf')
        except:
            QMessageBox.about(self, ' Ошибка', 'Закройте PDF файл перед запуском')
            return None
        if lta > index1:
            return None
        for date in range(index1, index2+1):
            temp_matrix_c = []
            temp_matrix = []
            for i, lat in enumerate(self.latitude):
                row = []
                row2 = []
                for j, lon in enumerate(self.longtitude):
                    temp1LTA = []
                    temp2LTA = []
                    for k in self.tempArray[:date + 1][-lta:]:
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
                temp_matrix_c.append(row)
                temp_matrix.append(row2)

            temp_chart1 = mapLonLat(self, self.longtitude,
                                    self.latitude, temp_matrix_c, self.dates[date], colTop, r'$\delta$' + 'Tc', clat, clon,
                                    colMap,
                                    colBot, crclCol,
                                    crclSize, latMin, latMax, lonMin, lonMax)
            pdf_map_lat_lon.savefig(temp_chart1.get_figure())
            del temp_chart1
        pdf_map_lat_lon.close()
        print(time.time()-start)


    def pdf_maker2(self):
        start = time.time()
        index1 = self.box_date1.currentIndex()
        index2 = self.box_date2.currentIndex()
        QApplication.processEvents()
        try:
            pdf_map_lev_lon = PdfPages('C:/Users/User/Documents/FiguresNh.pdf')
        except:
            QMessageBox.about(self, ' Ошибка', 'Закройте PDF файл перед запуском')
        lattit = float(self.boxLon1.currentText())
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())
        levMin = self.boxLevMin1.currentIndex()
        levMax = self.boxLevMax1.currentIndex()
        latMin = self.boxLatMin2.currentIndex()
        latMax = self.boxLatMax2.currentIndex()
        colMap = self.cmapBox.currentText()
        coltop = float(self.top2.text().replace(',', '.'))
        colBot = float(self.bot2.text().replace(',', '.'))
        lines_drawn = self.check_epic.isChecked()
        lat_epic = self.crcLat.currentIndex()
        for date in range(index1,index2+1):
            lev_lat_matrix = []
            for i, lev in enumerate(self.level):
                row = []
                for j, lat in enumerate(self.latitude):
                    tempLTA = []
                    for k in self.tempArray[:date + 1][-lta:]:
                        tempLTA.append(k[i][j][self.longtitude.index(lattit)])
                    tempSTA = tempLTA[-sta:]
                    lS = np.std(tempSTA) / np.std(tempLTA)
                    row.append(lS)
                lev_lat_matrix.append(row)
            temp_chart2 = mapLevLat(self, self.level,
                                    self.latitude, lev_lat_matrix, self.dates[date], coltop, colMap, colBot, levMin, levMax,
                                    latMin, latMax, lines_drawn, lat_epic)
            pdf_map_lev_lon.savefig(temp_chart2.get_figure())
        pdf_map_lev_lon.close()
        print(time.time()-start)

    def pdf_maker3(self):
        try:
            pdf_map_lev_lat = PdfPages('C:/Users/User/Documents/FigureEh.pdf')
        except:
            QMessageBox.about(self, ' Ошибка', 'Закройте PDF файл перед запуском')
        index1 = self.box_date1.currentIndex()
        index2 = self.box_date2.currentIndex()
        long = float(self.boxLat1.currentText())
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())
        colMap = self.cmapBox.currentText()
        levMin = self.boxLevMin2.currentIndex()
        levMax = self.boxLevMax2.currentIndex()
        lonMin = self.boxLonMin2.currentIndex()
        lonMax = self.boxLonMax2.currentIndex()
        coltop = float(self.top3.text().replace(',', '.'))
        colbot = float(self.bot3.text().replace(',', '.'))
        lines_drawn = self.check_epic.isChecked()
        lon_epic = self.crcLon.currentIndex()
        for date in range(index1,index2+1):
            lev_lon_matrix = []
            for i, lev in enumerate(self.level):
                row = []
                for j, lon in enumerate(self.longtitude):
                    tempLTA = []
                    for k in self.tempArray[:date + 1][-lta:]:
                        tempLTA.append(k[i][self.latitude.index(long)][j])
                    tempSTA = tempLTA[-sta:]
                    lS = np.std(tempSTA) / np.std(tempLTA)
                    row.append(lS)
                lev_lon_matrix.append(row)
            temp_chart3 = mapLevLon(self, self.level,
                                    self.longtitude, lev_lon_matrix, self.dates[date], coltop, colMap, colbot, levMin,
                                    levMax,
                                    lonMin,
                                    lonMax, lines_drawn, lon_epic)
            pdf_map_lev_lat.savefig(temp_chart3.get_figure())
        pdf_map_lev_lat.close()
        pass

if __name__.endswith('__main__'):
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
