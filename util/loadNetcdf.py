# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Creado: 15 / 05 / 2018
from netCDF4 import Dataset as nc
import pandas as pd
import numpy as np
"""Descripción: """
class LoadNetcdf():
    """"""

    def __init__(self,ncfile):
        self.ncfile=ncfile
        """Constructor for """

    def getInfo(self):
        ncMeta=nc(self.ncfile)
        print(ncMeta.dimensions)
        print(ncMeta.variables)
        print(ncMeta.variables['time'])
        ncMeta.close()

    def leeDiarios(self,ncvar,año):
        datanc=nc(self.ncfile)
        dataset = datanc.variables[ncvar][:]
        lon = datanc.variables['lon'][:]
        lat = datanc.variables['lat'][:]
        head = ["lat", "lon", "ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
        dias = [31,28,31,30,31,30,31,31,30,31,30,31]
        if (año % 4 == 0 and año % 100 != 0 or año % 400 == 0):
            dias[1]=29
        rows = []
        #print(np.shape(dataset))
        for i in range(0,len(lat)):#recorre las latitudes
            for j in range(0,len(lon)):#recorre las longitudes
                row = []
                mes = []
                row.extend([lat[i]])
                row.extend([lon[j]])
                di=0
                df=0
                for m in range(0,12):
                    df=di+dias[m]
                    mes.extend([np.mean(dataset[di:df,i,j])])
                    #print("dia inicio => ", di, " sumado ", dias[m], "dis es  : dia fin =>", df, " el promedio", mes)
                    di=df
                row.extend(mes)
                rows.append(row)
        datadf = pd.DataFrame(rows, columns=head)
        #print(datadf)

        datanc.close()

        return datadf



    def leeMensuales(self, ncvar):
        """lee el archivo nc y crea archivos de texto mensuales """
        datanc = nc(self.ncfile)
        dataset=datanc.variables[ncvar][:]
        lon = datanc.variables['lon'][:]
        lat = datanc.variables['lat'][:]
        head=["lat","lon","ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"]
        rows=[]
        print(np.shape(dataset))
        for i in range(0,len(lat)):#recorre las latitudes
            for j in range(0,len(lon)):#recorre las longitudes
                row = []
                row.extend([lat[i]])
                row.extend([lon[j]])
                row.extend(dataset[:,i,j])
                rows.append(row)

        datadf=pd.DataFrame(rows,columns=head)
        print(datadf)

        datanc.close()

        return datadf

    def creaTrim(self,ncvar,funcion):
        """crea datos trimestrales 4 trimestres de enero a diciembre EFM, AMJ, OND"""
        datanc = nc(self.ncfile)
        dataset = datanc.variables[ncvar][:]
        lon = datanc.variables['lon'][:]
        lat = datanc.variables['lat'][:]
        head = ["lat", "lon","EFM", "AMJ", "JAS", "OND"]
        rows = []
        print(np.shape(dataset))
        for i in range(0, len(lat)):  # recorre las latitudes
            for j in range(0, len(lon)):  # recorre las longitudes
                #row = [lat[i],lon[j],sum(dataset[0:3, i, j])]
                row = []
                row.extend([lat[i]])
                row.extend([lon[j]])
                if(funcion==1):
                    row.extend([sum(dataset[0:3, i, j])])
                    row.extend([sum(dataset[3:6, i, j])])
                    row.extend([sum(dataset[6:9, i, j])])
                    row.extend([sum(dataset[9:12, i, j])])
                else:
                    row.extend([np.mean(dataset[0:3, i, j])])
                    row.extend([np.mean(dataset[3:6, i, j])])
                    row.extend([np.mean(dataset[6:9, i, j])])
                    row.extend([np.mean(dataset[9:12, i, j])])
                rows.append(row)

        datadf = pd.DataFrame(rows, columns=head)
        #print(datadf)

        datanc.close()

        return datadf

    def mes2Trim(self,mensual,funcion):
        head = ["lat", "lon", "EFM", "AMJ", "JAS", "OND"]
        rows = []
        temData = mensual.iloc[:,[0,1]].copy()

        if funcion==1:#para la suma
            temData['EFM'] = mensual['ene'] + mensual['feb'] + mensual['mar']
            temData['AMJ'] = mensual['abr'] + mensual['may'] + mensual['jun']
            temData['JAS'] = mensual['jul'] + mensual['ago'] + mensual['sep']
            temData['OND'] = mensual['oct'] + mensual['nov'] + mensual['dic']
        else: # para el promedio
            temData['EFM'] = mensual.iloc[:, 2:5].mean(axis=1)
            temData['AMJ'] = mensual.iloc[:, 5:8].mean(axis=1)
            temData['JAS'] = mensual.iloc[:, 8:11].mean(axis=1)
            temData['OND'] = mensual.iloc[:, 11:14].mean(axis=1)

        return temData





""" 
####test

filenc="/media/darwin/Darwin/Diarios/TMax/RCP45/tasmax_day_Ecuador_CSIRO-Mk3-6-0_rcp45_2012.nc"

tcn=LoadNetcdf(filenc)
#tcn.getInfo()
#tcn.creaMensuales('precip')
#tcn.creaTrim('precip').to_csv("~/Escritorio/trimestre.csv",sep=";",index=False)
data=tcn.leeDiarios('tmax',2012)
datTrim=tcn.mes2Trim(data,2)
print(datTrim)
"""