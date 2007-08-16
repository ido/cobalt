'''This file defines scheduler policy modules'''
__revision__ = '$Revision: $'

class SchedulerPolicy(object):
    '''Null policy implementation'''
    __name__ = 'null'
    def __init__(self, qname, resources):
        self.qname = qname
        self.resources = resources

    def FilterSchedule(self, idle, jobs, reservations, placements):
        '''Remove potential placements (for all queues) before job placement beguns'''
        pass

    def PlaceJobs(self, idle, jobs, reservations, placements):
        '''Place jobs into proper locations'''
        return []

    def TidyPlacements(self, placements, newlocation):
        '''Remove any placements that overlap with newlocation'''
        nodecards = [res for res in self.resources \
                     if res.get('name') == newlocation][0].get('nodecards')
        overlap = [res.get('name') for res in self.resources \
                   if [nc for nc in res.get('nodecards') \
                       if nc in nodecards]]
        for queue in placements:
            for job, locations in queue.iteritems():
                [locations.remove(location) for location in locations \
                 if location in overlap]
                if not locations:
                    del queue[job]

class FirstFit(SchedulerPolicy):
    __name__ = 'FirstFit'

    def PlaceJobs(self, idle, jobs, reservations, placements):
        results = []
        while placements[self.qname]:
            next = min(placements[self.qname].keys())
            location = next[0]
            del placements[self.qname][next]
            results.append((next, location))
            self.TidyPlacements(location)
        return results

class DeferAll(FirstFit):
    __name__ = 'DeferAll'
    def FilterSchedule(self, idle, jobs, reservations, placements):
        '''If idle jobs in this queue exist, defer all others'''
        if [job for job in idle \
            if self.qname in job.get('queue').split(':')]:
            for queue in placements:
                if queue != self.qname and not queue.startswith('R.'):
                    placements[queue] = {}


