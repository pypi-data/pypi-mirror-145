# -*- coding: utf-8 -*-
"""
Created on Sun May 16 14:56:46 2021

@author: ormondt
"""

class Geometry:
    
    def __init__(self):
        pass

class RegularGrid(Geometry):   

    def __init__(self, x0, y0, dx, dy, nx, ny, rotation, crs=None):
        
        self.x0       = x0
        self.y0       = y0
        self.dx       = dx
        self.dy       = dy
        self.nx       = nx
        self.ny       = ny
        self.rotation = rotation
        self.crs      = crs
        
        self.xcor     = None
        self.ycor     = None
        self.xcen     = None
        self.ycen     = None
        
    def grid_coordinates_corners(self):
        
        x = None
        y = None
        
        if not self.xcor:        
            x = self.x0
            y = self.y0

        return x, y
        
    def grid_coordinates_centres(self):
        
        x = None
        y = None
        
        if not self.xcen:        
            x = self.x0
            y = self.y0

        return x, y
        
    def plot(self, ax):
        
        pass

class Point():
        
    def __init__(self, x, y, name = None, crs=None):
        
        self.x       = x
        self.y       = y
        self.crs     = crs
        self.name    = name
        self.data    = None

class Polyline(Geometry):
    
    def __init__(self, x=None, y=None, crs=None, name=None,
                 closed=False):
        
        self.point    = []
        self.name     = name
        self.data     = None
        self.closed   = closed
        self.crs      = crs
        
        if x is not None:
            for j, xp in enumerate(x):
                pnt = Point(x[j], y[j])
                self.point.append(pnt)
                

    def add_point(self, x, y, name=None, data=None, position=-1):
        
        pnt = Point(x, y, name=name, data=data)
        if position<0:
            # Add point to the end
            self.point.append(pnt)
        else:
            #
            pass

    def plot(self, ax=None):
        pass
    