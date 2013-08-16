#!/usr/bin/env python

import sys
import logging
import ConfigParser
import Cobalt
import time
from Cobalt.Components.base import Component, exposed, automatic, query, locking

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
logger = logging.getLogger('histm')

#Ap stands for Adjusting Parameter
#the predicted walltime = user_estimationn * Ap

def get_histm_config(option, default):
    try:
        value = config.get('histm', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

update_interval = float(get_histm_config('update_interval_hr', 0.5))

def parse_jobinfo(line):
    '''parse a line in job_info file, return a temp
    dictionary with parsed fields in the line'''
    temp = {}
    fields = line.split(' ')
    temp['jobid'] = fields[0]
    temp['user'] = fields[1]
    temp['project'] = fields[2]    
    temp['nodes'] = fields[3]
    temp['Rvalue'] = fields[4]   #Rvalue = runtime / walltime
    return temp

class HistoryManager(Component):
    '''Historical Data Manager'''

    implementation = 'histm'
    name = 'history-manager'
    
    def __init__(self, *args, **kwargs):
        
        Component.__init__(self, *args, **kwargs)
        self.least_item = int(get_histm_config('least_item', 10))  # tunable
        self.lastDays = int(get_histm_config("last_days", 60))    # tunable
        self.jobinfo_file = get_histm_config("jobinfo_file", "jobinfo.hist")
        self.jobinfo_script = get_histm_config("jobinfo_script", "jobinfo.py")
        self.fraction = float(get_histm_config("fraction", 0.8))
        self.minimum_ap = float(get_histm_config("minimum_ap", 0.5))
        
        self.job_dict = {}   #historical job dictionary
        self.project_set = set([])  #distinct project names of historical jobs
        self.user_set = set([])     #distinct user names of historical jobs
        self.pair_set = set([])  #distinct (user, project) pair 
        
        self.Ap_dict_proj = {}  #dictionary of walltime adjusting parameters by project name
        self.Ap_dict_user = {}  #dictionary of walltime adjusting parameters by user name
        self.Ap_dict_paired = {} #dictionary of walltime adjusting parameters by double key (user, project)
        
        self.update_Ap_Dict()
                
    def update_job_dict(self):
        '''initialize/update job_dict from jobinfo_file'''
        try:
            input_file = open(self.jobinfo_file, "r")
        except IOError:
            logger.error("History manager: unable to open jobinfo file %s", self.jobinfo_file)
            return
                
        for line in input_file:
            line = line.strip('\n')
            jobspec = parse_jobinfo(line)
            jobid = jobspec.get('jobid')
            if not self.job_dict.has_key(jobid):
                self.job_dict[jobid] = {}
            self.job_dict[jobid] = jobspec
            self.project_set.add(jobspec.get('project'))
            self.user_set.add(jobspec.get('user'))
            key_pair = (jobspec.get('user'), jobspec.get('project'))
            self.pair_set.add(key_pair)
                    
        input_file.close()            
                        
    def update_Ap_Dict(self):
        '''Update dictionary Adjust Parameter (Ap), including project based Dict and user based Dict'''
        
        self.update_job_dict()
        
        for projectname in self.project_set:
            if not self.Ap_dict_proj.has_key(projectname):
                ap = self.calculate_Ap('project', projectname)
                self.Ap_dict_proj[projectname] = ap
                
        for username in self.user_set:
            if not self.Ap_dict_proj.has_key(username):
                ap = self.calculate_Ap('user', username)
                self.Ap_dict_user[username] = ap
                
        for keypair in self.pair_set:
            if not self.Ap_dict_paired.has_key(keypair):
                ap = self.calculate_Ap_paired(keypair)
                keystr = "%s:%s" % (keypair[0], keypair[1])
                self.Ap_dict_paired[keystr] = ap                
      
        print "***********Adjusting Parameter Dict Updated***********"
        
    update_Ap_Dict = automatic(update_Ap_Dict, update_interval*3600)
                        
    def calculate_Ap(self, keyname, valname):
        '''get Adjust Parameter from dict, keyname: either 'project' or 'user', valname: value of the key'''
        Rlist = []  #list of R values
               
        for id in self.job_dict.keys():
            if self.job_dict[id][keyname] == valname:
                Rlist.append(float(self.job_dict[id]['Rvalue']))
                 
        if len(Rlist) > self.least_item:
            Rlist.sort()
            pos = int(self.fraction * len(Rlist))
            Ap = Rlist[pos]
        else:
            Ap = 1
        if Ap > 1:
            Ap = 1
        return Ap
    
    def calculate_Ap_paired(self, keypair):
        username = keypair[0]
        projectname = keypair[1]
        
        Rlist = [] 
        for id in self.job_dict.keys():
            if self.job_dict[id]['user'] == username and self.job_dict[id]['project'] == projectname:
                Rlist.append(float(self.job_dict[id]['Rvalue']))
            
        if len(Rlist) > self.least_item:
            Rlist.sort()
            pos = int(self.fraction * len(Rlist))
            Ap = Rlist[pos]
        else:
            Ap = 1
        if Ap < self.minimum_ap:
            Ap = self.minimum_ap
        if Ap > 1:
            Ap = 1
        return Ap
    
    def get_Ap(self, key, val):
        Ap = 1
        if key == 'user':
            Ap = self.Ap_dict_user.get(val, 1)
        if key == 'project':
            Ap = self.Ap_dict_proj.get(val, 1)
        return Ap
    get_Ap = exposed(get_Ap)
    
    def get_Ap_by_keypair(self, username, projectname):
        keypair = "%s:%s" % (username, projectname)
        Ap = self.Ap_dict_paired.get(keypair, 1)
        return Ap
    get_Ap_by_keypair = exposed(get_Ap_by_keypair)
    
    def get_Ap_dict(self, key):
        if key == 'project':
            return self.Ap_dict_proj
        elif key == 'user':
            return self.Ap_dict_user
        else:
            return None
    get_Ap_dict = exposed(get_Ap_dict)
    
    def is_alive(self):
        return True
    is_alive = exposed(is_alive)
