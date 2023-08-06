# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:02:04 2021

@author: ormondt
"""

import os

import cht.xmlkit as xml
from .cosmos_main import cosmos
from cht.misc_tools import rgb2hex


def read_config_file():
    
    main_path = cosmos.config.main_path
    
    config_file = os.path.join(main_path,
                               "configurations",
                               cosmos.config.config_file)
    
    # Defaults
    cosmos.config.ftp_hostname       = None
    cosmos.config.ftp_path           = None
    cosmos.config.ftp_username       = None
    cosmos.config.ftp_password       = None
    cosmos.config.webviewer_version  = None
    cosmos.config.sfincs_exe_path    = os.path.join(main_path, "exe", "sfincs")
    cosmos.config.hurrywave_exe_path = os.path.join(main_path, "exe", "hurrywave")
    cosmos.config.xbeach_exe_path    = os.path.join(main_path, "exe", "xbeach")
    cosmos.config.delft3dfm_exe_path = os.path.join(main_path, "exe", "delft3dfm")
    cosmos.config.cycle_interval     = 6
    cosmos.config.run_mode           = "serial"

    # Read xml config file
    xml_obj = xml.xml2obj(config_file)

    if hasattr(xml_obj, "ftp_hostname"):
        if hasattr(xml_obj.ftp_hostname[0],"value"):
            cosmos.config.ftp_hostname = xml_obj.ftp_hostname[0].value
    if hasattr(xml_obj, "ftp_path"):
        if hasattr(xml_obj.ftp_path[0],"value"):
            cosmos.config.ftp_path = xml_obj.ftp_path[0].value
    if hasattr(xml_obj, "ftp_username"):
        if hasattr(xml_obj.ftp_username[0],"value"):
            cosmos.config.ftp_username = xml_obj.ftp_username[0].value
    if hasattr(xml_obj, "ftp_password"):
        if hasattr(xml_obj.ftp_password[0],"value"):
            cosmos.config.ftp_password = xml_obj.ftp_password[0].value
    if hasattr(xml_obj, "webviewer_version"):
        cosmos.config.webviewer_version = xml_obj.webviewer_version[0].value
    if hasattr(xml_obj, "sfincs_exe_path"):
        cosmos.config.sfincs_exe_path = xml_obj.sfincs_exe_path[0].value
    if hasattr(xml_obj, "hurrywave_exe_path"):
        cosmos.config.hurrywave_exe_path = xml_obj.hurrywave_exe_path[0].value
    if hasattr(xml_obj, "xbeach_exe_path"):
        cosmos.config.xbeach_exe_path = xml_obj.xbeach_exe_path[0].value
    if hasattr(xml_obj, "delft3dfm_exe_path"):
        cosmos.config.delft3dfm_exe_path = xml_obj.delft3dfm_exe_path[0].value
    if hasattr(xml_obj, "cycle_interval"):
        cosmos.config.cycle_interval = xml_obj.cycle_interval[0].value

    # Map contours
    contour_file = os.path.join(main_path, "configurations", "map_contours.xml")
    xml_obj = xml.xml2obj(contour_file)
    cosmos.config.map_contours = []
    maps = xml_obj.tile_map
    for tm in maps:
        map_type = {}
        map_type["name"] = tm.name
        map_type["string"] = tm.legend_text[0].value
        map_type["contours"] = []
        for c in tm.contour:
            cnt = {}
            cnt["string"] = c.legend_text[0].value
            cnt["lower_value"] = c.lower[0].value
            cnt["upper_value"] = c.upper[0].value
            cnt["rgb"]   = c.rgb[0].value
            cnt["hex"]   = rgb2hex(tuple(cnt["rgb"]))
            
            map_type["contours"].append(cnt)

        cosmos.config.map_contours.append(map_type)    
