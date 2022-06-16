import os
from netCDF4 import Dataset
import numpy as np


class SomeDataset:
    def __init__(self, fp):
        self.dates = None
        self.temp_matrix = None
        self.vrem = None
        self.level = None
        self.latitude = None
        self.longtitude = None
        self.filepath = fp
        self.files = [x for x in os.listdir(self.filepath) if x.endswith('nc') or x.endswith('nc4')]

    def set_parameters(self):
        ds = Dataset(self.filepath + '/' + self.files[0])
        self.longtitude = ds['lon'][:]
        self.latitude = ds['lat'][:]
        self.level = ds['lev'][:]
        self.vrem = ds['time'][:]

    def create_temp_matrix(self):
        self.temp_matrix = []
        self.dates = []
        for file in self.files:
            ds = Dataset(self.filepath + '/' + file)
            for i in range(len(self.vrem)):
                temp = ds['T'][:]
                temp = temp[i][:][:][:]
                self.temp_matrix.append(temp)
                self.dates.append(file.split('.')[2] + '-' + str(int(self.vrem[i] // 60)) + ':00:00')

    def create_temparray_lev_lat_lon(self, lat_index, lon_index, lev_index):
        array = []
        for temp_index in range(len(self.temp_matrix)):
            t = self.temp_matrix[temp_index][lev_index][lat_index][lon_index]
            array.append(t)
        return array

    def create_ltasta_с_lev_lat_lon(self, lat_index, lon_index, lev1_index, lev2_index, lta, sta, date_index):
        if date_index < lta:
            print('fuck you')
            return None
        temparray = self.temp_matrix[date_index - lta:date_index]
        tarray1 = []
        tarray2 = []
        for temp in temparray:
            t1 = temp[lev1_index][lat_index][lon_index]
            t2 = temp[lev2_index][lat_index][lon_index]
            tarray1.append(t1)
            tarray2.append(t2)
        tarray11 = tarray1[-sta:]
        tarray21 = tarray2[-sta:]
        lta1 = np.std(tarray1)
        lta2 = np.std(tarray2)
        sta1 = np.std(tarray11)
        sta2 = np.std(tarray21)
        sl1, sl2 = sta1 / lta1, sta2 / lta2
        r = np.corrcoef(tarray11, tarray21)[0][1]
        if (sl1 * sl2) * r >= 0:
            return 0
        else:
            return (sl1 * sl2) * np.abs(r)

    def create_ltasta_lev_lat_lon(self, lat_index, lon_index, lev1_index, lev2_index, lta, sta, date_index):
        if date_index < lta:
            print('fuck you')
            return None
        temparray = self.temp_matrix[date_index - lta:date_index]
        tarray1 = []
        tarray2 = []
        for temp in temparray:
            t1 = temp[lev1_index][lat_index][lon_index]
            t2 = temp[lev2_index][lat_index][lon_index]
            tarray1.append(t1)
            tarray2.append(t2)
        tarray11 = tarray1[-sta:]
        tarray21 = tarray2[-sta:]
        lta1 = np.std(tarray1)
        lta2 = np.std(tarray2)
        sta1 = np.std(tarray11)
        sta2 = np.std(tarray21)
        sl1, sl2 = sta1 / lta1, sta2 / lta2
        return sl1 * sl2

# import matplotlib.pyplot as plt
#
# while True:
#     filepath = input('Type files path:')
#     if filepath == 'exit':
#         print('Process ended')
#         break
#     dataset1 = SomeDataset(filepath)
#     dataset1.set_parameters()
#     dataset1.create_temp_matrix()
#     for i in range(105,len(dataset1.dates)):
#         tempMatrix = []
#         for lat_index in range(len(dataset1.latitude)):
#             row = []
#             for lon_index in range(len(dataset1.longtitude)):
#                 temp = dataset1.create_ltasta_lev_lat_lon(lat_index,lon_index,0,1,105,21,i)
#                 row.append(temp)
#             tempMatrix.append(row)
#         a = plt.contourf(dataset1.longtitude,dataset1.latitude,tempMatrix,[0,0.2,0.4,0.6,0.8,1])
#         plt.colorbar(a)
#         plt.show()
