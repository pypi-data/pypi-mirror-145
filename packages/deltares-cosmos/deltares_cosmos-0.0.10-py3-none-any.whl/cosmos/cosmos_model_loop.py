# -*- coding: utf-8 -*-
"""
Created on Mon May 10 14:29:24 2021

@author: ormondt
"""
import time
import sched
import os

from .cosmos_main import cosmos
from .cosmos_postprocess import post_process
import cht.fileops as fo

class ModelLoop:

    def __init__(self):
        pass
        
    def start(self):
        
        self.status = "running"
        while self.status == "running":        
            # This will be repeated until the status of the model loop changes to "done" 
            self.scheduler = sched.scheduler(time.time, time.sleep)
            dt = 1.0 # Execute the next model loop 1 second from now
            self.scheduler.enter(dt, 1, self.run, ())
            self.scheduler.run()

    def stop(self):

        self.scheduler.cancel()

    def run(self):

        # First check for finished simulations
        finished_list = check_for_finished_simulations()
    
        # If there are simulations ready ...
        for model in finished_list:    
            # First move data from all finished simulations
            # (so that pre-processing of next model can commence)
            # Post-processing will happen later
            if not model.status =='failed':
                # Moving model input and output from job folder
                cosmos.log("Moving model " + model.long_name)                                
                model.move()
                path = os.path.join(cosmos.config.job_path,
                                    cosmos.scenario.name,
                                    model.name)
                fo.delete_folder(path)
                
                model.status = "simulation_finished"
    
        # Now prepare new models ready to run        
        waiting_list = update_waiting_list()

        # Pre process all waiting simulations
        for model in waiting_list:
            
            cosmos.log("Pre-processing " + model.long_name + " ...")
            model.pre_process()  # Adjust model input (nesting etc.)
            cosmos.log("Submitting " + model.long_name + " ...")
            model.submit_job()
            model.status = "running"

        # Now do post-processing on simulations that were finished
        for model in finished_list:

            cosmos.log("Post-processing " + model.long_name + " ...")
            # Make plots etc.
            model.post_process()
            model.status = "finished"
            
            # Write finished file            
            file_name = os.path.join(cosmos.job_list_path,
                                     model.name + ".finished")            
            fid = open(file_name, "w")
            fid.write("finished")
            fid.close()

        
        # Now check if all simulations are completely finished    
        all_finished = True
        for model in cosmos.scenario.model:
            if model.status != "failed" and model.status != "finished":
                all_finished = False

        if all_finished:

            cosmos.log("All models finished!")

            # Post process data (making floodmaps, uploading to server etc.)
            post_process()
                                    
            if cosmos.config.cycle_mode == "continuous" and cosmos.next_cycle_time:
                # Start new main loop
                cosmos.main_loop.start(cycle_time=cosmos.next_cycle_time)
            else:
                cosmos.log("All done.")

            # Move log file                
            log_file = os.path.join(cosmos.config.main_path, "cosmos.log")
            log_path = os.path.join(cosmos.scenario.path, "log_files")
            fo.mkdir(log_path)
            fo.move_file(log_file, os.path.join(log_path, cosmos.cycle_string + ".log"))

            self.status = "done"
            
            # Delete jobs folder
            pth = os.path.join(cosmos.config.job_path,
                               cosmos.scenario.name)
            fo.rmdir(pth)

        else:
            # Do another model loop 
            pass

def check_for_finished_simulations():
    
    finished_list = []
    
    for model in cosmos.scenario.model:
        if model.status == "running":
            file_name = os.path.join(cosmos.config.job_path,
                                     cosmos.scenario.name,
                                     model.name,
                                     "finished.txt")
            if os.path.exists(file_name):
                finished_list.append(model)
                              
    return finished_list

def update_waiting_list():

    # Check which models need to run next
    
    waiting_list = []
    priorities   = []
    running      = False

    for model in cosmos.scenario.model:

        if model.status == "waiting":
            # This model is waiting
            
            okay = True
            
            if model.flow_nested:
                if model.flow_nested.status != "finished":
                    okay = False
                if model.flow_nested.status == "failed":
                    model.status = "failed"
            if model.wave_nested:
                if model.wave_nested.status != "finished":
                    okay = False
                if model.wave_nested.status == "failed":
                    model.status = "failed"
                        
            if okay:
                waiting_list.append(model)
                priorities.append(model.priority)

        if model.status == "running":
            # There are model(s) running
            running = True

    if waiting_list:
        
        # Sort waiting list according to prioritization
        waiting_list.sort(key=lambda x: priorities, reverse = True)
        if cosmos.config.run_mode == "serial":
            # Only put first job in waiting list
            waiting_list = waiting_list[:1]        
            if running:
                # There is already a model running. Wait for it to finish.
                waiting_list = []

    return waiting_list
