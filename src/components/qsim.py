#!/usr/bin/env python

"""Qsim executable."""

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
from Cobalt.Components.bgsched import BGSched
from Cobalt.Components.qsim import Qsimulator
from Cobalt.Proxy import ComponentProxy, local_components
from datetime import datetime
import time

arg_list = ['bgjob', 'cjob', 'config_file', 'outputlog', 'sleep_interval', 
            'predict', 'coscheduling', 'wass', 'BG_Fraction', 'cluster_fraction',
            'bg_trace_start', 'bg_trace_end', 'c_trace_start', 'c_trace_end', 
            'Anchor', 'anchor', 'vicinity', 'mate_ratio', 'batch', 'backfill', 'reserve_ratio']

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
        
    if opts.bgjob and opts.cjob and opts.coscheduling:
        print "inserting 'unhold' events into event list..."
        if opts.coscheduling[0] == "hold":
            evsim.init_unhold_events(0)
        if opts.coscheduling[1] == "hold":
            evsim.init_unhold_events(1)

    if opts.batch:
        print "simulation started"
    else:
        raw_input("Press Enter to start simulation...")
            
    starttime_sec = time.time()
    
    if opts.batch:
        while not evsim.is_finished():
            evsim.event_driver()
    else:
        while not evsim.is_finished():
            evsim.event_driver()
            os.system('clear')
            if opts.bgjob:
                bqsim.print_screen()
                pass
            if opts.cjob:
                cqsim.print_screen()
                pass
    
    if opts.bgjob:
        bqsim.post_simulation_handling()
    if opts.cjob:
        cqsim.post_simulation_handling()
       
    endtime_sec = time.time()
    print "----Simulation is finished, please check output log for further analysis.----"
#    print "the simulation lasts %s seconds (~%s minutes)" % (int(endtime_sec - starttime_sec), int((endtime_sec - starttime_sec)/60))
    
if __name__ == "__main__":
    
    p = optparse.OptionParser()
    
    p.add_option("-j", "--job", dest="bgjob", type="string",
        help="file name of the job trace (when scheduling for bg system only)")
    p.add_option("-c", "--cjob", dest="cjob", type="string",
        help="file name of the job trace from the cluster system")
    p.add_option("-p", "--partition", dest="config_file", type="string",
        help="file name of the partition configuration of the Blue Gene system")
    p.add_option("-o", "--output", dest="outputlog", type="string",
        help="featuring string for output log")
    p.add_option("-i", "--interval", dest="sleep_interval", type="float",
        help="seconds to wait at each event when printing screens")
    p.add_option("-F", "--bg_frac", dest="BG_Fraction", type="float", default=False,
        help="parameter to adjust bg workload. All the interval between job arrivals will be multiplied with the parameter")
    p.add_option("-f", "--cluster_frac", dest="cluster_fraction", type="float", default=False,
        help="parameter to adjust cluster workload. All the interval between job arrivals will be multiplied with the parameter")
    p.add_option(Option("-S", "--Start",
        dest="bg_trace_start", type="date",
        help="bg job submission times (in job trace) should be after 12.01am on this date.\
        By default it equals to the first job submission time in job trace 'bgjob'"))
    p.add_option(Option("-E", "--End",
        dest="bg_trace_end", type="date",
        help="bg job submission time (in job trace) should be prior to 12.01am on this date \
        By default it equals to the last job submission time in job trace 'bgjob'"))
    p.add_option(Option("-s", "--start",
        dest="c_trace_start", type="date",
        help="cluster job submission times (in job trace) should be after 12.01am on this date. \
        By default it equals to the first job submission time in job trace 'cjob'"))
    p.add_option(Option("-e", "--end",
        dest="c_trace_end", type="date",
        help="cluster job submission time (in job trace) should be prior to 12.01am on this date \
        By default it equals to the last job submission time in job trace 'cjob'"))
    p.add_option(Option("-A", "--Anchor",
        dest="Anchor", type="date",
        help="the virtual start date of simulation for bqsim. If not specified, it is same as bg_trace_start"))
    p.add_option(Option("-a", "--anchor",
        dest="anchor", type="date",
        help="the virtual start date of simulation for bqsim. If not specified, it is same as c_trace_start"))
    p.add_option("-P", "--prediction", dest="predict", type="string", default=False,
        help="[xyz] x,y,z=0|1. x,y,z==1 means to use walltime prediction for (x:queuing / y:backfilling / z:running) jobs")
    p.add_option("-W", "--walltimeaware", dest="wass", type="string", default=False,
        help="[cons | aggr | both] specify the walltime aware spatial scheduling scheme: cons=conservative scheme, aggr=aggressive scheme, both=cons+aggr")
    p.add_option("-C", "--coscheduling", dest="coscheduling", nargs=2, type="string", default=False,
        help="[x y] (x,y=hold | yield). specify the coscheduling scheme: 'hold' or 'yield' resource if mate job can not run. x for bqsim, y for cqsim.")
    p.add_option("-v", "--vicinity", dest="vicinity", type="float", default=0.0,
        help="Threshold to determine mate jobs in coscheduling. \
        Two jobs can be considered mated only if their submission time difference is smaller than 'vicinity'")
    p.add_option("-r", "--ratio", dest="mate_ratio", type="float", default=0.0,
        help="Specifies the ratio of number mate jobs to number total jobs. Used in the case two job traces have the same number of total jobs.")
    p.add_option("-b", "--batch", dest="batch", action = "store_true", default = False, 
        help="enable batch execution model, do not print screen")
    p.add_option(Option("-l", "--backfill",
        dest="backfill", type="string",
        help="specify backfilling scheme [ff|bf|sjfb] ff=first-fit, bf=best-fit, sjfb=short-job-first backfill"))
    p.add_option(Option("-R", "--reservation",
        dest="reserve_ratio", type="float", default=0.0,
        help="float (0--1), specify the proportion of reserved jobs in the job trace, by default it is 0."))

    start_sec = time.time()
        
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
        print opts.coscheduling
        scheme1 = opts.coscheduling[0]
        if len(opts.coscheduling) == 2:
            scheme2 = opts.coscheduling[1]
        
        if not (scheme1 in coscheduling_schemes and scheme2 in coscheduling_schemes):
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
        if not len(scheme) == 3:
            invalid = True
        else:
            for s in scheme:
                if s not in ['0', '1']:
                    invalid = True
        if invalid:
            print "Error: invalid prediction scheme %s. Valid schemes are: xyz, x,y,z=0|1" % (scheme)
            p.print_help()
            sys.exit()
            
    if opts.bg_trace_start:
        print "bg trace start date=", opts.bg_trace_start
        t_tuple = time.strptime(str(opts.bg_trace_start), "%Y-%m-%d %H:%M:%S")
        opts.bg_trace_start = time.mktime(t_tuple)
    if opts.bg_trace_end:
        print "bg trace end date=", opts.bg_trace_end
        t_tuple = time.strptime(str(opts.bg_trace_end), "%Y-%m-%d %H:%M:%S")
        opts.bg_trace_end = time.mktime(t_tuple)

    if opts.c_trace_start:
        print "cluster trace start date=", opts.c_trace_start
        t_tuple = time.strptime(str(opts.c_trace_start), "%Y-%m-%d %H:%M:%S")
        opts.c_trace_start = time.mktime(t_tuple)
    if opts.c_trace_end:
        print "cluster trace end date=", opts.c_trace_end
        t_tuple = time.strptime(str(opts.c_trace_end), "%Y-%m-%d %H:%M:%S")
        opts.c_trace_end = time.mktime(t_tuple)
        
    if opts.Anchor:
        print "bg simulation start date=", opts.Anchor
        t_tuple = time.strptime(str(opts.Anchor), "%Y-%m-%d %H:%M:%S")
        opts.Anchor = time.mktime(t_tuple)
    if opts.anchor:
        print "cluster simulation start date=", opts.anchor
        t_tuple = time.strptime(str(opts.anchor), "%Y-%m-%d %H:%M:%S")
        opts.anchor = time.mktime(t_tuple)
                       
    options = {}
    for argname in arg_list:
        if getattr(opts, argname):
            options[argname] = getattr(opts, argname)
        
    integrated_main(options)
    
    #profile_main(options)
    
    end_sec = time.time()
    
    print "the simulation totally lasts %s seconds (~%s minutes)" % (int(end_sec - start_sec), int((end_sec - start_sec)/60))

    