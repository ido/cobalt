"""Breadboard Simulator"""

import logging
import os
import random
import thread
import time

from Cobalt.Components.base import automatic
from Cobalt.Components.bb import BBProcessGroup, BBSystem

__all__ = ["BBSimulator", "BBSimProcessGroup"]


logger = logging.getLogger(__name__)


class BBSimProcessGroup(BBProcessGroup):
    """Breadboard Process Group modified for simulation
    
    Methods (whether inherited, overridden, or new):
    _runjob -- inherited (but not used by simulator)
    signal -- OVERRIDDEN
    wait -- inherited (but not used by simulator)
    get_argv -- NEW
    """
    
    def __init__(self, spec):
        BBProcessGroup.simulator_init(self, spec, logger)
        self.signals = []

    def signal(self, signame="SIGINT"):
        """Modified signal() method for simulator"""
        self.signals.append(signame)

    def get_argv(self):
        """Returns the command string the process group would have used
        in execl command at the end of _runjob()"""
        argv = [self.executable, self.executable]
        os.environ["COBALT_NODEFILE"] = self.nodefile[1]
        if self.env:
            for key, value in self.env.iteritems():
                os.environ[key] = value
        if self.args:
            argv.extend([self.args])
        return argv



class BBSimulator(BBSystem):
    """Simulator for Breadboard system component
    
    Methods (whether inherited, overridden, or new):
    add_process_groups -- inherited
    get_process_groups -- inherited
    signal_process_groups -- inherited
    wait_process_groups -- inherited
    
    _start_pg -- OVERRIDDEN
    _check_builds_done -- OVERRIDDEN
    _sim_builds_done -- NEW
    _sim_start -- NEW
    _sim_runjob -- NEW
    node_done_building -- inherited
    _wait -- inherited
    _release_resources -- OVERRIDDEN

    add_resources -- inherited
    remove_resources -- inherited
    get_resources -- inherited
    set_attributes -- inherited
    remove_attributes -- inherited

    validate_job -- inherited
    verify_locations -- inherited
    find_job_location -- inherited
    find_queue_equivalence_classes -- inherited
    """

    name = "system"
    implementation = "breadboard simulator"

    def __init__(self, *args, **kwargs):
        BBSystem.__init__(self, *args, **kwargs)
        self.process_groups.item_cls = BBSimProcessGroup

    def _start_pg(self, pgp):
        """Modified _start_pg for simulator"""
        specs = [{"name":name, "attributes":"*"} for name in pgp.location]
        resources = self.get_resources(specs)
        action = "build-%s" % pgp.kernel
        for res in resources:
            # Set build action for each resource
            specs = [{"name":res.name}]
            new_attrs = {"attributes":{"action":action}}
            self.set_attributes(specs, new_attrs)
            # REMOVED linking/unlinking PXE stuff
        for res in resources:
            # REMOVED "pm -c" call
            pgp.building_nodes.append(res.name)
    
    def _check_builds_done(self):
        """Modified _check_builds_done for simulator"""
        for pgp in self.process_groups.itervalues():
            if len(pgp.building_nodes) > 0 or len(pgp.pinging_nodes) > 0:
                specs = [{"name":name, "attributes":"*"}
                         for name in pgp.building_nodes]
                building = self.get_resources(specs)
                build_action = "build-%s" % pgp.kernel
                for node in building:
                    if node.attributes["action"] != build_action:
                        pgp.building_nodes.remove(node.name)
                        pgp.pinging_nodes.append(node.name)
                for nodename in pgp.pinging_nodes:
                    # REMOVED actual call to ping
                    # Simulate ping success with 70-30 chance
                    if random.randint(0, 9) >= 3:
                        pgp.pinging_nodes.remove(nodename)
                if len(pgp.building_nodes) == 0 and len(pgp.pinging_nodes) == 0:
                    # CALLING new system '_sim_start()' method instead of
                    # PG start() method
                    self._sim_start(pgp)
    _check_builds_done = automatic(_check_builds_done)

    def _sim_builds_done(self):
        """Used to simulate a node finishing building"""
        for pgp in self.process_groups.itervalues():
            if len(pgp.building_nodes) > 0:
                if random.randint(0, 9) >= 3:
                    for name in pgp.location:
                        self.node_done_building(name)
    _sim_builds_done = automatic(_sim_builds_done)

    def _sim_start(self, pgp):
        """Starts a thread to simulate running a process group"""
        thread.start_new_thread(self._sim_runjob, (pgp, ))

    def _sim_runjob(self, pgp):
        """Simulates running a process group"""
        argv = pgp.get_argv()
        stdout = open(pgp.stdout or "/dev/null", "a")
        stderr = open(pgp.stderr or "/dev/null", "a")
        try:
            cobalt_log_file = open(pgp.cobalt_log_file or "/dev/null", "a")
            print >> cobalt_log_file, "%s\n" % " ".join(argv[1:])
            cobalt_log_file.close()
        except IOError:
            logger.error("Job %s/%s: unable to open cobalt log file %s"
                         % (pgp.id, pgp.user, pgp.cobalt_log_file))
        print >> stdout, "Running process_group: %s" % " ".join(argv)
        start_time = time.time()
        run_time = random.randint(60, 180)
        my_exit_status = 0
        print "Running for about %f seconds" % run_time
        while time.time() < (start_time + run_time):
            if "SIGKILL" in pgp.signals:
                pgp.exit_status = 1
                os.remove(pgp.nodefile[1])
                return
            elif "SIGTERM" in pgp.signals:
                print >> stderr, "ProcessGroup got signal SIGTERM"
                my_exit_status = 1
                break
            else:
                time.sleep(1)
        print >> stderr, "ProcessGroup %s switched to state TERMINATED" % pgp.id
        print >> stderr, "Exit Status:", my_exit_status
        pgp.exit_status = my_exit_status
        os.remove(pgp.nodefile[1])

    def _release_resources(self, pgp):
        """Modified _release_resources for simulator"""
        # REMOVED call to "pm -0"
        specs = [{"name":name} for name in pgp.location]
        new_attrs = {"state":"idle"}
        self.set_attributes(specs, new_attrs)
