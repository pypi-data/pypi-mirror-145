# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 14:53:18 2021

@author: ormondt
"""

from pyproj import CRS
from pyproj import Transformer

class CS:
    
    def __init__(self,name,kind):
        
        self.name = name
        self.type = kind
        self.epsg = CRS(name)

def convert(x0,y0,crs0,crs1):
    
    transformer = Transformer.from_crs(crs0.epsg, crs1.epsg, always_xy=True)

    x1, y1 = transformer.transform(x0, y0)
    
    return x1, y1
     