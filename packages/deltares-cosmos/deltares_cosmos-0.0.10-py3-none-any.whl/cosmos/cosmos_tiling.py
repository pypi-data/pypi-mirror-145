# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 12:17:22 2021

@author: ormondt
"""

from .cosmos_main import cosmos
from cht.tiling import make_png_tiles

def make_flood_map_tiles(zsmax, index_path, topo_path, flood_map_path,
                         water_level_correction=0.0):

    # Difference between MSL and NAVD88 (used in topo data)
    zsmax += water_level_correction

#    zoom_range = [0, 14]
    # index_path = os.path.join(model.path, "tiling", "indices")
    # topo_path = os.path.join(model.path, "tiling", "topobathy")

    # color_values = []

    # color_value = {}
    # color_value["lower_value"] = 0.05
    # color_value["upper_value"] = 0.30
    # color_value["string"]      = "0 - 1 ft"
    # color_value["rgb"]         = [0, 255, 0]
    # color_values.append(color_value)

    # color_value = {}
    # color_value["lower_value"] = 0.30
    # color_value["upper_value"] = 1.00
    # color_value["string"]      = "1 - 3 ft"
    # color_value["rgb"]         = [255, 255, 0]
    # color_values.append(color_value)

    # color_value = {}
    # color_value["lower_value"] = 1.00
    # color_value["upper_value"] = 2.00
    # color_value["string"]      = "3 - 6 ft"
    # color_value["rgb"]         = [255, 165, 0]
    # color_values.append(color_value)

    # color_value = {}
    # color_value["lower_value"] = 2.00
    # color_value["upper_value"] = 1000.0
    # color_value["rgb"] = [255, 0, 0]
    # color_value["string"]      = "> 6 ft"
    # color_values.append(color_value)

    mp = next((x for x in cosmos.config.map_contours if x["name"] == "flood_map"), None)    
    color_values = mp["contours"]

    make_png_tiles(zsmax, index_path, flood_map_path,
                   topo_path=topo_path,
#                   zoom_range=zoom_range,
                   option="floodmap",
                   color_values=color_values,
                   zbmax=1.0)

def make_wave_map_tiles(hm0max, index_path, wave_map_path):

    make_png_tiles(hm0max, index_path, wave_map_path, caxis=[0.0, 15.0])
