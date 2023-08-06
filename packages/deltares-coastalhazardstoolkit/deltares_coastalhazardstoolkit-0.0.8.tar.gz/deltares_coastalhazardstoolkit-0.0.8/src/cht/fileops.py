# -*- coding: utf-8 -*-
"""
Created on Tue May 18 12:00:56 2021

@author: ormondt
"""

import glob
import shutil
import os

def move_file(src, dst):
    
    for full_file_name in glob.glob(src):
        src_name = os.path.basename(full_file_name)        
        if os.path.exists(os.path.join(dst, src_name)):
            os.remove(os.path.join(dst, src_name))
        shutil.move(full_file_name, dst)

def copy_file(src, dst):
    
    for full_file_name in glob.glob(src):
        src_name = os.path.basename(full_file_name)        
        if os.path.exists(os.path.join(dst, src_name)):
            os.remove(os.path.join(dst, src_name))
        if os.path.isdir(full_file_name):
            dstf = os.path.join(dst, os.path.basename(full_file_name))
            shutil.copytree(full_file_name, dstf)
        else:    
            shutil.copy(full_file_name, dst)

def delete_file(src):
    
    for file_name in glob.glob(src):
        os.remove(src)

def rm(src):
    
    os.remove(src)

def mkdir(path):

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

def delete_folder(src):
    try:
        shutil.rmtree(src, ignore_errors=False, onerror=None)
    except:
        # Folder was probably open in another application
        print("Could not delete folder " + src)

def rmdir(src):
    try:
        if os.path.exists(src):
            shutil.rmtree(src, ignore_errors=False, onerror=None)
    except:
        # Folder was probably open in another application
        print("Could not delete folder " + src)

def exists(src):    
    if os.path.exists(src):
        return True
    else:
        return False    
