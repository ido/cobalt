"""Breadboard Component"""

import atexit
import logging
import os
import pwd
import sets
import signal
import sys
import tempfile

from Cobalt.DataTypes.ProcessGroup import ProcessGroup, ProcessGroupDict
from Cobalt.DataTypes.Resource import ResourceDict
from Cobalt.Components.base import Component, automatic, exposed, query
from Cobalt.Exceptions import JobValidationError

__all__ = ["BBSystem", "BBProcessGroup", "BBProcessGroupDict"]


logger = logging.getLogger(__name__)


class BBProcessGroup(ProcessGroup):
    """Process Group modified for Breadboard"""

    fields = ProcessGroup.fields + ["image"]

    def __init__(self, spec):
        ProcessGroup.__init__(self, spec, logger)
        self.image = spec.get("image", "default")
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
            logger.exception("Error getting uid/gid for process " + \
                                 "group %s" % self.id)
            os._exit(1)
        try:
            os.setgid(groupid)
            os.setuid(userid)
        except OSError:
            logger.exception("failed to change uid/gid for process " + \
                                 "group %s" % self.id)
            os._exit(1)
        if self.umask != None:
            try:
                os.umask(self.umask)
            except OSError:
                logger.exception("Failed to set umask to %s" % self.umask)
        nodes_file_path = self.nodefile[1]
        kerneloptions = self.kerneloptions
        app_envs = []
        for key, value in self.env.iteritems():
            app_envs.append((key, value))            
        envs = " ".join(["%s=%s" % x for x in app_envs])
        atexit._atexit = []
        stdin = open(self.stdin or "/dev/null", "r")
        os.dup2(stdin.fileno(), sys.__stdin__.fileno())
        try:
            stdout = open(self.stdout or tempfile.mktemp(), "a")
            os.dup2(stdout.fileno(), sys.__stdout__.fileno())
        except (IOError, OSError):
            logger.exception(("process group %s: error opening stdout " + \
                                  "file %s (stdout will be lost)") \
                                 % (self.id, self.stdout))
        try:
            stderr = open(self.stderr or tempfile.mktemp(), "a")
            os.dup2(stderr.fileno(), sys.__stderr__.fileno())
        except (IOError, OSError):
            logger.exception(("process group %s: error opening stderr " + \
                                  "file %s (stderr will be lost)") \
                                 % (self.id, self.stderr)) 
        cmd = (self.executable, self.executable, "-nodes_file", nodes_file_path)
        if self.args:
            cmd = cmd + ('-args', self.args)
        if envs:
            cmd = cmd + ('-env', envs)
        if kerneloptions:
            cmd = cmd + ('-kernel_options', kerneloptions)
        try:
            cobalt_log_file = open(self.cobalt_log_file or "/dev/null", "a")
            print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
            print >> cobalt_log_file, "called with environment:\n"
            for key in os.environ:
                print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
            print >> cobalt_log_file, "\n"
            cobalt_log_file.close()
        except IOError:
            logger.error("Job %s/%s: unable to open cobalt log file %s" \
                             % (self.id, self.user, self.cobalt_log_file))
        try:
            os.execl(*cmd)
        except OSError:
            logger.exception("Job %s/%s: unable to execl the script" \
                                 % (self.id, self.user))
            os._exit(1)

    def signal(self, signame="SIGINT"):
        """Do something with this process group depending on the signal"""
        if signame == "SIGINT":
            if self.head_pid and self.state != "terminated":
                try:
                    os.kill(self.head_pid, getattr(signal, signame))
                except OSError, e:
                    logger.exception("signal failure for PG %s: %s" \
                                         % (self.id, e))
        else:
            # Handle other signals
            if self.head_pid and self.state != "terminated":
                try:
                    os.kill(self.head_pid, getattr(signal, signame))
                except OSError, e:
                    logger.exception("signal failure for PG %s: %s" \
                                         % (self.id, e))

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

    def signal_process_groups(self, specs, signal):
        """Free the specified process group (set of allocated nodes)"""
        return self.process_groups.q_get(specs, lambda x, y:x.signal(y),
                                         signal)
    signal_process_groups = exposed(query(signal_process_groups))

    def wait_process_groups(self, specs):
        """Remove terminated process groups"""
        return self.process_groups.q_del(specs, lambda x,
                                         _:self._release_resources(x))
    wait_process_groups = exposed(query(wait_process_groups))

    #########################################
    # Methods for dealing with Process Groups
    #########################################
    def _start_pg(self, pg):
        """Starts a process group by initiating building/rebooting nodes"""
        specs = [{"name":name, "attributes":"*"} for name in pg.location]
        resources = self.get_resources(specs)
        action = "build-%s" % pg.image
        for res in resources:
            # Set build action for each resource
            specs = [{"name":res.name}]
            new_attrs = {"attributes":{"action":action}}
            self.set_attributes(specs, new_attrs)
            mac = res.attributes["mac"]
            linkname = "/tftpboot/pxelinux.cfg/01-%s" % \
                mac.replace(":", "-").lower()
            if os.readlink(linkname) == action:
                continue
            os.unlink(linkname)
            os.symlink(action, linkname)
        for res in resources:
            # Cycle power
            os.system("/usr/sbin/pm -c %s" % res.name)
            # Add resource to list of building nodes
            pg.building_nodes.append(res.name)

    def _check_builds_done(self):
        """Checks if nodes are done building for each process group and
        scripts can begin running"""
        for pg in self.process_groups.itervalues():
            if len(pg.building_nodes) > 0 or len(pg.pinging_nodes) > 0:
                specs = [{"name":name, "attributes":"*"} 
                         for name in pg.building_nodes]
                building = self.get_resources(specs)
                build_action = "build-%s" % pg.image
                for node in building:
                    if node.attributes["action"] != build_action:
                        pg.building_nodes.remove(node.name)
                        pg.pinging_nodes.append(node.name)
                for nodename in pg.pinging_nodes:
                    if os.system("/bin/ping -c 1 -W 1 %s > /dev/null" \
                                     % nodename):
                        continue
                    pg.pinging_nodes.remove(nodename)
                if len(pg.building_nodes) == 0 and len(pg.pinging_nodes) == 0:
                    pg.start()
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
        for pg in self.process_groups.itervalues():
            pg.wait()
    _wait = automatic(_wait)

    def _remove_terminated_groups(self):
        """Automatic method to periodically remove terminated process groups"""
        self.wait_process_groups([{"id":"*", "state":"terminated"}])
    _remove_terminated_groups = automatic(_remove_terminated_groups)

    def _release_resources(self, pg):
        """Releases the resources held by a process group"""
        os.system("/usr/sbin/pm -0 %s" % " ".join(pg.location))
        specs = [{"name":name} for name in pg.location]
        new_attrs = {"state":"idle"}
        self.set_attributes(specs, new_attrs)

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
                                    lambda x, y:[self.set_attr(x, key, val) \
                                                     for key, val \
                                                     in y.iteritems()], \
                                        newattrs)
    set_attributes = exposed(query(set_attributes))
    
    def set_attr(self, res, key, val):
        """Helper method for set_attributes - actually does the
        setting of each resources attributes"""
        if key != "attributes":
            setattr(res, key, val)
        else:
            for key2, val2 in val.iteritems():
                if key2 == "mac":
                    val2 = val2.replace("-", ":")
                res.attributes[key2] = val2

    def remove_attributes(self, specs, attrs):
        """Removes other attributes in specified resources

        Arguments:
        specs -- list of dictionaries with resource attributes to match
        attrs -- list of names of attributes to remove from resource.attributes

        Returns: a list of the changed resources
        """
        return self.resources.q_get(specs, lambda x, y:[self.rem_attr(x, key) \
                                                            for key in y], \
                                        attrs)
    remove_attributes = exposed(query(remove_attributes))

    def rem_attr(self, res, key):
        """Helper method for remove_attributes - actually does the
        removing of each resources attributes"""
        if key in res.attributes:
            del res.attributes[key]

    ##########################################################
    # Methods for interacting with scheduler and queue-manager
    ##########################################################
    def validate_job(self, spec):
        """Validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        max_nodes = len(self.get_resources([{"name":"*"}]))
        try:
            spec["nodecount"] = int(spec["nodecount"])
        except ValueError:
            raise JobValidationError("Non-integer node count")
        if not 0 < spec["nodecount"] <= max_nodes:
            raise JobValidationError("Node count out of realistic range")
        if float(spec["time"]) < 10:
            raise JobValidationError("Walltime less than minimum")
        if not spec["mode"] == "script":
            raise JobValidationError("Only 'script' mode supported")
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
            if "attrs" not in job:
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
        for q in self.queue_assignments:
            # skip queues that aren't running
            if not q in active_queue_names:
                continue
            found_a_match = False
            for e in equiv:
                if e['data'].intersection(self.queue_assignments[q]):
                    e['queues'].add(q)
                    e['data'].update(self.queue_assignments[q])
                    found_a_match = True
                    break
            if not found_a_match:
                equiv.append({'queues': set([q]),
                              'data': set(self.queue_assignments[q]),
                              'reservations': set()})
        real_equiv = []
        for eq_class in equiv:
            found_a_match = False
            for e in real_equiv:
                if e['queues'].intersection(eq_class['queues']):
                    e['queues'].update(eq_class['queues'])
                    e['data'].update(eq_class['data'])
                    found_a_match = True
                    break
            if not found_a_match:
                real_equiv.append(eq_class)
        equiv = real_equiv
        for eq_class in equiv:
            for res_name in reservation_dict:
                skip = True
                for host_name in reservation_dict[res_name].split(":"):
                    if host_name in eq_class['data']:
                        eq_class['reservations'].add(res_name)
            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
        return equiv
    find_queue_equivalence_classes = exposed(find_queue_equivalence_classes)
