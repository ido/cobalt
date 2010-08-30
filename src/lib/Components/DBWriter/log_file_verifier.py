#!/usr/bin/env python

import os
import sys
import re
import db2util

from dbWriter import DatabaseWriter



class AcctLogLine(object):
    
    def __init__(self, input_line):
        #Parse log line:
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


class BasicLogLine(object):
    
    """hide the messy parsing details and make it more convenient to
    get to line contents."""

    def __init__(self, line):

        self.norm_msg = False
        split_line = line.split()

        state_re = re.compile("State=")
        event_re = re.compile("Event=")
    
        match_line = state_re.match(split_line[2])
        
        if match_line:
            self.norm_msg = True
            self.state = split_line[2].split('=')[1].strip(';').lower()
            if not event_re.match(split_line[3]):
                self.event = None
            else:
                self.event = split_line[3].split('=')[1].strip(';').lower()
            self.message = ' '.join(split_line[4:])
            self.state_event = '.'.join([self.state, str(self.event)])
        
        else:
            self.message = ' '.join(split_line[2:])
                                   

if __name__ == '__main__':

    schema = 'COBALT_DB_DEV'
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

    db = DatabaseWriter(database_name,
                        user,
                        pwd,
                        schema)
    
    reasons = db.daos['JOB_STATES'].getStatesDict()

    logLine = re.compile(r'Job \d+/\w+:')
    actLogLine = re.compile('^[DESQR];\d+;\w+')
    findState = re.compile(r'State=')
    findMaxRunning = re.compile(r'maxrunning set to')

    f = open(os.path.join(cqm_console), "r")
    lines_to_check = {}
    for line in f:
        match = logLine.match(line)
        if match:
            jobid = int(match.string.split()[1].split('/')[0])
            if (jobid >= init_job_id) and (jobid <= final_job_id):
                if lines_to_check.has_key(jobid):
                    lines_to_check[jobid].append(line)
                else:
                    lines_to_check[jobid] = [line]
                    
        #    continue
        #This should be degenerate with messages above.
        #else: match = actLogLine.match(line)
        #if match: 
        #    jobid = int(match.string.split(';')[1])
        #    if (jobid >= init_job_id) and (jobid <= final_job_id):
        #        if lines_to_check.has_key(jobid):
        #            lines_to_check[jobid].append(line)
        #        else:
        #            lines_to_check[jobid] = [line]
    
    #print lines_to_check
    f.close()

    not_found_in_log = []
    not_found_in_db = []
    error_no_job_data = []
    
    missing_messages = dict.fromkeys(reasons.keys())
    for m in missing_messages:
        missing_messages[m] = []

    print missing_messages

    states = []
    events = []
    for key in lines_to_check.keys():
        for line in lines_to_check[key]:
            
            parsed_line = BasicLogLine(line)
            if parsed_line.norm_msg:
                if parsed_line.state not in states:
                    states.append(parsed_line.state)
                event_str = '.'.join([parsed_line.state, str(parsed_line.event)])
                if event_str not in events:
                        events.append(event_str)
    print "states: %s" % states
    print "events: %s" % events
    
    event_map = dict.fromkeys(events)
    event_map['ready.run'] = 'starting'
    event_map['prologue.progress'] = 'running'
    event_map['running.task_end'] = 'resource_epilogue_start'
    event_map['resource_epilogue.progress'] = 'resource_epilogue_finished'
    event_map['job_epilogue.progress'] = 'job_epilogue_finished'
    event_map['killing.task_end'] = 'killing'
    event_map['hold.release'] = 'hold_release'
    event_map['ready.hold'] = 'hold_set'
    event_map['ready.kill'] = 'killing'
    event_map['running.kill'] = 'killing'
    event_map['prologue.kill'] = 'killing'
    event_map['terminal.progress'] = 'killing'

    special_events = [None, 'terminal.progress', 'hold.release', 'ready.hold',
                      'resource_epilogue.progress'] 

    for jobid in xrange(init_job_id, final_job_id+1):
        
        print "checking Job: %d" % jobid
        #sys.stdout.write('.')
        #sys.stdout.flush()
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
        for line in current_lines:
            #print line
            parsed_line = BasicLogLine(line)
            #get type
            if not parsed_line.norm_msg:
                continue

            reason = event_map[parsed_line.state_event]
            
           
            if parsed_line.state_event not in special_events:
                if not reason:
                    #this line should have no entry.  Redundant line?
                    continue
                
                matching_records =  [record for record in prog_records if
                                     record.v.REASON == reasons[reason]]
                
                if (not matching_records 
                    and (jobid not in missing_messages[reason])):
                        missing_messages[reason].append(jobid)
                    
            else:
                if parsed_line.state_event == 'resource_epilogue.progress':
                    #look for two messages.
                    matching_records =  [record for record in prog_records if
                                     record.v.REASON == reasons[reason]]
                    matching_records2 = [record for record in prog_records if
                                     record.v.REASON == 
                                     reasons['job_epilogue_start']]
                    if (not matching_records 
                        and (jobid not in missing_messages[reason])):
                        missing_messages[reason].append(jobid)
                        if (not matching_records2
                            and (jobid not in missing_messages['job_epilogue_start'])):
                            missing_messages['job_epilogue_start'].append(jobid)
                #hold-handling

            
            #do we have a matching message Holds are special.
            #for others,a message must exist in the set of messages.
            #sanity check
            #???
            #PROFIT!

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
    
    print "Stick a fork in me, I'm done."
        
    
