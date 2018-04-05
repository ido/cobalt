"""Base process group management classes for Cobalt system components.


"""
import logging
import time
import Queue
import re
import xmlrpclib
from threading import RLock
from Cobalt.Proxy import ComponentProxy
from Cobalt.DataTypes.ProcessGroup import ProcessGroup, ProcessGroupDict
from Cobalt.Exceptions import ProcessGroupStartupError, ComponentLookupError
from Cobalt.Util import init_cobalt_config, get_config_option
from Cobalt.Data import IncrID

_logger = logging.getLogger()

class ProcessGroupManager(object): #degenerate with ProcessMonitor.
    '''Manager for process groups.  These are tasks that Cobalt run on behalf of
    the user.  Typically these are scripts submitted via qsub.'''

    def __init__(self, pgroup_type=ProcessGroup):
        '''Initialize process group manager.

        Input:
            pgroup_type: [optional] type of process group class to use. Must be
            compatible with the ProcessGroupDict class.

        '''
        self._init_config_vars()
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
            self.process_groups = state.get('process_groups', ProcessGroupDict())
            for pgroup in self.process_groups.values():
                _logger.info('recovering pgroup %s, jobid %s', pgroup.id, pgroup.jobid)
            self.process_groups.id_gen.set(int(state['next_pg_id']))
        self.process_group_actions = {}
        self.forkers = [] #list of forker identifiers to use with ComponentProxy
        self.forker_taskcounts = {} # dict of forkers and counts of pgs attached
        self.forker_locations = {}   # dict of forkers a tuple (host, port)
        self.forker_reachable = {}  # Is the forker currently reachable?
        self.remote_qsub_hosts = [] # list of hosts that qsub -I requires
                                    # ssh-ing to a forker host
        self.process_groups_lock = RLock()
        self.update_launchers()

    def _init_config_vars(self):
        '''Initialize variables from Cobalt's configuration files.'''
        init_cobalt_config()
        self.forker_re = re.compile('forker')
        self.sigkill_timeout = int(get_config_option('system', 'sigkill_timeout',
                300))
        self.remote_qsub_hosts = get_config_option('system',
                'elogin_hosts', '').split(":")
        _logger.info('REMOTE QSUB HOSTS: %s',
                ", ".join(self.remote_qsub_hosts))

    def __getstate__(self):
        state = {}
        state['pgroup_type'] = self.pgroup_type
        state['process_groups'] = self.process_groups
        state['next_pg_id'] = self.process_groups.id_gen.idnum + 1
        return state

    def __setstate__(self, state):
        self._init_config_vars()
        self.pgroup_type = state.get('pgroup_type', ProcessGroup)
        self._common_init_restart(state)
        return self

    def init_groups(self, specs):
        '''Add a set of process groups from specs.  Generate a unique id.

        Input:
            specs - a list of dictionaries that specify process groups for a
                    given system

        Returns:
            list of process groups that were just added.

        '''

        # modify the forker in specs to force the job to round-robbin forkers
        with self.process_groups_lock:
            for spec in specs:
                try:
                    spec['forker'] = self._select_forker(spec['jobid'])
                except RuntimeError:
                    _logger.error('Job %s: Unable to find valid forker to associate with pending process group.  Failing startup.',
                            spec['jobid'])
                    raise
            return self.process_groups.q_add(specs)

    def _select_forker(self, jobid):
        '''Select a forker from the list of registered forkers for job execution.
        This favors the forker with the lowest current running jobcount.

        Args:
            jobid - jobid for ProcessGroup object that we are assigning a forker to.

        Returns:
            String name of forker to use.  If none found, None returned

        Exceptions:
            Raises a RuntimeError if there are no registered forkers, or none otherwise available.

        '''
        selected_forker = None
        ordered_forkers = [f[0] for f in sorted(self.forker_taskcounts.items(), key=lambda x: x[1])]
        if len(ordered_forkers) < 0:
            raise RuntimeError("Job %s: No forkers registered!", jobid)
        else:
            for forker in ordered_forkers:
                if self.forker_reachable[forker]:
                    selected_forker = forker
                    self.forker_taskcounts[selected_forker] += 1
                    _logger.info("Job %s using forker %s", jobid, selected_forker)
                    break
        if selected_forker is None:
            # We didn't find a forker, raise a RuntimeError for this
            raise RuntimeError("Job %s: No valid forkers found!" % jobid)
        return selected_forker

    def signal_groups(self, pgids, signame="SIGTERM"):
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
            self.process_groups[pg_id].sigkill_timeout = int(now +
                    self.sigkill_timeout)

    def start_groups(self, pgids):
        '''Start process groups. Return groups that succeeded startup.

        '''
        with self.process_groups_lock:
            started = []
            for pg_id in pgids:
                process_group = self.process_groups[pg_id]
                try:
                    process_group.start()
                except ComponentLookupError:
                    # Retry this with a different forker, if we run out of forkers, then this startup fails.
                    self.forker_reachable[process_group.forker] = False
                    self.forker_taskcounts[process_group.forker] -= 1 #decrement since we failed to use this forker.
                    try:
                        process_group.forker = self._select_forker(process_group.jobid)
                    except RuntimeError as err:
                        #No forkers left!
                        _logger.critical('%s: Unable to assign forker to starting job.  Failing startup: %s',
                                process_group.label, err.message)
                        raise ProcessGroupStartupError('No functional forkers.')
                except (ProcessGroupStartupError, xmlrpclib.Fault, xmlrpclib.ProtocolError):
                    _logger.error("%s: Unable to start process group.", process_group.label)
                else:
                    started.append(pg_id)
                    process_group.startup_timeout = 0
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
        # Hold for update.  Process group addition also results in a forker call, so we need to lock that, too
        # so we have a consistent view
        with self.process_groups_lock:
            now = int(time.time())
            for forker in self.forkers:
                try:
                    child_data = ComponentProxy(forker).get_children("process group", None)
                except ComponentLookupError, e:
                    _logger.error("failed to contact the %s component to obtain a list of children", forker)
                except:
                    _logger.error("unexpected exception while getting a list of children from the %s component",
                        forker, exc_info=True)
                else:
                    completed[forker] = []
                    for child in child_data:
                        children[(forker, child['id'])] = child
            #clean up orphaned process groups
            for pg in self.process_groups.values():
                if pg.exit_status is not None:
                    # already have an exit status for this, and we've already cleaned it up.  Don't reset this
                    continue
                if pg.forker in completed:
                    if now < pg.startup_timeout:
                        #wait for startup timeout.  We don't want any hasty kills
                        continue
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
                        pg.exit_status = 1234567
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
        with self.process_groups_lock:
            cleaned_groups = []
            for pg_id in pgids:
                pg = self.process_groups[pg_id]
                cleaned_groups.append(pg)
                self.forker_taskcounts[pg.forker] -= 1
                del self.process_groups[pg_id]
                _logger.info('%s Process Group deleted', pg.label)
        return cleaned_groups

    def select_ssh_host(self):
        '''select a host to ssh to for interactive jobs.  Choose the most
        lightly loaded host at this time.

        Returns:
            A string hostname for SSH use to set up an interactive shell
            If no locaiton is specified, None is returneddddd

        Exceptions:
            RuntimeError if no forkers are currently set up.

        '''
        ordered_forkers = [f[0] for f in
                sorted(self.forker_taskcounts.items(), key=lambda x:x[1])]
        if len(ordered_forkers) < 0:
            raise RuntimeError("No forkers registered!")
        else:
            if len(ordered_forkers) > 0:
                forker = ordered_forkers[0] #this is now a tuple
            else:
                return None
        try:
            return self.forker_locations[forker]
        except KeyError:
            pass
        return None

    def update_launchers(self):
        '''Update the list of task launchers.  This right now works for
        alps_forkers.  Drop entries that slp doesn't know about and add in ones
        that it does.

        Args: None

        Returns: None

        Side Effects:
            Updates current active forkers.  If a new forker is found this is
            added to the list we can select from.  If a loss-of-contact is
            detected, by a forker being unregistered with SLP, then the forker
            data will be retained for possible reconnection, while it will at
            the same time be marked as unavailable for selection.

        Notes: This runs as a part of the state update driver loop and is
        invoked by a system component class.


        '''
        updated_forker_list = []
        new_forker_locations = {}
        found_services = []
        asf_re = re.compile('alps_script_forker')
        host_re = re.compile(r'https://(?P<host>.*):[0-9]*')
        try:
            services = ComponentProxy('service-location').get_services([{'name': '*', 'location': '*'}])
        except Exception:
            # SLP is down! We can't contact anybody at all
            for forker in self.forker_reachable.keys():
                self.forker_reachable[forker] = False
            _logger.critical('Unable to reach service-location', exc_info=True)
            return
        for service in services:
            if re.match(asf_re, service['name']):
                found_services.append(service)
                loc = re.match(host_re, service['location']).group('host')
                if loc:
                    new_forker_locations[service['name']] = loc
                updated_forker_list.append(service['name'])
                if service['name'] not in self.forker_taskcounts.keys():
                    self.forker_taskcounts[service['name']] = 0
                    _logger.info('Forker %s found', service['name'])
        # Get currently running tasks from forkers.  Different loop?
        with self.process_groups_lock:
            self.forkers = updated_forker_list
            self.forker_locations = new_forker_locations
            for service_name in self.forker_taskcounts.keys():
                self.forker_reachable[service_name] = service_name in [fs['name'] for fs in found_services]
        return
