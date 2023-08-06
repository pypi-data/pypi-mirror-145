# -*- coding: utf-8 -*-
"""
Created on Thu May 27 14:51:04 2021

@author: ormondt
"""

import math
import os
import glob
import numpy as np
from pyproj import CRS
from pyproj import Transformer
from PIL import Image
from matplotlib import cm
from scipy.interpolate import RegularGridInterpolator

def make_png_tiles(valg, index_path, png_path,
                   zoom_range=[0, 23],
                   option="direct",
                   topo_path=None,
                   color_values=None,
                   caxis=None,
                   zbmax=-999.0,
                   merge=True,
                   depth=None):
    """
    Generates PNG web tiles
    
    :param valg: Name of the scenario to be run.
    :type valg: array
    :param index_path: Path where the index tiles are sitting.
    :type index_path: str
    :param png_path: Output path where the png tiles will be created.
    :type png_path: str
    :param option: Option to define the type of tiles to be generated. Options are 'direct', 'floodmap', 'topography'. Defaults to 'direct', in which case the values in *valg* are used directly.
    :type option: str
    :param zoom_range: Zoom range for which the png tiles will be created. Defaults to [0, 23].
    :type zoom_range: list of int
    
    """
    
    if type(valg) == list:
        pass
    else:
        valg = valg.transpose().flatten()

    if not caxis:
        caxis = []
        caxis.append(np.nanmin(valg))
        caxis.append(np.nanmax(valg))
    
    for izoom in range(zoom_range[0], zoom_range[1] + 1):
        
        print("Processing zoom level " + str(izoom))
    
        index_zoom_path = os.path.join(index_path, str(izoom))
    
        if not os.path.exists(index_zoom_path):
            continue
    
        png_zoom_path = os.path.join(png_path, str(izoom))
        makedir(png_zoom_path)
    
        for ifolder in list_folders(os.path.join(index_zoom_path, "*")):
            
            path_okay = False
            ifolder = os.path.basename(ifolder)
            index_zoom_path_i = os.path.join(index_zoom_path, ifolder)
            png_zoom_path_i = os.path.join(png_zoom_path, ifolder)
        
            for jfile in list_files(os.path.join(index_zoom_path_i, "*.dat")):
                               
                jfile = os.path.basename(jfile)
                j = int(jfile[:-4])
                
                index_file = os.path.join(index_zoom_path_i, jfile)
                png_file   = os.path.join(png_zoom_path_i, str(j) + ".png")
                
                ind = np.fromfile(index_file, dtype="i4")
                
                if topo_path and option=="flood_probability_map":

                    # valg is actually CDF interpolator to obtain probability of water level

                    # Read bathy
                    bathy_file = os.path.join(topo_path, str(izoom),
                                              ifolder, str(j) + ".dat")
                    if not os.path.exists(bathy_file):
                        # No bathy for this tile, continue
                        continue
                    zb  = np.fromfile(bathy_file, dtype="f4")
                    zs  = zb + depth
                    
                    valt = valg[ind](zs)
                    valt[ind<0] = np.NaN


                elif topo_path and option=="floodmap":

                    # Read bathy
                    bathy_file = os.path.join(topo_path, str(izoom),
                                              ifolder, str(j) + ".dat")
                    if not os.path.exists(bathy_file):
                        # No bathy for this tile, continue
                        continue
                    zb  = np.fromfile(bathy_file, dtype="f4")
                    
                    valt = valg[ind]                   
                    valt = valt - zb
                    valt[valt<0.05] = np.NaN
                    valt[zb<zbmax] = np.NaN

                elif topo_path and option=="topography":

                    # Read bathy
                    bathy_file = os.path.join(topo_path, str(izoom),
                                              ifolder, str(j) + ".dat")
                    if not os.path.exists(bathy_file):
                        # No bathy for this tile, continue
                        continue
                    zb  = np.fromfile(bathy_file, dtype="f4")
                    
                    valt = zb

                else:                

                    valt = valg[ind]                   
                    valt[ind<0] = np.NaN

                
                if color_values:
                    
                    rgb = np.zeros((256*256,4),'uint8')                        

                    # Determine value based on user-defined ranges
                    for color_value in color_values:

                        inr = np.logical_and(valt>=color_value["lower_value"],
                                             valt<color_value["upper_value"])
                        rgb[inr,0] = color_value["rgb"][0]
                        rgb[inr,1] = color_value["rgb"][1]
                        rgb[inr,2] = color_value["rgb"][2]
                        rgb[inr,3] = 255
                        
                    rgb = rgb.reshape([256,256,4])
                    if not np.any(rgb>0):
                        # Values found, go on to the next tiles
                        continue
                    rgb = np.flip(rgb, axis=0)
                    im = Image.fromarray(rgb)

                else:

                    valt = np.flipud(valt.reshape([256, 256]))
                    valt = (valt - caxis[0]) / (caxis[1] - caxis[0])
                    valt[valt<0.0] = 0.0
                    valt[valt>1.0] = 1.0
                    im = Image.fromarray(cm.jet(valt, bytes=True))
                        
                if not path_okay:
                    if not os.path.exists(png_zoom_path_i):
                        makedir(png_zoom_path_i)
                        path_okay = True
                
                if os.path.exists(png_file):
                    # This tile already exists
                    if merge:
                        im0  = Image.open(png_file)
                        rgb  = np.array(im)
                        rgb0 = np.array(im0)
                        isum = np.sum(rgb, axis=2)
                        rgb[isum==0,:] = rgb0[isum==0,:]
#                        rgb[rgb==0] = rgb0[rgb==0]
                        im = Image.fromarray(rgb)
#                        im.show()
    
                im.save(png_file)            

def make_topobathy_tiles(path, dem_names, lon_range, lat_range,
                         index_path=None,
                         zoom_range=None,
                         z_range=None,
                         bathymetry_database_path="d:\\delftdashboard\\data\\bathymetry"):

    """
    Generates topo/bathy tiles
    
    :param path: Path where topo/bathy tiles will be stored.
    :type path: str
    :param dem_name: List of DEM names (dataset names in Bathymetry Database).
    :type dem_name: list
    :param png_path: Output path where the png tiles will be created.
    :type png_path: str
    :param option: Option.
    :type option: str
    :param zoom_range: Zoom range for which the png tiles will be created. Defaults to [0, 23].
    :type zoom_range: list of int
    
    """
    
    from cht.bathymetry_database import BathymetryDatabase
    from cht.misc_tools import interp2
    
    bathymetry_database = BathymetryDatabase(bathymetry_database_path)

    if not zoom_range:
        zoom_range = [0, 13]

    if not z_range:
        z_range = [-20000.0, 20000.0]

    npix = 256
    

    transformer_4326_to_3857 = Transformer.from_crs(CRS.from_epsg(4326),
                                                    CRS.from_epsg(3857),
                                                    always_xy=True)
    dem_crs = []
    transformer_3857_to_dem = []
    
    for dem_name in dem_names:
        
        dem_crs.append(bathymetry_database.get_crs(dem_name))
    
        transformer_3857_to_dem.append(Transformer.from_crs(CRS.from_epsg(3857),
                                                            dem_crs[-1],
                                                            always_xy=True))
    
    for izoom in range(zoom_range[0], zoom_range[1] + 1):
        
        print("Processing zoom level " + str(izoom))
    
        zoom_path = os.path.join(path, str(izoom))
    
        dxy = (40075016.686/npix) / 2 ** izoom
        xx = np.linspace(0.0, (npix - 1)*dxy, num=npix)
        yy = xx[:]
        xv, yv = np.meshgrid(xx, yy)
    
        ix0, iy0 = deg2num(lat_range[0], lon_range[0], izoom)
        ix1, iy1 = deg2num(lat_range[1], lon_range[1], izoom)
            
    
        for i in range(ix0, ix1 + 1):
        
            path_okay   = False
            zoom_path_i = os.path.join(zoom_path, str(i))
        
            for j in range(iy0, iy1 + 1):
                        
                file_name = os.path.join(zoom_path_i, str(j) + ".dat")
                
                if index_path:
                    # Only make tiles for which there is an index file
                    index_file_name = os.path.join(index_path, str(izoom),
                                                   str(i), str(j) + ".dat")
                    if not os.path.exists(index_file_name):
                        continue
        
                # Compute lat/lon at ll corner of tile
                lat, lon = num2deg(i, j, izoom)
        
                # Convert to Global Mercator
                xo, yo   = transformer_4326_to_3857.transform(lon,lat)
        
                # Tile grid on local mercator
                x3857 = xv[:] + xo + 0.5*dxy
                y3857 = yv[:] + yo + 0.5*dxy
                zg    = np.float32(np.full([npix, npix], np.nan))

                for idem, dem_name in enumerate(dem_names):
                                        
                    # Convert tile grid to crs of DEM
                    xg,yg      = transformer_3857_to_dem[idem].transform(x3857,y3857)
                    
                    # Bounding box of tile grid
                    if dem_crs[idem].is_geographic:
                        xybuf = dxy/50000.0
                    else:
                        xybuf = 2*dxy
                        
                    xl = [np.min(np.min(xg)) - xybuf, np.max(np.max(xg)) + xybuf]
                    yl = [np.min(np.min(yg)) - xybuf, np.max(np.max(yg)) + xybuf]
                
                    # Get DEM data (ddb format for now)
                    x,y,z = bathymetry_database.get_data(dem_name,
                                                         xl,
                                                         yl,
                                                         max_cell_size=dxy)
                                        
                    if x is np.NaN:
                        # No data obtained from bathymetry database
                        continue
    
                    zg0 = np.float32(interp2(x,y,z,xg,yg))
                    zg[np.isnan(zg)] = zg0[np.isnan(zg)]
                    
                    if not np.isnan(zg).any():
                        # No nans left, so no need to load subsequent DEMs
                        break
                    
                if np.isnan(zg).all():
                    # only nans in this tile
                    break
                    
                if np.nanmax(zg)<z_range[0] or np.nanmin(zg)>z_range[1]:
                    # all values in tile outside z_range
                    break
                                    
                if not path_okay:
                    if not os.path.exists(zoom_path_i):
                        makedir(zoom_path_i)
                        path_okay = True
                     
                # And write indices to file
                fid = open(file_name, "wb")
                fid.write(zg)
                fid.close()

def makedir(path):

    if not os.path.exists(path):
        os.makedirs(path)

def list_files(src):
    
    file_list = []
    full_list = glob.glob(src)
    for item in full_list:
        if os.path.isfile(item):
            file_list.append(item)

    return file_list

def list_folders(src):
    
    folder_list = []
    full_list = glob.glob(src)
    for item in full_list:
        if os.path.isdir(item):
            folder_list.append(item)

    return folder_list
    
def interp2(x0,y0,z0,x1,y1):
    
    f = RegularGridInterpolator((y0, x0), z0,
                                bounds_error=False, fill_value=np.nan)    
    # reshape x1 and y1
    sz = x1.shape
    x1 = x1.reshape(sz[0]*sz[1])
    y1 = y1.reshape(sz[0]*sz[1])    
    # interpolate
    z1 = f((y1,x1)).reshape(sz)        
    
    return z1

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n) 
    ytile = int((1.0 - math.asinh(math.tan(-lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

def num2deg(xtile, ytile, zoom):
    n = 2 ** zoom
    lon_deg = xtile / n * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * ytile / n)))
    lat_deg = math.degrees(-lat_rad)
    return (lat_deg, lon_deg)
