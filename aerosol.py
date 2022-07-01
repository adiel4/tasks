import netCDF4 as nc
ds = nc.Dataset('C:/Users/User/Downloads/2012022005_atec.nc')
print(ds)
aerosol = ds['atec'][:]
import matplotlib.pyplot as plt

plt.imshow(aerosol[:][:][0], cmap='coolwarm')
plt.show()