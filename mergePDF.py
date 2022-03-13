from PyPDF2 import PdfFileMerger
import os
from datetime import datetime
start_time = datetime.now()
os.chdir('/home/adilet/Desktop/pdfProfiles')
pdfs=[]
for i in range(len(os.listdir())):
    pdfs.append('figure'+str(i)+'.pdf')

merger=PdfFileMerger()
for pdf in pdfs:
    merger.append(pdf)
    print(datetime.now() - start_time)

print('FINISH')
print(datetime.now() - start_time)

    
merger.write('/home/adilet/Desktop/Profiles.pdf')
merger.close()
#for file in os.listdir():
    #pdfs.append(file)
#def Myfun(s):
    #return s[6:-4]
#print(sorted(pdfs,key=Myfun))