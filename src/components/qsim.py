#!/usr/bin/env python

"""Event Simulator executable."""

import inspect 
import optparse
import os
import sys

import Cobalt.Util
from Cobalt.Components.evsim import EventSimulator
from Cobalt.Components.bqsim import BGQsim
from Cobalt.Components.cqsim import ClusterQsim
from Cobalt.Components.histm import HistoryManager
from Cobalt.Components.base import run_component
from Cobalt.Components.slp import TimingServiceLocator
from Cobalt.Components.scriptm import ScriptManager
from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.qsim import Qsimulator
from Cobalt.Proxy import ComponentProxy, local_components
from datetime import datetime
import time

arg_list = ['bgjob', 'cjob', 'config_file', 'outputlog', 'sleep_interval', 
            'predict', 'coscheduling', 'wass', 'BG_Fraction', 'cluster_fraction',
            'sim_start', 'sim_end']

def datetime_strptime (value, format):
    """Parse a datetime like datetime.strptime in Python >= 2.5"""
    return datetime(*time.strptime(value, format)[0:6])

class Option (optparse.Option):
    
    """An extended optparse option with cbank-specific types.
    
    Types:
    date -- parse a datetime from a variety of string formats
    """
    
    DATE_FORMATS = [
        "%Y-%m-%d",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%y-%m-%d",
        "%y-%m-%d %H:%M:%S",
        "%y-%m-%d %H:%M",
        "%m/%d/%Y",
        "%m/%d/%Y %H:%M:%S",
        "%m/%d/%Y %H:%M",
        "%m/%d/%y",
        "%m/%d/%y %H:%M:%S",
        "%m/%d/%y %H:%M",
        "%Y%m%d",
    ]
    
    def check_date (self, opt, value):
        """Parse a datetime from a variety of string formats."""
        for format in self.DATE_FORMATS:
            try:
                dt = datetime_strptime(value, format)
            except ValueError:
                continue
            else:
                # Python can't translate dates before 1900 to a string,
                # causing crashes when trying to build sql with them.
                if dt < datetime(1900, 1, 1):
                    raise optparse.OptionValueError(
                        "option %s: date must be after 1900: %s" % (opt, value))
                else:
                    return dt
        raise optparse.OptionValueError(
            "option %s: invalid date: %s" % (opt, value))
    
    TYPES = optparse.Option.TYPES + ( "date", )
    

    TYPE_CHECKER = optparse.Option.TYPE_CHECKER.copy()
    TYPE_CHECKER['date'] = check_date


def profile_main(opts):
    '''profile integrated qsim'''
    import hotshot, hotshot.stats
    prof = hotshot.Profile("qsim.profile")
    prof.runcall(integrated_main, opts)
    
def integrated_main(options):
    TimingServiceLocator()
    
    if opts.predict:
        histm = HistoryManager(**options)
    
    evsim = EventSimulator(**options)
    
    if opts.bgjob:
        bqsim = BGQsim(**options)
    if opts.cjob:
        cqsim = ClusterQsim(**options)
    
    starttime_sec = time.time()
    
    while not evsim.is_finished():
        evsim.event_driver()
        os.system('clear')
        if opts.bgjob:
            bqsim.print_screen()
            pass
        if opts.cjob:
            cqsim.print_screen()
            pass
       
    endtime_sec = time.time()
    print "----Simulation is finished, please check output log for further analysis.----"
    print "the simulation lasts %s seconds (~%s minutes)" % (int(endtime_sec - starttime_sec), int((endtime_sec - starttime_sec)/60))
    
if __name__ == "__main__":
    
    p = optparse.OptionParser()

    p.add_option("-b", "--bgjob", dest="bgjob", type="string",
        help="file name of the job trace from the Blue Gene system")
    p.add_option("-c", "--cjob", dest="cjob", type="string",
        help="file name of the job trace from the cluster system")
    p.add_option("-p", "--partition", dest="config_file", type="string",
        help="file name of the partition configuration of the Blue Gene system")
    p.add_option("-o", "--output", dest="outputlog", type="string",
        help="featuring string for output log")
    p.add_option("-j", "--job", dest="bgjob", type="string",
        help="file name of the job trace (when scheduling for bg system only)")
    p.add_option("-i", "--interval", dest="sleep_interval", type="float",
        help="seconds to wait at each event when printing screens")
    p.add_option(Option("-s", "--start",
        dest="sim_start", type="date",
        help="job submission times should be after 12.01am on this date"))
    p.add_option(Option("-e", "--end",
        dest="sim_end", type="date",
        help="job submission time should be prior to 12.01am on this date"))
    p.add_option("-P", "--prediction", dest="predict", type="string", default=False,
        help="[xyz] x,y,z=0|1. x,y,z==1 means to use walltime prediction. x:queuing, y:backfilling, z:running job")
    p.add_option("-W", "--walltimeaware", dest="wass", type="string", default=False,
        help="[cons | aggr | both] specify the walltime aware spatial scheduling scheme: cons=conservative scheme, aggr=aggressive scheme, both=cons+aggr")
    p.add_option("-C", "--coscheduling", dest="coscheduling", type="string", default=False,
        help="[hold | yield] specify the coscheduling scheme: 'hold' or 'yield' resource if mate job can not run")
    p.add_option("-F", "--bg_frac", dest="BG_Fraction", type="float", default=False,
        help="parameter to adjust bg workload. All the interval between job arrivals will be multiplied with the parameter")
    p.add_option("-f", "--cluster_frac", dest="cluster_fraction", type="float", default=False,
        help="parameter to adjust cluster workload. All the interval between job arrivals will be multiplied with the parameter")
    
    coscheduling_schemes = ["hold", "yield"]
    wass_schemes = ["cons", "aggr", "both"]
    
    opts, args = p.parse_args()

    if not opts.bgjob and not opts.cjob:
        print "Error: Please specify at least one job trace!"
        p.print_help()
        sys.exit()
        
    if opts.bgjob and not opts.config_file:
        print "Error: Please specify partition configuration file for the Blue Gene system"
        p.print_help()
        sys.exit()
        
    if opts.coscheduling:
        if not opts.coscheduling in coscheduling_schemes:
            print "Error: invalid coscheduling scheme '%s'. Valid schemes are: %s" % (opts.coscheduling,  coscheduling_schemes)
            p.print_help()
            sys.exit()
            
    if opts.wass:
        if not opts.wass in wass_schemes:
            print "Error: invalid walltime-aware spatial scheduling scheme '%s'. Valid schemes are: %s" % (opts.wass,  wass_schemes)
            p.print_help()
            sys.exit()
            
    if opts.predict:
        invalid = False
        scheme = opts.predict
        if not len(scheme)==3:
            invalid = True
        else:
            for s in scheme:
                if s not in ['0', '1']:
                    invalid = True
        if invalid:
            print "Error: invalid prediction scheme %s. Valid schemes are: xyz, x,y,z=0|1" % (scheme)
            p.print_help()
            sys.exit()
            
                


    if opts.sim_start:
        print "start date=", opts.sim_start
        t_tuple = time.strptime(str(opts.sim_start), "%Y-%m-%d %H:%M:%S")
        opts.sim_start = time.mktime(t_tuple)
    if opts.sim_end:
        print "end date=", opts.sim_end
        t_tuple = time.strptime(str(opts.sim_end), "%Y-%m-%d %H:%M:%S")
        opts.sim_end = time.mktime(t_tuple)
                        
    options = {}
    for argname in arg_list:
        if getattr(opts, argname):
            options[argname] = getattr(opts, argname)
        
    integrated_main(options)
    #profile_main(options)