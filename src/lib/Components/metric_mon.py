#!/usr/bin/env python

'''Cobalt Metrics Monitor'''

import ConfigParser
import copy
import logging
import math
import os
import os.path
import random
import signal
import sys
import time
import inspect

from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
from datetime import datetime
import time

import Cobalt
import Cobalt.Cqparse
import Cobalt.Util
import Cobalt.Components.bgsched

from Cobalt.Components.qsim_base import *
from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.base import Component, exposed, automatic, query, locking
from Cobalt.Components.cqm import QueueDict, Queue
from Cobalt.Components.simulator import Simulator
from Cobalt.Data import Data, DataList
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Proxy import ComponentProxy, local_components
from Cobalt.Server import XMLRPCServer, find_intended_location

logging.basicConfig()
logger = logging.getLogger('mmon')

CP = ConfigParser.ConfigParser()
CP.read(Cobalt.CONFIG_FILES)
#if CP.has_section('iomon') and CP.get("iomon", "no_of_machines"):
#    no_of_machine = CP.get("evsim", "no_of_machines")

MAX_SYSTEM_IO_CAPACITY = 40960.0
    
def sec_to_date(sec, dateformat="%m/%d/%Y %H:%M:%S"):
    tmp = datetime.fromtimestamp(sec)
    fmtdate = tmp.strftime(dateformat)
    return fmtdate    
                      
def date_to_sec(fmtdate, dateformat="%m/%d/%Y %H:%M:%S"):
    t_tuple = time.strptime(fmtdate, dateformat)
    sec = time.mktime(t_tuple)
    return sec

   
class metricmon(Component):
    """metrics mointor: monitors the real time statistics of interested metrics such as average waiting time and system utilization rate"""
    
    implementation = "imon"
    name = "imon"
    
    def __init__(self, *args, **kwargs):
        
        Component.__init__(self, *args, **kwargs)
        self.event_manager = ComponentProxy("event-manager")
        self.bqsim = ComponentProxy("queue-manager")
        self.mmon_logger = None
        
    def get_current_time_sec(self):
        return self.event_manager.get_current_time()
    
    def get_current_time_date(self):
        return self.event_manager.get_current_date_time()
    
    def init_mmon_logger(self):
        if self.mon_logger == None:
            self.mmon_logger = PBSlogger(self.bqsim.get_outputlog_string() + "-mmon")
          
    def metric_monitor(self):
        self.bqsim.monitor_metrics()
        