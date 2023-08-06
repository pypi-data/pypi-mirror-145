# -*- coding: utf-8 -*-
"""
Created on Wed May 12 08:59:03 2021

@author: ormondt
"""

import xml.etree.ElementTree as ET
from datetime import datetime

def xml2obj(file_name):    

    xml_root = ET.parse(file_name).getroot()
    obj = xml2py(xml_root)

    return obj
    
def xml2py(node):

    name = node.tag

    pytype = type(name, (object, ), {})
    pyobj = pytype()

    for attr in node.attrib.keys():
        setattr(pyobj, attr, node.get(attr))

    if node.text and node.text != '' and node.text != ' ' and node.text != '\n':
        setattr(pyobj, 'text', node.text)
        setattr(pyobj, 'value', node.text)
        # Convert
        if node.attrib:
            if "type" in node.attrib.keys():
                if node.attrib["type"] == "float":
                    lst = node.text.split(",")
                    if len(lst)==1:
                       pyobj.value = float(node.text)
                    else:                    
                       float_list = [float(s) for s in lst]
                       pyobj.value = float_list
                elif node.attrib["type"] == "int":
                    if "," in node.text:                   
                        pyobj.value = [int(s) for s in node.text.split(',')]
                    else:    
                        pyobj.value = int(node.text)
                elif node.attrib["type"] == "datetime":
                    pyobj.value = datetime.strptime(node.text,
                                                    '%Y%m%d %H%M%S')

    for cn in node:
        if not hasattr(pyobj, cn.tag):
            setattr(pyobj, cn.tag, [])
        getattr(pyobj, cn.tag).append(xml2py(cn))

    return pyobj    

def get_value(file_name, tag):    

    xml_root = ET.parse(file_name).getroot()
    node     = xml_root.findall(tag)[0]
    val      = node.text
    if node.attrib:
        if "type" in node.attrib.keys():
            if node.attrib["type"] == "float":
                val = float(node.text)
            elif node.attrib["type"] == "int":
                val = int(node.text)
            elif node.attrib["type"] == "datetime":
                val = datetime.strptime(node.text,
                                                '%Y%m%d %H%M%S')
    return val
