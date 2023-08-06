# -*- coding: utf-8 -*-
"""
Created on Tue May 11 16:02:04 2021

@author: ormondt
"""

import os
import pandas as pd
import numpy as np
#from pyproj import CRS
#from pyproj import Transformer
import shutil

from cht.sfincs import SFINCS
import cht.fileops as fo
from cht.tide_predict import predict
from cht.deltares_ini import IniStruct

from .cosmos_main import cosmos
from .cosmos_model import Model
from .cosmos_tiling import make_flood_map_tiles
import cosmos.cosmos_meteo as meteo

#import xmlkit as xml

import cht.nesting as nesting


class CoSMoS_SFINCS(Model):
    
    def read_model_specific(self):
        
        # Read in the SFINCS model
        
        # First set some defaults
#        self.flow_spinup_time = 0.0
        
#        xml_obj = xml.xml2obj(self.file_name)        
#        if hasattr(xml_obj, "flowspinup"):
#            self.flow_spinup_time = float(xml_obj.flowspinup[0].value)
                        
        # Now read in the domain data
        input_file  = os.path.join(self.path, "input", "sfincs.inp")
        self.domain = SFINCS(input_file)

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
        self.domain.input.tref     = cosmos.scenario.ref_date
        self.domain.input.tstart   = self.flow_start_time
        self.domain.input.tstop    = self.flow_stop_time
        self.domain.input.dtmapout = 21600.0
        self.domain.input.dtmaxout = 21600.0
        self.domain.input.outputformat = "net"

        if self.flow_nested:
            self.domain.input.pavbnd = -999.0

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

            if self.domain.input.corfile:
                
                # Read cor file
                corfile = os.path.join(self.domain.path, self.domain.input.corfile)
                d = IniStruct(filename=corfile)
                astro = d.section[0].data

                times = self.domain.flow_boundary_point[0].data.index
                names = []
                amp   = []
                phi   = []
                
                for icmp, cmp in enumerate(astro.index):                
                    names.append(cmp)
                    amp.append(astro[1][icmp])
                    phi.append(astro[2][icmp])
                
                # for ind, point in enumerate(self.flow_boundary_point):
                #     point.astro = d.section[ind].data
                df = pd.DataFrame()
                df["component"] = pd.Series(names) 
                df["amplitude"] = pd.Series(amp) 
                df["phase"]     = pd.Series(phi) 
                df = df.set_index("component")
                vv = predict(df, times)

                for pnt in self.domain.flow_boundary_point:
                    pnt.data += vv
                

            # if self.sa_correction or self.ssa_correction:
            #     times = self.domain.flow_boundary_point[0].data.index
            #     names = []
            #     amp   = []
            #     phi   = []
            #     if self.sa_correction:
            #         names.append("SA")
            #         amp.append(self.sa_correction[0])
            #         phi.append(self.sa_correction[1])
            #     if self.ssa_correction:
            #         names.append("SSA")
            #         amp.append(self.ssa_correction[0])
            #         phi.append(self.ssa_correction[1])                
            #     df = pd.DataFrame()
            #     df["component"] = pd.Series(names) 
            #     df["amplitude"] = pd.Series(amp) 
            #     df["phase"]     = pd.Series(phi) 
            #     df = df.set_index("component")
            #     vv = predict(df, times)

            #     for pnt in self.domain.flow_boundary_point:
            #         pnt.data += vv
            
            self.domain.write_flow_boundary_conditions()
            
        elif self.domain.input.bcafile:
            
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

        if self.wave and self.wave_nested:
            
            # Get wave boundary conditions from overall model (Nesting 2)
            output_path = os.path.join(self.wave_nested.cycle_path, "output")   

            self.domain.input.bwvfile = "snapwave.bnd"
            self.domain.read_wave_boundary_points()
            nesting.nest2(self.wave_nested.domain,
                          self.domain,
                          output_path=output_path)
            self.domain.input.bwvfile = None

            self.domain.write_wave_boundary_conditions()

        # elif self.domain.input.bcafile:
            
        #     # Get boundary conditions from astronomic components            
        #     times = pd.date_range(start=self.flow_start_time,
        #                           end=self.flow_stop_time,
        #                           freq='600s')            

        #     # Make boundary conditions based on bca file
        #     for point in self.domain.flow_boundary_point:
        #         if self.tide:
        #             v = predict(point.astro, times)
        #         else:    
        #             v = np.zeros(len(times))
        #         point.data = pd.Series(v, index=times)
                    
        #     self.domain.write_flow_boundary_conditions()
                    
        # Meteo forcing
        if self.meteo_wind or self.meteo_atmospheric_pressure or self.meteo_precipitation:

            meteo.write_meteo_input_files(self,
                                          "sfincs",
                                          self.domain.input.tref)

            if self.meteo_wind:                
                self.domain.input.amufile = "sfincs.amu"
                self.domain.input.amvfile = "sfincs.amv"
    
            if self.meteo_atmospheric_pressure:
                self.domain.input.ampfile = "sfincs.amp"
                self.domain.input.baro    = 1
                            
            if self.meteo_precipitation:                
                self.domain.input.amprfile = "sfincs.ampr"
            else:
                self.domain.input.scsfile = None

        # TC forcing
#        if self.meteo_cyclone_track or cosmos.scenario.track_ensemble:
        if cosmos.scenario.track_ensemble:
            spwfile = cosmos.scenario.best_track_file
            fo.copy_file(spwfile, os.path.join(self.job_path, "sfincs.spw"))
            self.domain.input.spwfile = "sfincs.spw"
        
        elif self.meteo_spiderweb:
            
            # Spiderweb file given, copy to job folder

            self.domain.input.spwfile = "sfincs.spw"
            self.domain.input.spwfile = self.meteo_spiderweb
            self.domain.input.baro    = 1
            meteo_path = os.path.join(cosmos.config.main_path, "meteo", "spiderwebs")
            src = os.path.join(meteo_path, self.meteo_spiderweb)
            fo.copy_file(src, self.job_path)
                
        # Make observation points
        for station in self.station:
            self.domain.add_observation_point(station.x,
                                              station.y,
                                              station.name)
                
        # Add observation points for nested models (Nesting 1)
        if self.nested_flow_models:
            
            if not self.domain.input.obsfile:
                self.domain.input.obsfile = "sfincs.obs"
            
            for nested_model in self.nested_flow_models:
                nesting.nest1(self.domain, nested_model.domain)

        # Add other observation stations 
        if self.nested_flow_models or len(self.station)>0:
            if not self.domain.input.obsfile:
                self.domain.input.obsfile = "sfincs.obs"
            self.domain.write_observation_points()            

        # Make restart file
        trstsec = self.domain.input.tstop.replace(tzinfo=None) - self.domain.input.tref            
        if self.meteo_subset:
            if self.meteo_subset.last_analysis_time:
                trstsec = self.meteo_subset.last_analysis_time.replace(tzinfo=None) - self.domain.input.tref
        self.domain.input.trstout = trstsec.total_seconds()
        
        # Get restart file from previous cycle
        if self.flow_restart_file:
            src = os.path.join(self.restart_path, "flow",
                               self.flow_restart_file)
            dst = os.path.join(self.job_path,
                               "sfincs.rst")
            fo.copy_file(src, dst)
            self.domain.input.rstfile = "sfincs.rst"
            self.domain.input.tspinup = 0.0


        # Now write input file (sfincs.inp)
        self.domain.write_input_file()

        # Make run batch file
        batch_file = os.path.join(self.job_path, "run.bat")
        fid = open(batch_file, "w")
        fid.write("@ echo off\n")
        fid.write("DATE /T > running.txt\n")
        exe_path = os.path.join(cosmos.config.sfincs_exe_path, "sfincs.exe")
        fid.write(exe_path + "\n")
#        fid.write("d:\\checkouts\\SFINCS\\branches\\subgrid_openacc_12_wavemaker\\sfincs\\x64\\Release\\sfincs.exe\n")
        fid.write("move running.txt finished.txt\n")
#        fid.write("exit\n")
        fid.close()


        # Now loop through ensemble members
        if cosmos.scenario.track_ensemble and cosmos.config.run_ensemble:
            for member_name in cosmos.scenario.member_names:
                
                # Job path for this ensemble member
                member_path = self.job_path + "_" + member_name
                
                # Make job path for this ensemble member
                fo.mkdir(member_path)
                
                # Copy all files from best track job to member path
                fo.copy_file(os.path.join(self.job_path, "*"), member_path)
    
                # Boundary conditions        
                if self.flow_nested:
        
                    # Get boundary conditions from overall model (Nesting 2)
                    output_path = os.path.join(self.flow_nested.ensemble_path,
                                               member_name)   
                    
                    # This is necessary for reading the timeseries output for nesting
                    # when this model has already run
                    if self.flow_nested.type.lower() == "sfincs":
                        if not self.flow_nested.domain.input.tref:
                            self.flow_nested.domain.input.tref = self.domain.input.tref
                        if not self.flow_nested.domain.observation_point:
                            obs_file = os.path.join(self.flow_nested.results_path,
                                                    "archive",
                                                    cosmos.cycle_string,
                                                    "input",
                                                    "sfincs.obs")
                            self.flow_nested.domain.read_observation_points(file_name=obs_file)                    
                    
                    nesting.nest2(self.flow_nested.domain,
                                  self.domain,
                                  output_path=output_path,
                                  boundary_water_level_correction=self.boundary_water_level_correction)
        
                    bzsfile = os.path.join(member_path, self.domain.input.bzsfile)
                    self.domain.write_flow_boundary_conditions(file_name=bzsfile)
    
                # Copy spw file
                meteo_path = os.path.join(cosmos.config.main_path, "meteo")
                spwfile = os.path.join(meteo_path,
                                       cosmos.scenario.track_ensemble,
                                       member_name + ".spw")
                fo.copy_file(spwfile, os.path.join(member_path, "sfincs.spw"))

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
        fo.move_file(os.path.join(job_path, "*.dat"), output_path)
        fo.move_file(os.path.join(job_path, "*.txt"), output_path)
        fo.move_file(os.path.join(job_path, "sfincs_his.nc"), output_path)
        fo.move_file(os.path.join(job_path, "sfincs_map.nc"), output_path)
        
        fo.move_file(os.path.join(job_path, "sfincs.rst"), input_path)

        # Restart files 
        fo.move_file(os.path.join(job_path, "*.rst"), os.path.join(self.restart_path,
                                                                   "flow"))

        # Input
        fo.move_file(os.path.join(job_path, "*.*"), input_path)
        
        if cosmos.scenario.track_ensemble and cosmos.config.run_ensemble:
            # And now for the ensemble members
            # Only output
            for member_name in cosmos.scenario.member_names:
                
                pth = self.job_path + "_" + member_name
                output_path = os.path.join(self.ensemble_path, member_name)
                fo.mkdir(output_path)
                if os.path.isfile(os.path.join(pth, "zst.txt")):
                    fo.move_file(os.path.join(pth, "zst.txt"), output_path)
                if os.path.isfile(os.path.join(pth, "zst.dat")):
                    fo.move_file(os.path.join(pth, "zs.dat"), output_path)
                if os.path.isfile(os.path.join(pth, "zsmax.dat")):
                    fo.move_file(os.path.join(pth, "zsmax.dat"), output_path)
    
                try:
                    shutil.rmtree(pth)
                except:
                    # Folder was probably open in another application
                    pass

            

    def post_process(self):
        
        # Extract water levels

        # if not self.domain.observation_point:
        #     # This model has not been run. Need to load in the domain.
        #     input_file = os.path.join(self.cycle_path,
        #                                "input","sfincs.inp")
        #     self.domain.load(input_file)
            
        output_path = os.path.join(self.cycle_path,
                                   "output")
        post_path = os.path.join(self.cycle_path,
                                 "post")
            
        
        # if not self.domain.input.tref:
        #     # This model has been run before. The model instance has not data on tref, obs points etc.
        #     input_path = os.path.join(self.cycle_path,
        #                                "input")
        #     self.domain.read_input_file(os.path.join(input_path, "sfincs.inp"))
        #     self.domain.read_observation_points()
        
        if self.station:

            if self.domain.input.outputformat=="bin":
                nc_file = os.path.join(output_path, "zst.txt")
            else:    
                nc_file = os.path.join(output_path, "sfincs_his.nc")
            
            # if not self.domain.observation_point:
            #     obs_file = os.path.join(input_path, "sfincs.obs")
            #     self.domain.read_observation_points(file_name=obs_file)                    
            
            v = self.domain.read_timeseries_output(file_name=nc_file)
            
            v += self.vertical_reference_level_difference_with_msl
            
            for station in self.station:                
                vv=v[station.name]
                vv.index.name='date_time'
                vv.name='wl'
                vv = vv + station.water_level_correction
                file_name = os.path.join(post_path,
                                         "waterlevel." + station.name + ".csv")
                vv.to_csv(file_name,
                          date_format='%Y-%m-%dT%H:%M:%S',
                          float_format='%.3f')        

        # Make flood map tiles
#        if cosmos.config.make_flood_maps and self.make_flood_map and self.domain.input.outputformat=="bin":
        if cosmos.config.make_flood_maps and self.make_flood_map:

            flood_map_path = os.path.join(cosmos.scenario.path,
                                          "tiles",   
                                          "flood_map")
            
            index_path = os.path.join(self.path, "tiling", "indices")
            topo_path = os.path.join(self.path, "tiling", "topobathy")
            
            if os.path.exists(index_path) and os.path.exists(topo_path):

                # Read zs max
                # t0 = cosmos.cycle_time + datetime.timedelta(hours=1)
                # t1 = model.flow_stop_time
                
                # zsmax = self.domain.read_zsmax(zsmax_file = os.path.join(output_path, "zsmax.dat"),
                #                                time_range=[t0.replace(tzinfo=None),
                #                                            t1.replace(tzinfo=None)])
                
                if self.domain.input.outputformat[0:3]=="bin":                
                    zsmax_file = os.path.join(output_path, "zsmax.dat")
                    zsmax = self.domain.read_zsmax(zsmax_file=zsmax_file)
                else:
                    zsmax_file = os.path.join(output_path, "sfincs_map.nc")
                    zsmax = self.domain.read_zsmax(zsmax_file=zsmax_file)
                    

#                # Difference between MSL and NAVD88 (used in topo data)
#                zsmax -= 0.067 
    
                make_flood_map_tiles(zsmax, index_path, topo_path, flood_map_path,
                                         water_level_correction=0.0)
