# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:02:04 2021

@author: ormondt
"""

import os
import pandas as pd
import numpy as np
# from pyproj import CRS
# from pyproj import Transformer
# import shutil

from .cosmos_main import cosmos
from .cosmos_model import Model
import cht.xmlkit as xml
import cht.fileops as fo
# import cosmos.cosmos_meteo as meteo
from cht.tide_predict import predict
# from .cosmos_tiling import make_flood_map_tiles
# from cht.deltares_ini import IniStruct
from cht.xbeach import XBeach
from cht.sfincs import SFINCS
from cht.hurrywave import HurryWave

import cht.nesting as nesting

class CoSMoS_XBeach(Model):
    
    def read_model_specific(self):
        
        # Read in the XBeach model
        
        # First set some defaults
#        self.flow_spinup_time = 0.0
        
        flow_nesting_point_x = []
        flow_nesting_point_y = []
         
        xml_obj = xml.xml2obj(self.file_name)        
        if hasattr(xml_obj, "flow_nesting_point_1"):
            xystr = xml_obj.flow_nesting_point_1[0].value.split(",")
            flow_nesting_point_x.append(float(xystr[0]))
            flow_nesting_point_y.append(float(xystr[1]))
        if hasattr(xml_obj, "flow_nesting_point_2"):
            xystr = xml_obj.flow_nesting_point_2[0].value.split(",")
            flow_nesting_point_x.append(float(xystr[0]))
            flow_nesting_point_y.append(float(xystr[1]))
        if hasattr(xml_obj, "flow_nesting_point_3"):
            xystr = xml_obj.flow_nesting_point_3[0].value.split(",")
            flow_nesting_point_x.append(float(xystr[0]))
            flow_nesting_point_y.append(float(xystr[1]))
        if hasattr(xml_obj, "flow_nesting_point_4"):
            xystr = xml_obj.flow_nesting_point_4[0].value.split(",")
            flow_nesting_point_x.append(float(xystr[0]))
            flow_nesting_point_y.append(float(xystr[1]))            
                        
        # Now read in the domain data
        input_file  = os.path.join(self.path, "input", "params.txt")
        self.domain = XBeach(input_file)
        # Give names to the boundary points
        for ipnt, pnt in enumerate(self.domain.flow_boundary_point):
            pnt.name = str(ipnt + 1).zfill(4)
        for ipnt, pnt in enumerate(self.domain.wave_boundary_point):
            pnt.name = str(ipnt + 1).zfill(4)
        
        # Replace boundary points for nesting    
        if flow_nesting_point_x:
            for ipnt, pnt in enumerate(flow_nesting_point_x):            
                self.domain.flow_boundary_point[ipnt].geometry.x = flow_nesting_point_x[ipnt]
                self.domain.flow_boundary_point[ipnt].geometry.y = flow_nesting_point_y[ipnt]

        # Copy some attributes to the model domain (needed for nesting)
        self.domain.crs   = self.crs
        self.domain.type  = self.type
        self.domain.name  = self.name
        self.domain.runid = self.runid
        
        
    def pre_process(self):
        
        # First generate input that is identical for all members
        
#         if cosmos.scenario.track_ensemble:
# #            for member in cosmos.scenario.ensemble_members:
#             nens = 1
#         else:
#             nens = 0
#             members = [""]
                
        # Set path temporarily to job path
        pth = self.domain.path
        self.domain.path = self.job_path
#        self.domain.path = os.path.join(self.job_path, "best")
        
        # Start and stop times
        self.domain.tref   = self.flow_start_time
#        self.domain.input.tstart  = self.flow_start_time
        self.domain.params["tstop"] = (self.flow_stop_time - self.flow_start_time).total_seconds()

        # Boundary conditions        
        if self.flow_nested:

            # Get boundary conditions from overall model (Nesting 2)
            output_path = os.path.join(self.flow_nested.cycle_path, "output")   
            
            # This is necessary for reading the timeseries output for nesting
            # when this model has already run
            if self.flow_nested.type.lower() == "sfincs":
                if not self.flow_nested.domain.input.tref:
                    inp_file = os.path.join(self.flow_nested.results_path,
                                            "archive",
                                            cosmos.cycle_string,
                                            "input",
                                            "sfincs.inp") 
                    sf0 = SFINCS()
                    sf0.read_input_file(inp_file)
                    self.flow_nested.domain.input.tref = sf0.input.tref
                if not self.flow_nested.domain.observation_point:
                    obs_file = os.path.join(self.flow_nested.results_path,
                                            "archive",
                                            cosmos.cycle_string,
                                            "input",
                                            "sfincs.obs")                    
                    self.flow_nested.domain.read_observation_points(file_name=obs_file) 
            
            # Correct boundary water levels. Assuming that output from overall
            # model is in MSL !!!
            zcor = self.boundary_water_level_correction - self.vertical_reference_level_difference_with_msl
                    
            nesting.nest2(self.flow_nested.domain,
                          self.domain,
                          output_path=output_path,
                          boundary_water_level_correction=zcor)

            # if self.domain.input.corfile:
                
            #     # Read cor file
            #     corfile = os.path.join(self.domain.path, self.domain.input.corfile)
            #     d = IniStruct(filename=corfile)
            #     astro = d.section[0].data

            #     times = self.domain.flow_boundary_point[0].data.index
            #     names = []
            #     amp   = []
            #     phi   = []
                
            #     for icmp, cmp in enumerate(astro.index):                
            #         names.append(cmp)
            #         amp.append(astro[1][icmp])
            #         phi.append(astro[2][icmp])
                
            #     # for ind, point in enumerate(self.flow_boundary_point):
            #     #     point.astro = d.section[ind].data
            #     df = pd.DataFrame()
            #     df["component"] = pd.Series(names) 
            #     df["amplitude"] = pd.Series(amp) 
            #     df["phase"]     = pd.Series(phi) 
            #     df = df.set_index("component")
            #     vv = predict(df, times)

            #     for pnt in self.domain.flow_boundary_point:
            #         pnt.data += vv
                            
            self.domain.write_flow_boundary_conditions()
            
        elif self.domain.params.bcafile:
            
            # Get boundary conditions from astronomic components            

            times = pd.date_range(start=self.flow_start_time,
                                  end=self.flow_stop_time,
                                  freq='600s')            

            # Make boundary conditions based on bca file
            for point in self.domain.flow_boundary_point:
                if self.tide:
                    v = predict(point.astro, times)
                else:    
                    v = np.zeros(len(times))
                point.data = pd.Series(v, index=times)
                    
            self.domain.write_flow_boundary_conditions()

        # Boundary conditions        
        if self.wave_nested:

            # Get boundary conditions from overall model (Nesting 2)
            output_path = os.path.join(self.wave_nested.cycle_path, "output")   
            
            # This is necessary for reading the timeseries output for nesting
            # when this model has already run
            if self.wave_nested.type.lower() == "hurrywave":
                if not self.wave_nested.domain.input.tref:
                    inp_file = os.path.join(self.wave_nested.results_path,
                                            "archive",
                                            cosmos.cycle_string,
                                            "input",
                                            "hurrywave.inp") 
                    hw0 = HurryWave()
                    hw0.read_input_file(inp_file)
                    self.wave_nested.domain.input.tref = hw0.input.tref
                if not self.wave_nested.domain.observation_point:
                    obs_file = os.path.join(self.wave_nested.results_path,
                                            "archive",
                                            cosmos.cycle_string,
                                            "input",
                                            "hurrywave.obs")                    
                    self.wave_nested.domain.read_observation_points(file_name=obs_file) 
            
            nesting.nest2(self.wave_nested.domain,
                          self.domain,
                          output_path=output_path)

            self.domain.params["bcfile"] = "sp2list.txt"
            self.domain.params["instat"] = 5
            self.domain.write_wave_boundary_conditions()
                    
#         # Meteo forcing
#         if self.meteo_wind or self.meteo_atmospheric_pressure or self.meteo_precipitation:

#             meteo.write_meteo_input_files(self,
#                                           "sfincs",
#                                           self.domain.input.tref)

#             if self.meteo_wind:                
#                 self.domain.input.amufile = "sfincs.amu"
#                 self.domain.input.amvfile = "sfincs.amv"
    
#             if self.meteo_atmospheric_pressure:
#                 self.domain.input.ampfile = "sfincs.amp"
#                 self.domain.input.baro    = 1
                            
#             if self.meteo_precipitation:                
#                 self.domain.input.amprfile = "sfincs.ampr"
#             else:
#                 self.domain.input.scsfile = None

#         # TC forcing
# #        if self.meteo_cyclone_track or cosmos.scenario.track_ensemble:
#         if cosmos.scenario.track_ensemble:
#             spwfile = cosmos.scenario.best_track_file
#             fo.copy_file(spwfile, os.path.join(self.job_path, "sfincs.spw"))
#             self.domain.input.spwfile = "sfincs.spw"
        
#         elif self.meteo_spiderweb:
            
#             # Spiderweb file given, copy to job folder

#             self.domain.input.spwfile = "sfincs.spw"
#             self.domain.input.spwfile = self.meteo_spiderweb
#             self.domain.input.baro    = 1
#             meteo_path = os.path.join(cosmos.config.main_path, "meteo", "spiderwebs")
#             src = os.path.join(meteo_path, self.meteo_spiderweb)
#             fo.copy_file(src, self.job_path)
                
#         # Make observation points
#         for station in self.station:
#             self.domain.add_observation_point(station.x,
#                                               station.y,
#                                               station.name)
                
#         # Add observation points for nested models (Nesting 1)
#         if self.nested_flow_models:
            
#             if not self.domain.input.obsfile:
#                 self.domain.input.obsfile = "sfincs.obs"
            
#             for nested_model in self.nested_flow_models:                
#                 nesting.nest1(self.domain, nested_model.domain)

#         # Add other observation stations 
#         if self.nested_flow_models or len(self.station)>0:
#             if not self.domain.input.obsfile:
#                 self.domain.input.obsfile = "sfincs.obs"
#             self.domain.write_observation_points()            

#         # Make restart file
#         trstsec = self.domain.input.tstop.replace(tzinfo=None) - self.domain.input.tref            
#         if self.meteo_subset:
#             if self.meteo_subset.last_analysis_time:
#                 trstsec = self.meteo_subset.last_analysis_time.replace(tzinfo=None) - self.domain.input.tref
#         self.domain.input.trstout = trstsec.total_seconds()
        
#         # Get restart file from previous cycle
#         if self.flow_restart_file:
#             src = os.path.join(self.restart_path, "flow",
#                                self.flow_restart_file)
#             dst = os.path.join(self.job_path,
#                                "sfincs.rst")
#             fo.copy_file(src, dst)
#             self.domain.input.rstfile = "sfincs.rst"
#             self.domain.input.tspinup = 0.0


        # Now write input file (params.txt)
        params_file = os.path.join(self.job_path, "params.txt")
        self.domain.params.tofile(filename=params_file)

        # Make run batch file
        batch_file = os.path.join(self.job_path, "run.bat")
        fid = open(batch_file, "w")
        fid.write("@ echo off\n")
        fid.write("DATE /T > running.txt\n")
        fid.write("set xbeachdir=d:\\cosmos\\exe\\xbeach\n")
        fid.write('set mpidir="c:\\Program Files\\MPICH2\\bin"\n')
        fid.write("set PATH=%xbeachdir%;%PATH%\n")
        fid.write("set PATH=%mpidir%;%PATH%\n")
        fid.write("mpiexec.exe -n 8 %xbeachdir%\\xbeach.exe\n")
        fid.write("del q_*\n")
        fid.write("del E_*\n")
        fid.write("move running.txt finished.txt\n")
        fid.close()

        # # Now loop through ensemble members
        # if cosmos.scenario.track_ensemble and cosmos.config.run_ensemble:
        #     for member_name in cosmos.scenario.member_names:
                
        #         # Job path for this ensemble member
        #         member_path = self.job_path + "_" + member_name
                
        #         # Make job path for this ensemble member
        #         fo.mkdir(member_path)
                
        #         # Copy all files from best track job to member path
        #         fo.copy_file(os.path.join(self.job_path, "*"), member_path)
    
        #         # Boundary conditions        
        #         if self.flow_nested:
        
        #             # Get boundary conditions from overall model (Nesting 2)
        #             output_path = os.path.join(self.flow_nested.ensemble_path,
        #                                        member_name)   
                    
        #             # This is necessary for reading the timeseries output for nesting
        #             # when this model has already run
        #             if self.flow_nested.type.lower() == "sfincs":
        #                 if not self.flow_nested.domain.input.tref:
        #                     self.flow_nested.domain.input.tref = self.domain.input.tref
        #                 if not self.flow_nested.domain.observation_point:
        #                     obs_file = os.path.join(self.flow_nested.results_path,
        #                                             "archive",
        #                                             cosmos.cycle_string,
        #                                             "input",
        #                                             "sfincs.obs")
        #                     self.flow_nested.domain.read_observation_points(file_name=obs_file)                    
                    
        #             nesting.nest2(self.flow_nested.domain,
        #                           self.domain,
        #                           output_path=output_path,
        #                           boundary_water_level_correction=self.boundary_water_level_correction)
        
        #             bzsfile = os.path.join(member_path, self.domain.input.bzsfile)
        #             self.domain.write_flow_boundary_conditions(file_name=bzsfile)
    
        #         # Copy spw file
        #         meteo_path = os.path.join(cosmos.config.main_path, "meteo")
        #         spwfile = os.path.join(meteo_path,
        #                                cosmos.scenario.track_ensemble,
        #                                member_name + ".spw")
        #         fo.copy_file(spwfile, os.path.join(member_path, "sfincs.spw"))

        # Set the path back to the one in cosmos\models\etc.
        self.domain.path = pth

    def move(self):
        
        # Move files from job folder to archive folder
        
        # First clear archive folder      
        
        job_path    = os.path.join(cosmos.config.job_path,
                                   cosmos.scenario.name,
                                   self.name)

        # Delete finished.txt file
        fo.delete_file(os.path.join(job_path, "finished.txt"))
        
        output_path = os.path.join(self.cycle_path,
                                   "output")
        input_path = os.path.join(self.cycle_path,
                                 "input")        
        
        # Output        
        fo.move_file(os.path.join(job_path, "*.nc"), output_path)

        # Input
        fo.move_file(os.path.join(job_path, "*.*"), input_path)

    def post_process(self):
        
        # Extract water levels

        # if not self.domain.observation_point:
        #     # This model has not been run. Need to load in the domain.
        #     input_file = os.path.join(self.cycle_path,
        #                                "input","params.txt")
        #     self.domain.load(input_file)
            
        output_path = os.path.join(self.cycle_path,
                                   "output")
        post_path = os.path.join(self.cycle_path,
                                 "post")
            
#        zstfile = os.path.join(output_path, "zst.txt")
        
#         if not self.domain.input.tref:
#             # This model has been run before. The model instance has not data on tref, obs points etc.
#             input_path = os.path.join(self.cycle_path,
#                                        "input")
#             self.domain.read_input_file(os.path.join(input_path, "sfincs.inp"))
#             self.domain.read_observation_points()
        
#         if self.station:
            
#             if not self.domain.observation_point:
#                 obs_file = os.path.join(input_path, "sfincs.obs")
#                 self.domain.read_observation_points(file_name=obs_file)                    
            
#             v = self.domain.read_timeseries_output(file_name=zstfile)
            
#             v += self.vertical_reference_level_difference_with_msl
            
#             for station in self.station:                
#                 vv=v[station.name]
#                 vv.index.name='date_time'
#                 vv.name='wl'
#                 vv = vv + station.water_level_correction
#                 file_name = os.path.join(post_path,
#                                          "waterlevel." + station.name + ".csv")
#                 vv.to_csv(file_name,
#                           date_format='%Y-%m-%dT%H:%M:%S',
#                           float_format='%.3f')        

#         # Make flood map tiles
#         if cosmos.config.make_flood_maps and self.make_flood_map:

#             flood_map_path = os.path.join(cosmos.scenario.path,
#                                        "tiles",   
#                                        "floodmap")
            
#             index_path = os.path.join(self.path, "tiling", "indices")
#             topo_path = os.path.join(self.path, "tiling", "topobathy")
            
#             if os.path.exists(index_path) and os.path.exists(topo_path):

#                 # Read zs max
#                 # t0 = cosmos.cycle_time + datetime.timedelta(hours=1)
#                 # t1 = model.flow_stop_time
                
#                 # zsmax = self.domain.read_zsmax(zsmax_file = os.path.join(output_path, "zsmax.dat"),
#                 #                                time_range=[t0.replace(tzinfo=None),
#                 #                                            t1.replace(tzinfo=None)])
#                 zsmax_file = os.path.join(output_path, "zsmax.dat")
#                 zsmax = self.domain.read_zsmax(zsmax_file=zsmax_file)

# #                # Difference between MSL and NAVD88 (used in topo data)
# #                zsmax -= 0.067 
    
#                 make_flood_map_tiles(zsmax, index_path, topo_path, flood_map_path,
#                                          water_level_correction=0.0)
