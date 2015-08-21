"""Base process group management classes for Cobalt system components.


"""

import logging
from Cobalt.DataTypes.ProcessGroup import ProcessGroupDict
from Cobalt.Exceptions import ProcessGroupStartupError

_logger = logging.getLogger()

class ProcessGroupManager(object):
    '''Manager for process groups.  These are tasks that Cobalt run on behalf of
    the user.  Typically these are scripts submitted via qsub.'''

    def __init__(self):
        self._process_groups = ProcessGroupDict()
        self.monitor = ProcessGroupMonitor()
        self.forker_list = []

#TODO: add getstate and setstate methods.

    @property
    def process_groups(self):
        return self._process_groups

    def add_forker(self, forker):
        #add a forker for PG use
        return

    def add_pocess_groups(self, specs):
        '''Create and add process groups to tracking. Initialization will
        continue asynchronously'''
        self._process_groups.q_add(specs)

        return

    def start_process_groups(self, pg_ids):
        '''Start up process groups from a list of ID's.  If a process group is
        not found, then that id will be skipped.

        Returns a list of successfully started process group ID's

        '''
        succeeded = []
        for pg_id in pg_ids:
            try:
                self._process_groups[pg_id].start()
            except KeyError:
                _logger.error("Process group id: %s not found. Skipping.",
                        pg_id, exc_info=True)
            except ProcessGroupStartupError:
                _logger.error("%s/%s, Process group unable to start.",
                        self._process_groups[pg_id]['jobid'],
                        self._process_groups[pg_id]['user'], exc_info=True)
            else:
                succeeded.append(pg_id)
        return succeeded
    
    def wait_process_groups(self):
        
        return

    def signal_process_groups(self):
        return
class ProcessGroupMonitor(object):
    pass

class ProcessAction(object):
    pass


