#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Heckle_sched.py

Simple scheduler, based on BGL scheduler, adapted for Heckle.

'''

from Cobalt.Components.bgsched import *

logger = logging.getLogger("Cobalt.Components.scheduler")


class HeckleSched (BGSched):

    def _run_reservation_jobs (self, reservations_cache):
        # handle each reservation separately, as they shouldn't be competing for resources
        for cur_res in reservations_cache.itervalues():
            queue = cur_res.queue
            if not (self.queues.has_key(queue) and self.queues[queue].state == 'running'):
                continue
            
            temp_jobs = self.jobs.q_get([{'is_runnable':True, 'queue':queue}])
            active_jobs = []
            for j in temp_jobs:
                if not self.started_jobs.has_key(j.jobid) and cur_res.job_within_reservation(j):
                    active_jobs.append(j)
    
            if not active_jobs:
                continue
            active_jobs.sort(self.utilitycmp)
            
            job_location_args = []
            for job in active_jobs:
               job_location_args = ({
                         'jobid': str(job.jobid), 
                         'nodes': job.nodes, 
                         'queue': job.queue, 
                         'required': cur_res.partitions.split(":"),
                         'utility_score': job.score,
                         'walltime': job.walltime,
                         'attrs': job.attrs,
                                   } )

               # there's no backfilling in reservations
               try:
                    best_partition_dict = ComponentProxy("system").find_job_location(job_location_args, [])
               except:
                    self.logger.error("failed to connect to system component")
                    best_partition_dict = {}

               job = self.jobs[int(jobid)]
               self._start_job(job, best_partition_dict[jobid])
