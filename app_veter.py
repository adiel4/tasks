import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFileDialog, QCheckBox, QGridLayout, QTabWidget, QApplication, QWidget, QLabel, \
    QPushButton, QMainWindow, QLineEdit, QComboBox, QToolTip, QTableWidget, QTableWidgetItem, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.axes_grid1 import make_axes_locatable
from netCDF4 import Dataset


class Slice_Matrix(FigureCanvas):

    def __init__(self, parent, matrix, dates, y_values, col_map, name, y_val_min, y_val_max, name_clb):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 6}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=False)
        plt.subplots_adjust(left=0.08, bottom=0.285, right=1, top=0.925)
        plt.close('all')
        super().__init__(self.fig)
        self.setParent(parent)
        ac = self.ax.pcolormesh(dates, y_values, matrix, cmap=col_map)
        self.ax.set(title=name)
        self.ax.autoscale(True)
        self.ax.set_xticks(dates[0:-1:16])
        self.ax.set_xticklabels(xlabel[6:8] for xlabel in dates[0:-1:16])
        clb = self.fig.colorbar(ac, orientation='vertical')
        clb.ax.set_title(name_clb)
        self.ax.set_ylim(y_values[y_val_min] - 0.25, y_values[y_val_max] + 0.25)
        self.ax.set(xlabel='Дата', ylabel='')
        self.ax.grid(color='w', linewidth=0.1)


class Wind_Mag_Ang_Map(FigureCanvas):
    def __init__(self, parent, long, lat, wind_x, wind_y, magn, date, coltop, name, clat, clon, colMap, colBot, crclCol,
                 crclSize,
                 latMinInd, latMaxInd, lonMinInd, lonMaxInd, clat2, clon2, crclCol2, crclSize2, lin_dr):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=True, dpi=120)
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
        # highColor = round(coltop / 0.2)
        # lowColor = round(colBot / 0.2)
        self.levels = [x for x in range(colBot, coltop, round((coltop-colBot)/10))]
        ac = m.contourf(x, y, magn, self.levels, cmap=colMap)
        am = m.quiver(x, y, wind_x, wind_y)
        self.ax.set_title(date)
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.15)
        clb = self.fig.colorbar(ac, orientation='vertical', cax=cax)
        clb.ax.set_title(name)
        self.ax.set_xlabel('Долгота, E', labelpad=15)
        self.ax.set_ylabel('Широта, N', labelpad=20)
        coord = m(long[clon], lat[clat])


class plotTemp(FigureCanvas):
    def __init__(self, parent, dates, lineOne, lineTwo, dateTicks, dateLabels, clr1, clr2, w1, w2, name1, name2, latOne,
                 lonOne, dateMin, dateMax, plt_xlabel, plt_ylabel, plt_title):
        plt.close('all')
        font = {'weight': 'normal',
                'size': 8}
        matplotlib.rc('font', **font)
        self.fig, self.ax = plt.subplots(constrained_layout=True, dpi=120)
        super().__init__(self.fig)
        self.setParent(parent)
        self.l_1, = self.ax.plot(dates, lineOne, clr2[0] + '-', linewidth=w2)
        self.l_2, = self.ax.plot(dates, lineTwo, clr1[0] + '-', linewidth=w1)
        self.ax.legend([name1 + ' hPa', name2 + ' hPa'], loc='best')
        self.ax.set(xlabel=plt_xlabel, ylabel=plt_ylabel,
                    title=plt_title)
        self.ax.set_xticks(dateTicks)
        self.ax.set_xticklabels(dateLabels)
        self.ax.grid()
        self.ax.set_xlim(dates[dateMin], dates[dateMax])
        self.dates = dates

    def col(self, clr):
        self.ax.get_lines()[0].set_color(clr[0])

    def save4(self, name, dpi, docFormat):
        self.fig.savefig(name + docFormat, dpi=dpi, bbox_inches='tight')


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.wind_magn_array = []
        self.wind_angle_array = []
        self.east_wind_array = []
        self.north_wind_array = []
        self.dates = []
        self.level = []
        self.longtitude = []
        self.latitude = []

    def initUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        ## СВОЙСТВА КНОПОК #############################
        self.btnDwnld = QPushButton('Загрузка', self)
        self.btnDwnld.move(40, 230)
        self.btnDwnld.resize(100, 30)
        self.btnDwnld.clicked.connect(self.download)
        self.btnDwnld.clicked.connect(self.table_view)
        self.btnDwnld.clicked.connect(self.lat_changed)
        self.btnDwnld.clicked.connect(self.lon_changed)
        self.btnMap = QPushButton('Карта', self)
        self.btnMap.move(150, 250)
        self.btnMap.resize(100, 20)
        self.btnMap.clicked.connect(self.date_map)
        # self.btnMap.clicked.connect(self.dateMap2)
        # self.btnMap.clicked.connect(self.dateMap3)
        self.btnGraph = QPushButton('График', self)
        self.btnGraph.move(40, 270)
        self.btnGraph.resize(60, 30)
        self.btnGraph.clicked.connect(self.time_plot)
        self.btnPrevMap = QPushButton('<', self)
        self.btnPrevMap.move(150, 270)
        self.btnPrevMap.resize(30, 30)
        self.btnPrevMap.clicked.connect(self.prev_map)
        self.btnPrevMap.clicked.connect(self.date_map)
        # self.btnPrevMap.clicked.connect(self.dateMap2)
        # self.btnPrevMap.clicked.connect(self.dateMap3)
        self.btnNextMap = QPushButton('>', self)
        self.btnNextMap.move(180, 270)
        self.btnNextMap.resize(30, 30)
        self.btnNextMap.clicked.connect(self.next_map)
        self.btnNextMap.clicked.connect(self.date_map)
        # self.btnNextMap.clicked.connect(self.dateMap2)
        # self.btnNextMap.clicked.connect(self.dateMap3)

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
        self.boxLat1.currentIndexChanged.connect(self.lat_changed)
        self.boxLon1 = QComboBox(self)
        self.boxLon1.move(150, 120)
        self.boxLon1.resize(70, 20)
        self.boxLon1.currentIndexChanged.connect(self.lon_changed)
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
        self.tab4 = QWidget(self)
        self.tab5 = QWidget(self)
        self.tab6 = QWidget(self)
        self.tab7 = QWidget(self)
        self.tab8 = QWidget(self)

        self.tabs.addTab(self.tab1, "Карта(N/E)")
        self.tabs.addTab(self.tab2, 'Карта(N/E)')
        self.tabs.addTab(self.tab4, "Скорость")
        self.tabs.addTab(self.tab5, "Cрез_скорость")
        self.tabs.addTab(self.tab6, 'Cрез_угол')
        self.tabs.addTab(self.tab7, 'Таблица(скорость)')
        self.tabs.addTab(self.tab8, 'Таблица(угол)')

        self.tab1.layout = QGridLayout(self.tab1)
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.layout = QGridLayout(self.tab2)
        self.tab2.setLayout(self.tab2.layout)
        self.tab4.layout = QGridLayout(self.tab4)
        self.tab4.setLayout(self.tab4.layout)
        self.tab5.layout = QGridLayout(self.tab5)
        self.tab5.setLayout(self.tab5.layout)
        self.tab6.layout = QGridLayout(self.tab6)
        self.tab6.setLayout(self.tab6.layout)
        self.tab7.layout = QGridLayout(self.tab7)
        self.tab7.setLayout(self.tab7.layout)
        self.tab8.layout = QGridLayout(self.tab8)
        self.tab8.setLayout(self.tab8.layout)

        self.tab5.layout.setRowStretch(0, 1)
        self.tab5.layout.setRowStretch(1, 4)
        self.tab5.layout.setRowStretch(4, 4)
        self.tab5.layout.setRowStretch(3, 1)
        self.tab5.layout.setRowStretch(6, 1)

        self.tab6.layout.setRowStretch(0, 1)
        self.tab6.layout.setRowStretch(1, 4)
        self.tab6.layout.setRowStretch(4, 4)
        self.tab6.layout.setRowStretch(3, 1)
        self.tab6.layout.setRowStretch(6, 1)


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
        self.btnMap2.clicked.connect(self.lat_lon_map)
        self.cmapBox2 = QComboBox(self)
        self.tab5.layout.addWidget(self.cmapBox2, 0, 15, 1, 2)

        ########### Вкладка: Таблица скорости ветра #################

        self.table = QTableWidget(self)
        self.tab7.layout.addWidget(self.table, 0, 0)

        ########### Вкладка: Таблица угла ветра #################

        self.table2 = QTableWidget(self)
        self.tab8.layout.addWidget(self.table2, 0, 0)

        ######## ОСНОВНЫЕ СВОЙСТВА ВКЛАДОК НАСТРОЙКИ ################

        self.tabsOptions = QTabWidget(self)
        self.tabsOptions.move(20, 300)
        self.tabsOptions.resize(300, 400)

        self.tab_line_options = QTabWidget(self)
        self.tab4.layout.addWidget(self.tab_line_options, 0, 1, 2, 1)

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

        self.tabsOptions.addTab(self.tabMap, 'Карта')
        self.tabsOptions.addTab(self.tabLimits, 'Границы')

        self.tabMap.layout = QGridLayout(self.tabMap)
        self.tabMap.setLayout(self.tabMap.layout)
        self.tabLimits.layout = QGridLayout(self.tabLimits)
        self.tabLimits.setLayout(self.tabLimits.layout)
        ############### Вкладка: Свойства линий #####################

        self.labPlot1Wid = QLabel('Толщина и цвета линий:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot1Wid, 0, 0)
        self.labPlot2Wid = QLabel('Толщина и цвета линий:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot2Wid, 3, 0)
        self.labPlot3Wid = QLabel('Толщина и цвета линий:', self)
        self.tab_line_properties.layout.addWidget(self.labPlot3Wid, 6, 0)
        self.labPlot1Col = QLabel('Скоростной профиль', self)
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
        self.cmapBox = QComboBox(self)
        self.tabMap.layout.addWidget(self.cmapBox, 0, 0, 1, 2)
        for cmap_id in plt.colormaps():
            self.cmapBox.addItem(cmap_id)
            self.cmapBox2.addItem(cmap_id)
        self.cmapBox.setCurrentText('coolwarm')
        self.cmapBox2.setCurrentText('coolwarm')
        self.labGr = QLabel('Верх. и нижн. граница', self)
        self.tabMap.layout.addWidget(self.labGr, 1, 0, 1, 2)
        self.top1 = QLineEdit(self)
        self.top1.setText('10')
        self.tabMap.layout.addWidget(self.top1, 2, 0, 1, 1)
        self.labGr4 = QLabel('Карта(N/E)_1', self)
        self.tabMap.layout.addWidget(self.labGr4, 1, 2, 1, 3)
        self.bot1 = QLineEdit(self)
        self.bot1.setText('0')
        self.tabMap.layout.addWidget(self.bot1, 2, 2, 1, 1)
        self.labGr2 = QLabel('Верх. и нижн. граница', self)
        self.tabMap.layout.addWidget(self.labGr2, 3, 0, 1, 2)
        self.top2 = QLineEdit(self)
        self.top2.setText('20')
        self.tabMap.layout.addWidget(self.top2, 4, 0, 1, 1)
        self.labGr5 = QLabel('Карта(N/E)_2', self)
        self.tabMap.layout.addWidget(self.labGr5, 3, 2, 1, 3)
        self.bot2 = QLineEdit(self)
        self.bot2.setText('0')
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

        self.filedialog = QFileDialog()
        self.setGeometry(0, 0, 1300, 700)
        self.setWindowTitle('Algorithm')
        self.show()
        np.seterr(divide='ignore')

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
                 self.boxcrcDate, self.boxcrcDate2]
        for box in boxes:
            box.clear()
        self.level, self.latitude, self.longtitude, self.dates, self.wind_array = [], [], [], [], []

        files_list = self.filedialog.getOpenFileNames()[:-1][0]
        for file in files_list:
            if file[-2:] == 'c4' or file[-2:] == 'nc':
                ds = Dataset(file)
                east_wind_prof = ds['U'][:]  # x_values
                north_wind_prof = ds['V'][:]  # y_values
                if files_list.index(file) == 0:
                    self.level = tuple(ds['lev'][:])
                    self.latitude = tuple(ds['lat'][:])
                    self.longtitude = tuple(ds['lon'][:])
                    dates = tuple(ds['time'][:])
                for ind_1, ind_2 in enumerate(dates):
                    date_str = file.split('/')[-1].split('.')[2]
                    for boxdates in boxes[-9:]:
                        boxdates.addItem(date_str + '-' + str(int(ind_2 // 60)) + ':00:00')
                    self.dates.append(date_str + '-' + str(int(ind_2 // 60)) + ':00:00')
                    self.east_wind_array.append(tuple(east_wind_prof[ind_1][:][:][:]))
                    self.north_wind_array.append(tuple(north_wind_prof[ind_1][:][:][:]))
                    self.wind_magn_array.append(
                        tuple(np.sqrt(north_wind_prof[ind_1][:][:][:] ** 2 + east_wind_prof[ind_1][:][:][:] ** 2)))
                    self.wind_angle_array.append(
                        tuple(np.degrees(np.arctan2(east_wind_prof[ind_1][:][:][:], north_wind_prof[ind_1][:][:][:]))))
            else:
                continue
        for lev in self.level:
            for boxlev in boxes[11:17]:
                boxlev.addItem(str(lev))
        for lat in self.latitude:
            for boxlat in boxes[0:11]:
                boxlat.addItem(str(lat))
        for lon in self.longtitude:
            for boxlon in boxes[17:28]:
                boxlon.addItem(str(lon))
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

    @pyqtSlot()
    def table_view(self):
        self.table.setColumnCount(len(self.level))
        self.table.setRowCount(len(self.dates))
        self.table.setHorizontalHeaderLabels([str(i) + ' hPa' for i in self.level])
        self.table.setVerticalHeaderLabels(self.dates)
        self.table2.setColumnCount(len(self.level))
        self.table2.setRowCount(len(self.dates))
        self.table2.setHorizontalHeaderLabels([str(i) + ' hPa' for i in self.level])
        self.table2.setVerticalHeaderLabels(self.dates)

    @pyqtSlot()
    def lat_changed(self):
        lat = self.boxLat1.currentIndex()
        lon = self.boxLon1.currentIndex()
        for i in range(len(self.dates)):
            for j in range(len(self.level)):
                self.table.setItem(i, j, QTableWidgetItem(str(round(self.wind_magn_array[i][j][lat][lon], 2))))
                if self.wind_angle_array[i][j][lat][lon] > 0:
                    self.table2.setItem(i, j, QTableWidgetItem(str(round(self.wind_angle_array[i][j][lat][lon], 2))))
                else:
                    self.table2.setItem(i, j,
                                        QTableWidgetItem(str(round(self.wind_angle_array[i][j][lat][lon] % 360, 2))))

    @pyqtSlot()
    def lon_changed(self):
        lat = self.boxLat1.currentIndex()
        lon = self.boxLon1.currentIndex()
        for i in range(len(self.dates)):
            for j in range(len(self.level)):
                self.table.setItem(i, j, QTableWidgetItem(str(round(self.wind_magn_array[i][j][lat][lon], 2))))
                if self.wind_angle_array[i][j][lat][lon] > 0:
                    self.table2.setItem(i, j, QTableWidgetItem(str(round(self.wind_angle_array[i][j][lat][lon], 2))))
                else:
                    self.table2.setItem(i, j,
                                        QTableWidgetItem(str(round(self.wind_angle_array[i][j][lat][lon] % 360, 2))))

    @pyqtSlot()
    def time_plot(self):
        if self.boxLevel1.currentText() == '':
            return None
        lev_one = float(self.boxLevel1.currentText())
        lev_two = float(self.boxLevel2.currentText())
        lat_one = float(self.boxLat1.currentText())
        lon_one = float(self.boxLon1.currentText())

        self.wind_lev_one = [k[self.level.index(lev_one)][self.latitude.index(lat_one)][self.longtitude.index(lon_one)] for k in self.wind_magn_array]
        self.wind_lev_two = [k[self.level.index(lev_two)][self.latitude.index(lat_one)][self.longtitude.index(lon_one)] for k in self.wind_magn_array]
        self.angle_lev_one = [k[self.level.index(lev_one)][self.latitude.index(lat_one)][self.longtitude.index(lon_one)] for k in self.wind_angle_array]
        self.angle_lev_two = [k[self.level.index(lev_two)][self.latitude.index(lat_one)][self.longtitude.index(lon_one)] for k in self.wind_angle_array]
        self.east_wind_lev_one = [k[self.level.index(lev_one)][self.latitude.index(lat_one)][self.longtitude.index(lon_one)] for k in self.east_wind_array]
        self.east_wind_lev_two = [k[self.level.index(lev_two)][self.latitude.index(lat_one)][self.longtitude.index(lon_one)] for k in self.east_wind_array]
        self.north_wind_lev_one = [k[self.level.index(lev_one)][self.latitude.index(lat_one)][self.longtitude.index(lon_one)] for k in self.north_wind_array]
        self.north_wind_lev_two = [k[self.level.index(lev_two)][self.latitude.index(lat_one)][self.longtitude.index(lon_one)] for k in self.north_wind_array]

        date_ticks = self.dates[0:-1:50]
        self.date_ticks = self.dates[0:-1:50]
        date_labels = []
        for i in date_ticks:
            date_labels.append(i[6:8])
        self.date_labels = date_labels

        width1 = float(self.textPlot1Line2Width.text().replace(',', '.'))
        width2 = float(self.textPlot1Line1Width.text().replace(',', '.'))
        clr1 = self.boxPlot1Line2Color.currentText()
        clr2 = self.boxPlot1Line1Color.currentText()

        name1 = self.boxLevel1.currentText()
        name2 = self.boxLevel2.currentText()
        date_min1 = self.boxDatesMinPlot1.currentIndex()
        date_max1 = self.boxDatesMaxPlot1.currentIndex()

        plt_xlabel = 'Дата'
        plt_ylabel = u'Vₑ, м/c'
        plt_title = 'Скорость (' + str(lon_one) + '$^\circ$N  ' + str(lat_one) + '$^\circ$E)'

        self.chartPlot1 = plotTemp(self, self.dates, self.east_wind_lev_one, self.east_wind_lev_two, date_ticks, date_labels,
                              clr1, clr2, width1, width2, name1, name2, lat_one, lon_one, date_min1, date_max1,
                              plt_xlabel, plt_ylabel, plt_title)
        self.tab4.layout.addWidget(self.chartPlot1, 0, 0, 1, 1)
        # self.toolbarPlot1 = NavigationToolbar(self.chartPlot1, self)
        # self.toolbarPlot1.setOrientation(Qt.Horizontal)
        # self.tab4.layout.addWidget(self.toolbarPlot1, 1, 0, 1, 1)

        plt_ylabel = u'Vₙ, м/c'
        self.chartPlot2 = plotTemp(self, self.dates, self.north_wind_lev_one, self.north_wind_lev_two, date_ticks, date_labels,
                              clr1, clr2, width1, width2, name1, name2, lat_one, lon_one, date_min1, date_max1,
                              plt_xlabel, plt_ylabel, plt_title)
        self.tab4.layout.addWidget(self.chartPlot2, 1, 0, 1, 1)
        # self.toolbarPlot2 = NavigationToolbar(self.chartPlot2, self)
        # self.toolbarPlot2.setOrientation(Qt.Horizontal)
        # self.tab4.layout.addWidget(self.toolbarPlot2, 3, 0, 1, 1)

        plt_ylabel = u'Vᵣ, м/c'
        self.chartPlot3 = plotTemp(self, self.dates, self.wind_lev_one, self.wind_lev_two, date_ticks, date_labels,
                              clr1, clr2, width1, width2, name1, name2, lat_one, lon_one, date_min1, date_max1,
                              plt_xlabel, plt_ylabel, plt_title)
        self.tab4.layout.addWidget(self.chartPlot3, 2, 0, 1, 1)
        # self.toolbarPlot3 = NavigationToolbar(self.chartPlot3, self)
        # self.toolbarPlot3.setOrientation(Qt.Horizontal)
        # self.tab4.layout.addWidget(self.toolbarPlot3, 5, 1, 1, 1)

        plt_ylabel = u'Угол ,\N{DEGREE SIGN}'
        self.chartPlot4 = plotTemp(self, self.dates, self.angle_lev_one, self.angle_lev_two, date_ticks, date_labels,
                              clr1, clr2, width1, width2, name1, name2, lat_one, lon_one, date_min1, date_max1,
                              plt_xlabel, plt_ylabel, plt_title)
        self.tab4.layout.addWidget(self.chartPlot4, 2, 1, 1, 1)
        # self.toolbarPlot4 = NavigationToolbar(self.chartPlot4, self)
        # self.toolbarPlot4.setOrientation(Qt.Horizontal)
        # self.tab4.layout.addWidget(self.toolbarPlot4, 5, 0, 1, 1)

    @pyqtSlot()
    def date_map(self):
        lev_1 = float(self.boxLevel1.currentText())
        lev_2 = float(self.boxLevel2.currentText())
        date = self.boxDates.currentText()
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())

        time_index = int(self.boxDates.currentIndex())
        lev_index = int(self.boxLevel1.currentIndex())
        lev_index_2 = int(self.boxLevel2.currentIndex())

        wind_mag_lev1 = self.wind_magn_array[time_index][lev_index][:][:]
        east_wind_lev1 = self.east_wind_array[time_index][lev_index][:][:]
        north_wind_lev1 = self.north_wind_array[time_index][lev_index][:][:]

        wind_mag_lev2 = self.wind_magn_array[time_index][lev_index_2][:][:]
        east_wind_lev2 = self.east_wind_array[time_index][lev_index_2][:][:]
        north_wind_lev2 = self.north_wind_array[time_index][lev_index_2][:][:]

        setMaxMap1 = round(np.ceil(max([max(i) for i in wind_mag_lev1])))
        setMinMap1 = round(np.ceil(min([min(i) for i in wind_mag_lev1])))

        setMaxMap2 = round(np.ceil(max([max(i) for i in wind_mag_lev2])))
        setMinMap2 = round(np.ceil(min([min(i) for i in wind_mag_lev2])))

        self.top1.setText(str(setMaxMap1))
        self.bot1.setText(str(setMinMap1))

        self.top2.setText(str(setMaxMap2))
        self.bot2.setText(str(setMinMap2))

        latMin = self.boxLatMin1.currentIndex()
        latMax = self.boxLatMax1.currentIndex()
        lonMin = self.boxLonMin1.currentIndex()
        lonMax = self.boxLonMax1.currentIndex()
        crclCol = self.boxCrclColor.currentText()
        crclSize = self.textCrclSize.text().replace(',', '.')
        self.colMap = self.cmapBox.currentText()
        colTop = int(self.top1.text().replace(',', '.'))
        colBot = int(self.bot1.text().replace(',', '.'))
        colTop2 = int(self.top2.text().replace(',', '.'))
        colBot2 = int(self.bot2.text().replace(',', '.'))
        clat = self.latitude.index(float(self.crcLat.currentText()))
        clon = self.longtitude.index(float(self.crcLon.currentText()))
        crclCol2 = self.boxCrclColor2.currentText()
        crclSize2 = self.textCrclSize2.text().replace(',', '.')
        clat2 = self.latitude.index(float(self.crcLat2.currentText()))
        clon2 = self.longtitude.index(float(self.crcLon2.currentText()))
        lines_drawn = self.check_epic2.isChecked()

        self.chartMap1 = Wind_Mag_Ang_Map(self, self.longtitude, self.latitude, east_wind_lev1, north_wind_lev1,
                                       wind_mag_lev1, date, colTop, 'Скорость м/c', clat, clon,
                                       self.colMap,
                                       colBot, crclCol,
                                       crclSize, latMin, latMax, lonMin, lonMax,
                                       clat2, clon2, crclCol2, crclSize2, lines_drawn)
        self.tab1.layout.addWidget(self.chartMap1, 0, 0, 1, 1)
        self.toolbarMap1 = NavigationToolbar(self.chartMap1, self)
        self.toolbarMap1.setOrientation(Qt.Horizontal)
        self.tab1.layout.addWidget(self.toolbarMap1, 1, 0, 1, 1)

        self.chartMap2 = Wind_Mag_Ang_Map(self, self.longtitude, self.latitude, east_wind_lev2, north_wind_lev2,
                                       wind_mag_lev2, date, colTop2, 'Скорость м/c', clat, clon,
                                       self.colMap,
                                       colBot2, crclCol,
                                       crclSize, latMin, latMax, lonMin, lonMax,
                                       clat2, clon2, crclCol2, crclSize2, lines_drawn)
        self.tab2.layout.addWidget(self.chartMap2, 2, 0, 1, 1)
        self.toolbarMap2 = NavigationToolbar(self.chartMap2, self)
        self.toolbarMap2.setOrientation(Qt.Horizontal)
        self.tab2.layout.addWidget(self.toolbarMap2, 3, 0, 1, 1)

    @pyqtSlot()
    def prev_map(self):
        ind = self.boxDates.currentIndex()
        try:
            self.boxDates.setCurrentIndex(ind - 1)
        except:
            dlg = QDialog(self)
            dlg.setWindowTitle("Error")
            dlg.exec()

    @pyqtSlot()
    def next_map(self):
        ind = self.boxDates.currentIndex()
        try:
            self.boxDates.setCurrentIndex(ind + 1)
        except:
            dlg = QDialog(self)
            dlg.setWindowTitle("Error")
            dlg.exec()

    @pyqtSlot()
    def lat_lon_map(self):
        index_1 = self.boxDates2.currentIndex()
        index_2 = self.boxDates3.currentIndex()
        lat = self.boxLat3.currentIndex()
        lon = self.boxLon3.currentIndex()

        lev_1 = self.boxLevel1.currentIndex()
        lev_2 = self.boxLevel2.currentIndex()

        colmap = self.cmapBox2.currentText()

        lat_min, lat_max = self.boxLatMin3.currentIndex(), self.boxLatMax3.currentIndex()
        lon_min, lon_max = self.boxLonMin3.currentIndex(), self.boxLonMax3.currentIndex()

        self.wind_slice_lat1_lev1 = []
        self.wind_slice_lon1_lev1 = []
        self.angle_slice_lat1_lev1 = []
        self.angle_slice_lon1_lev1 = []

        self.wind_slice_lat1_lev2 = []
        self.wind_slice_lon1_lev2 = []
        self.angle_slice_lat1_lev2 = []
        self.angle_slice_lon1_lev2 = []

        for i, lat_i in enumerate(self.latitude):
            row_wind_lon1_lev1 = []
            row_angle_lon1_lev1 = []
            row_wind_lon1_lev2 = []
            row_angle_lon1_lev2 = []
            for k in range(index_1, index_2 + 1, 1):
                row_wind_lon1_lev1.append(self.wind_magn_array[k][lev_1][i][lon])
                if self.wind_angle_array[k][lev_1][i][lon] > 0:
                    row_angle_lon1_lev1.append(self.wind_angle_array[k][lev_1][i][lon])
                else:
                    row_angle_lon1_lev1.append(self.wind_angle_array[k][lev_1][i][lon] % 360)
                row_wind_lon1_lev2.append(self.wind_magn_array[k][lev_2][i][lon])
                if self.wind_angle_array[k][lev_2][i][lon] > 0:
                    row_angle_lon1_lev2.append(self.wind_angle_array[k][lev_2][i][lon])
                else:
                    row_angle_lon1_lev2.append(self.wind_angle_array[k][lev_2][i][lon] % 360)
            self.wind_slice_lon1_lev1.append(row_wind_lon1_lev1)
            self.angle_slice_lon1_lev1.append(row_angle_lon1_lev1)
            self.wind_slice_lon1_lev2.append(row_wind_lon1_lev2)
            self.angle_slice_lon1_lev2.append(row_angle_lon1_lev2)

        for i, lon_i in enumerate(self.longtitude):
            row_wind_lat1_lev1 = []
            row_angle_lat1_lev1 = []
            row_wind_lat1_lev2 = []
            row_angle_lat1_lev2 = []
            for k in range(index_1, index_2 + 1, 1):
                row_wind_lat1_lev1.append(self.wind_magn_array[k][lev_1][lat][i])
                if self.wind_angle_array[k][lev_1][lat][i] > 0:
                    row_angle_lat1_lev1.append(self.wind_angle_array[k][lev_1][lat][i])
                else:
                    row_angle_lat1_lev1.append(self.wind_angle_array[k][lev_1][lat][i] % 360)
                row_wind_lat1_lev2.append(self.wind_magn_array[k][lev_2][lat][i])
                if self.wind_angle_array[k][lev_2][lat][i]:
                    row_angle_lat1_lev2.append(self.wind_angle_array[k][lev_2][lat][i])
                else:
                    row_angle_lat1_lev2.append(self.wind_angle_array[k][lev_2][lat][i] % 360)
            self.wind_slice_lat1_lev1.append(row_wind_lat1_lev1)
            self.angle_slice_lat1_lev1.append(row_angle_lat1_lev1)
            self.wind_slice_lat1_lev2.append(row_wind_lat1_lev2)
            self.angle_slice_lat1_lev2.append(row_angle_lat1_lev2)
        name = 'Срез скорости по долготе(Высота 1)'
        name_clb = 'Скорость м/с'
        self.chartSlice1 = Slice_Matrix(self, self.wind_slice_lat1_lev1, self.dates[index_1:index_2 + 1], self.longtitude,
                                   colmap, name, lon_min, lon_max, name_clb)
        self.toolbarSlice1 = NavigationToolbar(self.chartSlice1, self)
        self.toolbarSlice1.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chartSlice1, 1, 0, 2, 11)
        self.tab5.layout.addWidget(self.toolbarSlice1, 2, 0, 1, 8)

        name = 'Срез скорости по долготе(Высота 2)'
        name_clb = 'Скорость м/с'
        self.chartSlice2 = Slice_Matrix(self, self.wind_slice_lat1_lev2, self.dates[index_1:index_2 + 1], self.longtitude,
                                   colmap, name, lon_min, lon_max, name_clb)
        self.toolbarSlice2 = NavigationToolbar(self.chartSlice2, self)
        self.toolbarSlice2.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chartSlice2, 4, 0, 2, 11)
        self.tab5.layout.addWidget(self.toolbarSlice2, 5, 0, 1, 8)

        name = 'Срез скорости по широте(Высота 1)'
        name_clb = 'Скорость м/с'
        self.chartSlice3 = Slice_Matrix(self, self.wind_slice_lon1_lev2, self.dates[index_1:index_2 + 1], self.latitude,
                                   colmap, name, lat_min, lat_max, name_clb)
        self.toolbarSlice3 = NavigationToolbar(self.chartSlice3, self)
        self.toolbarSlice3.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chartSlice3, 1, 12, 2, 11)
        self.tab5.layout.addWidget(self.toolbarSlice3, 2, 12, 1, 8)

        name = 'Срез скорости по широте(Высота 2)'
        name_clb = 'Скорость м/с'
        self.chartSlice4 = Slice_Matrix(self, self.wind_slice_lon1_lev2, self.dates[index_1:index_2 + 1], self.latitude,
                                   colmap, name, lat_min, lat_max, name_clb)
        self.toolbarSlice4 = NavigationToolbar(self.chartSlice4, self)
        self.toolbarSlice4.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chartSlice4, 4, 12, 2, 11)
        self.tab5.layout.addWidget(self.toolbarSlice4, 5, 12, 1, 8)

        name = 'Срез угла по долготе(Высота 1)'
        name_clb = 'Угол'
        self.chartSlice5 = Slice_Matrix(self, self.angle_slice_lat1_lev1, self.dates[index_1:index_2 + 1], self.longtitude,
                                   colmap, name, lon_min, lon_max, name_clb)
        self.toolbarSlice5 = NavigationToolbar(self.chartSlice5, self)
        self.toolbarSlice5.setOrientation(Qt.Horizontal)
        self.tab6.layout.addWidget(self.chartSlice5, 1, 0, 2, 11)
        self.tab6.layout.addWidget(self.toolbarSlice5, 2, 0, 1, 8)

        name = 'Срез угла по долготе(Высота 2)'
        name_clb = 'Угол'
        self.chartSlice6 = Slice_Matrix(self, self.angle_slice_lat1_lev2, self.dates[index_1:index_2 + 1], self.longtitude,
                                   colmap, name, lon_min, lon_max, name_clb)
        self.toolbarSlice6 = NavigationToolbar(self.chartSlice6, self)
        self.toolbarSlice6.setOrientation(Qt.Horizontal)
        self.tab6.layout.addWidget(self.chartSlice6, 4, 0, 2, 11)
        self.tab6.layout.addWidget(self.toolbarSlice6, 5, 0, 1, 8)

        name = 'Срез угла по широте(Высота 1)'
        name_clb = 'Угол'
        self.chartSlice7 = Slice_Matrix(self, self.angle_slice_lon1_lev2, self.dates[index_1:index_2 + 1], self.latitude,
                                   colmap, name, lat_min, lat_max, name_clb)
        self.toolbarSlice7 = NavigationToolbar(self.chartSlice7, self)
        self.toolbarSlice7.setOrientation(Qt.Horizontal)
        self.tab6.layout.addWidget(self.chartSlice7, 1, 12, 2, 11)
        self.tab6.layout.addWidget(self.toolbarSlice7, 2, 12, 1, 8)

        name = 'Срез угла по широте(Высота 2)'
        name_clb = 'Угол'
        self.chartSlice8 = Slice_Matrix(self, self.angle_slice_lon1_lev2, self.dates[index_1:index_2 + 1], self.latitude,
                                   colmap, name, lat_min, lat_max, name_clb)
        self.toolbarSlice8 = NavigationToolbar(self.chartSlice8, self)
        self.toolbarSlice8.setOrientation(Qt.Horizontal)
        self.tab6.layout.addWidget(self.chartSlice8, 4, 12, 2, 11)
        self.tab6.layout.addWidget(self.toolbarSlice8, 5, 12, 1, 8)


if __name__.endswith('__main__'):
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
