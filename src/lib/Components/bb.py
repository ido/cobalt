"""Breadboard Component"""

import atexit
import logging
import os
import os.path
import pwd
import sets
import signal
import stat
import sys
import tempfile

from Cobalt.DataTypes.ProcessGroup import ProcessGroup, ProcessGroupDict
from Cobalt.DataTypes.Resource import ResourceDict
from Cobalt.Components.base import Component, automatic, exposed, query
from Cobalt.Exceptions import JobValidationError


### ADDED FOR BACK-COMPATIBILITY WITH BBTOOLS
import bblib
### END BACK-COMPATIBILITY


__all__ = ["BBSystem", "BBProcessGroup"]


logger = logging.getLogger(__name__)


class BBProcessGroup(ProcessGroup):
    """Process Group modified for Breadboard"""

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec, logger)
        if not self.kernel:
            self.kernel = "default"
        self.building_nodes = []
        self.pinging_nodes = []
        self.nodefile = tempfile.mkstemp()
        os.write(self.nodefile[0], " ".join(self.location))
        os.chmod(self.nodefile[1], stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|
                  stat.S_IROTH)
        os.close(self.nodefile[0])

    def simulator_init(self, spec, log):
        """Used by BBSimulator to be able to extend BBProcessGroup
        and pass through correct logger"""
        ProcessGroup.__init__(self, spec, log)
        if not self.kernel:
            self.kernel = "default"
        self.building_nodes = []
        self.pinging_nodes = []
        self.nodefile = tempfile.mkstemp()
        os.write(self.nodefile[0], " ".join(self.location))
        os.close(self.nodefile[0])

    def _runjob(self):
        """Sets up the environment and execs to the executable script."""
        try:
            userid, groupid = pwd.getpwnam(self.user)[2:4]
        except KeyError:
            logger.exception("Error getting userid/groupid for process group %s"
                             % self.id)
            os._exit(1)
        try:
            os.setgid(groupid)
            os.setuid(userid)
        except OSError:
            logger.exception("Failed to set userid/groupid for process group %s"
                             % self.id)
            os._exit(1)
        if self.umask != None:
            try:
                os.umask(self.umask)
            except OSError:
                logger.exception("Failed to set umask to %s" % self.umask)
        nodes_file_path = self.nodefile[1]
        os.environ["COBALTNODEFILE"] = nodes_file_path
        for key, value in self.env.iteritems():
            os.environ[key] = value
        atexit._atexit = []
        stdin = open(self.stdin or "/dev/null", "r")
        os.dup2(stdin.fileno(), sys.__stdin__.fileno())
        try:
            stdout = open(self.stdout or tempfile.mktemp(), "a")
            os.dup2(stdout.fileno(), sys.__stdout__.fileno())
        except (IOError, OSError):
            logger.exception(("Process Group %s: error opening stdout " +
                              "file %s (stdout will be lost)")
                             % (self.id, self.stdout))
        try:
            stderr = open(self.stderr or tempfile.mktemp(), "a")
            os.dup2(stderr.fileno(), sys.__stderr__.fileno())
        except (IOError, OSError):
            logger.exception(("Process Group %s: error opening stderr " +
                              "file %s (stderr will be lost)")
                             % (self.id, self.stderr)) 
        cmd = (self.executable, self.executable)
        if self.args:
            cmd = cmd + (self.args)
        try:
            cobalt_log_file = open(self.cobalt_log_file or "/dev/null", "a")
            print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
            print >> cobalt_log_file, "called with environment:\n"
            for key in os.environ:
                print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
            print >> cobalt_log_file, "\n"
            cobalt_log_file.close()
        except IOError:
            logger.error("Job %s/%s: unable to open cobalt log file %s"
                         % (self.id, self.user, self.cobalt_log_file))
        try:
            os.execl(*cmd)
        except OSError:
            logger.exception("Job %s/%s: unable to execl the script"
                             % (self.id, self.user))
            os._exit(1)

    def signal(self, signame="SIGINT"):
        """Do something with this process group depending on the signal"""
        if self.head_pid and self.state != "terminated":
            try:
                os.kill(self.head_pid, getattr(signal, signame))
            except OSError, err:
                logger.exception("signal failure for PG %s: %s"
                                 % (self.id, err))
        elif not self.head_pid and self.state != "terminated":
            if signame == "SIGINT" or signame == "SIGTERM" or \
                    signame == "SIGKILL":
                os.remove(self.nodefile[1])
                self.exit_status = 1

    def wait(self):
        """Sets the PG state to 'terminated' if done"""
        if self.head_pid:
            try:
                pid, status = os.waitpid(self.head_pid, os.WNOHANG)
            except OSError:
                return
            if self.head_pid == pid:
                # Child has terminated
                status = status >> 8
                # Remove temporary file with node locations
                os.remove(self.nodefile[1])
                self.exit_status = status
                # Do something if exit status is non-zero?



class BBSystem(Component):
    """Breadboard system component.

    Methods:
    add_process_groups -- allocates nodes
    get_process_groups -- get process groups based on specs
    signal_process_groups -- signal a process group
    wait_process_groups -- removed process groups based on specs
    """

    name = "system"
    implementation = "Breadboard"

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.resources = ResourceDict()
        self.process_groups = ProcessGroupDict()
        self.process_groups.item_cls = BBProcessGroup
        self.queue_assignments = {}
        self.queue_assignments["default"] = sets.Set(self.resources)

    #####################
    # Main set of methods
    #####################
    def add_process_groups(self, specs):
        """Allocate nodes and add the list of those allocated to the PGDict"""
        return self.process_groups.q_add(specs, lambda x, _:self._start_pg(x))
    add_process_groups = exposed(query(add_process_groups))

    def get_process_groups(self, specs):
        """Get a list of existing allocations"""
        self._wait()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))

    def signal_process_groups(self, specs, sig):
        """Free the specified process group (set of allocated nodes)"""
        return self.process_groups.q_get(specs, lambda x, y:x.signal(y),
                                         sig)
    signal_process_groups = exposed(query(signal_process_groups))

    def wait_process_groups(self, specs):
        """Remove terminated process groups"""
        return self.process_groups.q_del(specs, lambda x,
                                         _:self._release_resources(x))
    wait_process_groups = exposed(query(wait_process_groups))

    #########################################
    # Methods for dealing with Process Groups
    #########################################
    def _start_pg(self, pgp):
        """Starts a process group by initiating building/rebooting nodes"""

        ###########################################
        ### The following is for back-compatibility
        ### with bballoc (bbtools) until breadboard
        ### is switched entirely to run on cobalt
        ###########################################
        bbdata = bblib.BBConfig("/etc/bb.xml")
        bbdata.SetNodeAttr(pgp.location, {"user":pgp.user, "state":"Cobalt",
                                          "comment":"Managed by Cobalt"})
        bbdata.WriteAndClose()
        ###########################################
        ### End of back-compatibility
        ###########################################

        specs = [{"name":name, "attributes":"*"} for name in pgp.location]
        resources = self.get_resources(specs)
        action = "build-%s" % pgp.kernel
        for res in resources:
            # Set build action for each resource
            specs = [{"name":res.name}]
            new_attrs = {"attributes":{"action":action}}
            self.set_attributes(specs, new_attrs)
            mac = res.attributes["mac"]
            linkname = "/tftpboot/pxelinux.cfg/01-%s" \
                % mac.replace(":", "-").lower()
            if os.readlink(linkname) == action:
                continue
            os.unlink(linkname)
            os.symlink(action, linkname)
        for res in resources:
            # Cycle power
            os.system("/usr/sbin/pm -c %s" % res.name)
            # Add resource to list of building nodes
            pgp.building_nodes.append(res.name)

    def _check_builds_done(self):
        """Checks if nodes are done building for each process group and
        scripts can begin running"""
        for pgp in [x for x in self.process_groups.itervalues() if
                    (len(x.building_nodes) > 0 or len(x.pinging_nodes) > 0)]:
            specs = [{"name":name, "attributes":"*"}
                     for name in pgp.building_nodes]
            building = self.get_resources(specs)
            build_action = "build-%s" % pgp.kernel
            for node in building:
                if node.attributes["action"] != build_action:
                    pgp.building_nodes.remove(node.name)
                    pgp.pinging_nodes.append(node.name)
            for nodename in pgp.pinging_nodes:
                if os.system("/bin/ping -c 1 -W 1 %s > /dev/null"
                             % nodename):
                    continue
                pgp.pinging_nodes.remove(nodename)
            if len(pgp.building_nodes) == 0 and len(pgp.pinging_nodes) == 0:
                pgp.start()
    _check_builds_done = automatic(_check_builds_done)

    def node_done_building(self, node):
        """Sets a node as done building
        
        Arguments:
        node -- string name of node that is done building

        Returns: nothing
        """
        specs = [{"name":node, "attributes":"*"}]
        nodedata = self.get_resources(specs)
        if len(nodedata) > 0:
            buildimage = nodedata[0].attributes["action"]
            nodedata[0].attributes["action"] = buildimage.replace("build-",
                                                                  "boot-")
    node_done_building = exposed(node_done_building)

    def _wait(self):
        """Calls the process group container's wait() method"""
        for pgp in self.process_groups.itervalues():
            pgp.wait()
    _wait = automatic(_wait)

    def _release_resources(self, pgp):
        """Releases the resources held by a process group"""
        os.system("/usr/sbin/pm -0 %s" % " ".join(pgp.location))
        specs = [{"name":name} for name in pgp.location]
        new_attrs = {"state":"idle"}
        self.set_attributes(specs, new_attrs)

        ###########################################
        ### The following is for back-compatibility
        ### with bballoc (bbtools) until breadboard
        ### is switched entirely to run on cobalt
        ###########################################
        bbdata = bblib.BBConfig("/etc/bb.xml")
        bbdata.SetNodeAttr(pgp.location, {"user":"Cobalt"})
        bbdata.WriteAndClose()
        ###########################################
        ### End of back-compatibility
        ###########################################

    ####################################
    # Methods for dealing with resources
    ####################################
    def add_resources(self, specs):
        """Add a resource to this system
        
        Arguments:
        specs -- A list of dictionaries with the attributes for the resources
        
        Returns: list of values added
        """
        try:
            ret = self.resources.q_add(specs)
            for res in ret:
                self.queue_assignments["default"].add(res)
        except KeyError:
            ret = "KeyError"
        return ret
    add_resources = exposed(query(add_resources))

    def remove_resources(self, specs):
        """Remove a resource from this system
        
        Arguments:
        specs -- A list of dictionaries with the attributes to pick which
                 resources to remove

        Returns: list of resources removed
        """
        ret = self.resources.q_del(specs)
        for res in ret:
            self.queue_assignments["default"].discard(res)
        return ret
    remove_resources = exposed(remove_resources)

    def get_resources(self, specs):
        """Returns a list of all the resources for this system matching the
        given specs (list of dictionaries)"""
        return self.resources.q_get(specs)
    get_resources = exposed(query(get_resources))

    def set_attributes(self, specs, newattrs):
        """Sets an attribute in specified resources

        Arguments:
        specs -- list of dictionaries with resource attributes to match
        newattrs -- a dictionary with key:val pairs of attributes to set

        Returns: a list of the changed resources
        """
        return self.resources.q_get(specs,
                                    lambda x, y:[set_attr(x, key, val)
                                                 for key, val in y.iteritems()],
                                    newattrs)
    set_attributes = exposed(query(set_attributes))

    def remove_attributes(self, specs, attrs):
        """Removes other attributes in specified resources

        Arguments:
        specs -- list of dictionaries with resource attributes to match
        attrs -- list of names of attributes to remove from resource.attributes

        Returns: a list of the changed resources
        """
        return self.resources.q_get(specs, lambda x, y:[rem_attr(x, key)
                                                        for key in y], attrs)
    remove_attributes = exposed(query(remove_attributes))

    ##########################################################
    # Methods for interacting with scheduler and queue-manager
    ##########################################################
    def validate_job(self, spec):
        """Validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        max_nodes = len(self.get_resources([{"name":"*", "functional":True,
                                             "scheduled":True}]))
        try:
            spec["nodecount"] = int(spec["nodecount"])
        except ValueError:
            raise JobValidationError("Non-integer node count")
        if not 0 < spec["nodecount"] <= max_nodes:
            raise JobValidationError("Node count out of realistic range")
        if float(spec["time"]) < 15:
            raise JobValidationError("Walltime less than minimum 15 minutes")
        if "kernel" in spec:
            if not (os.path.exists("/tftpboot/pxelinux.cfg/build-%s" %
                                   spec["kernel"]) and 
                    os.path.exists("/tftpboot/pxelinux.cfg/boot-%s" %
                                   spec["kernel"])):
                raise JobValidationError(("Specified image %s (from -k " +
                                         "'kernel' flag does not exist")
                                         % spec["kernel"])
        if "attrs" in spec:
            matched_res = self.resources.get_attr_matched_resources(
                [{"name":"*", "functional":True, "scheduled":True,
                  "attributes":"*"}],
                spec["attrs"])
            if spec["nodecount"] > len(matched_res):
                raise JobValidationError("Not enough nodes exist with the " +
                                         "attributes to match")
        return spec
    validate_job = exposed(validate_job)

    def verify_locations(self, location_list):
        """Makes sure a 'location string' is valid"""
        resources = self.get_resources([{"name":r} for r in location_list])
        return [r.name for r in resources]
    verify_locations = exposed(verify_locations)

    def find_job_location(self, job_location_args, end_times):
        """Finds and reserves a list of nodes in which the job can run
        
        Arguments:
        job_location_args -- A list of dictionaries with info about the job
            jobid -- string identifier
            nodes -- int number of nodes
            queue -- string queue name
            required -- ??
            utility_score -- ??
            threshold -- ??
            walltime -- ??
            attrs -- dictionary of attributes to match against
        end_times -- supposed time the job will end

        Returns: Dictionary with list of nodes a job can run on, keyed by jobid
        """
        locations = {}
        def jobsort(job):
            """Used to sort job list by utility score"""
            return job["utility_score"]
        job_location_args.sort(key=jobsort)
        for job in job_location_args:
            specs = [{"name":"*", "functional":True, "scheduled":True,
                      "state":"idle", "attributes":"*"}]
            if "attrs" not in job or job["attrs"] is None:
                job["attrs"] = {}
            resources = self.resources.get_attr_matched_resources(specs,
                                                                  job["attrs"])
            if len(resources) < job["nodes"]:
                #Can't schedule job - not enough resources
                continue
            def namesort(res):
                """Used to sort resources by name"""
                return res.name
            resources.sort(key=namesort)
            used_resources = resources[:job["nodes"]]
            for res in used_resources:
                res.state = "busy"
            locations[job["jobid"]] = [r.name for r in used_resources]
        return locations
    find_job_location = exposed(find_job_location)

    def find_queue_equivalence_classes(self, reservation_dict, 
                                       active_queue_names):
        """Finds equivalent queues"""
        equiv = []
        for queue in self.queue_assignments:
            # skip queues that aren't running
            if not queue in active_queue_names:
                continue
            found_a_match = False
            for equ in equiv:
                if equ['data'].intersection(self.queue_assignments[queue]):
                    equ['queues'].add(queue)
                    equ['data'].update(self.queue_assignments[queue])
                    found_a_match = True
                    break
            if not found_a_match:
                equiv.append({'queues': set([queue]),
                              'data': set(self.queue_assignments[queue]),
                              'reservations': set()})
        real_equiv = []
        for eq_class in equiv:
            found_a_match = False
            for equ in real_equiv:
                if equ['queues'].intersection(eq_class['queues']):
                    equ['queues'].update(eq_class['queues'])
                    equ['data'].update(eq_class['data'])
                    found_a_match = True
                    break
            if not found_a_match:
                real_equiv.append(eq_class)
        equiv = real_equiv
        for eq_class in equiv:
            for res_name in reservation_dict:
                for host_name in reservation_dict[res_name].split(":"):
                    if host_name in eq_class['data']:
                        eq_class['reservations'].add(res_name)
            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
        return equiv
    find_queue_equivalence_classes = exposed(find_queue_equivalence_classes)



######################################################
# Functions used by above classes, but are not methods
######################################################
def set_attr(res, key, val):
    """Helper method for system:set_attributes - actually does the
    setting of each resources attributes"""
    if key != "attributes":
        setattr(res, key, val)
    else:
        for key2, val2 in val.iteritems():
            if key2 == "mac":
                val2 = val2.replace("-", ":")
            res.attributes[key2] = val2

def rem_attr(res, key):
    """Helper method for system:remove_attributes - actually does the
    removing of each resources attributes"""
    if key in res.attributes:
        del res.attributes[key]
