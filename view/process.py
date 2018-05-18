# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Creado: 15 / 05 / 2018
from pandas._libs.hashtable import na_sentinel

from util import listFiles as lf, loadNetcdf as lnc
import pandas as pd, numpy as np


"""Descripción: """
class Process():
    """"""

    def __init__(self,rootPath):
        """Constructor for Process"""
        self.rootPath=rootPath

    def procesPeriod(self,añoi,añof,var='precip',funcion=1):
        """Une los archivos generados por cada año en un solo dataframe"""
        cab=["lat", "lon"]
        for i in range(añoi,añof+1):
            cab.extend(['EFM'+str(i),'AMJ'+str(i),'JAS'+str(i),'OND'+str(i)])
            ncfile=self.rootPath+str(i)+".nc"
            nc=lnc.LoadNetcdf(ncfile=ncfile)
            print("procesando archivo ",ncfile)
            if(i==añoi):
                dattemp = nc.creaTrim(var,funcion)
            else:
                dattemp = pd.concat([dattemp,nc.creaTrim(var,funcion).loc[:,["EFM", "AMJ", "JAS", "OND"]]],axis=1,join='inner')
        dattemp.columns = cab
        #print(np.shape(dattemp))
        #print(len(cab))
        """"Genera promedios por trimestre y agrega las columnas"""
        dattemp["EFM_TOT"] = dattemp.loc[:, dattemp.columns.map(lambda x: x.startswith("EFM"))].mean(axis=1)
        dattemp["AMJ_TOT"] = dattemp.loc[:, dattemp.columns.map(lambda x: x.startswith("AMJ"))].mean(axis=1)
        dattemp["JAS_TOT"] = dattemp.loc[:, dattemp.columns.map(lambda x: x.startswith("JAS"))].mean(axis=1)
        dattemp["SON_TOT"] = dattemp.loc[:, dattemp.columns.map(lambda x: x.startswith("OND"))].mean(axis=1)
        ##
        return dattemp

    def procesPeriodDia(self,añoi,añof,var='precip',funcion=1):
        """Une los archivos generados por cada año en un solo dataframe" a partir de los archivos diarios"""
        cab=["lat", "lon"]
        for i in range(añoi,añof+1):
            cab.extend(['EFM'+str(i),'AMJ'+str(i),'JAS'+str(i),'OND'+str(i)])
            ncfile=self.rootPath+str(i)+".nc"
            nc=lnc.LoadNetcdf(ncfile=ncfile)
            print("procesando archivo ",ncfile)
            if(i==añoi):
                data = nc.leeDiarios(var, i)
                dattemp = nc.mes2Trim(data, funcion)
            else:
                data = nc.leeDiarios(var, i)
                datTrim = nc.mes2Trim(data, funcion)
                dattemp = pd.concat([dattemp,datTrim.loc[:,["EFM", "AMJ", "JAS", "OND"]]],axis=1,join='inner')
        dattemp.columns = cab
        #print(np.shape(dattemp))
        #print(len(cab))
        """"Genera promedios por trimestre y agrega las columnas"""
        dattemp["EFM_TOT"] = dattemp.loc[:, dattemp.columns.map(lambda x: x.startswith("EFM"))].mean(axis=1)
        dattemp["AMJ_TOT"] = dattemp.loc[:, dattemp.columns.map(lambda x: x.startswith("AMJ"))].mean(axis=1)
        dattemp["JAS_TOT"] = dattemp.loc[:, dattemp.columns.map(lambda x: x.startswith("JAS"))].mean(axis=1)
        dattemp["SON_TOT"] = dattemp.loc[:, dattemp.columns.map(lambda x: x.startswith("OND"))].mean(axis=1)
        ##
        return dattemp


######seccion de ejecucion
#/media/drosero/Darwin/Mensuales/Prec/RCP45/pr_day_Galapagos_IPSL-CM5A-MR_rcp45_2064.nc
#guar="/media/drosero/Datos/DATOSTCN/"
guar="/home/darwin/Documentos/Datos/Chrips/DATOSTCN/"
"""
####Datos de precipitacion con rcp 45
preci="/media/drosero/Darwin/Mensuales/Prec/RCP45/pr_day_Ecuador_IPSL-CM5A-MR_rcp45_"
####periodo 2011-2030
pr=Process(preci)
data=pr.procesPeriod(2011,2030)
data.to_csv(guar+"rr_2011-2030rcp45.csv", sep=";", index=False, encoding="utf-8")
####periodo 2031-2050
data=pr.procesPeriod(2031,2050)
data.to_csv(guar+"rr_2031-2050rcp45.csv", sep=";", index=False, encoding="utf-8")
####periodo 2051-2070
data=pr.procesPeriod(2051,2070)
data.to_csv(guar+"rr_2051-2070rcp45.csv", sep=";", index=False, encoding="utf-8")

####Datos de precipitacion con rcp 85
preci="/media/drosero/Darwin/Mensuales/Prec/RCP85/pr_day_Ecuador_IPSL-CM5A-MR_rcp85_"
####periodo 2011-2030
pr=Process(preci)
data=pr.procesPeriod(2011,2030)
data.to_csv(guar+"rr_2011-2030rcp85.csv", sep=";", index=False, encoding="utf-8")
####periodo 2031-2050
data=pr.procesPeriod(2031,2050)
data.to_csv(guar+"rr_2031-2050rcp85.csv", sep=";", index=False, encoding="utf-8")
####periodo 2051-2070
data=pr.procesPeriod(2051,2070)
data.to_csv(guar+"rr_2051-2070rcp85.csv", sep=";", index=False, encoding="utf-8")
"""
#################################################################################
#################################################################################
####Datos de temperatura maxima con rcp 45
preci="/media/darwin/Darwin/Diarios/TMax/RCP45/tasmax_day_Ecuador_Ensamble_rcp45_"
####periodo 2011-2030
pr=Process(preci)
data=pr.procesPeriodDia(2011,2030,var='tmax',funcion=2)
data.to_csv(guar+"tmax_2011-2030rcp45.csv", sep=";", index=False, encoding="utf-8")
####periodo 2031-2050
data=pr.procesPeriodDia(2031,2050,var='tmax',funcion=2)
data.to_csv(guar+"tmax_2031-2050rcp45.csv", sep=";", index=False, encoding="utf-8")
####periodo 2051-2070
data=pr.procesPeriodDia(2051,2070,var='tmax',funcion=2)
data.to_csv(guar+"tmax_2051-2070rcp45.csv", sep=";", index=False, encoding="utf-8")

####Datos de temperatura maxima con rcp 85
#/media/drosero/Darwin/Mensuales/TMax/RCP85/tasmax_day_Ecuador_IPSL-CM5A-MR_rcp85_2022.nc
#preci="/media/drosero/Darwin/Mensuales/TMax/RCP85/tasmax_day_Ecuador_IPSL-CM5A-MR_rcp85_"
preci="/media/darwin/Darwin/Diarios/TMax/RCP85/tasmax_day_Ecuador_Ensamble_rcp85_"
####periodo 2011-2030
pr=Process(preci)
data=pr.procesPeriodDia(2011,2030,var='tmax',funcion=2)
data.to_csv(guar+"tmax_2011-2030rcp85.csv", sep=";", index=False, encoding="utf-8")
####periodo 2031-2050
data=pr.procesPeriodDia(2031,2050,var='tmax',funcion=2)
data.to_csv(guar+"tmax_2031-2050rcp85.csv", sep=";", index=False, encoding="utf-8")
####periodo 2051-2070
data=pr.procesPeriodDia(2051,2070,var='tmax',funcion=2)
data.to_csv(guar+"tmax_2051-2070rcp85.csv", sep=";", index=False, encoding="utf-8")


#################################################################################
#################################################################################
####Datos de temperatura minima con rcp 45
preci="/media/darwin/Darwin/Diarios/TMin/RCP45/tasmin_day_Ecuador_Ensamble_rcp45_"
####periodo 2011-2030
pr=Process(preci)
data=pr.procesPeriodDia(2011,2030,var='tmin',funcion=2)
data.to_csv(guar+"tmin_2011-2030rcp45.csv", sep=";", index=False, encoding="utf-8")
####periodo 2031-2050
data=pr.procesPeriodDia(2031,2050,var='tmin',funcion=2)
data.to_csv(guar+"tmin_2031-2050rcp45.csv", sep=";", index=False, encoding="utf-8")
####periodo 2051-2070
data=pr.procesPeriodDia(2051,2070,var='tmin',funcion=2)
data.to_csv(guar+"tmin_2051-2070rcp45.csv", sep=";", index=False, encoding="utf-8")
####Datos de temperatura minima con rcp 85
preci="/media/darwin/Darwin/Diarios/TMin/RCP85/tasmin_day_Ecuador_Ensamble_rcp85_"
####periodo 2011-2030
pr=Process(preci)
data=pr.procesPeriodDia(2011,2030,var='tmin',funcion=2)
data.to_csv(guar+"tmin_2011-2030rcp85.csv", sep=";", index=False, encoding="utf-8")
####periodo 2031-2050
data=pr.procesPeriodDia(2031,2050,var='tmin',funcion=2)
data.to_csv(guar+"tmin_2031-2050rcp85.csv", sep=";", index=False, encoding="utf-8")
####periodo 2051-2070
data=pr.procesPeriodDia(2051,2070,var='tmin',funcion=2)
data.to_csv(guar+"tmin_2051-2070rcp85.csv", sep=";", index=False, encoding="utf-8")


#################################################################################
#################################################################################
####Datos de temperatura media con rcp 45
preci="/media/darwin/Darwin/Diarios/TMed/RCP45/tas_day_Ecuador_Ensamble_rcp45_"
####periodo 2011-2030
pr=Process(preci)
data=pr.procesPeriodDia(2011,2030,var='temp',funcion=2)
data.to_csv(guar+"tmed_2011-2030rcp45.csv", sep=";", index=False, encoding="utf-8")
####periodo 2031-2050
data=pr.procesPeriodDia(2031,2050,var='temp',funcion=2)
data.to_csv(guar+"tmed_2031-2050rcp45.csv", sep=";", index=False, encoding="utf-8")
####periodo 2051-2070
data=pr.procesPeriodDia(2051,2070,var='temp',funcion=2)
data.to_csv(guar+"tmed_2051-2070rcp45.csv", sep=";", index=False, encoding="utf-8")
####Datos de temperatura minima con rcp 85
preci="/media/darwin/Darwin/Diarios/TMed/RCP85/tas_day_Ecuador_Ensamble_rcp85_"
####periodo 2011-2030
pr=Process(preci)
data=pr.procesPeriodDia(2011,2030,var='temp',funcion=2)
data.to_csv(guar+"tmed_2011-2030rcp85.csv", sep=";", index=False, encoding="utf-8")
####periodo 2031-2050
data=pr.procesPeriodDia(2031,2050,var='temp',funcion=2)
data.to_csv(guar+"tmed_2031-2050rcp85.csv", sep=";", index=False, encoding="utf-8")
####periodo 2051-2070
data=pr.procesPeriodDia(2051,2070,var='temp',funcion=2)
data.to_csv(guar+"tmed_2051-2070rcp85.csv", sep=";", index=False, encoding="utf-8")