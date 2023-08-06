# -*- coding: utf-8 -*-
"""
Created on Thu May 20 14:56:45 2021

@author: ormondt
"""

import os
import numpy as np
import datetime
import pandas as pd
import xarray as xr
import netCDF4 as nc
import importlib

from pyproj import CRS
from pyproj import Transformer

from cht.misc_tools import interp2
import cht.fileops as fo

class MeteoSource():
    
    # e.g. GFS forecast
    def __init__(self, name, module_name, source_type, crs=None, long_name=None, delay=None):

        self.name   = name
        if not long_name:
            self.long_name = name
        else:
            self.long_name=long_name
        self.module_name = module_name
        self.crs  = crs
        self.type = source_type
        self.delay = delay

class MeteoMatrixScalar():
    
    def __init__(self):
        self.name  = None
        self.val   = None
        self.unit  = None

class MeteoMatrixVector():
    
    def __init__(self):
        self.name  = None
        self.u     = None
        self.v     = None
        self.unit  = None

class MeteoGrid():

    # e.g. gfs_forecast_0p25_conus
    # includes parameters

    def __init__(self,
                 name=None,
                 source=None,
                 parameters=None,
                 path=None,
                 x_range=None,
                 y_range=None,
                 long_name=None,
                 crs=None,
                 xystride=1,
                 tstride=1):

        self.name   = name
        self.crs    = crs
        if not long_name:
            self.long_name = name
        else:
            self.long_name=long_name
        self.source = source
        self.x_range  = x_range
        self.y_range  = y_range
        self.xystride = xystride
        self.tstride = tstride
        
        if not parameters:
            self.parameters = ["wind","barometric_pressure","precipitation"]
        else:
            self.parameters = parameters
        self.path = path
        
        self.time                 = None
        self.x                    = None
        self.y                    = None
        self.quantity             = []
        self.last_analysis_time   = None
            
    def download(self, time_range, parameters=None, path=None):
        
        if not parameters:
            parameters = self.parameters
        
        if not path:
            path = self.path
        
        
#        module = __import__(self.source.module_name)
        module = importlib.import_module("cht.meteosources." + self.source.module_name)

        fo.mkdir(path)
        
        if self.source.type == "forecast":
            
            # Need to check on previous cycles
            
            # Round down to hour
            
            h0 = time_range[0].hour
            h0 = h0 - np.mod(h0, 6)
            t0 = time_range[0].replace(microsecond=0, second=0, minute=0, hour=h0,
                                       tzinfo=datetime.timezone.utc)

            t1 = time_range[1].replace(microsecond=0, second=0, minute=0,
                                       tzinfo=datetime.timezone.utc)
            
            # Current (last available) cycle
            t_current = datetime.datetime.now(datetime.timezone.utc) - \
                datetime.timedelta(hours=self.source.delay)
            h0 = t_current.hour
            h0 = h0 - np.mod(h0, 6)
            t_current = t_current.replace(microsecond=0, second=0, minute=0, hour=h0)
            
            t_last = t_current - datetime.timedelta(hours=6)
            
            t0 = min(t0, t_last)
                        
            # Previous cycles
            previous_cycle_times = pd.date_range(start=t0,
                                                 end=t_last,
                                                 freq='6H').to_pydatetime().tolist()
            
            # Loop through previous cycles (which have the analyzed data)
            # to see if they are there
            for t in previous_cycle_times:

                cycle_path = os.path.join(path, t.strftime("%Y%m%d_%Hz"))
                if not os.path.exists(cycle_path):
                    fo.mkdir(cycle_path)

                # Check if both files (00h and 03h) are there
                t0          = t
                time_string = t.strftime("%Y%m%d_%H%M")    
                f0          = self.name + "." + time_string + ".nc"
                f0          = os.path.join(cycle_path, f0)

                t3          = t + datetime.timedelta(hours=3)
                time_string = t3.strftime("%Y%m%d_%H%M")    
                f3          = self.name + "." + time_string + ".nc"
                f3          = os.path.join(cycle_path, f3)

                if not os.path.exists(f0) or not os.path.exists(f3):
                    # Download data
                    print(cycle_path)
                    data = module.download(parameters,
                                           self.x_range,
                                           self.y_range,
                                           [t, t + datetime.timedelta(hours=3)],
                                           t)
                    self.save_to_nc(cycle_path, data)
                    self.last_analysis_time = t

            if t1>=t_current:
                # And now download the forecast data (last available cycle)  
                cycle_path = os.path.join(path, t_current.strftime("%Y%m%d_%Hz"))
                print(cycle_path)
                fo.mkdir(cycle_path)
                data = module.download(parameters,
                                       self.x_range,
                                       self.y_range,
                                       [t_current, t1],
                                       t)
                self.save_to_nc(cycle_path, data)    
                self.last_analysis_time = t_current
            
        else:

            # Much easier, but do NOT hardcode frequency!!!
            requested_times = pd.date_range(start=time_range[0],
                              end=time_range[1],
                              freq='3H').to_pydatetime().tolist()
            rtimes = []
            # Check which files do not yet exist
            for t in requested_times:
                time_string = t.strftime("%Y%m%d_%H%M")    
                file_name = self.name + "." + time_string + ".nc"
                full_file_name = os.path.join(path, file_name)
                if not os.path.exists(full_file_name):
                    rtimes.append(t)                  
            
            if rtimes:
                data = module.download(parameters,
                                       self.x_range,
                                       self.y_range,
                                       path,
                                       self.name,
                                       times=rtimes)
#                self.save_to_nc(path, data)    
            else:
                print("Requested meteo data already available")
        
    def save_to_nc(self, path, data):
        
        # Stick everything in one file for now
        for it, t in enumerate(data[0].time):

            time_string = t.strftime("%Y%m%d_%H%M")    
            file_name = self.name + "." + time_string + ".nc"
            full_file_name = os.path.join(path, file_name)
            ds = xr.Dataset()            

            for dd in data:
                if dd.quantity == "wind":
                    uu = dd.u[it,:,:]
                    da = xr.DataArray(uu,
                                          coords=[("lat", dd.y),
                                                  ("lon", dd.x)])
                    ds["wind_u"] = da
                    vv = dd.v[it,:,:]
                    da = xr.DataArray(vv,
                                          coords=[("lat", dd.y),
                                                  ("lon", dd.x)])
                    ds["wind_v"] = da
                else:
                    try:
                        val = dd.val[it,:,:]
                        da = xr.DataArray(val,
                                              coords=[("lat", dd.y),
                                                      ("lon", dd.x)])
                        ds[dd.quantity] = da
                    except:
                        print("Could not write " + dd.quantity + " to file ...")

            ds.to_netcdf(path=full_file_name)

            ds.close()

    def collect(self, time_range, parameters=None, xystride=1, tstride=1):
        
        if not parameters:
            parameters = self.parameters

        # Merge data from netcdf files

        if self.source.type == "forecast":

            requested_times = pd.date_range(start=time_range[0],
                                      end=time_range[1],
                                      freq='3H').to_pydatetime().tolist()
            requested_files = []
            for t in requested_times:
                requested_files.append(None)

            # Make list of all cyc
            all_cycle_paths = fo.list_folders(os.path.join(self.path, "*"))
            # Loop through all cycle paths
            for cycle_path in all_cycle_paths:
                t = datetime.datetime.strptime(cycle_path[-12:-1], "%Y%m%d_%H")
                # Check if path falls within requested range
                if t>=time_range[0] and t<=time_range[1]:
                    # Find all times available in this cycle
                    files_in_cycle = fo.list_files(os.path.join(cycle_path, "*.nc"))
                    for file in files_in_cycle:
                        t_file = datetime.datetime.strptime(file[-16:-3],
                                                            "%Y%m%d_%H%M")
                        if t_file in requested_times:
                            ind = requested_times.index(t_file)
                            requested_files[ind] = file
                            self.last_analysis_time = t
                            
            # Get rid of None values
            for ind, file in enumerate(requested_files):
                if not file:
                    requested_times.remove(requested_times[ind])
            if None in requested_files:         
                requested_files.remove(None)
            # Turn time array into nump array
            requested_times = np.array(requested_times)

        else:

            # requested_times = pd.date_range(start=time_range[0],
            #               end=time_range[1],
            #               freq='3H').to_pydatetime().tolist()

            requested_files = []
            requested_times = []
            files_in_cycle = fo.list_files(os.path.join(self.path, "*.nc"))
#            for file in files_in_cycle:                
            for ifile in range(0, len(files_in_cycle), tstride):
                file = files_in_cycle[ifile]
                t_file = datetime.datetime.strptime(file[-16:-3],
                                                    "%Y%m%d_%H%M")
                if t_file>=time_range[0] and t_file<=time_range[1]:
                    requested_files.append(os.path.join(self.path, file))
                    requested_times.append(t_file)
                     
        # And now loop through the files, read them and store them in large array
        self.time = np.array(requested_times)
        
        if not requested_files:
            print("No meteo data files found within requested time range")
            return

        # Read in first file to get dimensions
        dnc   = nc.Dataset(requested_files[0])
        lon   = dnc["lon"][0::xystride].data - 360.0
        lat   = dnc["lat"][0::xystride].data
        lat   = np.flip(lat)
        nrows = len(lat)
        ncols = len(lon)
        ntime = len(requested_times)
        self.x = lon
        self.y = lat

        for ind, param in enumerate(parameters):

            if param == "wind":
                matrix = MeteoMatrixVector()
            else:
                matrix = MeteoMatrixScalar()
                
            matrix.name = param
            
            if param == "wind":            
                matrix.u    = np.empty((ntime, nrows, ncols))
                matrix.v    = np.empty((ntime, nrows, ncols))
                matrix.u[:] = np.nan
                matrix.v[:] = np.nan
            else:
                matrix.val    = np.empty((ntime, nrows, ncols))
                matrix.val[:] = np.nan
        
            for it, time in enumerate(requested_times):
                
                print("Reading " + requested_files[it] + " ...")
                dnc = nc.Dataset(requested_files[it])
                uuu = dnc["wind_u"]
                                
                try:
                    if param == "wind":            
                        uuu = dnc["wind_u"][:,:].data
                        vvv = dnc["wind_v"][:,:].data
                        uuu = np.flipud(uuu[0::xystride,0::xystride])
                        vvv = np.flipud(vvv[0::xystride,0::xystride])
                        matrix.u[it,:,:] = uuu
                        matrix.v[it,:,:] = vvv
#                        matrix.u[it,:,:] = np.flipud(dnc["wind_u"][0::xystride,0::xystride].data)
#                        matrix.v[it,:,:] = np.flipud(dnc["wind_v"][0::xystride,0::xystride].data)
                    else:    
                        uuu = dnc[param][:,:].data
                        uuu = np.flipud(uuu[0::xystride,0::xystride])
                        matrix.val[it,:,:] = uuu
                except:
                    print("Could not collect " + param + " from " + requested_files[it])
            
            self.quantity.append(matrix)        

    def read_from_delft3d(self, file_name, crs=None):
        pass

    def write_to_delft3d(self,
                         file_name,
                         version="1.03",
                         path=None,
                         header_comments=False,
                         refdate=None,
                         parameters=None,
                         time_range=None):
        
        if not refdate:
            refdate = self.time[0]

        if not time_range:
            time_range = [self.time[0], self.time[-1]]

        if not parameters:
            parameters = []
            for q in self.quantity:
                parameters.append(q.name)
        
        if self.crs.is_geographic:
            grid_unit = "degrees"
        else:
            grid_unit = "m"

        files=[]
        for param in parameters:            
            # Look up index of this parameter
            for ind, quant in enumerate(self.quantity):
                if param == quant.name:                    
                    q = self.quantity[ind]
                    break
            if param == "wind":
                file = dict()
                file["data"] = q.u
                file["ext"] = "amu"
                file["quantity"] = "x_wind"
                file["unit"] = "m s-1"
                file["fmt"]  = "%6.1f"
                files.append(file)
                file = dict()
                file["data"] = q.v
                file["ext"] = "amv"
                file["quantity"] = "y_wind"
                file["unit"] = "m s-1"
                file["fmt"]  = "%6.1f"
                files.append(file)
            elif param == "barometric_pressure":
                file = dict()
                file["data"] = q.val
                file["ext"] = "amp"
                file["quantity"] = "air_pressure"
                file["unit"] = "Pa"
                file["fmt"]  = "%7.0f"
                files.append(file)
            elif param == "precipitation":
                file = dict()
                file["data"] = q.val
                file["ext"] = "ampr"
                file["quantity"] = "precipitation"
                file["unit"] = "mm h-1"
                file["fmt"]  = "%7.1f"
                files.append(file)
        
            
        # if self.quantity == "x_wind":
        #     unit = "m s-1"
        #     ext  = "amu"
        #     fmt  = "%6.1f"
        # elif self.quantity == "y_wind":
        #     unit = "m s-1"
        #     ext  = "amv"
        #     fmt  = "%6.1f"
        # elif self.quantity == "air_pressure":
        #     unit = "Pa"
        #     ext  = "amp"
        #     fmt  = "%7.0f"
        # elif self.quantity == "air_temperature":
        #     unit = "Celsius"
        #     ext  = "amt"
        #     fmt  = "%7.1f"
        # elif self.quantity == "relative_humidity":
        #     unit = "%"
        #     ext  = "amr"
        #     fmt  = "%7.1f"
        # elif self.quantity == "cloudiness":
        #     unit = "%"
        #     ext  = "amc"
        #     fmt  = "%7.1f"
        # elif self.quantity == "sw_radiation_flux":
        #     unit = "W/m2"
        #     ext  = "ams"
        #     fmt  = "%7.1f"
        # elif self.quantity == "precipitation":
        #     unit = "mm/h"
        #     ext  = "ampr"
        #     fmt  = "%7.1f"

        for file in files:

            ncols = len(self.x)
            nrows = len(self.y)
    
            dx = (self.x[-1]-self.x[0])/(len(self.x)-1)
            dy = (self.y[-1]-self.y[0])/(len(self.y)-1)
            
            if path:
                full_file_name = os.path.join(path, file_name + "." + file["ext"])
            else:
                full_file_name = file_name + "." + file["ext"]
                    
            fid = open(full_file_name, "w")
            
            if header_comments:
                fid.write("### START OF HEADER\n")
                fid.write("### All text on a line behind the first # is parsed as commentary\n")
                fid.write("### Additional commments\n")
    
            fid.write("FileVersion      =   " + version + "                                               # Version of meteo input file, to check if the newest file format is used\n")
            fid.write("filetype         =   meteo_on_equidistant_grid                          # Type of meteo input file: meteo_on_flow_grid, meteo_on_equidistant_grid, meteo_on_curvilinear_grid or meteo_on_spiderweb_grid\n")
            fid.write("NODATA_value     =   -999                                               # Value used for undefined or missing data\n")
            fid.write("n_cols           =   " + str(ncols) + "\n")
            fid.write("n_rows           =   " + str(nrows) + "\n")
            fid.write("grid_unit        =   " + grid_unit + "\n")
#            fid.write("x_llcorner       =   " + str(min(self.x)) + "\n")
#            fid.write("y_llcorner       =   " + str(min(self.y)) + "\n")
            fid.write("x_llcorner       =   " + str(min(self.x) - 0.5*dx) + "\n")
            fid.write("y_llcorner       =   " + str(min(self.y) - 0.5*dy) + "\n")
            if version == "1.02":
                fid.write("value_pos       =    corner\n")
            fid.write("dx               =   " + str(dx) + "\n")
            fid.write("dy               =   " + str(dy) + "\n")
            fid.write("n_quantity       =   1                                                  # Number of quantities prescribed in the file\n")
            fid.write("quantity1        =   " + file["quantity"] + "\n")
            fid.write("unit1            =   " + file["unit"] + "\n")
            if header_comments:
                fid.write("### END OF HEADER\n")

            # Add extra blocks if data does not cover time range
            if self.time[0] > time_range[0]:
                dt  = time_range[0] - refdate
                tim = dt.total_seconds()/60
                val = np.flipud(file["data"][0,:,:])                
                # Skip blocks with only nans
                if not np.all(np.isnan(val)):
                    val[val==np.nan] = -999.0
                    fid.write("TIME = " + str(tim) + ' minutes since ' + refdate.strftime("%Y-%m-%d %H:%M:%S") + ' +00:00\n')
                    np.savetxt(fid, val, fmt=file["fmt"])                
            
            for it, time in enumerate(self.time):
                
                dt  = time - refdate
                tim = dt.total_seconds()/60
                val = np.flipud(file["data"][it,:,:])
                
                if param=="wind":
                    if np.max(val)>1000.0:
                        val = np.nan
                    if np.min(val)<-1000.0:
                        val = np.nan
                if param=="barometric_pressure":      
                    if np.max(val)>200000.0:
                        val = np.nan
                    if np.min(val)<10000.0:
                        val = np.nan
                if param=="precipitation":      
                    if np.max(val)>10000.0:
                        val = np.nan
                    if np.min(val)<-100.0:
                        val = np.nan
                    if np.any(np.isnan(val)):
                        val = np.zeros_like(val)  #or zeros_like?
                        print("Warning! Filling NaNs in precipitation with zeros")

                if np.all(np.isnan(val)):
                    print("Warning! Only NaNs found for " + param + " at " + time.strftime("%Y-%m-%d %H:%M:%S") + " ! Using data from previous time.")
                    file["data"][it,:,:] = file["data"][it - 1,:,:]
                    val = np.flipud(file["data"][it,:,:])
                
                # Skip blocks with only nans
                if not np.all(np.isnan(val)):
                    val[val==np.nan] = -999.0
                    fid.write("TIME = " + str(tim) + ' minutes since ' + refdate.strftime("%Y-%m-%d %H:%M:%S") + ' +00:00\n')
                    np.savetxt(fid, val, fmt=file["fmt"])                    

            # Add extra blocks if data does not cover time range
            if self.time[-1] < time_range[1]:
                dt  = time_range[1] - refdate
                tim = dt.total_seconds()/60
                val = np.flipud(file["data"][-1,:,:])                
                # Skip blocks with only nans
                if not np.all(np.isnan(val)):
                    val[val==np.nan] = -999.0
                    fid.write("TIME = " + str(tim) + ' minutes since ' + refdate.strftime("%Y-%m-%d %H:%M:%S") + ' +00:00\n')
                    np.savetxt(fid, val, fmt=file["fmt"])                

            fid.close()

    def write_wind_to_json(self, file_name, time_range=None, iref=1):
        
        import json
        
        if not time_range:
            time_range = []
            time_range.append(self.time[0])
            time_range.append(self.time[-1])

        data = []
        
        header = {
            "discipline":0,
            "disciplineName":"Meteorological products",
            "gribEdition":2,
            "gribLength":76420,
            "center":7,
            "centerName":"US National Weather Service - NCEP(WMC)",
            "subcenter":0,
            "refTime":"2016-04-30T06:00:00.000Z",
            "significanceOfRT":1,
            "significanceOfRTName":"Start of forecast",
            "productStatus":0,
            "productStatusName":"Operational products",
            "productType":1,
            "productTypeName":"Forecast products",
            "productDefinitionTemplate":0,
            "productDefinitionTemplateName":"Analysis/forecast at horizontal level/layer at a point in time",
            "parameterCategory":2,
            "parameterCategoryName":"Momentum",
            "parameterNumber":2,
            "parameterNumberName":"U-component_of_wind",
            "parameterUnit":"m.s-1",
            "genProcessType":2,
            "genProcessTypeName":"Forecast",
            "forecastTime":0,
            "surface1Type":103,
            "surface1TypeName":"Specified height level above ground",
            "surface1Value":10.0,
            "surface2Type":255,
            "surface2TypeName":"Missing",
            "surface2Value":0.0,
            "gridDefinitionTemplate":0,
            "gridDefinitionTemplateName":"Latitude_Longitude",
            "numberPoints":65160,
            "shape":6,
            "shapeName":"Earth spherical with radius of 6,371,229.0 m",
            "gridUnits":"degrees",
            "resolution":48,
            "winds":"true",
            "scanMode":0,
            "nx":360,
            "ny":181,
            "basicAngle":0,
            "subDivisions":0,
            "lo1":0.0,
            "la1":90.0,
            "lo2":359.0,
            "la2":-90.0,
            "dx":1.0,
            "dy":1.0,
        }
        
        header["lo1"] = float(min(self.x) + 360.0)
        header["lo2"] = float(max(self.x) + 360.0)
        header["la1"] = float(max(self.y))
        header["la2"] = float(min(self.y))
        header["dx"]  = float(self.x[1] - self.x[0])
        header["dy"]  = float(self.y[1] - self.y[0])
        header["nx"]  = len(self.x)
        header["ny"]  = len(self.y)
        header["numberPoints"] = len(self.x)*len(self.y)
        
        header_u = header.copy()
        header_v = header.copy()
        
        header_u["parameterNumberName"] = "U-component_of_wind"
        header_u["parameterNumber"]     = 2
        header_v["parameterNumberName"] = "V-component_of_wind"
        header_v["parameterNumber"]     = 3
        
        for it, t in enumerate(self.time):
            if t>=time_range[0] and t<=time_range[1]:
                
                dd = []

                tstr = t.strftime("%Y-%m-%dT%H:%M:%SZ")

                u_list = np.flipud(np.around(self.quantity[0].u[it,:,:],decimals=1)).flatten().tolist()
                data0 = {"header": header_u.copy(), "data": u_list}
                data0["header"]["refTime"] = tstr
                dd.append(data0)
                
                v_list = np.flipud(np.around(self.quantity[0].v[it,:,:],decimals=1)).flatten().tolist()
                data0 = {"header": header_v.copy(), "data": v_list}
                data0["header"]["refTime"] = tstr
                dd.append(data0)

                data.append(dd)
        
        json_string = json.dumps(data, separators=(',',':'))
        fid = open(file_name, "w")
        fid.write(json_string)
        fid.close()


    def write_to_netcdf(self,
                        file_name):
        pass

    def subset(self, name=None,
               parameters=None,
               time_range = [],
               x=None,    y=None, 
               xlim=None, ylim=None,
               stride=1,
               crs=None):

        # if not time_range:
        #     time_range.append[self.time[0]]
        #     time_range.append[self.time[-1]]
        if not time_range:
            times = self.time
        else:
            it0 = np.where(self.time == time_range[0])[0]
            if np.size(it0)==0:
                # Find first available time
                it0 = np.where((self.time >= time_range[0]) * (self.time<=time_range[1]))[0]
                if np.size(it0) == 0:
                    print("No data found in requested time range.")
                    dataset = []
                    return dataset
                else:
                    it0 = it0[0]
                    print("First requested time not found. Using first time available.")

            else:    
                it0 = it0[0]

            it1 = np.where(self.time == time_range[1])[0]
            if np.size(it1)==0:
                # Find last available time
                it1 = np.where((self.time >= time_range[0]) * (self.time<=time_range[1]))[0]
                if np.size(it1) == 0:
                    print("No data found in requested time range.")
                    dataset = []
                    return dataset
                else:
                    it1 = it1[-1]
                    print("Last requested time not found. Using last time available.")
            else:
                it1 = it1[0]

            times = self.time[it0:it1 + 1]
        interp = False
        if x is not None and y is not None:
            # Re-interpolate
            xg, yg = np.meshgrid(x, y)
            interp = True
        elif xlim is not None and ylim is not None:
            # Limit based on bbox
            jlast = np.where(self.x >= xlim[1])[-1]
            j0 = np.asarray(np.where(self.x <= xlim[0]))[0][-1]
            j1 = np.asarray(np.where(self.x >= xlim[1]))[0][0] + 1
            i0 = np.asarray(np.where(self.y <= ylim[0]))[0][-1]
            i1 = np.asarray(np.where(self.y >= ylim[1]))[0][0] + 1
            x = self.x[j0:j1:stride]
            y = self.y[i0:i1:stride]       
        else:    
            j0 = 0
            j1 = len(self.x) - 1
            i0 = 0
            i1 = len(self.y) - 1
            x = self.x[j0:j1:stride]
            y = self.y[i0:i1:stride]
        if not crs:
            crs = self.crs
        else:
            if interp:
                transformer = Transformer.from_crs(crs, self.crs, always_xy=True)
                xg, yg = transformer.transform(xg, yg)
                    
        # Make a new dataset
        dataset      = MeteoGrid()

        dataset.time = times
        dataset.x    = x
        dataset.y    = y
        dataset.crs  = crs
        dataset.last_analysis_time = self.last_analysis_time
        
        nrows   = len(y)
        ncols   = len(x)
        nt      = len(times)
        
        for q in self.quantity:
            
            if q.name == "wind":
                q1 = MeteoMatrixVector()
                q1.u = np.zeros((nt, nrows, ncols))
                q1.v = np.zeros((nt, nrows, ncols))
            else:    
                q1     = MeteoMatrixScalar()
                q1.val = np.zeros((nt, nrows, ncols))

            q1.name = q.name
            q1.unit = q.unit
            
            for it, time in enumerate(times):
                
                it0 = int(np.where(self.time == time)[0])
                    
                if interp:

                    if q.name == "wind":
                        q1.u[it,:,:] = interp2(self.x, self.y, q.u[it0,:,:], xg, yg)
                        q1.v[it,:,:] = interp2(self.x, self.y, q.v[it0,:,:], xg, yg)                    
                    else:
                        q1.val[it,:,:] = interp2(self.x, self.y, q.val[it0,:,:], xg, yg)

                else:

                    if q.name == "wind":
                        q1.u[it,:,:] = q.u[it0,i0:i1:stride,j0:j1:stride]
                        q1.v[it,:,:] = q.v[it0,i0:i1:stride,j0:j1:stride]                   
                    else:
                        q1.val[it,:,:] = q.val[it0,i0:i1:stride,j0:j1:stride]
                
            dataset.quantity.append(q1)    
                
        return dataset    

    def to_pandas(self):
        pass

class MeteoSpiderweb():
    
    def __init__(self, filename=None):
        pass

        if filename:
            self.read(filename)

    def read(self, file_name, crs=None):
        pass

    def write(self, file_name, refdate=None):
        pass
    
    def to_grid(self, x, y, crs=None):
        grd = MeteoGrid()        
        return grd
    
    def from_grid(self, meteo_grid, crs=None):
        pass

def merge(forcing_list):

    meteo_grid = MeteoGrid()

    return meteo_grid
