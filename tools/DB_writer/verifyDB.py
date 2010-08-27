#!/usr/bin/env python

import os
import sys
import db2util

from dbWriter import DatabaseWriter





if __name__ == '__main__':

    schema = 'COBALT_DB_DEV'
    database_name = 'COBALT_D'
    user = 'cobaltdev'
    pwd = 'miD2.bud'

    init_job_id = int(sys.argv[1])
    final_job_id = int(sys.argv[2])

    db = DatabaseWriter(database_name,
                        user,
                        pwd,
                        schema)
    
    reasons = db.daos['JOB_STATES'].getStatesDict()

    notfound = []
    nocreation = []
    notermination = []
    waskilled = []
    normalterm = []
    has_dummy = []
    has_unreleased_hold = []
    norm_term_missing_records = []
    messages_after_termination = []
    #mod_data_wrong = []

    for jobid in xrange(init_job_id, final_job_id+1):
        
        job_data_ids = db.daos['JOB_DATA'].search_by_jobid(jobid)
         
        if not job_data_ids:
            #print "No job data found for %s!" % jobid
            notfound.append(jobid)
            continue
    
        data_records = []
        prog_records = []
        for job_data_id in job_data_ids:
            data_records.append(db.daos['JOB_DATA'].getID(job_data_id))
            prog_records.extend(db.daos['JOB_PROG'].get_list_by_data_id(job_data_id))

        #do we have uncorrected dummy data?
        for record in data_records:
            if record.v.PROJECT == "COBALT_DUMMY":
                has_dummy.append(jobid)

        #do we have a creation record?
        if not [record for record in prog_records if record.v.REASON == reasons['created']]:
            nocreation.append(jobid)

        if not [record for record in prog_records 
                if ((record.v.REASON == reasons['job_epilogue_finished']) or
                    (record.v.REASON == reasons['killing']))]:
            #TODO: Put a check to see if the job's walltime has been exceeded.
            notermination.append(jobid)

        killing_records = [record for record in prog_records 
                           if record.v.REASON == reasons['killing']]
        

        #we had better not have multiple of these...overkill shouldn't happen.
        if (not killing_records) and (jobid not in notermination):
            #we should see a sequence: created, started, running, resource_epilogue_start
            #resource_epilogue_finished, job_epilogue_start job_epilogue_finished.
            #out of order would be bad.  Ignore holds for now.
            normal_order_names = ['created', 'starting', 'running', 'resource_epilogue_start',
             'resource_epilogue_finished', 'job_epilogue_start', 'job_epilogue_finished']

            normal_order_vals = [reasons[entry] for entry in normal_order_names]

            next_msg_idx = 0
            for record in prog_records:
                if next_msg_idx >= len(normal_order_vals):
                    #we have messages after termination for a "normal" execution?
                    messages_after_termination.append(jobid)
                    break
                if record.v.REASON == normal_order_vals[next_msg_idx]:
                    next_msg_idx += 1
                elif record.v.REASON not in normal_order_vals:
                    continue
                else:
                    norm_term_missing_records.append(jobid)
                    break
                

        
        #REPORT:

    print "Report for database state for jobs \[%d : %d\]" % (init_job_id, final_job_id)
    print "Jobs not found in range:"
    print notfound
    print "Missing Records: Normal Run:"
    print norm_term_missing_records
    print "Has Dummy Data:"
    print has_dummy
    print "No Creation Record:"
    print nocreation
    print "Has No Termination Record:"
    print notermination
    print "Has records after \"Termination\":"
    print messages_after_termination
                               
        
    
