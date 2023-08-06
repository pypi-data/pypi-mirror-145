# -*- coding: utf-8 -*-
"""
Created on Fri Sep  3 13:40:56 2021

@author: ormondt
"""

import os
from pyproj import CRS
from pyproj import Transformer
import pandas as pd

def nest1(overall, detail, option=None):
    
    # Returns a list with observation point objects
    
    if overall.type.lower() == "delft3dfm":
        if detail.type.lower() == "delft3dfm":
            nest1_delft3dfm_in_delft3dfm(overall, detail)
        elif detail.type.lower() == "sfincs":
            nest1_sfincs_in_delft3dfm(overall, detail)
        elif detail.type.lower() == "beware":
            pass
#            nest1_beware_in_delft3dfm(overall, detail)
            
    elif overall.type.lower() == "sfincs":
        if detail.type.lower() == "sfincs":
            nest1_sfincs_in_sfincs(overall, detail)
        elif detail.type.lower() == "xbeach":
            nest1_xbeach_in_sfincs(overall, detail)

    elif overall.type.lower() == "hurrywave":
        if detail.type.lower() == "hurrywave":
            nest1_hurrywave_in_hurrywave(overall, detail)
        elif detail.type.lower() == "xbeach":    
            if not option:
                option = "timeseries"
            nest1_xbeach_in_hurrywave(overall, detail, option=option)
        elif detail.type.lower() == "sfincs":    
            nest1_sfincs_in_hurrywave(overall, detail)

#        elif detail.type == "delft3dfm":
#            obs = nest1_delft3dfm_in_sfincs(overall, detail)

#    return obs    

def nest2(overall,
          detail,
          boundary_water_level_correction=None,
          output_path=None,
          output_file=None):


    if not boundary_water_level_correction:
        # Path of the overall output time series
        boundary_water_level_correction = 0.0
    
    if overall.type.lower() == "delft3dfm":

        if detail.type.lower() == "delft3dfm":
            nest2_delft3dfm_in_delft3dfm(overall,
                                         detail,
                                         output_path,
                                         output_file,
                                         boundary_water_level_correction)

        elif detail.type.lower() == "sfincs":
            nest2_sfincs_in_delft3dfm(overall,
                                      detail,
                                      output_path,
                                      output_file,
                                      boundary_water_level_correction)

        elif detail.type.lower() == "beware":
            nest2_beware_in_delft3dfm(overall,
                                      detail,
                                      output_path,
                                      output_file,
                                      boundary_water_level_correction)
            
    elif overall.type.lower() == "sfincs":

        if detail.type.lower() == "sfincs":
            nest2_sfincs_in_sfincs(overall,
                                   detail,
                                   output_path,
                                   output_file,
                                   boundary_water_level_correction)
        elif detail.type.lower() == "xbeach":
            nest2_xbeach_in_sfincs(overall,
                                   detail,
                                   output_path,
                                   output_file,
                                   boundary_water_level_correction)

    elif overall.type.lower() == "hurrywave":

        if detail.type.lower() == "hurrywave":
            nest2_hurrywave_in_hurrywave(overall,
                                   detail,
                                   output_path,
                                   output_file)
        elif detail.type.lower() == "xbeach":
            nest2_xbeach_in_hurrywave(overall,
                                   detail,
                                   output_path,
                                   output_file)
        elif detail.type.lower() == "sfincs":
            nest2_sfincs_in_hurrywave(overall,
                                      detail,
                                      output_path,
                                      output_file)

    elif overall.type.lower() == "beware":

        if detail.type.lower() == "sfincs":
            nest2_sfincs_in_beware(overall,
                                   detail,
                                   output_path,
                                   output_file)

def nest1_delft3dfm_in_delft3dfm(overall, detail):
    
#    from delft3dfm import ObservationPoint as obspoint
    
    transformer = Transformer.from_crs(detail.crs,
                                       overall.crs,
                                       always_xy=True)
    
    for ind, bnd in enumerate(detail.boundary):        
        for ip, point in enumerate(bnd.point):
            x, y = transformer.transform(point.geometry.x,
                                         point.geometry.y)
            overall.add_observation_point(x, y, detail.name + "_" + point.name)
    
def nest1_sfincs_in_delft3dfm(overall, detail):
    
#    from delft3dfm import ObservationPoint as obspoint
    
    transformer = Transformer.from_crs(detail.crs,
                                       overall.crs,
                                       always_xy=True)
    
    for ind, point in enumerate(detail.flow_boundary_point):

        name = detail.name + "_" + str(ind + 1).zfill(4)
        x, y = transformer.transform(point.geometry.x,
                                     point.geometry.y)
#        obs_list.append(obspoint(x, y, name, crs=overall.crs))
        overall.add_observation_point(x, y, name)
    
    
def nest1_sfincs_in_sfincs(overall, detail):
    
#    from sfincs import ObservationPoint as obspoint

    transformer = Transformer.from_crs(detail.crs,
                                       overall.crs,
                                       always_xy=True)
    
    for ind, point in enumerate(detail.flow_boundary_point):

        name = detail.name + "_" + str(ind + 1).zfill(4)
        x, y = transformer.transform(point.geometry.x,
                                     point.geometry.y)
#        obs_list.append(obspoint(x, y, name, crs=overall.crs))
        overall.add_observation_point(x, y, name)

def nest1_xbeach_in_sfincs(overall, detail):
    
    transformer = Transformer.from_crs(detail.crs,
                                       overall.crs,
                                       always_xy=True)
    
    for ind, point in enumerate(detail.flow_boundary_point):

        name = detail.name + "_" + str(ind + 1).zfill(4)
        x, y = transformer.transform(point.geometry.x,
                                     point.geometry.y)
#        obs_list.append(obspoint(x, y, name, crs=overall.crs))
        overall.add_observation_point(x, y, name)


def nest1_hurrywave_in_hurrywave(overall, detail):
    
    transformer = Transformer.from_crs(detail.crs,
                                       overall.crs,
                                       always_xy=True)
    
    for ind, point in enumerate(detail.boundary_point):

        name = detail.name + "_" + str(ind + 1).zfill(4)
        x, y = transformer.transform(point.geometry.x,
                                     point.geometry.y)
#        obs_list.append(obspoint(x, y, name, crs=overall.crs))
        overall.add_observation_point_sp2(x, y, name)

def nest1_xbeach_in_hurrywave(overall, detail, option="sp2"):
    
    transformer = Transformer.from_crs(detail.crs,
                                       overall.crs,
                                       always_xy=True)
    
    for ind, point in enumerate(detail.wave_boundary_point):

        name = detail.name + "_" + str(ind + 1).zfill(4)
        x, y = transformer.transform(point.geometry.x,
                                     point.geometry.y)
#        obs_list.append(obspoint(x, y, name, crs=overall.crs))
#        if option=="sp2":
        overall.add_observation_point_sp2(x, y, name)
#        else:
        overall.add_observation_point(x, y, name)

def nest1_sfincs_in_hurrywave(overall, detail):
    
    transformer = Transformer.from_crs(detail.crs,
                                       overall.crs,
                                       always_xy=True)

    for ind, point in enumerate(detail.wave_boundary_point):

        name = detail.name + "_" + str(ind + 1).zfill(4)
        x, y = transformer.transform(point.geometry.x,
                                     point.geometry.y)
        overall.add_observation_point(x, y, name)
            
def nest2_delft3dfm_in_delft3dfm(overall,
                                 detail,
                                 output_path,
                                 output_file,
                                 boundary_water_level_correction):

    if not output_file:
        # Path of the overall output time series
        output_file = overall.runid + "_his.nc"

#    output_file = os.path.join(output_path, output_file)

    for ind, bnd in enumerate(detail.boundary):        
        point_names = []
        for ip, point in enumerate(bnd.point):
            point_names.append(detail.name + "_" + point.name)
        # Return DataFrame bzs
        bzs = overall.read_timeseries_output(name_list=point_names,
                                             path=output_path,
                                             file_name=output_file)
        ts  = bzs.index
        for ip, point in enumerate(bnd.point):
            point.data = pd.Series(bzs.iloc[:,ip].values, index=ts) + boundary_water_level_correction    
    
def nest2_sfincs_in_delft3dfm(overall,
                              detail,
                              output_path,
                              output_file,
                              boundary_water_level_correction):

    if not output_file:
        # Path of the overall output time series
        output_file = overall.runid + "_his.nc"
    
    point_names = []
    for point in detail.flow_boundary_point:
        point_names.append(detail.name + "_" + point.name)                    
    output_file = os.path.join(output_path, output_file)

    # Return DataFrame bzs
    bzs = overall.read_timeseries_output(name_list=point_names,
                                         path=output_path,
                                         file_name=output_file)

    ts  = bzs.index
    for icol, point in enumerate(detail.flow_boundary_point):
        point.data = pd.Series(bzs.iloc[:,icol].values, index=ts) + boundary_water_level_correction    

def nest2_beware_in_delft3dfm(overall,
                              detail,
                              output_path,
                              output_file,
                              boundary_water_level_correction):

    if not output_file:
        # Path of the overall output time series
        output_file = overall.runid + "_his.nc"
    
    point_names = []
    for point in detail.flow_boundary_point:
        point_names.append(detail.name + "_" + point.name)                    
    output_file = os.path.join(output_path, output_file)

    # Return DataFrame bzs
    bzs = overall.read_timeseries_output(name_list=point_names,
                                         path=output_path,
                                         file_name=output_file)

    ts  = bzs.index
    for icol, point in enumerate(detail.flow_boundary_point):
        point.data = pd.Series(bzs.iloc[:,icol].values, index=ts) + boundary_water_level_correction    
    
def nest2_sfincs_in_sfincs(overall,
                           detail,
                           output_path,
                           output_file,
                           boundary_water_level_correction):

    if not output_path:
        # Path of the overall output time series
        output_path = overall.path
    
        
    if overall.input.outputformat[0:3] == "bin":
        # ascii output        
        if not output_file:
            output_file = "zst.txt"
    else:
        # netcdf        
        if not output_file:
            output_file = "sfincs_his.nc"
    
    point_names = []
    for point in detail.flow_boundary_point:
        point_names.append(detail.name + "_" + point.name)                    
    zstfile = os.path.join(output_path, output_file)

    # Return DataFrame bzs
    bzs = overall.read_timeseries_output(name_list=point_names,
                                         file_name=zstfile)

    ts  = bzs.index
    for icol, point in enumerate(detail.flow_boundary_point):
        point.data = pd.Series(bzs.iloc[:,icol].values, index=ts) + boundary_water_level_correction

def nest2_xbeach_in_sfincs(overall,
                           detail,
                           output_path,
                           output_file,
                           boundary_water_level_correction):

    if not output_path:
        # Path of the overall output time series
        output_path = overall.path
        
    if not output_file:
        output_file = "zst.txt"
    
    point_names = []
    for point in detail.flow_boundary_point:
        point_names.append(detail.name + "_" + point.name)                    
    zstfile = os.path.join(output_path, output_file)

    # Return DataFrame bzs
    bzs = overall.read_timeseries_output(name_list=point_names,
                                         file_name=zstfile)

    ts  = bzs.index
    for icol, point in enumerate(detail.flow_boundary_point):
        point.data = pd.Series(bzs.iloc[:,icol].values, index=ts) + boundary_water_level_correction
    
def nest2_hurrywave_in_hurrywave(overall,
                                 detail,
                                 output_path,
                                 output_file):
    import xarray as xr
    import numpy as np

    if not output_path:
        # Path of the overall output time series
        output_path = overall.path
        
    if not output_file:
        output_file = "hurrywave_sp2.nc"

    file_name = os.path.join(output_path, output_file)

    # Open netcdf file
    ddd = xr.open_dataset(file_name)
    stations=ddd.station_name.values
    all_stations = []
    for ist, st in enumerate(stations):
        st=str(st.strip())[2:-1]
        all_stations.append(st)

    point_names = []    
    if detail.boundary_point:
        # Find required boundary points        
        for point in detail.boundary_point:
            point_names.append(detail.name + "_" + point.name)                    
        
    else:
        point_names = all_stations.copy()
        
    times   = ddd.point_spectrum2d.coords["time"].values
    sigma   = ddd.point_spectrum2d.coords["sigma"].values
    theta   = ddd.point_spectrum2d.coords["theta"].values

    ireq = []    
    for ip, point in enumerate(point_names):
        for ist,st in enumerate(all_stations):
            if point.lower() == st.lower():
                ireq.append(ist)            
                break

    for ip, point in enumerate(detail.boundary_point):

        sp2 = ddd.point_spectrum2d.values[:,ireq[ip],:,:]

        ds = xr.Dataset(
                data_vars = dict(point_spectrum2d=(["time", "theta", "sigma"], sp2)),
                coords    = dict(time=times,
                                 theta=theta,
                                 sigma=sigma)
                )
        
        point.data = ds
            
    # point_names = []
    # for point in detail.flow_boundary_point:
    #     point_names.append(detail.name + "_" + point.name)                    
    # zstfile = os.path.join(output_path, output_file)

    # # Return DataFrame bzs
    # bzs = overall.read_timeseries_output(name_list=point_names,
    #                                      file_name=zstfile)

    # ts  = bzs.index
    # for icol, point in enumerate(detail.flow_boundary_point):
    #     point.data = pd.Series(bzs.iloc[:,icol].values, index=ts) + boundary_water_level_correction
     
def nest2_xbeach_in_hurrywave(overall,
                              detail,
                              output_path,
                              output_file,
                              option='sp2'):
    import xarray as xr
    import numpy as np

    if not output_path:
        # Path of the overall output time series
        output_path = overall.path
        
    if not output_file:
        output_file = "hurrywave_sp2.nc"

    file_name = os.path.join(output_path, output_file)

    # Open netcdf file
    ddd = xr.open_dataset(file_name)
    stations=ddd.station_name.values
    all_stations = []
    for ist, st in enumerate(stations):
        st=str(st.strip())[2:-1]
        all_stations.append(st)

    point_names = []    
    if detail.wave_boundary_point:
        # Find required boundary points        
        for point in detail.wave_boundary_point:
            point_names.append(detail.name + "_" + point.name)                    
        
    else:
        point_names = all_stations.copy()
        
    times   = ddd.point_spectrum2d.coords["time"].values
    sigma   = ddd.point_spectrum2d.coords["sigma"].values
    theta   = ddd.point_spectrum2d.coords["theta"].values

    ireq = []    
    for ip, point in enumerate(point_names):
        for ist,st in enumerate(all_stations):
            if point.lower() == st.lower():
                ireq.append(ist)            
                break

    for ip, point in enumerate(detail.wave_boundary_point):

        sp2 = ddd.point_spectrum2d.values[:,ireq[ip],:,:]

        ds = xr.Dataset(
                data_vars = dict(point_spectrum2d=(["time", "theta", "sigma"], sp2)),
                coords    = dict(time=times,
                                 theta=theta,
                                 sigma=sigma)
                )
        
        point.data = ds

def nest2_sfincs_in_hurrywave(overall,
                              detail,
                              output_path,
                              output_file):
    import xarray as xr
    import numpy as np

    if not output_path:
        # Path of the overall output time series
        output_path = overall.path
        
    if not output_file:
        output_file = "hurrywave_his.nc"

    file_name = os.path.join(output_path, output_file)

    # Open netcdf file
    ddd = xr.open_dataset(file_name)
    stations=ddd.station_name.values
    all_stations = []
    for ist, st in enumerate(stations):
        st=str(st.strip())[2:-1]
        all_stations.append(st)

    point_names = []    
    if detail.wave_boundary_point:
        # Find required boundary points        
        for point in detail.wave_boundary_point:
            point_names.append(detail.name + "_" + point.name)                    
        
    else:
        point_names = all_stations.copy()
        
    times   = ddd.point_hm0.coords["time"].values

    ireq = []    
    for ip, point in enumerate(point_names):
        for ist,st in enumerate(all_stations):
            if point.lower() == st.lower():
                ireq.append(ist)            
                break

    for ip, point in enumerate(detail.wave_boundary_point):

        hm0     = ddd.point_hm0.values[:,ireq[ip]]
        tp      = ddd.point_tp.values[:,ireq[ip]]
        wavdir  = ddd.point_wavdir.values[:,ireq[ip]]
        dirspr  = ddd.point_dirspr.values[:,ireq[ip]]

        df = pd.DataFrame(index=times)
        df.insert(0,"hm0",hm0)
        df.insert(1,"tp",tp)
        df.insert(2,"wavdir",wavdir)
        df.insert(3,"dirspr",dirspr)

        point.data = df

def nest2_sfincs_in_beware(overall,
                           detail,
                           output_path,
                           output_file,
                           option='sp2'):
    import xarray as xr
    import numpy as np
    