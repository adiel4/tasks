import pandas as pd
import numpy as np
import sys,os,datetime
allfiles=[]
for file in os.listdir('/media/adilet/ADI/документы/csv'):
    #print(file+'\n')
    allfiles.append(file)
print(sorted(allfiles))