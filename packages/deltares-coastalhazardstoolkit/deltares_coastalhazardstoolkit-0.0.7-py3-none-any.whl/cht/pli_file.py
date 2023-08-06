# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 12:08:35 2021

@author: ormondt
"""

from cht.geometry import Polyline as polyline
import cht.tekal as tek

class PliFile:
    
    def __init__(self, file_name):
        
        self.file_name=file_name

    def read(self):
        
        D = tek.tekal(self.file_name)
        D.info()
        m=D.read(0)
        x = m[0,:,0]
        y = m[1,:,0]
        
        p = polyline(x=x,y=y)

        return p
