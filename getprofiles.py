import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
fn='/home/adilet/Downloads/profiles/MERRA2_200.inst3_3d_asm_Np.19920701.SUB.nc'
ds=nc.Dataset(fn)
print(ds)
lat=ds['lat'][:]
tim=ds['time'][:]
lon=ds['lon'][:]
lev=ds['lev'][:]
temp=ds['T'][:]
#data=np.array(temp[0][0][:][:])
#print(temp[0][0][:][:])
for i in range(0,(len(lev))):
    row=len(lev)
    fig,ax=plt.subplots(row,1)
    im = ax.imshow(temp[0][i][:][:],cmap='jet')
    ax.set_xticks(np.arange(len(lon)), labels=lon)
    ax.set_yticks(np.arange(len(lat)), labels=lat)
    plt.title('')
    plt.setp(ax.get_xticklabels(), rotation=90, ha="right",rotation_mode="anchor")
    fig.tight_layout()
    plt.show()

