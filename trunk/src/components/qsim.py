#!/usr/bin/env python

"""Queue Simulator executable."""

import sys

import Cobalt.Util
from Cobalt.Components.qsim import Qsimulator 
from Cobalt.Components.base import run_component

__helpmsg__ = "Usage: qsim <work-load-file-path>"

if __name__ == "__main__":
       
    OPTIONS = {}
    DOPTIONS = {}

    (OPTS, ARGS) = Cobalt.Util.dgetopt_long(sys.argv[0:], OPTIONS,
                                            DOPTIONS, __helpmsg__)
    
    if len(ARGS) == 1:
        print __helpmsg__
        sys.exit(1)
    
    if ARGS[1]:
        WORKLOAD_PATH = ARGS[1]
        
    print WORKLOAD_PATH
  
    try:
        run_component(Qsimulator, register=True, 
                     cls_kwargs={'workload_file':WORKLOAD_PATH, 'config_file':'simulator.xml'})
    except KeyboardInterrupt:
        sys.exit(1)