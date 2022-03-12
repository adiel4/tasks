import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import os,sys,time
import matplotlib as mpl
start_time = datetime.now()
allProfileFiles=[]
for file in os.listdir('/home/adilet/Рабочий стол/profiles'):
    if file[-2:]=='c4' or file[-2:]=='nc':
        allProfileFiles.append(file)
def Myfn(s):
    s=s.split('.')
    m=s[2]
    d=m[2:4]+'/'+m[4:6]+'/'+m[6:8]
    return datetime.strptime(d,'%y/%m/%d')
allProfileFiles=sorted(allProfileFiles,key=Myfn)

for i,file in enumerate(allProfileFiles[0:1]):    
    fn='/home/adilet/Рабочий стол/profiles/'+file
    ds=nc.Dataset(fn)    
    temp=ds['T'][:]
    timZond=ds['time'][:]
    lev=ds['lev'][:]
    lon=ds['lon'][:]
    lat=ds['lat'][:]
    levels1=np.linspace(195.97,259.07,17)
    levels2=np.linspace(9.96,60.73,17)
    cmap=plt.colormaps['coolwarm']
    ylat=['39','41','43','45']
    xlon=['68','71','74','77','80','83']



    plt.subplot(3,1,1)
    cs1=plt.contourf(temp[0][0][:][:],levels1,cmap=cmap)
    plt.title('350 hPa')
    plt.xlabel(xlon)
    plt.ylabel(ylat)
    cbar1=plt.colorbar(cs1)
    plt.subplot(3,1,2)
    cs2=plt.contourf(temp[0][3][:][:],levels1,cmap=cmap)
    plt.clim(min(levels1),max(levels1))
    plt.title('100 hPa')
    cbar2=plt.colorbar(cs2)    
    plt.subplot(3,1,3)
    diff=np.subtract(temp[0][0][:][:],temp[0][3][:][:])
    cs3=plt.contourf(diff,levels2,cmap=cmap)
    name=file.split('.')[2]
    datZond=name[0:4]+'-'+name[4:6]+'-'+name[6:8]
    plt.title('dT '+datZond+' '+'00:00:00')
    plt.clim(min(levels2),max(levels2))
    cba3r=plt.colorbar(cs3)
    plt.tight_layout()
    plt.show()