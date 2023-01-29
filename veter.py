import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
ds = nc.Dataset('/home/adilet/Desktop/git/tasks/profile/MERRA2_300.inst3_3d_asm_Np.20080802.SUB.nc')
#East wind - U x
#North - V y
x_day_profile = ds['U'][0][0]
y_day_profile = ds['V'][0][0]
profile = []
angle = []
for i in range(len(x_day_profile)):
    a = []
    b = []
    for j in range(len(x_day_profile[0])):
        a.append(np.sqrt(x_day_profile[i][j]**2+y_day_profile[i][j]**2))
        c = x_day_profile[i][j] / y_day_profile[i][j]
        if x_day_profile[i][j] < 0:
            b.append()
    profile.append(a)

plt.contourf(profile)
plt.show()
