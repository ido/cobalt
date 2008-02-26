'''This file defines scheduler policy modules'''
__revision__ = '$Revision$'

class SchedulerPolicy(object):
    '''Null policy implementation'''
    __name__ = 'null'
    def __init__(self, qname):
        self.qname = qname
#        self.resources = resources
#        self.jobs = jobs
#        self.reservations = reservations

    def Prepare(self, idle, potential):
        '''Prepare scheduler policy for schedule interation'''
        pass

    def PlaceJob(self, job, potential):
        '''Place jobs into proper locations'''
        return []

class FirstFit(SchedulerPolicy):
    __name__ = 'FirstFit'

    def PlaceJob(self, job, potential):
        return (job, potential[job.jobid][0])

class DeferAll(FirstFit):
    __name__ = 'DeferAll'
    def Prepare(self, idle, potential):
        '''If idle jobs in this queue exist, defer all others'''
        if [job for job in idle \
            if self.qname in job.queue.split(':')]:
            for job in potential:
                if job.queue != self.qname and \
                       not job.queue.startswith('R.'):
                    del potential[job]

names = {'default': FirstFit,
         'spruce': DeferAll}
