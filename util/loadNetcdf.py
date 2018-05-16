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

    def creaMensuales(self, ncvar):
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

    def creaTrim(self,ncvar):
        """crea datos trimestrales 4 trimestres de enero a diciembre EFM, AMJ, OND"""
        datanc = nc(self.ncfile)
        dataset = datanc.variables[ncvar][:]
        lon = datanc.variables['lon'][:]
        lat = datanc.variables['lat'][:]
        head = ["lat", "lon","ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic","EFM", "AMJ", "JAS", "OND"]
        rows = []
        print(np.shape(dataset))
        for i in range(0, len(lat)):  # recorre las latitudes
            for j in range(0, len(lon)):  # recorre las longitudes
                #row = [lat[i],lon[j],sum(dataset[0:3, i, j])]
                row = []
                row.extend([lat[i]])
                row.extend([lon[j]])
                row.extend(dataset[:, i, j])
                row.extend([sum(dataset[0:3, i, j])])
                row.extend([sum(dataset[3:6, i, j])])
                row.extend([sum(dataset[6:9, i, j])])
                row.extend([sum(dataset[9:12, i, j])])
                rows.append(row)

        datadf = pd.DataFrame(rows, columns=head)
        print(datadf)

        datanc.close()

        return datadf



####test

filenc="/media/darwin/Darwin/Mensuales/Prec/RCP45/pr_day_Ecuador_Ensamble_rcp45_2011.nc"

tcn=LoadNetcdf(filenc)
#tcn.getInfo()
#tcn.creaMensuales('precip')
tcn.creaTrim('precip').to_csv("~/Escritorio/trimestre.csv",sep=";",index=False)


