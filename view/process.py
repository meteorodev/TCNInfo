# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Creado: 15 / 05 / 2018

from util import listFiles as lf, loadNetcdf as lnc

"""Descripción: """
class Process():
    """"""

    def __init__(self,rootPath):
        """Constructor for Process"""
        self.rootPath=rootPath

    def procesPeriod(self,añoi,añof):
        listfiles=[]
        for i in range(añoi,añof+1):
            print(i)


######seccion de ejecucion
preci="~/Documentos/TCN/"
pr=Process(preci)
pr.procesPeriod(2011,2030)