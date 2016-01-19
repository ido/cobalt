"""Base process group management classes for Cobalt system components.


"""

import logging
import time
import Queue
from Cobalt.Proxy import ComponentProxy
from Cobalt.DataTypes.ProcessGroup import ProcessGroup
from Cobalt.Exceptions import ProcessGroupStartupError, ComponentLookupError
from Cobalt.Util import init_cobalt_config, get_config_option
from Cobalt.Data import IncrID

_logger = logging.getLogger()

init_cobalt_config()

class ProcessGroupManager(object): #degenerate with ProcessMonitor.
    '''Manager for process groups.  These are tasks that Cobalt run on behalf of
    the user.  Typically these are scripts submitted via qsub.'''


    SIGKILL_TIMEOUT = int(get_config_option('system', 'sigkill_timeout', 300))

    def __init__(self):
        self._pg_id_gen = IncrID()
        self.process_groups = {}
        self.process_group_actions = {}
        self.forkers = [] #list of forker identifiers to use with ComponentProxy

#TODO: add getstate and setstate methods.

    def init_groups(self, specs):
        '''Add a set of process groups from specs.  Generate a unique id.]

        Input:
            specs - a list of dictionaries that specify process groups for a
                    given system

        Returns:
            list of process groups that were just added.

        '''
        pg_to_add = {}
        for spec in specs:
            spec['id'] = self._pg_id_gen.next()
            pg_to_add[spec['id']] = ProcessGroup(spec)
        self.process_groups.update(pg_to_add)
        return list(pg_to_add.values())

    def signal_groups(self, pgids, signame="SIGINT"):
        '''Send signal with signame to a list of process groups.

        '''
        for pgid in pgids:
            self.process_groups[pgid].signal(signame)
        return

    def terminate_groups(self, pgids):
        '''Send SIGINTs to process groups to allow them to terminate gracefully.
        Set the time at which a SIGKILL will be send if the process group has
        not completed.

        '''
        now = int(time.time())
        self.signal_groups(pgids)
        for pg_id in pgids:
            self.process_groups[pg_id].sigkill_timeout = int(now +
                    self.SIGKILL_TIMEOUT)

    def start_groups(self, pgids):
        '''Start process groups. Return groups that succeeded startup.

        '''
        started = []
        for pg_id in pgids:
            try:
                self.process_groups[pg_id].start()
            except ProcessGroupStartupError:
                _logger.error("%s: Unable to start process group.",
                        self.process_groups[pg_id].label)
            else:
                started.append(pg_id)
        return started

    #make automatic get final status of process group
    def update_groups(self):
        '''update process groups with information from forkers. This will also
        trigger information cleanup for terminated processes.  If the child data
        isn't found for a ProcessGroup, and no exit status has been set, then the
        process group must be terminated and marked as having a lost child.

        '''
        children = {}
        completed = {}
        orphaned = []
        now = int(time.time())
        for forker in self.forkers:
            completed[forker] = []
            try:
                child_data = ComponentProxy(forker).get_children("process group",
                        None)
            except ComponentLookupError, e:
                _logger.error("failed to contact the %s component to obtain a list of children", forker)
            except:
                _logger.error("unexpected exception while getting a list of children from the %s component",
                    forker, exc_info=True)
            else:
                for child in child_data:
                    children[(forker, child['id'])] = child

        #clean up orphaned process groups
        for pg_id, pg in self.process_groups:
            child_uid = (pg.forker, pg.head_pid)
            if child_uid not in children:
                orphaned.append(pg_id)
                pg.exit_status = 1234567 #FIXME: what should this sentinel be?
            else:
                children[child_uid]['found'] = True
                pg.update_data(children[child_uid])
                if pg.exit_status is not None:
                    completed[pg.forker].append(children[child_uid]['id'])

        #check for children without process groups and clean
        for key, child in children.keys():
            forker, child_id = key
            if not children[(forker, child_id)].has_key('found'):
                completed[forker].append(child)

        #clear completed
        for forker in completed:
            try:
                ComponentProxy(forker).cleanup_children(completed[forker])
            except ComponentLookupError:
                _logger.error("failed to contact the %s component to cleanup children", forker)
            except Exception:
                _logger.error("unexpected exception while requesting that the %s component perform cleanup",
                        forker, exc_info=True)

        #Send any needed SIGKILLs for children that have been sent a SIGINT.
        for pg in self.process_groups:
            if now >= pg.sigkill_timeout and pg.exit_status is None:
                pg.signal('SIGKILL')

        return

    def cleanup_groups(self, pgids):
        '''Clean up process group data from completed and logged process groups.

        '''
        for pg_id in pgids:
            del self.process_groups[pg_id]
