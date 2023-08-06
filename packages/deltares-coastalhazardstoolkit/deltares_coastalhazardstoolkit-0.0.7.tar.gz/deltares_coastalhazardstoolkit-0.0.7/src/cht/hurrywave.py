# -*- coding: utf-8 -*-
"""
Created on Sat May 15 08:08:40 2021

@author: ormondt
"""
import os
import pandas as pd
import datetime
import numpy as np
from pandas.tseries.offsets import DateOffset
import xarray as xr

import math
from pyproj import CRS
from pyproj import Transformer

from cht.geometry import RegularGrid
from cht.geometry import Point
from cht.deltares_ini import IniStruct

class HurryWave:
    
    def __init__(self, input_file=None, crs=None):
        
        if not crs:
            crs = CRS(4326)
 
        self.input                    = HurryWaveInput()
        self.crs                      = crs
        self.grid                     = None
        self.mask                     = None
        self.boundary_point           = []
        self.observation_point        = []
        self.obstacle                 = []
        
        if input_file:
            self.path = os.path.dirname(input_file)
            self.load(input_file)

    def load(self, inputfile):
        # Reads hurrywave.inp and attribute files
        self.read_input_file(inputfile)
        self.read_attribute_files()
    
    def read_input_file(self, inputfile):
        
        # Reads hurrywave.inp
        
        # Get the path of hurrywave.inp
        self.path = os.path.dirname(inputfile)
        
        fid = open(inputfile, 'r')
        lines = fid.readlines()
        fid.close()
        for line in lines:
            str = line.split("=")
            if len(str)==1:
               # Empty line
               continue
            name = str[0].strip()
            val  = str[1].strip()
            try:
                # First try to convert to int
                val = int(val)
            except ValueError:
                try:
                    # Now try to convert to float
                    val = float(val)
                except:
                    pass
            if name == "tref":
                val = datetime.datetime.strptime(val.rstrip(), '%Y%m%d %H%M%S')
            if name == "tstart":
                val = datetime.datetime.strptime(val.rstrip(), '%Y%m%d %H%M%S')
            if name == "tstop":
                val = datetime.datetime.strptime(val.rstrip(), '%Y%m%d %H%M%S')
            setattr(self.input, name, val)

        if self.input.crs_utmzone:
            self.crs = CRS("WGS 84 / UTM zone " + self.input.utmzone)
                        
    def write_input_file(self, input_file=None):

        if not input_file:
            input_file = os.path.join(self.path, "hurrywave.inp")
            
        fid = open(input_file, "w")
        for key, value in self.input.__dict__.items():
            if not value is None:
                if type(value) == "float":
                    string = f'{key.ljust(20)} = {float(value)}\n'
                elif type(value) == "int":
                    string = f'{key.ljust(20)} = {int(value)}\n'
                elif isinstance(value, datetime.date):
                    dstr = value.strftime("%Y%m%d %H%M%S")
                    string = f'{key.ljust(20)} = {dstr}\n'
                else:
                    string = f'{key.ljust(20)} = {value}\n'                
                fid.write(string)
        fid.close()    
                       
    def read_attribute_files(self):

        # Grid
#        self.grid = SfincsGrid()

        # Wave boundary conditions
        self.read_boundary_points()
#        self.read_boundary_conditions()

        # Observation points
        self.read_observation_points()
        self.read_observation_points_sp2()

#        self.grid.compute_coordinates(x0,y0,dx,dy,nx,ny,rotation)
    
    def read_index_file(self):
        pass
        
    def read_depth_file(self):
        pass

    def read_mask_file(self):
        pass
    
    def write_index_file(self):
        pass

    def write_depth_file(self):
        pass

    def write_mask_file(self):
        pass

##### Boundary points #####
    
    def read_boundary_points(self):
        
        # Read HurryWave bnd file
        
        self.boundary_point = []
        
        if not self.input.bndfile:
            return
                    
        bnd_file = os.path.join(self.path,
                                self.input.bndfile)

        if not os.path.exists(bnd_file):
            return
        
        # Read the bnd file
        df = pd.read_csv(bnd_file, index_col=False, header=None,
             delim_whitespace=True, names=['x', 'y'])
        
        # Loop through points
        for ind in range(len(df.x.values)):
            name = str(ind + 1).zfill(4)
            point = BoundaryPoint(df.x.values[ind],
                                  df.y.values[ind],
                                  name=name)
            self.boundary_point.append(point)

    def write_boundary_points(self, file_name=None):

        # Write HurryWave bnd file
        if not file_name:
            if not self.input.bndfile:
                return
            file_name = os.path.join(self.path,
                                     self.input.bndfile)
            
        if not file_name:
            return
            
        fid = open(file_name, "w")
        for point in self.boundary_point:
            string = f'{point.geometry.x:12.1f}{point.geometry.y:12.1f}"\n'
            fid.write(string)
        fid.close()    

    # def read_boundary_conditions(self, file_name=None):

    #     # Read HurryWave bhs file
        
    #     if not file_name:
    #         if not self.input.bhsfile:
    #             return
    #         file_name = os.path.join(self.path,
    #                                  self.input.bzsfile)
            
    #     if not file_name:
    #         return
        
    #     if not os.path.exists(file_name):
    #         return
        
    #     if not self.input.tref:
    #         # tref has not yet been defined
    #         return

    #     df = read_timeseries_file(file_name, self.input.tref)

    #     ts  = df.index
    #     for icol, point in enumerate(self.boundary_point):
    #         point.data = pd.Series(df.iloc[:,icol].values, index=ts)
        
    def write_boundary_conditions(self, file_name=None):

        import xarray as xr

        # Write HurryWave bsp file
        if not file_name:
            if not self.input.bspfile:
                return
            file_name = os.path.join(self.path,
                                      self.input.bspfile)
            
        if not file_name:
            return

        times = self.boundary_point[0].data.point_spectrum2d.coords["time"].values
#        tref  = np.datetime64(self.input.tref)
#        times = np.single((times-tref)/1000000000)
        
        sigma = self.boundary_point[0].data.point_spectrum2d.coords["sigma"].values
        theta = self.boundary_point[0].data.point_spectrum2d.coords["theta"].values

        sp2 = np.zeros([len(times), len(self.boundary_point), len(theta), len(sigma)])

        points = []
        xs     = np.zeros([len(self.boundary_point)])
        ys     = np.zeros([len(self.boundary_point)])
        for ip,point in enumerate(self.boundary_point):
            points.append(point.name)
            xs[ip] = point.geometry.x
            ys[ip] = point.geometry.y
            sp2[:,ip,:,:] = point.data.point_spectrum2d.values

        # Convert to single        
        xs  = np.single(xs)            
        ys  = np.single(ys)            
        sp2 = np.single(sp2)            

        ds = xr.Dataset(
                data_vars = dict(point_spectrum2d=(["time", "stations", "theta", "sigma"], sp2),
                                 station_x=(["stations"], xs),
                                 station_y=(["stations"], ys),
                                 ),
                coords    = dict(time=times,
                                 stations=points,
                                 theta=theta,
                                 sigma=sigma)
                )

        dstr = "seconds since " + self.input.tref.strftime("%Y%m%d %H%M%S")
                
        ds.to_netcdf(path=file_name,
                     mode='w',
                     encoding={'time':{'units':dstr}})
#        ds.to_netcdf(path=file_name,
#                     mode='w')
        

    ### Observation points (regular) ###

    def add_observation_point(self, x, y, name):
                
        self.observation_point.append(ObservationPoint(x, y, name, crs=None))

    def read_observation_points(self, file_name=None):
        
        self.observation_point = []

        if not file_name:
            if not self.input.obsfile:
                return
            file_name = os.path.join(self.path,
                                     self.input.obsfile)
                            
        if not os.path.exists(file_name):
            print("Warning : file " + file_name + " does not exist !")
            return
        
        # Loop through points
        df = pd.read_csv(file_name, index_col=False, header=None,
             delim_whitespace=True, names=['x', 'y', 'name'])
        
        for ind in range(len(df.x.values)):
            point = ObservationPoint(df.x.values[ind],
                                     df.y.values[ind],
                                     name=str(df.name.values[ind]))
            self.observation_point.append(point)

    def write_observation_points(self, file_name=None):

        if not file_name:
            file_name = os.path.join(self.path,
                                     self.input.obsfile)
        if self.crs.is_geographic:
            fid = open(file_name, "w")
            for point in self.observation_point:
                string = f'{point.geometry.x:12.6f}{point.geometry.y:12.6f}  "{point.name}"\n'
                fid.write(string)
            fid.close()
        else:
            fid = open(file_name, "w")
            for point in self.observation_point:
                string = f'{point.geometry.x:12.1f}{point.geometry.y:12.1f}  "{point.name}"\n'
                fid.write(string)
            fid.close()
        
    ### Observation points (2d spectra) ###

    def add_observation_point_sp2(self, x, y, name):
                
        self.observation_point_sp2.append(ObservationPoint(x, y, name, crs=None))

    def read_observation_points_sp2(self, file_name=None):
        
        self.observation_point_sp2 = []

        if not file_name:
            if not self.input.ospfile:
                return
            file_name = os.path.join(self.path,
                                     self.input.ospfile)
                            
        if not os.path.exists(file_name):
            print("Warning : file " + file_name + " does not exist !")
            return
        
        # Loop through points
        df = pd.read_csv(file_name, index_col=False, header=None,
             delim_whitespace=True, names=['x', 'y', 'name'])
        
        for ind in range(len(df.x.values)):
            point = ObservationPoint(df.x.values[ind],
                                     df.y.values[ind],
                                     name=str(df.name.values[ind]))
            self.observation_point_sp2.append(point)

    def write_observation_points_sp2(self, file_name=None):

        if not file_name:
            file_name = os.path.join(self.path,
                                     self.input.ospfile)
        if self.crs.is_geographic:    
            fid = open(file_name, "w")
            for point in self.observation_point_sp2:
                string = f'{point.geometry.x:12.6f}{point.geometry.y:12.6f}  "{point.name}"\n'
                fid.write(string)
            fid.close()
        else:
            fid = open(file_name, "w")
            for point in self.observation_point_sp2:
                string = f'{point.geometry.x:12.1f}{point.geometry.y:12.1f}  "{point.name}"\n'
                fid.write(string)
            fid.close()
            

    ### Output ###

    def read_timeseries_output(self,
                               name_list = None,
                               path=None,
                               file_name = None,
                               parameter = "hm0"):

        import xarray as xr
        import pandas as pd
        import numpy as np

        # Returns a dataframe with timeseries    
        
        if not path:
            path = self.path

        if not file_name:
            file_name = "hurrywave_his.nc"

        file_name = os.path.join(path, file_name)
                    
        # Open netcdf file
        ddd = xr.open_dataset(file_name)
        stations=ddd.station_name.values
        all_stations = []
        for ist, st in enumerate(stations):
            st=str(st.strip())[2:-1]
            all_stations.append(st)
        
        times   = ddd.point_hm0.coords["time"].values

        # If name_list is empty, add all points    
        if not name_list:
            name_list = []
            for st in all_stations:
                name_list.append(st)
        
        df = pd.DataFrame(index=times, columns=name_list)
        
        if parameter.lower() == "hm0":
        
            for station in name_list:
                for ist, st in enumerate(all_stations):
                    if station == st:
                        data = ddd.point_hm0.values[:,ist]
                        data[np.isnan(data)] = -999.0
                        df[st]=data
                        break            

        elif parameter.lower() == "tp":
        
            for station in name_list:
                for ist, st in enumerate(all_stations):
                    if station == st:
                        data = ddd.point_tp.values[:,ist]
                        data[np.isnan(data)] = -999.0
                        df[st]=data
                        break            

        elif parameter.lower() == "wavdir":
        
            for station in name_list:
                for ist, st in enumerate(all_stations):
                    if station == st:
                        data = ddd.point_wavdir.values[:,ist]
                        data[np.isnan(data)] = -999.0
                        df[st]=data
                        break            

        elif parameter.lower() == "dirspr":
        
            for station in name_list:
                for ist, st in enumerate(all_stations):
                    if station == st:
                        data = ddd.point_dirsp.values[:,ist]
                        data[np.isnan(data)] = -999.0
                        df[st]=data
                        break            

        ddd.close()
        
        return df    
        
        # # Returns a dataframe with timeseries
    
        # if not file_name:
        #     file_name = os.path.join(self.path, "zst.txt")
    
        # if not self.observation_point:
        #     # First read observation points
        #     self.read_observation_points()
        
        # columns = []
        # for point in self.observation_point:
        #     columns.append(point.name)
            
        # df = read_timeseries_file(file_name, self.input.tref)

        # # Add column names
        # df.columns = columns
            
        # if name_list:
        #     df = df[name_list]
            
        # return df    

    def read_hm0max(self, time_range=None, hm0max_file=None):
    
        if not hm0max_file:
            hm0max_file = os.path.join(self.path, "hm0max.dat")
            
        fname, ext = os.path.splitext(hm0max_file)
        
        if ext == ".dat":

            ind_file = os.path.join(self.path, self.input.indexfile)
    
            freqstr = str(self.input.dtmaxout) + "S"
            t00     = datetime.timedelta(seconds=self.input.t0out + self.input.dtmaxout)
            output_times = pd.date_range(start=self.input.tstart + t00,
                                          end=self.input.tstop,
                                          freq=freqstr).to_pydatetime().tolist()
            nt = len(output_times)
            
            if time_range is None:
                time_range = [self.input.tstart + t00, self.input.tstop]
            
            for it, time in enumerate(output_times):
                if time<=time_range[0]:
                    it0 = it
                if time<=time_range[1]:
                    it1 = it
    
            # Get maximum values
            nmax = self.input.nmax + 2
            mmax = self.input.mmax + 2
                            
            # Read sfincs.ind
            data_ind = np.fromfile(ind_file, dtype="i4")
            npoints = data_ind[0]
            data_ind = np.squeeze(data_ind[1:])
            
            # Read zsmax file
            data_zs = np.fromfile(hm0max_file, dtype="f4")
            data_zs = np.reshape(data_zs,[nt, npoints + 2])[it0:it1+1, 1:-1]

            data_zs = np.amax(data_zs, axis=0)
            zs_da = np.full([nmax*mmax], np.nan)        
            zs_da[data_ind - 1] = np.squeeze(data_zs)
            zs_da = np.where(zs_da == -999, np.nan, zs_da)
            zs_da = np.transpose(np.reshape(zs_da, [mmax, nmax]))[1:-1,1:-1]
        
        elif ext==".nc":

            dsin = xr.open_dataset(hm0max_file)
            zs_da = np.transpose(np.amax(dsin.hm0max.values, axis=0))
            dsin.close()
            
        else:
            # Must be txt file
            return None
        

        return zs_da
        
#     def write_hmax_geotiff(self, dem_file, index_file, hmax_file, time_range=None, zsmax_file=None):
        
#         no_datavalue = -9999
    
#         zs_da = self.read_zsmax(time_range=time_range, zsmax_file=zsmax_file)
#         zs_da = 100 * zs_da
        
#         # Read indices for DEM and resample SFINCS max. water levels on DEM grid
#         dem_ind   = np.fromfile(index_file, dtype="i4")
#         ndem      = dem_ind[0]
#         mdem      = dem_ind[1]
#         indices   = dem_ind[2:]
#         zsmax_dem = np.zeros_like(indices)
#         zsmax_dem = np.where(zsmax_dem == 0, np.nan, 0)
#         valid_indices = np.where(indices > 0)
#         indices = np.where(indices == 0, 1, indices)
#         indices = indices - 1  # correct for python start counting at 0 (matlab at 1)
#         zsmax_dem[valid_indices] = zs_da[indices][valid_indices]
#         zsmax_dem = np.flipud(zsmax_dem.reshape(mdem, ndem).transpose())

#         # Open DEM file
#         dem_ds = gdal.Open(dem_file)
#         band = dem_ds.GetRasterBand(1)
#         dem = band.ReadAsArray()
#         # calculate max. flood depth as difference between water level zs and dem, do not allow for negative values
#         hmax_dem = zsmax_dem - dem  ## just for testing
#         hmax_dem = np.where(hmax_dem < 0, 0, hmax_dem)
#         # set no data value to -9999
#         hmax_dem = np.where(np.isnan(hmax_dem), no_datavalue, hmax_dem)
#         # convert cm to m
#         hmax_dem = hmax_dem/100

#         # write max. flood depth (in m) to geotiff
#         [cols, rows] = dem.shape
#         driver = gdal.GetDriverByName("GTiff")
#         outdata = driver.Create(hmax_file, rows, cols, 1, gdal.GDT_Float32)
#         outdata.SetGeoTransform(dem_ds.GetGeoTransform())  ## sets same geotransform as input
#         outdata.SetProjection(dem_ds.GetProjection())      ## sets same projection as input
#         outdata.GetRasterBand(1).WriteArray(hmax_dem)
#         outdata.GetRasterBand(1).SetNoDataValue(no_datavalue)  ## if you want these values transparent
# #        outdata.SetMetadata({k: str(v) for k, v in scenarioDict.items()})

#         outdata.FlushCache()  ## saves to disk!!
#         outdata = None
#         band = None
#         dem_ds = None

    def grid_coordinates(self, loc='cor'):

        cosrot = math.cos(self.input.rotation*math.pi/180)
        sinrot = math.sin(self.input.rotation*math.pi/180)
        if loc=="cor":
            xx     = np.linspace(0.0,
                                 self.input.mmax*self.input.dx,
                                 num=self.input.mmax + 1)
            yy     = np.linspace(0.0,
                                 self.input.nmax*self.input.dy,
                                 num=self.input.nmax + 1)
        else:
            xx     = np.linspace(0.5*self.input.dx,
                                 self.input.mmax*self.input.dx - 0.5*self.input.dx,
                                 num=self.input.mmax)
            yy     = np.linspace(0.5*self.input.dy,
                                 self.input.nmax*self.input.dy - 0.5*self.input.dy,
                                 num=self.input.nmax)
            
        xg0, yg0 = np.meshgrid(xx, yy)
        xg = self.input.x0 + xg0*cosrot - yg0*sinrot
        yg = self.input.y0 + xg0*sinrot + yg0*cosrot

        return xg, yg
    
    def bounding_box(self, crs=None):

        xg, yg = self.grid_coordinates(loc='cor')
        
        if crs:
            transformer = Transformer.from_crs(self.crs,
                                               crs,
                                               always_xy=True)
            xg, yg = transformer.transform(xg, yg)
        
        x_range = [np.min(np.min(xg)), np.max(np.max(xg))]
        y_range = [np.min(np.min(yg)), np.max(np.max(yg))]
        
        return x_range, y_range

    def outline(self, crs=None):

        xg, yg = self.grid_coordinates(loc='cor')
        
        if crs:
            transformer = Transformer.from_crs(self.crs,
                                               crs,
                                               always_xy=True)
            xg, yg = transformer.transform(xg, yg)
        
        xp = [ xg[0,0], xg[0,-1], xg[-1,-1], xg[-1,0], xg[0,0] ]
        yp = [ yg[0,0], yg[0,-1], yg[-1,-1], yg[-1,0], yg[0,0] ]
        
        return xp, yp
        
    def make_index_tiles(self, path, zoom_range=None):
        
        from tiling import deg2num
        from tiling import num2deg
        import fileops as fo
        
        if not zoom_range:
            zoom_range = [0, 13]

        npix = 256
        
        # Compute lon/lat range
        lon_range, lat_range = self.bounding_box(crs=CRS.from_epsg(4326))
        
        cosrot = math.cos(-self.input.rotation*math.pi/180)
        sinrot = math.sin(-self.input.rotation*math.pi/180)       
        
        transformer_a = Transformer.from_crs(CRS.from_epsg(4326),
                                             CRS.from_epsg(3857),
                                             always_xy=True)
        transformer_b = Transformer.from_crs(CRS.from_epsg(3857),
                                             self.crs,
                                             always_xy=True)
        
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
            
                path_okay = False
                zoom_path_i = os.path.join(zoom_path, str(i))
            
                for j in range(iy0, iy1 + 1):
            
                    file_name = os.path.join(zoom_path_i, str(j) + ".dat")
            
                    # Compute lat/lon at ll corner of tile
                    lat, lon = num2deg(i, j, izoom)
            
                    # Convert to Global Mercator
                    xo, yo   = transformer_a.transform(lon,lat)
            
                    # Tile grid on local mercator
                    x        = xv[:] + xo + 0.5*dxy
                    y        = yv[:] + yo + 0.5*dxy
            
                    # Convert tile grid to crs of HurryWave model
                    x,y      = transformer_b.transform(x,y)
                    
                    # Now rotate around origin of HurryWave model
                    x00 = x - self.input.x0
                    y00 = y - self.input.y0
                    xg  = x00*cosrot - y00*sinrot
                    yg  = x00*sinrot + y00*cosrot
                    
                    iind = np.floor(xg/self.input.dx).astype(int)
                    jind = np.floor(yg/self.input.dy).astype(int)
                    ind  = iind*self.input.nmax + jind
                    ind[iind<0]   = -999
                    ind[jind<0]   = -999
                    ind[iind>=self.input.mmax] = -999
                    ind[jind>=self.input.nmax] = -999


#                    ind           = np.ascontiguousarray(np.transpose(ind))

                    # if i==142 and j==305:
                    
                    #     from matplotlib import pyplot as plt
                    #     fig, ax = plt.subplots(1,1)                                            
                    #     ax.plot(x,y)
                    #     ax.plot(x.transpose(),y.transpose())
                    #     ax.axis('equal')
                    #     x_range, y_range = self.bounding_box()
                    #     xp = [x_range[0], x_range[1],x_range[1],x_range[0],x_range[0]]
                    #     yp = [y_range[0], y_range[0],y_range[1],y_range[1],y_range[0]]
                    #     ax.plot(xp,yp)
                    #     xout, yout = self.outline()
                    #     ax.plot(xout,yout)
                    #     fig, ax = plt.subplots(1,1)                                            
                    #     ax.pcolor(ind.reshape([256, 256]))
                    #     xxx=1
                    
                    if np.any(ind>=0):
                        
                        if not path_okay:
                            if not os.path.exists(zoom_path_i):
                                fo.mkdir(zoom_path_i)
                                path_okay = True
                             
                        # And write indices to file
                        fid = open(file_name, "wb")
                        fid.write(ind)
                        fid.close()

class HurryWaveInput():
    def __init__(self):
        self.mmax         = 0
        self.nmax         = 0
        self.dx           = 0.1
        self.dy           = 0.1
        self.x0           = 0.0
        self.y0           = 0.0
        self.rotation     = 0.0
        self.latitude     = 0.0
        self.tref         = None
        self.tstart       = None
        self.tstop        = None
        self.tspinup      = 60.0
        self.t0out        = -999.0
        self.dtmapout     = 3600.0
        self.dthisout     = 600.0
        self.dtrstout     = 0.0
        self.dtsp2out     = 0.0
        self.dtmaxout     = 0.0
        self.trstout      = -999.0
        self.dtwnd        = 1800.0
        self.rhoa         = 1.25
        self.rhow         = 1024.0
        self.dmx1         = 0.2
        self.dmx2         = 0.00001
        self.crsgeo       = 0
        self.freqmin      = 0.04
        self.freqmax      = 0.5
        self.nsigma       = 12
        self.ntheta       = 36
        self.crs_name     = "WGS 84"
        self.crs_type     = "geographic"
        self.crs_utmzone  = None
        self.crs_epsg     = None
        self.gammajsp     = 3.3
        self.spinup_meteo = 0
        self.quadruplets  = 1
        self.utmzone      = None
        
        self.depfile      = None
        self.mskfile      = None
        self.indexfile    = None
        self.bndfile      = None
        self.bhsfile      = None
        self.btpfile      = None
        self.bwdfile      = None
        self.bdsfile      = None
        self.bspfile      = None
        self.rstfile      = None
        self.spwfile      = None
        self.amufile      = None
        self.amvfile      = None
        self.wndfile      = None
        self.obsfile      = None
        self.ospfile      = None
        
        self.inputformat  = "bin"
        self.outputformat = "bin"
        
        self.cdnrb        = 3
        self.cdwnd        = [0.0,28.0,50.0]
        self.cdval        = [0.001,0.0025,0.0015]

class HurryWaveGrid():

    def __init__(self, x0, y0, dx, dy, nx, ny, rotation):
        self.geometry = RegularGrid(x0, y0, dx, dy, nx, ny, rotation)

    # def plot(self,ax):
    #     self.geometry.plot(ax)

    # def corner_coordinates(self):
    #     x,y = self.geometry.grid_coordinates_corners()
    #     return x, y

    # def centre_coordinates(self):
    #     x,y = self.geometry.grid_coordinates_centres()
    #     return x, y

class HurryWaveDepth():
    def __init__(self):
        self.value = []
        self.geometry = []
    def plot(self,ax):
        pass
    def read(self):
        pass

class HurryWaveMask():
    def __init__(self):
        self.msk = []
    def plot(self,ax):
        pass

class HurryWaveBoundaryConditions():
    
    def __init__(self):
        self.geometry = []

    def read(self, bndfile, bzsfile):
        self.read_points(bndfile)
        self.read_time_series(bzsfile)

    def read_points(self, file_name):
        pass

    def read_time_series(self, file_name):
        pass
    
    def set_xy(self, x, y):
        self.geometry.x = x
        self.geometry.y = y
        pass
    
    def plot(self,ax):
        pass

class HurryWaveBoundaryConditions():
    
    def __init__(self):
        self.geometry = []

    def read(self, bndfile, bzsfile):
        self.read_points(bndfile)
        self.read_time_series(bzsfile)

    def read_points(self, file_name):
        pass

    def read_time_series(self, file_name):
        pass
    
    def set_xy(self, x, y):
        self.geometry.x = x
        self.geometry.y = y
        pass
    
    def plot(self,ax):
        pass

class BoundaryPoint():

    def __init__(self, x, y, name=None, crs=None, data=None, astro=None):
        
        self.name                   = name
        self.geometry               = Point(x, y, crs=crs)
        self.data                   = data

class ObservationPoint():

    def __init__(self, x, y, name, crs=None):
        
        self.name     = name
        self.geometry = Point(x, y, crs=crs)

                    
def read_timeseries_file(file_name, ref_date):
    
    # Returns a dataframe with time series for each of the columns

    df = pd.read_csv(file_name, index_col=0, header=None,
                      delim_whitespace=True)
    ts = ref_date + pd.to_timedelta(df.index, unit="s")
    df.index = ts
    
    return df
    