"""Base process group management classes for Cobalt system components.


"""

import logging
import time
import Queue
import re
from threading import RLock
from Cobalt.Proxy import ComponentProxy
from Cobalt.DataTypes.ProcessGroup import ProcessGroup, ProcessGroupDict
from Cobalt.Exceptions import ProcessGroupStartupError, ComponentLookupError
from Cobalt.Util import init_cobalt_config, get_config_option
from Cobalt.Data import IncrID

_logger = logging.getLogger()

init_cobalt_config()

FORKER_RE = re.compile('forker')

class ProcessGroupManager(object): #degenerate with ProcessMonitor.
    '''Manager for process groups.  These are tasks that Cobalt run on behalf of
    the user.  Typically these are scripts submitted via qsub.'''


    SIGKILL_TIMEOUT = int(get_config_option('system', 'sigkill_timeout', 300))

    def __init__(self, pgroup_type=ProcessGroup):
        '''Initialize process group manager.

        Input:
            pgroup_type: [optional] type of process group class to use. Must be
            compatible with the ProcessGroupDict class.

        '''
        self.pgroup_type = pgroup_type
        self._common_init_restart()


    def _common_init_restart(self, state=None):
        '''common intitialization code for both cold initilaization and
        reinitialization.

        '''
        if state is None:
            self.process_groups = ProcessGroupDict()
            self.process_groups.item_cls = self.pgroup_type
        else:
            self.process_groups = ProcessGroupDict()
            self.process_groups.item_cls = self.pgroup_type
            _logger.info("%s", state['process_groups'])
            for pgroup in state['process_groups']:
                pg = self.process_groups.item_cls().__setstate__(pgroup)
                self.process_groups[pg.id] = pg
            self.process_groups.q_add(state['process_groups'])
            self.process_groups.id_gen.set(int(state['next_pg_id']))
        self.process_group_actions = {}
        self.forkers = [] #list of forker identifiers to use with ComponentProxy
        self.forker_taskcounts = {} # dict of forkers and counts of pgs attached
        self.process_groups_lock = RLock()
        self.update_launchers()

    def __getstate__(self):
        state = {}
        state['process_groups'] = [pg.__getstate__ for pg in
                self.process_groups.values()]
        state['next_pg_id'] = self.process_groups.id_gen.idnum + 1
        return state

    def __setstate__(self, state):
        self._common_init_restart(state)
        return self

    def init_groups(self, specs):
        '''Add a set of process groups from specs.  Generate a unique id.]

        Input:
            specs - a list of dictionaries that specify process groups for a
                    given system

        Returns:
            list of process groups that were just added.

        '''

        # modify the forker in specs to force the job to round-robbin forkers
        for spec in specs:
            ordered_forkers = [f[0] for f in
                    sorted(self.forker_taskcounts.items(), key=lambda x:x[1])]
            if len(ordered_forkers) < 0:
                raise RuntimeError("No forkers registered!")
            else:
                spec['forker'] = ordered_forkers[0] #this is now a tuple
                self.forker_taskcounts[spec['forker']] += 1
                _logger.info("Job %s using forker %s", spec['jobid'], spec['forker'])
        return self.process_groups.q_add(specs)

    def signal_groups(self, pgids, signame="SIGINT"):
        '''Send signal with signame to a list of process groups.

        Returns:
        List of signaled process groups

        '''
        signaled_pgs = []
        for pgid in pgids:
            if self.process_groups[pgid].mode == 'interactive':
                self.process_groups[pgid].interactive_complete = True
                signaled_pgs.append(self.process_groups[pgid])
            elif self.process_groups[pgid].signal(signame):
                signaled_pgs.append(self.process_groups[pgid])
        return signaled_pgs

    def terminate_groups(self, pgids):
        '''Send SIGINTs to process groups to allow them to terminate gracefully.
        Set the time at which a SIGKILL will be send if the process group has
        not completed.

        '''
        now = int(time.time())
        self.signal_groups(pgids)
        for pg_id in pgids:
            self.process_groups[pg_id].sigkill_timeout = int(now + self.SIGKILL_TIMEOUT)

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
        completed_pgs = []
        now = int(time.time())
        for forker in self.forkers:
            completed[forker] = []
            try:
                child_data = ComponentProxy(forker).get_children("process group", None)
            except ComponentLookupError, e:
                _logger.error("failed to contact the %s component to obtain a list of children", forker)
            except:
                _logger.error("unexpected exception while getting a list of children from the %s component",
                    forker, exc_info=True)
            else:
                for child in child_data:
                    children[(forker, child['id'])] = child

        #clean up orphaned process groups
        for pg in self.process_groups.values():
            pg_id = pg.id
            child_uid = (pg.forker, pg.head_pid)
            if child_uid not in children:
                if pg.mode == 'interactive':
                    #interactive job, there is no child job
                    if pg.interactive_complete:
                        completed_pgs.append(pg)
                        #not really orphaned, but this causes the proper cleanup
                        #to occur
                        orphaned.append(pg_id)
                    continue
                orphaned.append(pg_id)
                _logger.warning('%s: orphaned job exited with unknown status', pg.jobid)
                pg.exit_status = 1234567 #FIXME: what should this sentinel be?
                completed_pgs.append(pg)
            else:
                children[child_uid]['found'] = True
                pg.update_data(children[child_uid])
                if pg.exit_status is not None:
                    _logger.info('%s: job exited with status %s', pg.jobid,
                                 pg.exit_status)
                    completed[pg.forker].append(children[child_uid]['id'])
                    completed_pgs.append(pg)
        #check for children without process groups and clean
        for forker, child_id  in children.keys():
            if not children[(forker, child_id)].has_key('found'):
                completed[forker].append(child_id)

        #clear completed
        for forker in completed:
            if not completed[forker] == []:
                try:
                    ComponentProxy(forker).cleanup_children(completed[forker])
                except ComponentLookupError:
                    _logger.error("failed to contact the %s component to cleanup children",
                                  forker)
                except Exception:
                    _logger.error("unexpected exception while requesting that the %s component perform cleanup",
                            forker, exc_info=True)

        #Send any needed SIGKILLs for children that have been sent a SIGINT.
        for pg in self.process_groups.values():
            if (pg.sigkill_timeout is not None and
                    now >= pg.sigkill_timeout and
                    pg.exit_status is None):
                pg.signal('SIGKILL')
        # clear out the orphaned groups.  There is no backend data for these
        # groups.  CQM shouldn't get anything back for these beyond tracking is
        # lost.
        self.cleanup_groups(orphaned)
        #return the exited process groups so we can invoke cleanup

        return completed_pgs

    def cleanup_groups(self, pgids):
        '''Clean up process group data from completed and logged process groups.

        '''
        cleaned_groups = []
        for pg_id in pgids:
            pg = self.process_groups[pg_id]
            cleaned_groups.append(pg)
            self.forker_taskcounts[pg.forker] -= 1
            del self.process_groups[pg_id]
            _logger.info('%s Process Group deleted', pg.label)
        return cleaned_groups

    def update_launchers(self):
        '''Update the list of task launchers.  This right now works for
        alps_forkers.  Drop entries that slp doesn't know about and add in ones
        that it does.

        Will want to run this in the normal update loop

        If we have no launchers, we should prevent jobs from starting.

        resets the internal forker list to an updated list based on SLP registry

        return is void
        '''
        # TODO: Move this to something Cray-specific later

        updated_forker_list = []
        try:
            services = ComponentProxy('service-location').get_services([{'name':'*'}])
        except Exception:
            _logger.critical('Unable to reach service-location', exc_info=True)
            return
        for service in services:
            asf_re = re.compile('alps_script_forker')
            if re.match(asf_re, service['name']):
                updated_forker_list.append(service['name'])
                if service['name'] not in self.forker_taskcounts.keys():
                    self.forker_taskcounts[service['name']] = 0
        # Get currently running tasks from forkers.  Different loop?
        self.forkers = updated_forker_list
        return
