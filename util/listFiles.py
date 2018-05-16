# _*_ coding: utf-8 *_*
#Autor: Darwin Rosero Vaca
#Creado: 15 / 05 / 2018
from glob import glob
"""Descripción: """
class ListFiles():
    """"""

    def __init__(self,):
        """Constructor for ListFiles"""

    def makeList(self, filePath, prefijo="nada", sufijo="nada"):
        """Lee los archivos dado un directorio y un sufijo igual para todo los archivos"""
        # print("def listFile(self,filePath, prefijo=\"nada\", sufijo=\"nada\"):")
        # print(prefijo,"",sufijo)
        if prefijo == "nada":
            return glob(filePath + "*" + sufijo)
        else:
            return glob(filePath + "" + prefijo + "*")