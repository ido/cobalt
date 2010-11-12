#!/usr/bin/env python

"""Extract queue wait times from the database.
These are defined as the time queued (created), until the time the job ran,
minus the time the job spent in any kind of hold.  This would be the entire
time the job was elligible to run.

    Can take a range of dates to search
    Output:
    jobid time_queued time_ran wait_time

"""

import os
import sys
import optparse

import db2util

from cdbaccess import cdbaccess, JobSummaryData, JobProgData






if __name__  == '__main__':

    
    database = sys.argv[1]
    schema = sys.argv[2]
    user = sys.argv[3]
    pwd = sys.argv[4]

    start = sys.argv[5]
    end = sys.argv[6]

    start += '-00.00.00.000000'
    end += '-23.59.59.999999'
    print start, end

    db = cdbaccess(database, user, pwd, schema)


    jobids = db.daos['JOB_SUMMARY'].get_job_ids_in_date_range(start, end)

    print '# Jobid, Total Queued Time,Wait Time'
    output_tuples = []
    for jobid in jobids:
        histList = db.daos['JOB_SUMMARY'].get_job_history(jobid)
        tqt_time = db.daos['JOB_PROG'].get_total_queued_time(jobid)
        hold_times = db.daos['JOB_PROG'].get_hold_times(jobid)
        wait_time = 0

        in_hold = False
        if hold_times == None:
            #could not recover any hold times, this is likely a db error
            wait_time = "Error"
        elif hold_times[0] == 0:
            #job was never in hold
            wait_time = tqt_time
        elif hold_times[len(hold_times)-1] == None:
            #job still in hold, hasn't run yet.
            wait_time = "Job still in hold"
            in_hold = True
        else:
            if tqt_time == None:
                #this would be an error condition
                wait_time = "Undefined"
            else:
                #job entered hold, left, and ran
                wait_time = tqt_time - sum(hold_times)

        if wait_time not in ["Error", "Job still in hold", "Undefined"]:
            output_tuples.append((jobid, tqt_time, wait_time))
       # print jobid, wait_time
    print "\n".join(["\t".join([str(j) for j in item]) for item in output_tuples])
