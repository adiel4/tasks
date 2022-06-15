
from PyQt5.QtWidgets import QFileDialog,QCheckBox,QGridLayout,QTabWidget,QApplication,QWidget,QLabel,QPushButton,QMainWindow,QLineEdit,QComboBox,QToolTip
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QFont
import numpy as np
from PyQt5.QtCore import pyqtSlot, Qt
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from scipy.signal import find_peaks
from mpl_toolkits.basemap import Basemap
import sys
from mpl_toolkits.axes_grid1 import make_axes_locatable

class plotTemp(FigureCanvas):
    def __init__(self, parent, dates, lineOne,lineTwo,  dateTicks, dateLabels, clr1, clr2, w1, w2,name1,name2,latOne,lonOne,dateMin,dateMax):
        plt.close('all')
        self.fig, self.ax = plt.subplots(constrained_layout=True,dpi=120)
        super().__init__(self.fig)
        self.setParent(parent)
        self.l1, = self.ax.plot(dates, lineOne, clr2[0]+'-', linewidth=w2)
        self.l2, = self.ax.plot(dates, lineTwo, clr1[0]+'-', linewidth=w1)
        self.ax.legend([name1+' hPa',name2+' hPa'], loc='best')
        self.ax.set(xlabel='Дата', ylabel='Температура, К',
                    title='Температурный профиль('+str(lonOne)+'$^\circ$N  '+str(latOne)+'$^\circ$E)')
        self.ax.set_xticks(dateTicks)
        self.ax.set_xticklabels(dateLabels, rotation=45)
        self.ax.grid()
        self.ax.set_xlim(dates[dateMin],dates[dateMax])
        
    def col(self,clr):
        self.ax.get_lines()[0].set_color(clr[0])
    def save4(self,name,dpi,docFormat):
        self.fig.savefig(name+docFormat,dpi=dpi)
    
        #fig.tight_layout()
class plotdeltaT(FigureCanvas):
    def __init__(self, parent, dates, dataForPlot, dataForPlot2, dateTicks1, dateLabels1, clr1, clr2, w1, w2,f1,f2,marc1,marc2,name1,name2,latOne,lonOne,dateMin,dateMax):
        plt.close('all')
        self.fig, self.ax = plt.subplots(constrained_layout=True,dpi=120)
        super().__init__(self.fig)
        self.setParent(parent)
        indices, h = find_peaks(dataForPlot, distance=50, height=1)
        indices2, h2 = find_peaks(dataForPlot2, distance=50, height=1)
        self.l1 = self.ax.plot(dates, dataForPlot, clr1[0]+'-', linewidth=w1)
        self.ax.plot(dates, dataForPlot2, clr2[0]+'-', linewidth=w2)
        self.ax.legend([name1+' hPa', name2+' hPa'], loc='best')
        for m in range(len(indices)):
            #self.ax.text(indices[m], 0.1, dates[indices[m]][4:8])
            self.ax.plot(indices[m], h['peak_heights'][m], marc1[0]+f1[0])
        for n in range(len(indices2)):
            #self.ax.text(indices2[n], 0.2, dates[indices2[n]][4:8])
            self.ax.plot(indices2[n], h2['peak_heights']
                         [n], marc2[0]+f2[0])
        self.ax.set(xlabel='Дата', ylabel='STA/LTA', title='STA/LTA профиль('+str(lonOne)+'$^\circ$N   '+str(latOne)+'$^\circ$E)')
        self.ax.set_xticks(dateTicks1)
        self.ax.set_xticklabels(dateLabels1, rotation=90)
        self.ax.grid()
        self.ax.set_xlim(dates[dateMin],dates[dateMax])
        #fig.tight_layout()
    def save5(self,name,dpi,docFormat):
        self.fig.savefig(name+docFormat,dpi=dpi)

    def lineColor(self,color):
        
        pass

class plotdeltaTc(FigureCanvas):
    def __init__(self, parent, dates, dataForPlot, dataForPlot2, dateTicks1, dateLabels1, clr1, clr2, w1, w2,f1,f2,mc1,mc2,latOne,lonOne,dateMin,dateMax):
        plt.close('all')
        self.fig, self.ax = plt.subplots(constrained_layout=True,dpi=120)
        super().__init__(self.fig)
        self.setParent(parent)
        indices, h = find_peaks(dataForPlot, distance=50, height=1)
        indices2, h2 = find_peaks(dataForPlot2, distance=50, height=1)
        self.ax.plot(dates, dataForPlot, clr1[0]+'-', linewidth=w1)
        self.ax.plot(dates, dataForPlot2, clr2[0]+'-', linewidth=w2)
        self.ax.legend([r'$\delta$'+'T', r'$\delta$'+'Tc'], loc='best')
        for m in range(len(indices)):
            #self.ax.text(indices[m], 0.1, dates[indices[m]][4:8])
            self.ax.plot(indices[m], h['peak_heights'][m], mc1[0]+f1[0])
        for n in range(len(indices2)):
            #self.ax.text(indices2[n], 0.2, dates[indices2[n]][4:8])
            self.ax.plot(indices2[n], h2['peak_heights']
                         [n], mc2[0]+f2[0])
        self.ax.set(xlabel='Дата', ylabel=r'$\delta$'+'T',
                    title='Интегральный профиль('+str(lonOne)+'$^\circ$N   '+str(latOne)+'$^\circ$E)')
        self.ax.set_xticks(dateTicks1)
        self.ax.set_xticklabels(dateLabels1, rotation=90)
        self.ax.set_xlim(dates[dateMin],dates[dateMax])
        self.ax.grid()
    def save6(self,name,dpi,docFormat):
        self.fig.savefig(name+docFormat,dpi=dpi)
        
class mapLonLat(FigureCanvas):
    def __init__(self, parent, long, lat, matrix, date,coltop,name,clat,clon,colMap,colBot,crclCol,crclSize,latMinInd,latMaxInd,lonMinInd,lonMaxInd):
        plt.close('all')
        self.fig, self.ax = plt.subplots(constrained_layout=True)
        super().__init__(self.fig)
        self.setParent(parent)
        m = Basemap(projection='merc',llcrnrlat=lat[latMinInd],urcrnrlat=lat[latMaxInd],\
            llcrnrlon=long[lonMinInd],urcrnrlon=long[lonMaxInd],lat_ts=20,resolution='i')
        m.drawcountries()
        m.drawcoastlines(linewidth=0.5)
        xs,ys = np.meshgrid(long,lat)
        x,y = m(xs,ys) 
        m.drawparallels(np.arange(lat[2],lat[-1],2),labels=[1,0,0,0],linewidth=0.1)
        merid = m.drawmeridians(np.arange(long[2],long[-1],3),labels=[0,0,0,1],linewidth=0.1)
        for k in merid:
            try:
                merid[k][1][0].set_rotation(45)
            except:
                pass
            
        highColor = round(coltop/0.2)
        lowColor = round(colBot/0.2)
        self.levels = [0.2*x for x in range(lowColor,highColor+1)]      
        ac = m.contourf(x,y, matrix, self.levels, cmap=colMap)
        self.ax.set(title='Время зондирования:'+date)
        clb = self.fig.colorbar(ac, orientation='vertical')
        clb.ax.set_title(name)
        self.ax.set_xlabel('Долгота',labelpad=50)
        self.ax.set_ylabel('Широта',labelpad=30)
        circle = plt.Circle(m(long[clon],lat[clat]),radius=float(crclSize[:-2])*100000,color=crclCol[0],fill=True)
        self.ax.add_artist(circle)
        self.ax.grid(color='w',linewidth=0.1)        
    def save1(self,name,dpi,docFormat):
        self.fig.savefig(name+docFormat,dpi=dpi)        
    
class mapLevLat(FigureCanvas):
    def __init__(self, parent, level, lat,name):
        plt.close('all')
        self.fig, self.ax = plt.subplots(constrained_layout=True)
        super().__init__(self.fig)
        self.setParent(parent)  
        self.h_km = []
        for i in level:
            a = round(44.33*(1-(i/1013.25)**(1/5.255)),2)
            self.h_km.append(a)
        self.ax.set(xlabel = name,ylabel ='Высота,км')
        self.ax.grid(linewidth=0.1)
    def plot(self,lat,matrix,colMap,date,coltop,colbot,levMin,levMax,latMin,latMax):
        self.ax.set_xlim(lat[latMin],lat[latMax])
        self.ax.set_ylim(self.h_km[levMin],self.h_km[levMax])                
        self.ax.set(title='Время зондирования:'+date)
        highColor = round(coltop/0.2)
        lowColor = round(colbot/0.2)
        levels = [0.2*x for x in range(lowColor,highColor+1)]        
        self.ac = self.ax.contourf(lat, self.h_km, matrix, levels, cmap=colMap)
        self.clb = self.fig.colorbar(self.ac, orientation='vertical')
        self.clb.ax.set_title(r'$\delta$'+'T')
    def save2(self,name,dpi,docFormat):
        self.fig.savefig(name+docFormat,dpi=dpi)          

class plotLatLevDT(FigureCanvas):
    def __init__(self, parent, dtLat, dates,lat,colMap):
        plt.close('all')
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)  
        extent = 0, len(dates),lat[0],lat[-1]
        ac = self.ax.imshow(dtLat,cmap=colMap,interpolation='bilinear',extent=extent)
        self.ax.set(title='Временной график:'+r'$\delta$'+'T')
        #self.ax.set_xticks([dates[0:-1:5]])
        self.ax.set_yticks([x for x in lat[0:-1:5]])
        self.ax.set_yticklabels([x for x in lat[0:-1:5]])
        self.ax.set_xticks([i for i in range(0,len(dates),8)])
        self.ax.set_xticklabels([x[6:8] for x in dates[0:-1:8]],rotation=45)
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.15)
        clb = fig.colorbar(ac, orientation='vertical',cax=cax)
        clb.ax.set_title(r'$\delta$'+'T')
        self.ax.set(xlabel = 'Дата',ylabel ='Широта')
        self.ax.grid()
        fig.tight_layout()
    def save(self,name,dpi,docFormat):
        self.fig.savefig(name+docFormat,dpi=dpi)
        
class plotLatLevDTc(FigureCanvas):
    def __init__(self, parent, dtLatc, dates,lat,colMap):
        plt.close('all')
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)  
        extent = 0, len(dates),lat[0],lat[-1]
        ac = self.ax.imshow(dtLatc,cmap=colMap,interpolation='bilinear',extent=extent)
        self.ax.set(title='Временной график:'+r'$\delta$'+'Tc')
        self.ax.set_yticks([x for x in lat[0:-1:5]])
        self.ax.set_yticklabels([x for x in lat[0:-1:5]])
        self.ax.set_xticks([i for i in range(0,len(dates),8)])
        self.ax.set_xticklabels([x[6:8] for x in dates[0:-1:8]],rotation=45) 
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.15)
        
        clb = fig.colorbar(ac, orientation='vertical',cax=cax)
        clb.ax.set_title(r'$\delta$'+'Tc')
       
        self.ax.set(xlabel = 'Дата',ylabel ='Широта')
        self.ax.grid(linewidth=0.1) 
        fig.tight_layout()
    def save(self,name,dpi,docFormat):
        self.fig.savefig(name+docFormat,dpi=dpi)


class plotLonLevDT(FigureCanvas):
    def __init__(self, parent, dtLon, dates,lon,colMap):
        plt.close('all')
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)  
        extent = 0, len(dates),lon[0],lon[-1]
        ac = self.ax.imshow(dtLon,cmap=colMap,interpolation='bilinear',extent=extent)
        self.ax.set(title='Временной график:'+r'$\delta$'+'T')
        self.ax.set_yticks([x for x in lon[0:-1:5]])
        self.ax.set_yticklabels([x for x in lon[0:-1:5]])
        self.ax.set_xticks([i for i in range(0,len(dates),8)])
        self.ax.set_xticklabels([x[6:8] for x in dates[0:-1:8]],rotation=45)
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.15)
        clb = fig.colorbar(ac, orientation='vertical',cax=cax)
        clb.ax.set_title(r'$\delta$'+'T')
      
        self.ax.set(xlabel = 'Дата',ylabel ='Долгота')
        self.ax.grid(linewidth=0.1) 
        fig.tight_layout()
        
class plotLonLevDTc(FigureCanvas):
    def __init__(self, parent, dtLonc, dates,lon,colMap):
        plt.close('all')
        fig, self.ax = plt.subplots()
        super().__init__(fig)
        self.setParent(parent)  
        extent = 0, len(dates),lon[0],lon[-1]
        ac = self.ax.imshow(dtLonc,cmap=colMap,interpolation='bilinear',extent=extent)
        self.ax.set(title='Временной график:'+r'$\delta$'+'Tc')
        self.ax.set_yticks([x for x in lon[0:-1:5]])
        self.ax.set_yticklabels([x for x in lon[0:-1:5]])
        self.ax.set_xticks([i for i in range(0,len(dates),8)])
        self.ax.set_xticklabels([x[6:8] for x in dates[0:-1:8]],rotation=45)         
        divider = make_axes_locatable(self.ax)
        cax = divider.append_axes("right", size="5%", pad=0.15)
        
        clb = fig.colorbar(ac, orientation='vertical',cax=cax)
        clb.ax.set_title(r'$\delta$'+'Tc')       
        self.ax.set(xlabel = 'Дата',ylabel ='Долгота')
        self.ax.grid(linewidth=0.1) 
        fig.tight_layout()
    def save(self,name,dpi,docFormat):
        plt.savefig(name+docFormat,dpi=dpi)        
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
        
        
        ## СВОЙСТВА КНОПОК #############################
        
        self.btnDwnld = QPushButton('Загрузка',self)
        self.btnDwnld.move(40,230)
        self.btnDwnld.resize(100,30)
        self.btnDwnld.clicked.connect(self.download)
        self.btnDwnld.clicked.connect(self.otrisovka1)
        self.btnDwnld.clicked.connect(self.otrisovka2)
        self.btnExit = QPushButton('Выход',self)
        self.btnExit.move(40,600)
        self.btnExit.resize(50,50)
        #self.btnExit.clicked.connect(self.exit)
        self.btnMap = QPushButton('Карта',self)
        self.btnMap.move(150,250)
        self.btnMap.resize(100,20)
        self.btnMap.clicked.connect(self.dateMap)
        self.btnMap.clicked.connect(self.dateMap2)
        self.btnMap.clicked.connect(self.dateMap3)
        self.btnGraph = QPushButton('График',self)
        self.btnGraph.move(40,270)
        self.btnGraph.resize(60,30)
        self.btnGraph.clicked.connect(self.timePlot)
        
        self.btnPrevMap = QPushButton('<',self)
        self.btnPrevMap.move(150,270)
        self.btnPrevMap.resize(30,30)  
        self.btnPrevMap.clicked.connect(self.PrevMap)
        self.btnPrevMap.clicked.connect(self.dateMap)
        self.btnPrevMap.clicked.connect(self.dateMap2)
        self.btnPrevMap.clicked.connect(self.dateMap3)
        self.btnNextMap = QPushButton('>',self)
        self.btnNextMap.move(180,270)
        self.btnNextMap.resize(30,30)
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
        
        
        ########### СВОЙСТВА  ОКОН ДЛЯ ТЕКСТА ##############
        self.textLTA = QLineEdit(self)
        self.textLTA.move(250,60)
        self.textLTA.setText('105')
        self.textLTA.resize(50,20)
        self.textSTA = QLineEdit(self)
        self.textSTA.move(250,120)
        self.textSTA.setText('21')
        self.textSTA.resize(50,20)
        
        
        ################ СВОЙСТВА ТАБЛИЦ   #####################
        self.boxLevel1 = QComboBox(self)
        self.boxLevel1.move(150,30)
        self.boxLevel1.resize(70,20)
        self.boxLevel2 = QComboBox(self)
        self.boxLevel2.move(150,60)
        self.boxLevel2.resize(70,20)
        self.boxLat1 = QComboBox(self)
        self.boxLat1.move(150,90)
        self.boxLat1.resize(70,20)
        self.boxLon1 = QComboBox(self)
        self.boxLon1.move(150,120)
        self.boxLon1.resize(70,20)
        self.boxLat2 = QComboBox(self)
        self.boxLat2.move(150,150)
        self.boxLat2.resize(70,20)
        self.boxLon2 = QComboBox(self)
        self.boxLon2.move(150,180)
        self.boxLon2.resize(70,20)
        self.boxDates = QComboBox(self)
        self.boxDates.move(150,230)
        self.boxDates.resize(100,20)
        self.boxDates.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        
        ############# ОСНОВНЫЕ СВОЙСТВА ОСНОВНЫХ ВКЛАДОК ###############
        
        self.tabs = QTabWidget(self)
        self.tabs.resize(950,700)
        self.tabs.move(320,0) 

        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tab3 = QWidget(self)
        self.tab4 = QWidget(self)
        self.tab5 = QWidget(self)
        self.tab6 = QWidget(self)
        
        
        self.tabs.addTab(self.tab1, "Карта(Широта/Долгота)")
        self.tabs.addTab(self.tab2, "Карта(Широта/Высота)")
        self.tabs.addTab(self.tab3, "Карта(Долгота/Высота)")
        self.tabs.addTab(self.tab4, "Временной График;STA/LTA") 
        self.tabs.addTab(self.tab5, "Временной График(Широта/Долгота)")
        self.tabs.addTab(self.tab6,'Сохранение Графиков')
        
        self.tab1.layout = QGridLayout(self.tab1)
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.layout = QGridLayout(self.tab2)
        self.tab2.setLayout(self.tab2.layout)
        self.tab3.layout = QGridLayout(self.tab3)
        self.tab3.setLayout(self.tab3.layout)  
        self.tab4.layout = QGridLayout(self.tab4)
        self.tab4.setLayout(self.tab4.layout)
        self.tab5.layout = QGridLayout(self.tab5)
        self.tab5.setLayout(self.tab5.layout)        
        self.tab6.layout = QGridLayout(self.tab6)
        self.tab6.setLayout(self.tab6.layout)
        
        
        self.tab5.layout.setRowStretch(0,1)
        self.tab5.layout.setRowStretch(1,4)
        self.tab5.layout.setRowStretch(4,4)
        self.tab5.layout.setRowStretch(3,1)
        self.tab5.layout.setRowStretch(6,1)
        
        
        ########### ВКЛАДКА: Временной график (Широта/Долгота) #################
        
        self.labDate = QLabel('Даты',self)
        self.tab5.layout.addWidget(self.labDate,0,0,1,1)
        self.boxDates2 = QComboBox(self)
        self.boxDates2.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tab5.layout.addWidget(self.boxDates2,0,1,1,4)
        self.boxDates3 = QComboBox(self)
        self.boxDates3.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.tab5.layout.addWidget(self.boxDates3,0,5,1,4)        
        self.lablat = QLabel('Широта',self)
        self.tab5.layout.addWidget(self.lablat,0,9,1,1)
        self.boxLat3 = QComboBox(self)
        self.tab5.layout.addWidget(self.boxLat3,0,10,1,1)
        self.lablon = QLabel('Долгота',self)
        self.tab5.layout.addWidget(self.lablon,0,11,1,1)
        self.boxLon3 = QComboBox(self)
        self.tab5.layout.addWidget(self.boxLon3,0,12,1,1)
        self.btnMap2 = QPushButton('График',self)
        self.tab5.layout.addWidget(self.btnMap2,0,13,1,2)
        self.btnMap2.clicked.connect(self.latlonMap)  
        self.cmapBox2 = QComboBox(self)
        self.tab5.layout.addWidget(self.cmapBox2,0,15,1,2)
        
        ########### ВКЛАДКА: Сохранение графиков #################
        
        self.labSave1 = QLabel('Карта(Широта/Долгота)',self)
        self.tab6.layout.addWidget(self.labSave1,0,0)
        self.textSave1 = QLineEdit(self)
        self.textSave1.setText('file1')
        self.tab6.layout.addWidget(self.textSave1,0,1)
        self.boxFormats1 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats1,0,2)
        self.textDPI = QLineEdit(self)
        self.textDPI.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI,0,3)
        self.btnSaveMap1 = QPushButton('Сохранить',self)
        self.tab6.layout.addWidget(self.btnSaveMap1,0,4)
        self.btnSaveMap1.clicked.connect(self.Save1)
        
        self.labSave2 = QLabel('Карта(Широта/Высота)',self)
        self.tab6.layout.addWidget(self.labSave2,1,0)
        self.textSave2 = QLineEdit(self)
        self.textSave2.setText('file2')
        self.tab6.layout.addWidget(self.textSave2,1,1)
        self.boxFormats2 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats2,1,2)
        self.textDPI2 = QLineEdit(self)
        self.textDPI2.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI2,1,3)
        self.btnSaveMap2 = QPushButton('Сохранить',self)
        self.tab6.layout.addWidget(self.btnSaveMap2,1,4)        
        self.btnSaveMap2.clicked.connect(self.Save2)
        
        self.labSave3 = QLabel('Карта(Долгота/Высота)',self)
        self.tab6.layout.addWidget(self.labSave3,2,0)
        self.textSave3 = QLineEdit(self)
        self.textSave3.setText('file3')
        self.tab6.layout.addWidget(self.textSave3,2,1)
        self.boxFormats3 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats3,2,2)
        self.textDPI3 = QLineEdit(self)
        self.textDPI3.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI3,2,3)
        self.btnSaveMap3 = QPushButton('Сохранить',self)
        self.tab6.layout.addWidget(self.btnSaveMap3,2,4)    
        self.btnSaveMap3.clicked.connect(self.Save3)
        
        self.labSave4 = QLabel('Температурный профиль',self)
        self.tab6.layout.addWidget(self.labSave4,3,0)
        self.textSave4 = QLineEdit(self)
        self.textSave4.setText('file4')
        self.tab6.layout.addWidget(self.textSave4,3,1)
        self.boxFormats4 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats4,3,2)
        self.textDPI4 = QLineEdit(self)
        self.textDPI4.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI4,3,3)
        self.btnSaveMap4 = QPushButton('Сохранить',self)
        self.tab6.layout.addWidget(self.btnSaveMap4,3,4)     
        self.btnSaveMap4.clicked.connect(self.Save4)
        
        self.labSave5 = QLabel('STA/LTA профиль',self)
        self.tab6.layout.addWidget(self.labSave5,4,0)
        self.textSave5 = QLineEdit(self)
        self.textSave5.setText('file5')
        self.tab6.layout.addWidget(self.textSave5,4,1)
        self.boxFormats5 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats5,4,2)
        self.textDPI5 = QLineEdit(self)
        self.textDPI5.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI5,4,3)
        self.btnSaveMap5 = QPushButton('Сохранить',self)
        self.tab6.layout.addWidget(self.btnSaveMap5,4,4)         
        self.btnSaveMap5.clicked.connect(self.Save5)

        self.labSave6 = QLabel('Интегральный профиль',self)
        self.tab6.layout.addWidget(self.labSave6,5,0)
        self.textSave6 = QLineEdit(self)
        self.textSave6.setText('file6')
        self.tab6.layout.addWidget(self.textSave6,5,1)
        self.boxFormats6 = QComboBox(self)
        self.tab6.layout.addWidget(self.boxFormats6,5,2)
        self.textDPI6 = QLineEdit(self)
        self.textDPI6.setText('300 dpi')
        self.tab6.layout.addWidget(self.textDPI6,5,3)
        self.btnSaveMap6 = QPushButton('Сохранить',self)
        self.tab6.layout.addWidget(self.btnSaveMap6,5,4)   
        self.btnSaveMap6.clicked.connect(self.Save6)
        
        imgFormats = ['.tiff','.png','.eps','.jpeg','.ps','.raw','.svg']
        
        for form in imgFormats:
            self.boxFormats1.addItem(form)
            self.boxFormats2.addItem(form)
            self.boxFormats3.addItem(form)
            self.boxFormats4.addItem(form)
            self.boxFormats5.addItem(form)
            self.boxFormats6.addItem(form)
        ######## ОСНОВНЫЕ СВОЙСТВА ВКЛАДОК НАСТРОЙКИ ################
        
        self.tabsOptions = QTabWidget(self)
        self.tabsOptions.move(20,300)
        self.tabsOptions.resize(300,300)
        
        self.tabLines = QWidget(self)
        self.tabMark = QWidget(self)
        self.tabMap = QWidget(self)
        self.tabLimits = QWidget(self)
        
        self.tabsOptions.addTab(self.tabLines,'Линии')
        self.tabsOptions.addTab(self.tabMark,'Маркеры')
        self.tabsOptions.addTab(self.tabMap, 'Карта')
        self.tabsOptions.addTab(self.tabLimits,'Границы')
        
        self.tabLines.layout = QGridLayout(self.tabLines)
        self.tabLines.setLayout(self.tabLines.layout) 
        self.tabMap.layout = QGridLayout(self.tabMap)
        self.tabMap.setLayout(self.tabMap.layout) 
        self.tabMark.layout = QGridLayout(self.tabMark)
        self.tabMark.setLayout(self.tabMark.layout) 
        self.tabLimits.layout = QGridLayout(self.tabLimits)
        self.tabLimits.setLayout(self.tabLimits.layout)
        
        ############### Вкладка: Свойства линий #####################
        
        self.labPlot1Wid = QLabel('Толщина линий(График 1)', self)
        self.tabLines.layout.addWidget(self.labPlot1Wid,0,0)
        self.labPlot2Wid = QLabel('Толщина линий(График 2)', self)
        self.tabLines.layout.addWidget(self.labPlot2Wid,3,0)
        self.labPlot3Wid = QLabel('Толщина линий(График 3)', self)
        self.tabLines.layout.addWidget(self.labPlot3Wid,6,0)
        self.labPlot1Col = QLabel('Цвета линий(График 1)', self)
        self.tabLines.layout.addWidget(self.labPlot1Col,0,3)
        self.labPlot2Col = QLabel('Цвета линий(График 2)', self)
        self.tabLines.layout.addWidget(self.labPlot2Col,3,3)
        self.labPlot3Col = QLabel('Цвета линий(График 3)', self)   
        self.tabLines.layout.addWidget(self.labPlot3Col,6,3)  
        self.textPlot1Line1Width = QLineEdit(self)
        self.textPlot1Line1Width.setText('1')      
        self.tabLines.layout.addWidget(self.textPlot1Line1Width,1,0)
        self.textPlot1Line2Width = QLineEdit(self)
        self.textPlot1Line2Width.setText('1')
        self.tabLines.layout.addWidget(self.textPlot1Line2Width,2,0)
        self.textPlot2Line1Width = QLineEdit(self)
        self.textPlot2Line1Width.setText('0.8')
        self.tabLines.layout.addWidget(self.textPlot2Line1Width,4,0)
        self.textPlot2Line2Width = QLineEdit(self)
        self.textPlot2Line2Width.setText('0.8')
        self.tabLines.layout.addWidget(self.textPlot2Line2Width,5,0)
        self.textPlot3Line1Width = QLineEdit(self)
        self.textPlot3Line1Width.setText('0.8')
        self.tabLines.layout.addWidget(self.textPlot3Line1Width,7,0)
        self.textPlot3Line2Width = QLineEdit(self)
        self.textPlot3Line2Width.setText('0.8')
        self.tabLines.layout.addWidget(self.textPlot3Line2Width,8,0)
        self.boxPlot1Line1Color = QComboBox(self)
        self.tabLines.layout.addWidget(self.boxPlot1Line1Color,1,3)
        self.boxPlot1Line2Color = QComboBox(self)
        self.tabLines.layout.addWidget(self.boxPlot1Line2Color,2,3)
        self.boxPlot2Line1Color = QComboBox(self)
        self.tabLines.layout.addWidget(self.boxPlot2Line1Color,4,3)
        self.boxPlot2Line2Color = QComboBox(self)
        self.tabLines.layout.addWidget(self.boxPlot2Line2Color,5,3)
        self.boxPlot3Line1Color = QComboBox(self)
        self.tabLines.layout.addWidget(self.boxPlot3Line1Color,7,3)
        self.boxPlot3Line2Color = QComboBox(self)        
        self.tabLines.layout.addWidget(self.boxPlot3Line2Color,8,3)
        
        ############### Вкладка: Свойства маркеров #####################        
        self.labMark = QLabel('Размеры маркеров(График 2)',self)
        self.tabMark.layout.addWidget(self.labMark,0,0,1,4)
        self.markW = QLineEdit(self)
        self.markW.setText('1')
        self.tabMark.layout.addWidget(self.markW,1,0)
        self.markW2 = QLineEdit(self)
        self.markW2.setText('1')
        self.boxcol = QComboBox(self)
        self.tabMark.layout.addWidget(self.boxcol,1,1)
        self.boxcol2 = QComboBox(self)
        self.tabMark.layout.addWidget(self.boxcol2,1,3)         
        self.labMark2 = QLabel('Форма маркеров(График 2)',self)
        self.tabMark.layout.addWidget(self.labMark2,2,0,1,4)
        self.tabMark.layout.addWidget(self.markW2,1,2)
        self.boxMark = QComboBox(self)
        self.tabMark.layout.addWidget(self.boxMark,3,0,1,2)
        self.boxMark2 = QComboBox(self)
        self.tabMark.layout.addWidget(self.boxMark2,3,2,1,2)        
        self.labMark3 = QLabel('Размеры маркеров(График 3)',self)
        self.tabMark.layout.addWidget(self.labMark3,4,0,1,4) 
        self.markW3 = QLineEdit(self)
        self.markW3.setText('1')
        self.tabMark.layout.addWidget(self.markW3,5,0)
        self.markW4 = QLineEdit(self)
        self.markW4.setText('1')  
        self.tabMark.layout.addWidget(self.markW4,5,2)
        self.labMark3 = QLabel('Форма маркеров(График 3)',self)
        self.tabMark.layout.addWidget(self.labMark3,6,0,1,4) 
        self.boxcol3 = QComboBox(self)
        self.tabMark.layout.addWidget(self.boxcol3,5,1)
        self.boxcol4 = QComboBox(self)
        self.tabMark.layout.addWidget(self.boxcol4,5,3)          
        self.boxMark3 = QComboBox(self)
        self.tabMark.layout.addWidget(self.boxMark3,7,0,1,2)
        self.boxMark4 = QComboBox(self)
        self.tabMark.layout.addWidget(self.boxMark4,7,2,1,2)         
        
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
        self.labisC = QLabel('Коэффициент корреляции',self)
        self.tabMap.layout.addWidget(self.labisC,0,0,1,2)
        self.isC = QCheckBox(self)
        self.isC.setChecked(True)
        self.tabMap.layout.addWidget(self.isC,0,2)
        self.cmapBox = QComboBox(self)
        self.tabMap.layout.addWidget(self.cmapBox,0,3,1,2)
        for cmap_id in plt.colormaps():
            self.cmapBox.addItem(cmap_id)
            self.cmapBox2.addItem(cmap_id)
        self.cmapBox.setCurrentText('coolwarm')
        self.cmapBox2.setCurrentText('coolwarm')   
        self.labGr = QLabel('Верхняя граница',self)
        self.tabMap.layout.addWidget(self.labGr,1,0,1,2)
        self.top1 = QLineEdit(self)
        self.top1.setText('1.5')
        self.tabMap.layout.addWidget(self.top1,2,0,1,1)
        self.labGr4 = QLabel('Нижняя граница(Карта 1)',self)
        self.tabMap.layout.addWidget(self.labGr4,1,2,1,3)
        self.bot1 = QLineEdit(self)
        self.bot1.setText('-1.5')
        self.tabMap.layout.addWidget(self.bot1,2,2,1,1)
        self.labGr2 = QLabel('Верхняя граница',self)
        self.tabMap.layout.addWidget(self.labGr2,3,0,1,2)   
        self.top2 = QLineEdit(self)
        self.top2.setText('1.8')
        self.tabMap.layout.addWidget(self.top2,4,0,1,1)
        self.labGr5 = QLabel('Нижняя граница(Карта 2)',self)
        self.tabMap.layout.addWidget(self.labGr5,3,2,1,3)
        self.bot2 = QLineEdit(self)
        self.bot2.setText('-0.2')
        self.tabMap.layout.addWidget(self.bot2,4,2,1,1)        
        self.labGr3 = QLabel('Верхняя граница',self)
        self.tabMap.layout.addWidget(self.labGr3,5,0,1,2)
        self.top3 = QLineEdit(self)
        self.top3.setText('1.8')
        self.tabMap.layout.addWidget(self.top3,6,0,1,1) 
        self.labGr6 = QLabel('Нижняя граница(Карта 2)',self)
        self.tabMap.layout.addWidget(self.labGr6,5,2,1,3)
        self.bot3 = QLineEdit(self)
        self.bot3.setText('-0.2')
        self.tabMap.layout.addWidget(self.bot3,6,2,1,1)             
        self.crclLabel = QLabel('Эпицентр',self)
        self.crclLabelLon = QLabel('Долгота',self)
        self.crclLabelLat = QLabel('Широта',self)
        self.tabMap.layout.addWidget(self.crclLabelLat,8,0)
        self.tabMap.layout.addWidget(self.crclLabelLon,8,2)
        self.tabMap.layout.addWidget(self.crclLabel,7,0)
        self.crcLat = QComboBox(self)
        self.tabMap.layout.addWidget(self.crcLat,8,1)
        self.crcLon = QComboBox(self)
        self.tabMap.layout.addWidget(self.crcLon,8,3,1,2)
        
        self.crclLabelColor = QLabel('Цвет',self)
        self.tabMap.layout.addWidget(self.crclLabelColor,9,0)
        self.crclLabelSize = QLabel('Размер',self)
        self.tabMap.layout.addWidget(self.crclLabelSize,9,2)
        
        self.boxCrclColor = QComboBox(self)
        self.tabMap.layout.addWidget(self.boxCrclColor,9,1)
        
        self.textCrclSize = QLineEdit(self)
        self.textCrclSize.setText('0.3 см')
        self.tabMap.layout.addWidget(self.textCrclSize,9,3)
        
        colors = ['b-синий', 'g-зеленый', 'r-красный', 'c-голубой', 'm-фиолетовый', 'y-желтый', 'k-черный']
        for color in colors:
            self.boxPlot1Line1Color.addItem(color)
            self.boxPlot1Line2Color.addItem(color)
            self.boxPlot2Line1Color.addItem(color)
            self.boxPlot2Line2Color.addItem(color)
            self.boxPlot3Line1Color.addItem(color)
            self.boxPlot3Line2Color.addItem(color)  
            self.boxcol.addItem(color)  
            self.boxcol2.addItem(color)  
            self.boxcol3.addItem(color)  
            self.boxcol4.addItem(color) 
            self.boxCrclColor.addItem(color)
            
        self.boxPlot1Line1Color.setCurrentIndex(0)
        self.boxPlot1Line2Color.setCurrentIndex(1)
        self.boxPlot2Line2Color.setCurrentIndex(2)
        self.boxPlot3Line1Color.setCurrentIndex(3)
        self.boxPlot3Line2Color.setCurrentIndex(5)
        self.boxPlot2Line1Color.setCurrentIndex(4)        
        self.boxDates.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        
        ###############Вкладка: Свойства границ ######################
        self.labLimit1 = QLabel('Границы карты(широта/долгота)',self)
        self.labLimit2 = QLabel('Границы карты(широта/высота)',self)
        self.labLimit3 = QLabel('Границы карты(высота/долгота)',self)
        self.labLimit4 = QLabel('Границы Темп. профиля',self)
        self.labLimit5 = QLabel('Границы STA/LTA проф.',self)
        self.labLimit6 = QLabel('Границы Интег. профиля',self)
        
        self.tabLimits.layout.addWidget(self.labLimit1,0,0,1,4)
        self.tabLimits.layout.addWidget(self.labLimit2,2,0,1,4)
        self.tabLimits.layout.addWidget(self.labLimit3,4,0,1,4)
        self.tabLimits.layout.addWidget(self.labLimit4,6,0,1,4)
        self.tabLimits.layout.addWidget(self.labLimit5,8,0,1,4)
        self.tabLimits.layout.addWidget(self.labLimit6,10,0,1,4)
        
        self.boxLatMin1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMin1,1,0,1,1)
        self.boxLatMax1  = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMax1,1,1,1,1)
        self.boxLonMin1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMin1,1,2,1,1)
        self.boxLonMax1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMax1,1,3,1,1)
        self.boxLatMin2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMin2,3,0,1,1)
        self.boxLatMax2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLatMax2,3,1,1,1)
        self.boxLevMin1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLevMin1,3,2,1,1)
        self.boxLevMax1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLevMax1,3,3,1,1)
        self.boxLevMin2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLevMin2,5,0,1,1)
        self.boxLevMax2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLevMax2,5,1,1,1)
        self.boxLonMin2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMin2,5,2,1,1)
        self.boxLonMax2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxLonMax2,5,3,1,1)
        
        self.boxDatesMinPlot1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMinPlot1,7,0,1,2)
        self.boxDatesMaxPlot1 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMaxPlot1,7,2,1,2)
        self.boxDatesMinPlot2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMinPlot2,9,0,1,2)
        self.boxDatesMaxPlot2 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMaxPlot2,9,2,1,2)
        self.boxDatesMinPlot3 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMinPlot3,11,0,1,2)
        self.boxDatesMaxPlot3 = QComboBox(self)
        self.tabLimits.layout.addWidget(self.boxDatesMaxPlot3,11,2,1,2)
        #self.cmapBox.currentTextChanged.connect(self.colChanged)
        #self.boxPlot1Line1Color.currentTextChanged.connect(self.exit)
        self.filedialog = QFileDialog()
        self.setGeometry(0, 0, 1300, 700)
        self.setWindowTitle('Algorithm')
        self.show()
        
    
    @pyqtSlot()
    def download(self):
        self.boxLat1.clear()
        self.boxLat2.clear()
        self.boxLevel1.clear()
        self.boxLevel2.clear()
        self.boxLon1.clear()
        self.boxLon2.clear()
        self.boxDates.clear()
        self.level = []
        self.latitude = []
        self.longtitude = []
        self.dates = []
        self.tempArray = []
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
                        self.dates.append(a+'-'+str(int(k//60))+':00:00')
                        self.boxDates.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.boxDates2.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.boxDates3.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.boxDatesMinPlot1.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.boxDatesMaxPlot1.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.boxDatesMinPlot2.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.boxDatesMinPlot3.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.boxDatesMaxPlot2.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.boxDatesMaxPlot3.addItem(a+'-'+str(int(k//60))+':00:00')
                        self.tempArray.append(temp[m][:][:][:])
                else:
                    continue
        for i in self.level:
            self.boxLevel1.addItem(str(i))
            self.boxLevel2.addItem(str(i))
            self.boxLevMin1.addItem(str(i))
            self.boxLevMax1.addItem(str(i))
            self.boxLevMin2.addItem(str(i))
            self.boxLevMax2.addItem(str(i))
        for j in self.latitude:
            self.boxLat1.addItem(str(j))
            self.boxLat2.addItem(str(j))
            self.boxLat3.addItem(str(j))
            self.crcLat.addItem(str(j))
            self.boxLatMin1.addItem(str(j))
            self.boxLatMin2.addItem(str(j))
            self.boxLatMax1.addItem(str(j))
            self.boxLatMax2.addItem(str(j))
        for k in self.longtitude:
            self.boxLon1.addItem(str(k))
            self.boxLon2.addItem(str(k))
            self.boxLon3.addItem(str(k))
            self.crcLon.addItem(str(k))
            self.boxLonMin1.addItem(str(k))
            self.boxLonMin2.addItem(str(k))
            self.boxLonMax1.addItem(str(k))
            self.boxLonMax2.addItem(str(k))
        self.boxDates.adjustSize()
        self.boxDates2.setCurrentIndex(0)
        self.boxDates3.setCurrentIndex(len(self.tempArray)-1)      
        self.boxDatesMaxPlot1.setCurrentIndex(len(self.tempArray)-1)
        self.boxDatesMaxPlot2.setCurrentIndex(len(self.tempArray)-1)
        self.boxDatesMaxPlot3.setCurrentIndex(len(self.tempArray)-1)
        self.boxDatesMinPlot2.setCurrentIndex(int(self.textLTA.text()))
        self.boxDatesMinPlot3.setCurrentIndex(int(self.textLTA.text()))
        
        self.boxLatMax1.setCurrentIndex(len(self.latitude)-1)
        self.boxLatMax2.setCurrentIndex(len(self.latitude)-1)
        self.boxLonMax1.setCurrentIndex(len(self.longtitude)-1)
        self.boxLonMax2.setCurrentIndex(len(self.longtitude)-1)
        self.boxLevMax1.setCurrentIndex(len(self.level)-1)
        self.boxLevMax2.setCurrentIndex(len(self.level)-1)
        
    def otrisovka1(self):
       
        self.chart6 = mapLevLat(self, self.level,
                              self.longtitude,'Долгота')        
    def otrisovka2(self):
       
        self.chart5 = mapLevLat(self, self.level,
                              self.latitude,'Широта')        
    def exit(self,value):
        self.chart.col(value)

        
    @pyqtSlot()    
    def dateMap(self):
        lev = float(self.boxLevel1.currentText())
        lev2 = float(self.boxLevel2.currentText())
        date = self.boxDates.currentText()
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())
        isC = self.isC.isChecked()
        tempMatrix = []
        if lta > self.dates.index(date):
            return None

        for i, lat in enumerate(self.latitude):
            row = []
            for j, lon in enumerate(self.longtitude):
                temp1LTA = []
                temp2LTA = []
                for k in self.tempArray[:self.dates.index(date)-1][-lta:]:
                    temp1LTA.append(k[self.level.index(lev)][i][j])
                    temp2LTA.append(k[self.level.index(lev2)][i][j])
                temp1STA = temp1LTA[-sta:]
                temp2STA = temp2LTA[-sta:]
                if isC==True:
                    r = np.corrcoef(temp1STA, temp2STA)[0][1]
                    name = r'$\delta$'+'Tc'
                else:
                    r=1
                    name = r'$\delta$'+'T'
                lS1 = np.std(temp1STA)/np.std(temp1LTA)
                lS2 = np.std(temp2STA)/np.std(temp2LTA)
                if (lS1*lS2)*r >= 0:
                    result = 0
                else:
                    result = (lS1*lS2)*np.abs(r)
                row.append(result)
            tempMatrix.append(row)


        latMin = self.boxLatMin1.currentIndex()
        latMax = self.boxLatMax1.currentIndex()
        lonMin = self.boxLonMin1.currentIndex()
        lonMax = self.boxLonMax1.currentIndex()
        crclCol = self.boxCrclColor.currentText()
        crclSize = self.textCrclSize.text().replace(',','.')
        self.colMap = self.cmapBox.currentText()
        colTop = float(self.top1.text().replace(',','.'))
        colBot = float(self.bot1.text().replace(',','.'))
        clat = self.latitude.index(float(self.crcLat.currentText()))
        clon = self.longtitude.index(float(self.crcLon.currentText()))
        self.chart4 = mapLonLat(self, self.longtitude,
                              self.latitude, tempMatrix, date,colTop,name,clat,clon,self.colMap,colBot,crclCol,crclSize,latMin,latMax,lonMin,lonMax)

        self.tab1.layout.addWidget(self.chart4,0,0)
        self.toolbar = NavigationToolbar(self.chart4, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab1.layout.addWidget(self.toolbar,1,0)      
        pass
    @pyqtSlot()
    def dateMap2(self):
        date = self.boxDates.currentText()
        lattit = float(self.boxLon2.currentText())
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())

        if lta > self.dates.index(date):
            return None
        tempMatrix = []
        for i,lev in enumerate(self.level):
            row = []
            for j, lat in enumerate(self.latitude):
                tempLTA = []
                for k in self.tempArray[:self.dates.index(date)-1][-lta:]:
                    tempLTA.append(k[i][j][self.longtitude.index(lattit)])
                tempSTA = tempLTA[-sta:]
                lS = np.std(tempSTA)/np.std(tempLTA)
                row.append(lS)
            tempMatrix.append(row)
            
            
        coltop = float(self.top2.text().replace(',','.'))
        colBot = float(self.bot2.text().replace(',','.'))

        levMin = self.boxLevMin1.currentIndex()
        levMax = self.boxLevMax1.currentIndex()
        latMin = self.boxLatMin2.currentIndex()
        latMax = self.boxLatMax2.currentIndex()         
        self.chart5.plot(self.latitude,tempMatrix,self.colMap,date, coltop,colBot,levMin,levMax,latMin,latMax)
        self.tab2.layout.addWidget(self.chart5,0,0)
        self.toolbar = NavigationToolbar(self.chart5, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab2.layout.addWidget(self.toolbar,1,0)  
    @pyqtSlot()
    def dateMap3(self):
        date = self.boxDates.currentText()
        long = float(self.boxLat2.currentText())
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())

        if lta > self.dates.index(date):
            return None
        tempMatrix = []
        for i, lev in enumerate(self.level):
            row = []
            for j,lon in enumerate(self.longtitude):
                tempLTA = []
                for k in self.tempArray[:self.dates.index(date)-1][-lta:]:
                    tempLTA.append(k[i][self.latitude.index(long)][j])
                tempSTA = tempLTA[-sta:]
                lS = np.std(tempSTA)/np.std(tempLTA)
                row.append(lS)
            tempMatrix.append(row)
            
            

        coltop = float(self.top3.text().replace(',','.'))
        colbot = float(self.bot3.text().replace(',','.'))

        levMin = self.boxLevMin2.currentIndex()
        levMax = self.boxLevMax2.currentIndex()
        lonMin = self.boxLonMin2.currentIndex()
        lonMax = self.boxLonMax2.currentIndex()         
        self.chart6.plot(self.longtitude,tempMatrix,self.colMap,date, coltop,colbot,levMin,levMax,lonMin,lonMax)
        self.tab3.layout.addWidget(self.chart6,0,0)
        self.toolbar = NavigationToolbar(self.chart6, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab3.layout.addWidget(self.toolbar,1,0)
        
        
        
    @pyqtSlot()
    def NextMap(self):
        ind = self.boxDates.currentIndex()
        self.boxDates.setCurrentIndex(ind+1)
    @pyqtSlot()
    def PrevMap(self):
        ind = self.boxDates.currentIndex()
        self.boxDates.setCurrentIndex(ind-1)    
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
            self.tempLevOneCoorOne.append(k[self.level.index(levOne)][self.latitude.index(latOne)][self.longtitude.index(lonOne)])
            self.tempLevOneCoorTwo.append(k[self.level.index(levTwo)][self.latitude.index(latOne)][self.longtitude.index(lonOne)])
        dateTicks = self.dates[0:-1:30]
        dateLabels = []   
        
        for i in dateTicks:
            dateLabels.append(i[4:8])
        width1 = float(self.textPlot1Line2Width.text().replace(',','.'))
        width2 = float(self.textPlot1Line1Width.text().replace(',','.'))
        clr1 = self.boxPlot1Line2Color.currentText()
        clr2 = self.boxPlot1Line1Color.currentText()

        name1 = self.boxLevel1.currentText()
        name2 = self.boxLevel2.currentText()
        dateMin1 = self.boxDatesMinPlot1.currentIndex()
        dateMax1 = self.boxDatesMaxPlot1.currentIndex()
        self.chart = plotTemp(self, self.dates,self.tempLevOneCoorOne,self.tempLevOneCoorTwo, dateTicks, dateLabels, clr1, clr2, width1, width2,name1,name2,latOne,lonOne,dateMin1,dateMax1)
        self.tab4.layout.addWidget(self.chart,0,0,1,2)
        self.toolbar = NavigationToolbar(self.chart, self)
        self.toolbar.setOrientation(Qt.Horizontal)
        self.tab4.layout.addWidget(self.toolbar,1,0,1,1)       
        
        
        
        arrayLev1 = []
        arrayLev2 = []
        integArray = []
        integArraywR = []
      
        
        for i in range(lta,len(self.tempLevOneCoorTwo),1):
            index1= i-lta
            index2 = i+1
            lTA = np.std(self.tempLevOneCoorTwo[index1:index2])
            sTA = np.std(self.tempLevOneCoorTwo[:i][-sta:])
            lTA2 = np.std(self.tempLevOneCoorOne[index1:index2])
            sTA2 = np.std(self.tempLevOneCoorOne[:i][-sta:])   
            stalta = sTA/lTA
            stalta2 = sTA2/lTA2     
            arrayLev1.append(stalta)
            arrayLev2.append(stalta2)
            integArray.append(stalta*stalta2)
            coef = np.corrcoef(self.tempLevOneCoorTwo[:i][-sta:],self.tempLevOneCoorOne[:i][-sta:])[0][1]            
            
        
            if stalta*stalta2*coef >=0:
                result = 0
                integArraywR.append(result)
            else:
                result = stalta*stalta2*np.abs(coef)
                integArraywR.append(result)
        
        dateTicks = self.dates[lta:][0:-1:30]
        dateLabels = []
        for i in dateTicks:
            dateLabels.append(i[4:8])

        clr1 = self.boxPlot2Line1Color.currentText()
        clr2 = self.boxPlot2Line2Color.currentText()
        clr3 = self.boxPlot3Line1Color.currentText()
        clr4 = self.boxPlot3Line2Color.currentText()

        width1 = float(self.textPlot2Line1Width.text().replace(',','.'))
        width2 = float(self.textPlot2Line2Width.text().replace(',','.'))
        width3 = float(self.textPlot3Line1Width.text().replace(',','.'))
        width4 = float(self.textPlot3Line2Width.text().replace(',','.'))
        
        form1 = self.boxMark.currentText()
        form2 = self.boxMark2.currentText()
        form3 = self.boxMark3.currentText()
        form4 = self.boxMark4.currentText()
        
        marCol1 = self.boxcol.currentText()
        marCol2 = self.boxcol2.currentText()
        marCol3 = self.boxcol3.currentText()
        marCol4 = self.boxcol4.currentText()
        dateMin2 = self.boxDatesMinPlot2.currentIndex()-int(self.textLTA.text())
        dateMax2 = self.boxDatesMaxPlot2.currentIndex()-int(self.textLTA.text())
        dateMin3 = self.boxDatesMinPlot3.currentIndex()-int(self.textLTA.text())
        dateMax3 = self.boxDatesMaxPlot3.currentIndex()-int(self.textLTA.text())    
        self.chart2 = plotdeltaT(
            self, self.dates[lta:], arrayLev1,arrayLev2, dateTicks, dateLabels, clr1, clr2, width1, width2,form1,form2,marCol1,marCol2,name1,name2,latOne,lonOne,dateMin2,dateMax2)
        
        self.toolbar2 = NavigationToolbar(self.chart2, self)
        self.toolbar2.setOrientation(Qt.Horizontal)

        self.chart3 = plotdeltaTc(
            self, self.dates[lta:], integArray, integArraywR, dateTicks, dateLabels, clr3, clr4, width3, width4,form3,form4,marCol3,marCol4,latOne,lonOne,dateMin3,dateMax3)
        self.toolbar3 = NavigationToolbar(self.chart3, self)
        self.toolbar3.setOrientation(Qt.Horizontal)
        
        self.tab4.layout.addWidget(self.chart2,2,0,1,1)
        self.tab4.layout.addWidget(self.toolbar2,3,0,1,1)  
        self.tab4.layout.addWidget(self.chart3,2,1,1,1)
        self.tab4.layout.addWidget(self.toolbar3,3,1,1,1)          
        
    def latlonMap(self):
        index1 = self.boxDates2.currentIndex()
        index2 = self.boxDates3.currentIndex()
        lta = int(self.textLTA.text())
        sta = int(self.textSTA.text())
        latitude = self.boxLat3.currentIndex()
        longtitude = self.boxLon3.currentIndex()
        if index1<lta:
            return
        levOne = self.boxLevel1.currentIndex()
        levTwo = self.boxLevel2.currentIndex()
        
        latdT = []
        londT = []
        latdTc = []
        londTc = []
        for i,lat in enumerate(self.latitude):
            rowdT1 = []
            rowdTc1 = []
            for k in range(index1,index2+1,1):
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
                coef = np.corrcoef(array1[-sta:],array3[-sta:])[0][1]
                sL1 = stalat/ltalat
                sL3 = stalat2/ltalat2
                if sL1*sL3*coef >=0:
                    result = 0
                    rowdTc1.append(result)
                else:
                    result = sL1*sL3*np.abs(coef)
                    rowdTc1.append(result)
                rowdT1.append(sL1)
            latdT.append(rowdT1)
            latdTc.append(rowdTc1)
            
        for j,lon in enumerate(self.longtitude):
            rowdT2 = []
            rowdTc2 = []
            for y in range(index1,index2+1,1):
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
                coef = np.corrcoef(array2[-sta:],array4[-sta:])[0][1]
                sL2 = stalon/ltalon
                sL4 = stalon2/ltalon2
                if sL2*sL4*coef >=0:
                    result = 0
                    rowdTc2.append(result)
                else:
                    result = sL2*sL4*np.abs(coef)
                    rowdTc2.append(result)
                rowdT2.append(sL2*sL4)
            londTc.append(rowdTc2)
            londT.append(rowdT2)
                
        colmap = self.cmapBox2.currentText()
        self.chart4 = plotLatLevDT(self,latdT, self.dates[index1:index2+1],self.latitude,colmap)
        self.toolbar4 = NavigationToolbar(self.chart4, self)
        self.toolbar4.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chart4,1,0,2,8)
        self.tab5.layout.addWidget(self.toolbar4,3,0,1,4)                           
        
        self.chart6 = plotLatLevDTc(self,latdTc, self.dates[index1:index2+1],self.latitude,colmap)
        self.toolbar6 = NavigationToolbar(self.chart6, self)
        self.toolbar6.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chart6,1,9,2,8)
        self.tab5.layout.addWidget(self.toolbar6,3,9,1,4)  
        
        self.chart5 = plotLonLevDT(self,londT, self.dates[index1:index2+1],self.longtitude,colmap)
        self.toolbar5 = NavigationToolbar(self.chart5, self)
        self.toolbar5.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chart5,4,0,2,8)
        self.tab5.layout.addWidget(self.toolbar5,6,0,1,4) 
        
        self.chart7 = plotLonLevDTc(self,londTc, self.dates[index1:index2+1],self.longtitude,colmap)
        self.toolbar7 = NavigationToolbar(self.chart7, self)
        self.toolbar7.setOrientation(Qt.Horizontal)
        self.tab5.layout.addWidget(self.chart7,4,9,2,8)
        self.tab5.layout.addWidget(self.toolbar7,6,9,1,4) 
    def Save1(self):
        form = self.boxFormats1.currentText()
        dpi  = int(self.textDPI.text()[:3])
        name = self.textSave1.text()
        directory = str(QFileDialog.getExistingDirectory(self,'Выберите папку для сохранения'))        
        self.chart4.save1(directory+'/'+name,dpi,form)
    def Save2(self):
        form = self.boxFormats2.currentText()
        dpi  = int(self.textDPI2.text()[:3])
        name = self.textSave2.text()
        directory = str(QFileDialog.getExistingDirectory(self,'Выберите папку для сохранения'))        
        self.chart5.save2(directory+'/'+name,dpi,form)
    def Save3(self):
        form = self.boxFormats3.currentText()
        dpi  = int(self.textDPI3.text()[:3])
        name = self.textSave3.text()
        directory = str(QFileDialog.getExistingDirectory(self,'Выберите папку для сохранения'))        
        self.chart6.save2(directory+'/'+name,dpi,form)        
    def Save4(self):
        form = self.boxFormats4.currentText()
        dpi  = int(self.textDPI4.text()[:3])
        name = self.textSave4.text()
        directory = str(QFileDialog.getExistingDirectory(self,'Выберите папку для сохранения'))
        self.chart.save4(directory+'/'+name,dpi,form)
    def Save5(self):
        form = self.boxFormats5.currentText()
        dpi  = int(self.textDPI5.text()[:3])
        name = self.textSave5.text()
        directory = str(QFileDialog.getExistingDirectory(self,'Выберите папку для сохранения'))        
        self.chart2.save5(directory+'/'+name,dpi,form)
    def Save6(self):
        form = self.boxFormats6.currentText()
        dpi  = int(self.textDPI6.text()[:3])
        name = self.textSave6.text()
        directory = str(QFileDialog.getExistingDirectory(self,'Выберите папку для сохранения'))        
        self.chart3.save6(directory+'/'+name,dpi,form)
if __name__.endswith('__main__'):
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())