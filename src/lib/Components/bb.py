"""Breadboard Component"""

import os
import string
import time

from Cobalt.Data import Data, DataDict, IncrID
from Cobalt.Components.base import Component, exposed, automatic, query
from Cobalt.Exceptions import DataCreationError


__all__ = ['BBSystem', 'ProcessGroup']


class Resource(Data):
    """A single unit of a resource
    
    Attributes:
    tag -- resource
    scheduled -- Whether the resource can be scheduled on (default False)
    name -- canonical name
    functional -- Whether the resource is functional (default False)
    queue -- Name of the queue which this resource is in (default "default")
    size -- ??
    attributes -- a dictionary of other attributes of this resource

    Properties:
    state -- "idle", "busy", or "blocked"
    """

    fields = Data.fields + ["tag", "scheduled", "name", "functional", "queue",
                            "size", "attributes", "state"]

    def __init__(self, spec):
        """Initiates a new resource unit."""
        Data.__init__(self, spec)
        self.tag = "Resource"
        self.scheduled = spec.get("scheduled", False)
        self.name = spec.get("name", None)
        self.functional = spec.get("functional", False)
        self.queue = spec.get("queue", "default")
        self.size = 1
        self.attributes = spec.get("attributes", {})
        self.state = spec.get("state", "idle")

    def match_attributes(self, attrs):
        """Returns true if the 'attributes' attribute of the resource
        contains the provided attributes in 'attrs' (a dictionary)"""
        for key, val in attrs.iteritems():
            if not key in self.attributes or self.attributes[key] != val:
                return False
        return True




class ResourceDict(DataDict):
    """Default container for resources.
    Keyed by resource name.
    """

    item_cls = Resource
    key = "name"

    def get_resources(self, specs, attrs):
        """Get those resources that match specs and attrs

        Arguments:
        specs -- list of dictionaries with details for resource to match
        attrs -- dictionary with attributes for the resource to match

        Returns a list of resources that matched specs and attrs"""
        resources = self.q_get(specs)
        for r in resources[:]:
            if not r.match_attributes(attrs):
                resources.remove(r)
        return resources


        

class ProcessGroup(Data):
    """A set of nodes allocated by a user"""
    fields = Data.fields + ['id', 'user', 'size', 'cwd', 'executable', 'env',
                            'args', 'location', 'head_pid', 'stdin', 'stdout',
                            'stderr', 'exit_status', 'state', 'mode',
                            'kerneloptions', 'true_mpi_args']

    #required = ['user']

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.tag = "process group"
        self.id = spec.get("id")
        self.user = spec.get("user", "")
        self.size = spec.get("size")
        self.cwd = spec.get("cwd")
        self.executable = spec.get("executable")
        self.env = spec.get("env", {})
        self.args = " ".join(spec.get("args", []))
        self.location = spec.get("location", [])
        self.head_pid = None
        self.stdin = spec.get("stdin")
        self.stdout = spec.get("stdout")
        self.stderr = spec.get("stderr")
        self.exit_status = None
        self.state = "running"
        self.mode = spec.get("mode")
        self.kerneloptions = spec.get("kerneloptions")
        self.true_mpi_args = spec.get("true_mpi_args")

    def get_state(self):
        """Return the state of the process group"""
        return self.state

    def start(self):
        """Start the process group"""
        ######################
        ## bballoc-like stuff
        ## will go in here
        ######################
        child_pid = os.fork()
        if not child_pid:
            time.sleep(30)
            self.state = "terminated"
            self.exit_status = 0
            os._exit(0)
        else:
            self.head_pid = child_pid

    def signal(self, sig):
        """Do something with this process group depending on the signal"""
        os.system("/usr/sbin/pm -0 %s" % (" ".join(self.location)))




class ProcessGroupDict(DataDict):
    """A container for holding the different sets of allocated nodes.
    Keyed by process group id.
    """

    item_cls = ProcessGroup
    key = "id"
    
    def __init__(self):
        DataDict.__init__(self)
        self.id_gen = IncrID()

    def q_add(self, specs, callback=None, cargs={}):
        """Add a process group to the container"""
        for spec in specs:
            if spec.get("id", "*") != "*":
                raise DataCreationError("cannot specify an id")
            spec['id'] = self.id_gen.next()
        return DataDict.q_add(self, specs, callback, cargs)

    def wait(self):
        """Runs through the process groups and sets state to 'terminated' and
        sets the appropriate exit status if the process group has finished"""
        for pg in self.itervalues():
            try:
                pid, status = os.waitpid(pg.head_pid, os.WNOHANG)
            except OSError: # the child has not terminated
                continue
            # if the child has terminated
            if pg.head_pid == pid:
                status = status >> 8
                pg.exit_status = status
                pg.state = "terminated"

#    def find_by_jobid(self, jobid):
#        for id, pg in self.iteritems():
#            if pg.id == jobid:
#                return pg
#        return None




class BBSystem(Component):
    """Breadboard system component.

    Methods:
    add_process_groups -- allocates nodes
    get_process_groups -- get currently allocated nodes
    wait_process_groups -- removed terminated process groups
    signal_process_groups -- free allocated nodes
    """

    name = "system"
    implementation = "Breadboard"

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self.resources = ResourceDict()
        self.process_groups = ProcessGroupDict()
       
 
    def add_process_groups(self, specs):
        """Allocate nodes and add the list of those allocated to the PGDict"""
        process_groups = self.process_groups.q_add([specs],
                                                   lambda x, _:x.start())
        return process_groups
    add_process_groups = exposed(query(add_process_groups))


    def get_process_groups(self, specs):
        """Get a list of existing allocations"""
        self._wait()
        return self.process_groups.q_get(specs)
    get_process_groups = exposed(query(get_process_groups))


    def _wait(self):
        """Calls the process group container's method to mark
        finished process groups as terminated"""
        self.process_groups.wait()
    _wait = automatic(_wait)


    def wait_process_groups(self, specs):
        """Remove terminated process groups"""
        return self.process_groups.q_del(specs)
    wait_process_groups = exposed(query(wait_process_groups))


    def signal_process_groups(self, specs, signal):
        """Free the specified process group (set of allocated nodes)"""
        return self.process_groups.q_get(specs, lambda x, y:x.signal(y),
                                         signal)
    signal_process_groups = exposed(query(signal_process_groups))


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
        return self.resources.q_get(specs, lambda x, y:[self.set_attr(x, key, \
                                                                          val)\
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
                    val2 = string.replace(val2, "-", ":")
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

    def add_resources(self, specs):
        """Add a resource to this system
        
        Arguments:
        specs -- A list of dictionaries with the attributes for the resources
        
        Returns: list of values added
        """
        try:
            return self.resources.q_add(specs)
        except KeyError:
            return "KeyError"
    add_resources = exposed(add_resources)


    def remove_resources(self, specs):
        """Remove a resource from this system
        
        Arguments:
        specs -- A list of dictionaries with the attributes to pick which
                 resources to remove

        Returns: list of resources removed
        """
        return self.resources.q_del(specs)
    remove_resources = exposed(remove_resources)


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
            resources = self.resources.get_resources(specs, job["attrs"])
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
