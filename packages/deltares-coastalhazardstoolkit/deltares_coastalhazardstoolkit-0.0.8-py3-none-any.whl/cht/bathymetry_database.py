# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 10:58:08 2021

@author: Maarten van Ormondt
"""

import os
import xml.etree.ElementTree as ET
import numpy as np
import math
import urllib
import netCDF4 as nc

from .coordinate_systems import CS

class ZoomLevel:

    def __init__(self):
        
        self.dx = 0.0
        self.dy = 0.0
        self.i_available = []
        self.j_available = []

class BathymetryDatabase:

    """
    The main Bathymetry Database class
    
    :param pth: Path name where bathymetry tiles will be cached.
    :type pth: string            
    """
    
    def __init__(self, pth):
        
        self.path    = pth
        self.dataset = []
        self.read()
       
    def read(self):
        """
        Reads meta-data of all datasets in the database. 
        """
        
        # Read in database
        xml_file = os.path.join(self.path, "bathymetry.xml")
        xml_root = ET.parse(xml_file).getroot()

        for xml_dataset in xml_root.findall('dataset'):
            
            try:

                dataset = BathymetryDataset()
                
                # Set attributes
                for prop in xml_dataset:
                    setattr(dataset, prop.tag.lower(), prop.text)
                
                dataset.local_path = os.path.join(self.path, dataset.name)
    
                # Read metadata for this dataset from separate xml file
                dataset.read()
                
                self.dataset.append(dataset)
            
            except:
                print("Could not read dataset " + dataset.name +". Need to fix this by downloading dataset xml.")
                pass
        
    def get_data(self, dataset_name, xlim, ylim, max_cell_size):
        """
        Returns imported data from database 
        
        :param dataset_name: Name of requested bathymetry dataset.
        :type dataset_name: str
        :param xlim: x-limits.
        :type xlim: list
        :param y_lim: y-limits.
        :type y_lim: list
        :param max_cell_size: Maximum cell size (in metres)
        :type max_cell_size: float, optional
        :param dx: dx
        :type dx: float, optional
        :param dx: dy
        :type dy: float, optional
        :param crs: name of coordinate reference system
        :type crs: str, optional
        """
        
        # Read in data from database
        # Find corresponding dataset dataset
        for d in self.dataset:
            if d.name == dataset_name:
                x,y,z = d.get_data(xlim, ylim, max_cell_size)
                return x, y, z

    def get_crs(self, dataset_name):
        """
        Returns coordinate reference system (CRS) of dataset

        :param dataset_name: Name of requested bathymetry dataset.
        :type dataset_name: str
        :return: CRS  
        :rtype: str
        """
        
        # Read in data from database
        # Find corresponding dataset dataset
        for d in self.dataset:
            if d.name == dataset_name:
                return d.crs.epsg

    # def get_data_on_array(self, dataset_name, xarr, yarr, crs):
        
    #     # Get data interpolated onto array xarr, yarr
        
    #     zarr = 0.0
        
    #     return zarr
    
    def get_sources(self):

        sources      = []
        source_names = []
        
        for dataset in self.dataset:
                       
            source    = dataset.source
            
            if source in source_names:
                # Existing source
                for src in sources:
                    if src.name == source:
                        src.dataset.append(dataset)                
                        break
            else:
                # New source
                src = BathymetrySource(source)
                src.dataset.append(dataset)                
                sources.append(src)
                source_names.append(source)
        
        return sources

class BathymetryDataset:
    """
    Bathymetry dataset class 

    :ivar name: initial value: ''
    :ivar nr_zoom_levels: initial value: 0
    """

    def __init__(self):
        
        self.name              = ''
        self.long_name         = ''
        self.source            = ''
        self.data_format       = '' # netcdftiles, geotiff, etc
        self.nr_zoom_levels    = 0
        self.zoom_level        = []
        self.coordinate_system = []
        self.use_cache         = True
        self.remote_path       = ''
        self.local_path        = ''
        self.vertical_reference_level_name = 'MSL'
        self.vertical_reference_level_difference_with_MSL = 0.0

    def read(self):
        
        xml_file = os.path.join(self.local_path, self.name + ".xml")

        xml_root = ET.parse(xml_file).getroot()

        # Set attributes
        for prop in xml_root:
            setattr(self, prop.tag.lower(), prop.text)
        self.nr_zoom_levels = int(self.nr_zoom_levels)    
        self.x0             = float(self.x0)
        self.y0             = float(self.y0)
        self.dx             = float(self.dx)
        self.dy             = float(self.dy)
        self.nr_tiles_x     = int(self.nr_tiles_x)
        self.nr_tiles_y     = int(self.nr_tiles_y)
        self.pixels_in_tile = int(self.pixels_in_tile)
        if self.coord_ref_sys_kind[0:3] == "geo":
            self.coord_ref_sys_kind = "geographic"
        
        self.crs = CS(self.coord_ref_sys_name, self.coord_ref_sys_kind)

                
        dx = self.dx
        dy = self.dy
        nnx = self.nr_tiles_x
        nny = self.nr_tiles_y
        for izoom in range(self.nr_zoom_levels):
            zl = ZoomLevel()
            zl.x0 = self.x0
            zl.y0 = self.y0
            zl.dx = dx
            zl.dy = dy
            zl.nr_tiles_x = nnx
            zl.nr_tiles_y = nny
            self.zoom_level.append(zl)
            dx  = dx*2
            dy  = dy*2
            nnx = math.ceil(nnx/2)
            nny = math.ceil(nny/2)
            
    def get_data(self, xlim, ylim, max_cell_size):
        """
        Reads data from database. Returns x, y, z 
        """
        
        x=0.0
        y=0.0
        z=0.0
        
        if self.type.lower() == 'netcdftiles':
            x, y, z = self.read_data_from_netcdf_tiles(xlim, ylim, 0, max_cell_size)
        elif self.type == 'geotiff':
            x = 1.0    

        return x,y,z
        
    def read_data_from_netcdf_tiles(self, xl, yl, izoom, max_cell_size):
        """
        Reads data from database. Returns x, y, z 
        """
        
        just_get_tiles = False
        iopendap       = False
                  
        x = np.nan
        y = np.nan
        z = np.nan

        cell_size_x = np.array([])
        cell_size_y = np.array([])
        
        for zl in self.zoom_level:
            cell_size_x = np.append(cell_size_x, zl.dx)
            cell_size_y = np.append(cell_size_y, zl.dy)

            # Should multiply with unit here...
        
        if izoom == 0:
            # Find zoom level based on resolution
            if self.coord_ref_sys_kind == 'geographic':
                cell_size_x = cell_size_x*111111
                cell_size_y = cell_size_y*111111
            # Find first level with cell size greater than max cell size    
            ilev1 = find_last(cell_size_x<=max_cell_size)
            if ilev1 == None:
                # All levels have cell sizes smaller than max cell size
                ilev1 = 0
            ilev2 = ilev1
        elif izoom == -1:
            # Get all the data from each zoom level !
            just_get_tiles = True
            ilev1 = 0
            ilev2 = self.nr_zoom_levels
        else:
            ilev1 = izoom
            ilev2 = izoom
        
        for ilev in range(ilev1,ilev2+1):
            
            x0  = self.zoom_level[ilev].x0   # lower-left corner x
            y0  = self.zoom_level[ilev].y0   # lower-left corner y
            dx  = self.zoom_level[ilev].dx   # cell size x
            dy  = self.zoom_level[ilev].dy   # cell size y
            nx  = self.pixels_in_tile        # number of pixels in tile x
            ny  = self.pixels_in_tile        # number of pixels in tile y
            nnx = self.zoom_level[ilev].nr_tiles_x  # number of tiles x
            nny = self.zoom_level[ilev].nr_tiles_y  # number of tiles y
            iav = self.zoom_level[ilev].i_available
            jav = self.zoom_level[ilev].j_available
            
            # Read i_available and j_available (if they have not yet been read)
#            if not iav:
            if not np.any(iav):
                ncfile = os.path.join(self.local_path, self.name + ".nc")
                ds  = nc.Dataset(ncfile)
                iav = ds["iavailable" + str(ilev + 1)][:].data - 1
                jav = ds["javailable" + str(ilev + 1)][:].data - 1
                self.zoom_level[ilev].i_available = iav
                self.zoom_level[ilev].j_available = jav

#            vert_unit = self.vertical_coordinate_system.unit
            
            tile_size_x = dx*nx
            tile_size_y = dy*ny
            
             # Directories and names
            name   = self.name;
            levdir = 'zl' + str(ilev + 1).zfill(2)
            
            iopendap = False

            if self.url[0:4] == 'http':
                # Tiles stored on OpenDAP server
                iopendap  = True
                remotedir = self.url + '/' + levdir + '/'
                localdir  = os.path.join(self.local_path, levdir)
            else:
                # Tiles are stored locally
                localdir  = os.path.join(self.local_path, levdir)
                remotedir = localdir
                
            # Tiles
            # Array with x and y origin of available tiles
            # all_tiles_x0 = np.arange(x0, x0 + (nnx)*tile_size_x, tile_size_x)
            # all_tiles_y0 = np.arange(y0, y0 + (nny)*tile_size_y, tile_size_y)
            all_tiles_x0 = np.linspace(x0, x0 + (nnx - 1)*tile_size_x, num=nnx)
            all_tiles_y0 = np.linspace(y0, y0 + (nny - 1)*tile_size_y, num=nny)
            
            # Make sure that tiles are read east +180 deg lon.
            all_tiles_index_x = np.arange(0, nnx)
            all_tiles_index_y = np.arange(0, nny)
            
            if self.coord_ref_sys_kind == 'geographic' and nnx*tile_size_x>350.0:
                # Probably a global dataset
                all_tiles_x0 = np.concatenate((all_tiles_x0 - 360.0,
                                               all_tiles_x0,
                                               all_tiles_x0 + 360.0))
                all_tiles_index_x = np.concatenate((all_tiles_index_x,
                                                    all_tiles_index_x,
                                                    all_tiles_index_x))
            
            # Required tile indices
            if all_tiles_x0[0]>xl[1] or all_tiles_y0[0]>yl[1] or all_tiles_x0[-1] + tile_size_x<xl[0] or all_tiles_y0[-1] + tile_size_y<yl[0]:
                ok = False
                print('Tiles are outside of search range')
                return x, y, z
             
            ix1 = find_last(all_tiles_x0<=xl[0])
            if ix1 == None:
                ix1 = 0
            ix2 = find_last(all_tiles_x0<xl[1])
            iy1 = find_last(all_tiles_y0<=yl[0])
            if iy1 == None:
                iy1 = 0
            iy2 = find_last(all_tiles_y0<yl[1])
          
            # Total number of tiles to read in x and y direction
            nnnx = ix2 - ix1 + 1
            nnny = iy2 - iy1 + 1

            # Indices of tiles to be loaded
            tiles_index_x = all_tiles_index_x[ix1:ix2 + 1]
            tiles_index_y = all_tiles_index_y[iy1:iy2 + 1]
            # Origins of tiles to be loaded
            tiles_x0 = all_tiles_x0[ix1:ix2 + 1]
            tiles_y0 = all_tiles_y0[iy1:iy2 + 1]

            if not just_get_tiles:
                # Mesh of horizontal coordinates
                # x = np.arange(tiles_x0[0],
                #                tiles_x0[-1] + tile_size_x, dx)
                # y = np.arange(tiles_y0[0],
                #                tiles_y0[-1] + tile_size_y, dy)

                x = np.linspace(tiles_x0[0], tiles_x0[-1] + tile_size_x - dx, num=nnnx*nx)
                y = np.linspace(tiles_y0[0], tiles_y0[-1] + tile_size_y - dy, num=nnny*ny)

                # Allocate z
                z = np.empty((nnny*ny,nnnx*nx))
                z[:] = np.nan

            # Start indices for each tile in larger matrix
            istartx = []
            for i in range(nnnx):
                iii1 = find_first(abs(x - tiles_x0[i]) == min(abs(x - tiles_x0[i])))
                istartx.append(iii1)

            tilen = 0 # Tile number index (only used for waitbox)
            ntiles = nnnx*(iy2 - iy1 + 1) # Total number of tiles
            
#             if not quiet
#                 wb = awaitbar(0,'Getting tiles ...')
            
            # Now get the tiles
            for i in range(nnnx):
                
                itile = tiles_index_x[i]
                
                for j in range(nnny):

                    jtile = tiles_index_y[j]
    
                    tilen = tilen + 1
                     
#                     # # Waitbar
#                     # if not quiet:
#                     #     if justgettiles
#                     #         str=['Getting bathymetry level ' num2str(ilev) ' of ' num2str(nLevels) ' - tile ' num2str(tilen) ' of ' ...
#                     #             num2str(ntiles) ' ...'];
#                     #     else
#                     #         str=['Getting bathymetry - tile ' num2str(tilen) ' of ' ...
#                     #             num2str(ntiles) ' ...'];
#                     #     end
#                     #     if verLessThan('matlab', '8.4')
#                     #         [hh,abort2]=awaitbar(tilen/ntiles,wb,str);
#                     #     else
#                     #         [hh,abort2]=awaitbar(tilen/ntiles,get(wb,'Number'),str);
#                     #     end
#                     #     if abort2 % Abort the process by clicking abort button
#                     #         break;
#                     #     end;
#                     #     if isempty(hh); % Break the process when closing the figure
#                     #         break;
#                     #     end;
#                     # end

                    zzz = np.empty((ny,nx)) # make empty tile
                    zzz[:] = np.nan

                    # First check whether required file exists at at all
                    both_ok = (iav == itile) * (jav == jtile)

                    if both_ok.any():

                        file_name = name + '.' + levdir + '.' + str(itile + 1).zfill(5) + '.' + str(jtile + 1).zfill(5) + '.nc'
                        full_file_name = os.path.join(localdir, file_name)
    
                        if iopendap:
                            if self.use_cache:
                                # First check if file is available locally
                                idownload = False
                                if not os.path.exists(full_file_name):
                                    # File not available locally
                                    idownload = True
                                else:
                                    # Check if the file size seems right
                                    fsize = os.path.getsize(full_file_name)
                                    if fsize<1000:
                                        # Probably something wrong with
                                        # this file. Delete it and download
                                        # again.
                                        idownload = True
                                        os.remove(full_file_name);
    
                                if idownload:
                                    # Make localdir if it does not yet exist
                                    if not os.path.exists(localdir):
                                        os.mkdir(localdir)
                                    # Download file    
                                    try:
                                        urllib.request.urlretrieve(remotedir + file_name,
                                                                       full_file_name)
                                    except:
                                        print('Could not download tile ...')
    
                                ncfile = full_file_name # name of local netcdf file
    
                            else:
    
                                # Don't use cache
                                ncfile = remotedir + file_name
    
                        else:
    
                            ncfile = full_file_name
                            
#                        print(ncfile)    
                        if not just_get_tiles:
                            
                            # Read the data in the tile
                            if os.path.exists(ncfile):
                                ds  = nc.Dataset(ncfile)
                                zzz = ds["depth"][:]
    #                            fill_value = nc_attget(ncfile, 'depth', 'fill_value')
                        
                            # Now stick the tile data in the large array

                            i1 = istartx[i]
                            i2 = istartx[i] + nx

                            j1 = j*ny
                            j2 = (j + 1)*ny

                            z[j1:j2,i1:i2] = zzz
                    
            
#             # # Close waitbar
#             # if ~quiet
#             #     if ~isempty(hh)
#             #         close(wb);
#             #     end
#             # end

            # Now crop the data to the requested limits
            if not just_get_tiles:
                
#                z(z<-15000)=NaN # Set values to NaN

                ix1 = find_last(x<=xl[0])
                if ix1 == None:
                    ix1 = 0
                ix2 = find_first(x>xl[1])
                if ix2 == None:
                    ix2 = len(x)
                iy1 = find_last(y<=yl[0])
                if iy1 == None:
                    iy1 = 0
                iy2 = find_first(y>yl[1])
                if iy2 == None:
                    iy2 = len(y)
                
                x = x[ix1:ix2]
                y = y[iy1:iy2]
                
                data_in_cell_centres = True

                if data_in_cell_centres:
                    x = x + 0.5*dx # This really should be added as the data are defined in the cell centres!!!               
                    y = y + 0.5*dy
                
                z = z[iy1:iy2,ix1:ix2]
                
                # Convert to metres
                if self.vertical_units == 'cm':
                    z = z*0.01
                elif self.vertical_units == 'ft':
                    z = z*0.3048

        return x,y,z
           
def find_first(a):
    if not a.any():
        i = None
    else:
        i = np.nonzero(a)[0][0]
    return i

def find_last(a):
    if not a.any():
        i = None
    else:
        i = np.nonzero(a)[0][-1]
    return i

class BathymetrySource:
    
    def __init__(self, name):
        
        self.name    = name
        self.dataset = []
