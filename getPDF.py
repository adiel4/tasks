import netCDF4 as nc
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import os,time
start_time = datetime.now()
allProfileFiles=[]
for file in os.listdir('/home/adilet/Downloads/profiles'):
    if file[-2:]=='c4' or file[-2:]=='nc':
        allProfileFiles.append(file)
def Myfn(s):
    s=s.split('.')
    m=s[2]
    d=m[2:4]+'/'+m[4:6]+'/'+m[6:8]
    return datetime.strptime(d,'%y/%m/%d')
allProfileFiles=sorted(allProfileFiles,key=Myfn)



for i,file in enumerate(allProfileFiles):
    pdf=PdfPages('/home/adilet/Desktop/pdfProfiles/figure'+str(i)+'.pdf')
    fn='/home/adilet/Downloads/profiles/'+file
    ds=nc.Dataset(fn)    
    temp=ds['T'][:]
    timZond=ds['time'][:]
    lev=ds['lev'][:]
    lon=ds['lon'][:]
    lat=ds['lat'][:]

    
    

    
    for j,zondTim in enumerate(timZond):
        name=file.split('.')[2]
        datZond=name[0:4]+'-'+name[4:6]+'-'+name[6:8]        
        plot3name=str(timedelta(minutes=zondTim))
        profile1=temp[j][0][:][:]
        profile2=temp[j][3][:][:]
        profile3=np.subtract(temp[j][0][:][:],temp[j][3][:][:])
        
        levels1=np.linspace(195.97,259.07,17)
        levels2=np.linspace(9.96,60.73,17)        
        cmap=plt.colormaps['coolwarm']        
        lonxticks=[68,71,74,77,80,83]
        latyticks=[39,41,43,45] 
        lonxlabel=['68 \N{DEGREE SIGN}E','71 \N{DEGREE SIGN}E','74 \N{DEGREE SIGN}E','77 \N{DEGREE SIGN}E','80 \N{DEGREE SIGN}E','83 \N{DEGREE SIGN}E']
        latylabel=['39 \N{DEGREE SIGN}N','41 \N{DEGREE SIGN}N','43 \N{DEGREE SIGN}N','45 \N{DEGREE SIGN}N']        
        
        
        plt.subplot(3,1,1)
        cs1=plt.contourf(lon,lat,profile1,levels1,cmap=cmap)
        plt.title('350 hPa')
        plt.xticks(ticks=lonxticks,labels=lonxlabel)
        plt.yticks(ticks=latyticks,labels=latylabel)
        plt.grid(color='dimgray', linestyle='--', linewidth=1)
        cbar1=plt.colorbar(cs1)
        
        

        plt.subplot(3,1,2)
        cs2=plt.contourf(lon,lat,profile2,levels1,cmap=cmap)
        plt.clim(min(levels1),max(levels1))
        plt.title('100 hPa')
        plt.xticks(ticks=lonxticks,labels=lonxticks)
        plt.yticks(ticks=latyticks,labels=latylabel)
        plt.grid(color='dimgray', linestyle='--', linewidth=1)
        cbar2=plt.colorbar(cs2) 
        
        
        plt.subplot(3,1,3)
        cs3=plt.contourf(lon,lat,profile3,levels2,cmap=cmap)
        plt.title('dT '+datZond+' '+plot3name)
        plt.clim(min(levels2),max(levels2))
        cba3r=plt.colorbar(cs3)
        plt.xticks(ticks=lonxticks,labels=lonxticks)
        plt.yticks(ticks=latyticks,labels=latylabel)
        
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.08,right=0.898,left=0.126,top=0.922,hspace=0.65,wspace=0.2)
        plt.grid(color='dimgray', linestyle='--', linewidth=1)
        f=plt.gcf()
        f.set_size_inches(6.69,8.27)
        pdf.savefig()
        plt.close()
    print(datetime.now() - start_time)
    pdf.close()
