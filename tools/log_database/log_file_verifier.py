#!/usr/bin/env python

import os
import sys
import re
import db2util

from cdbaccess import cdbaccess


#ignore if messages don't correspond to any database messages.  also useful if 
#they correspond to multiple lines for the same event.

cqmMsgsToDBMsgs = {
    'preparing job for execution':['starting'],
    'Running job on ANL-R00-1024':['ignore'],
    "transitioning to the 'Prologue' state": ['ignore'],
    'instructing the system component to begin executing the task': ['ignore'],
    "transitioning to the 'Running' state": ['running'],
    'process group no longer executing': ['ignore'],
    'task completed normally; finalizing task and obtaining exit code':['ignore'],
    'task completed normally with an exit code of ; initiating job cleanup and removal':['ignore'],
    "transitioning to the 'Resource_Epilogue' state":['resource_epilogue_start'],
    "transitioning to the 'Job_Epilogue' state":['resource_epilogue_finished','job_epilogue_start'],
    "transitioning to the 'Terminal' state":['job_epilogue_finished', 'terminated'],
    "user delete requested; removing job from the queue": ['killing'],
    "user delete requested with signal": ['ignore'],
    "instructing the system component to send signal": ['ignore'],
    "transitioning to the 'Killing' state":['killing'],
    "task terminated; finalizing task": ['ignore'],
    "task terminated; initiating resource cleanup": ['ignore']
     }

cqmMsgs = cqmMsgsToDBMsgs.keys()

class AcctLogLine(object):
    
    def __init__(self, input_line):
        #Parse log line:
        print input_line
        line = input_line.split()
        self.date_str = line[0]
        self.time_str = line[1]
        self.message = line[2].split(';')
        self.type = message[0]
        self.jobid = message[1]
        self.user = message[2]
        if self.type == 'Q':
            self.queue = message[3]
        elif self.type == 'S':
            self.jobname = message[3]
            self.nodes = int(message[4])
            self.procs = int(message[5])
            self.mode = message[6]
            self.walltime = int(message[7])
        elif self.type == 'D':
            pass
        elif self.type == 'E':
            self.usedtime = int(message[3])
        else:
            print "unhandled message of %s type" % self.type


class SyslogLine(object):
    
    def __init__(self, lineTupple):
        self.timestamp = lineTupple[0]
        self.host = lineTupple[1]
        self.component = lineTupple[2]
        self.pid = lineTupple[3]
        self.message = lineTupple[4]
        self.componentLine = None                           

class cqmLine(object):

    cqmLogLine = re.compile(r'Job \d+/\w+:')
    acctLogLine = re.compile(r'^[DESQR];\d+;\w+')

    state_re = re.compile(r'State=')
    event_re = re.compile(r'Event=')
    
    def __init__(self, string):
        
        self.is_valid_line = False
        self.is_acct_log_line = False
        self.string = string
        
        match = cqmLogLine.match(string)
        if match:
            
            self.is_valid_line = True
            
            fragments = match.string.split()
            job_user_id = fragments[1].split('/')
            self.jobid = int(job_user_id[0])
            self.user = job_user_id[1].strip(':')
            
            has_state = self.state_re.match(fragments[2])
            has_event = None
            self.state = None
            self.event = None

            if has_state:
                self.state = fragments[2].split('=')[1].strip(';')
                has_event = self.event_re.match(fragments[3])
                if has_event:
                    self.event = fragments[3].split('=')[1].strip(';')
                    self.cobalt_msg = ' '.join(fragments[4:])
                else:
                    self.cobalt_msg = ' '.join(fragments[3:])
            else:
                self.cobalt_msg = ' '.join(fragments[2:])
            
            return 
        
        match = actLogLine.match(string)
        if match:
            self.is_act_log_line = True
            #self.is_valid_line = True
            
            #self.acct_log_line = AcctLogLine(match.string)
            #self.jobid = self.acct_log_line.jobid
            return
        
        #if these don't match then don't consider the line.
        
    def __str__(self):
        if not self.is_valid_line:
            return "Invalid Line."
        return self.string
        

if __name__ == '__main__':

    schema = 'COBALT_LOG_DB'
    database_name = 'COBALT_D'
    user = 'cobaltdev'
    pwd = 'miD2.bud'

    init_job_id = int(sys.argv[len(sys.argv)-2])
    final_job_id = int(sys.argv[len(sys.argv)-1])
    if sys.argv[0] != sys.argv[len(sys.argv)-3]:
        cqm_console = sys.argv[len(sys.argv)-3]
    else: 
        None
        
    #files in logs first, then cqm log messages.

    db = cdbaccess(database_name,
                   user,
                   pwd,
                   schema)
    
    events = db.daos['JOB_EVENTS'].getStatesDict()

    syslogLine = re.compile(r'(?P<timestamp>[a-zA-Z]{3} \d{2} \d\d:\d\d:\d\d) (?P<host>\w+) (?P<component>\w+)\[(?P<pid>\d+)\]: (?P<message>[^\n]+)')
    cqmLogLine = re.compile(r'Job \d+/\w+:')
    actLogLine = re.compile(r'^[DESQR];\d+;\w+')
    findState = re.compile(r'State=')
    findMaxRunning = re.compile(r'maxrunning set to')
    

    cobaltComponents = ['cqm', 'slp', 'bgsched', 'cdbwriter', 'bgsystem',
                        'brooklyn', 'scriptm', 'bgforker']

    f = open(os.path.join('/var/log/cobalt.log'))
    lines_to_check = {}
    
    for line in f:
        
        syslogMatch = syslogLine.match(line)
        cqm_line = cqmLine('')

        if syslogMatch:
            if syslogMatch.group('component') == 'cqm':
                cqm_line = cqmLine(syslogMatch.group('message'))
        if not cqm_line.is_valid_line:
            continue

        if not cqm_line.is_acct_log_line:
            
            if (cqm_line.jobid >= init_job_id) and (cqm_line.jobid <= final_job_id):
                if lines_to_check.has_key(cqm_line.jobid):
                    lines_to_check[cqm_line.jobid].append(cqm_line)
                else:
                    lines_to_check[cqm_line.jobid] = [cqm_line]
                            
    #print "Lines:"
    #for key in lines_to_check.keys():
    #    print '\n'.join([str(line) for line in lines_to_check[key]])
    f.close()


    not_found_in_log = []
    not_found_in_db = []
    error_no_job_data = []
    error_out_of_place_message = []
    

    
    missing_messages = dict.fromkeys(events.values())
    for m in missing_messages:
        missing_messages[m] = []
    

    #print missing_messages

    for jobid in xrange(init_job_id, final_job_id+1):
        
        print "checking Job: %d" % jobid
        
        if not lines_to_check.has_key(jobid):
            not_found_in_log.append(jobid)
            continue

        current_lines = lines_to_check[jobid]
        #get data from db for jobid:

        job_data_ids = db.daos['JOB_DATA'].search_by_jobid(jobid)
        
        data_records = []
        prog_records = []

        #first sanity: do we actually have a data object?
        if not job_data_ids:
            error_no_job_data.append(jobid)
            continue

        for job_data_id in job_data_ids:
            data_records.append(db.daos['JOB_DATA'].getID(job_data_id))
            prog_records.extend(db.daos['JOB_PROG'].get_list_by_data_id(job_data_id))  
    

        #do we have the objects to match these messages? We'd better.
        record_count = 1
        
        line_count = len(current_lines)
        
        for line in current_lines:
            #print line
            line_count -= 1
            #the order of entries in the logfile implies an ordering
            #on the messages that should be in the database.
            
            if line.cobalt_msg not in cqmMsgs:
                #this doesn't correspond to a database entry, yet.
                continue
            if 'ignore' in cqmMsgsToDBMsgs[line.cobalt_msg]:
                #this message is an extra message, already handled.
                continue
            
            prog_record_events = [events[record.v.EVENT_TYPE] for record in prog_records]
            if record_count < len(prog_record_events):
                messagesToFind = cqmMsgsToDBMsgs[line.cobalt_msg]
                
                for message in messagesToFind:
                    print prog_record_events[record_count]
                    if prog_record_events[record_count] != message:
                        if message in prog_record_events[:record_count] :
                            error_out_of_place_message.append((line.jobid, message, "Early"))
                        elif message in prog_record_events[record_count:]:
                            error_out_of_place_message.append((line.jobid, message, "Late"))
                        else:
                            error_out_of_place_message.append((line.jobid, message, "Not Found"))
                            missing_messages[message].append(line.jobid)
            
                            
                
                    else:
                        print "found: %s" % message
                    record_count += 1
            else:
                
                break

            # do we have a matching message Holds are special.
            #for others,a message must exist in the set of messages.
            #sanity check
            #???
            #PROFIT!            
        if line_count > 0:
            for line in current_lines[(len(current_lines)-line_db):]:
                missing_messages[message].append(line.jobid)
            
                            
    db.close()

    #Reporting
    if not_found_in_log:
        print "Requested lines not found in log output:"
        print not_found_in_log
    if error_no_job_data:
        print "Requested Jobs have no data in database:"
        print error_no_job_data
    for key in missing_messages:
        if missing_messages[key]:
            print "Missing messages of type %s in database:" % key
            print missing_messages[key]
    if error_out_of_place_message:
         print "Messages out of place:"
         #print error_out_of_place_message
         for entry in error_out_of_place_message:
             output = ["Job: %s;" % entry[0]]
             output.append( "Expected: %s;" % entry[1])
             output.append("Message Was: %s" % entry[2])
             print ' '.join(output)
    
    print "Stick a fork in me, I'm done."
        
    
