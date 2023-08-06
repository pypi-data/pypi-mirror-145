# -*- coding: utf-8 -*-
"""
Created on Tue May 11 14:29:26 2021

@author: ormondt
"""
import os
import datetime

from .cosmos_main import cosmos
from cht import fileops as fo
from cht import xmlkit as xml

class Scenario:
    
    def __init__(self, name):

        self.name        = name
        self.model       = []
        self.long_name   = name
        self.description = name
        self.lon         = 0.0
        self.lat         = 0.0
        self.zoom        = 10
        
    def read(self):

        xml_obj = xml.xml2obj(self.file_name)

        # Check if cycle is supplied (if not, this is a forecasting run)
        if hasattr(xml_obj, "longname"):
            self.long_name = xml_obj.longname[0].value
        else:
            self.long_name = self.name
        
        # Check if cycle is supplied (if not, this is a forecasting run)
        if hasattr(xml_obj, "cycle"):
            self.cycle_time = xml_obj.cycle[0].value
        else:
            self.cycle_time = None # To be determined later

        if hasattr(xml_obj, "last_cycle"):
            self.cycle_stop_time = xml_obj.last_cycle[0].value.replace(tzinfo=datetime.timezone.utc)
        else:
            self.cycle_stop_time = None # To be determined later

#        cosmos.catchup = False    
            
        self.run_duration = xml_obj.runtime[0].value

        if hasattr(xml_obj, "track_ensemble"):
            self.track_ensemble = xml_obj.track_ensemble[0].value
            cosmos.scenario.member_names = []
            ensemble_path = os.path.join(cosmos.config.main_path,
                                         "meteo",
                                         self.track_ensemble)
            file_names = fo.list_files(os.path.join(ensemble_path, "*.spw"))
            # Loop through file names
            for file_name in file_names:                
                if file_name[-13:-4]=="besttrack":
                    cosmos.scenario.best_track_file = os.path.join(ensemble_path,
                                                                   file_name)
                else:
                    cosmos.scenario.member_names.append(os.path.split(file_name)[1][0:-4])
            
        else:
            self.track_ensemble = None

        if hasattr(xml_obj, "observations_path"):
            self.observations_path = xml_obj.observations_path[0].value
        else:
            self.observations_path = None
            
        scn_meteo_dataset              = None
        scn_meteo_spiderweb            = None
        scn_meteo_wind                 = False
        scn_meteo_atmospheric_pressure = False
        scn_meteo_precipitation        = False

        # Read meteo forcing            
        if hasattr(xml_obj, "meteo_dataset"):
            scn_meteo_dataset = xml_obj.meteo_dataset[0].value

        if hasattr(xml_obj, "meteo_spiderweb"):
            scn_meteo_spiderweb = xml_obj.meteo_spiderweb[0].value

        if hasattr(xml_obj, "wind"):
            if xml_obj.wind[0].value[0] == "y":
                scn_meteo_wind = True
            else:    
                scn_meteo_wind = False
        
        if hasattr(xml_obj, "atmospheric_pressure"):
            if xml_obj.atmospheric_pressure[0].value[0] == "y":
                scn_meteo_atmospheric_pressure = True
            else:    
                scn_meteo_atmospheric_pressure = False

        if hasattr(xml_obj, "precipitation"):
            if xml_obj.precipitation[0].value[0] == "y":
                scn_meteo_precipitation = True
            else:    
                scn_meteo_precipitation = False

        if hasattr(xml_obj, "lon"):
            self.lon = xml_obj.lon[0].value
        if hasattr(xml_obj, "lat"):
            self.lat = xml_obj.lat[0].value
        if hasattr(xml_obj, "zoom"):
            self.zoom = xml_obj.zoom[0].value
            
        # Add models
        self.model = []
        for mdl in xml_obj.model:
            
            if type(mdl.name) == list:
                name = mdl.name[0].value
            else:
                # this is the preferred way
                name = mdl.name

            # Check if meteo data is specified for this model. If so, override what was defined for teh scenario.

            meteo_dataset              = scn_meteo_dataset
            meteo_spiderweb            = scn_meteo_spiderweb
            meteo_wind                 = scn_meteo_wind
            meteo_atmospheric_pressure = scn_meteo_atmospheric_pressure
            meteo_precipitation        = scn_meteo_precipitation
            
            # Override default nesting from model xml file
            if hasattr(mdl, "flownested"):
                mdl.flow_nested = True
                mdl.flow_nested_name = mdl.flownested[0].value
            if hasattr(mdl, "wavenested"):
                mdl.wave_nested = True
                mdl.wave_nested_name = mdl.wavenested[0].value            

            # Read meteo forcing            
            if hasattr(mdl, "meteo_dataset"):
                meteo_dataset = mdl.meteo_dataset[0].value

            if hasattr(mdl, "meteo_spiderweb"):
                meteo_spiderweb = mdl.meteo_spiderweb[0].value

            if hasattr(mdl, "wind"):
                if mdl.wind[0].value[0] == "y":
                    meteo_wind = True
                else:    
                    meteo_wind = False
            
            if hasattr(mdl, "atmospheric_pressure"):
                if mdl.atmospheric_pressure[0].value[0] == "y":
                    meteo_atmospheric_pressure = True
                else:    
                    meteo_atmospheric_pressure = False

            if hasattr(mdl, "precipitation"):
                if mdl.precipitation[0].value[0] == "y":
                    meteo_precipitation = True
                else:    
                    meteo_precipitation = False

            if hasattr(mdl, "version"):
                vsn = mdl.version[0].value
            else:
                vsn = "001"
                
            # Find out where this model is sitting (which region)
            region = None
            for mdl_dict in cosmos.model_list:
                if mdl_dict["name"].lower() == name:
                    region = mdl_dict["region"]
                    tp     = mdl_dict["type"].lower()
                    break
                                
            if not region:
                cosmos.log("Warning : model " + name + " not found!")
                continue

            path = os.path.join(cosmos.config.main_path,
                                "models", region, tp, name)
            
            scenario_model_path = os.path.join(self.path,
                                               "models", region, tp, name)

            # Find out what type of model this is
            file_name = os.path.join(path, name + ".xml")
#            tp        = xml.get_value(file_name, "type")

            # Initialize models
            if tp.lower() == "ww3":
                from cosmos.cosmos_ww3 import CoSMoS_WW3
                model = CoSMoS_WW3()
                model.wave = True
            elif tp.lower() == "hurrywave":
                from cosmos.cosmos_hurrywave import CoSMoS_HurryWave
                model = CoSMoS_HurryWave()
                model.wave = True
            elif tp.lower() == "sfincs":
                from cosmos.cosmos_sfincs import CoSMoS_SFINCS
                model = CoSMoS_SFINCS()
                model.flow = True
            elif tp.lower() == "delft3dfm":
                from cosmos.cosmos_delft3dfm import CoSMoS_Delft3DFM
                model = CoSMoS_Delft3DFM()
                model.flow = True
            elif tp.lower() == "xbeach":
                from cosmos.cosmos_xbeach import CoSMoS_XBeach
                model = CoSMoS_XBeach()
                model.wave = True
                        
            model.name                       = name
            model.version                    = vsn
            model.path                       = path
            model.results_path               = scenario_model_path
            model.region                     = region
            model.file_name                  = file_name
            model.type                       = tp
            model.meteo_dataset              = meteo_dataset
            model.meteo_spiderweb            = meteo_spiderweb
            model.meteo_wind                 = meteo_wind
            model.meteo_precipitation        = meteo_precipitation
            model.meteo_atmospheric_pressure = meteo_atmospheric_pressure

            model.flow_start_time            = None
            model.flow_stop_time             = None

            if hasattr(mdl, "tide"):
                tide = mdl.tide[0].value
                if tide == "yes":
                    model.tide = True
                else:
                    model.tide = False
            else:
                model.tide = True

            # Read in model generic data (from xml file)
            model.read_generic()

            # Read in model specific data (input files)
            model.read_model_specific()
            
            # Overrule data in in model xml with those found in scenario xml
            if hasattr(mdl, "boundary_water_level_correction"):
                model.boundary_water_level_correction = mdl.boundary_water_level_correction[0].value
            if hasattr(mdl, "make_flood_map"):
                if mdl.make_flood_map[0].value[0].lower() == "y":
                    model.make_flood_map = True
                else:    
                    model.make_flood_map = False
            if hasattr(mdl, "make_wave_map"):
                if mdl.make_wave_map[0].value[0].lower() == "y":
                    model.make_wave_map = True
                else:    
                    model.make_wave_map = False

            # Additional stations
            if hasattr(mdl, "station"):
                for station in mdl.station:
                    model.add_stations(station.value[0].lower)
            
            model.archive_path = os.path.join(model.results_path,
                                              "archive")        
                        
            self.model.append(model)
