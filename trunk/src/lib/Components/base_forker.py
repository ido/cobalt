"""Implementations of the forker component.

Classes:
BaseForker -- generic implementation

The forker component provides a single threaded component which can safely
fork new processes.

"""

import logging
import sys
import copy
import os
import signal
import ConfigParser
import threading
Lock = threading.Lock
import Cobalt
import Cobalt.Statistics
Statistics = Cobalt.Statistics.Statistics
import Cobalt.Components.base
Component = Cobalt.Components.base.Component
exposed = Cobalt.Components.base.exposed
automatic = Cobalt.Components.base.automatic
import Cobalt.Data
IncrID = Cobalt.Data.IncrID
import Cobalt.Util
sleep = Cobalt.Util.sleep

__all__ = [
    "BaseForker",
    "BasePreexec",
]

_logger = logging.getLogger(__name__.split('.')[-1])

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)

def get_forker_config(option, default):
    try:
        value = config.get('forker', option)
    except Exception, e:
        if isinstance(e, ConfigParser.NoSectionError):
            _logger.info("[forker] section missing from cobalt.conf")
            value = default
        elif isinstance(e, ConfigParser.NoOptionError):
            value = default
        else:
            raise e
    return value


class Child(object):
    '''Simple container for data about child processes.

    '''

    def __init__(self):
        self.id = None
        self.pid = None
        self.label = None
        self.exit_status = None
        self.signum = 0
        self.core_dump = False
        self.tag = None
        self.cmd = None
        self.args = None
        self.env = None
        self.stdout = None
        self.stderr = None
        self.ignore_output = False
        self.complete = False
        self.old_child = False
        #keep the Popen object handle.
        self.proc = None
        self.runid = None
    
    def from_dict(self, old_dict):
        for key in old_dict:
            self.__dict__[key] = old_dict[key]

    def get_dict(self):
        
        retdict = {}
        for key in self.__dict__:
            if key != "proc":
                retdict[key] = self.__dict__[key]

        return retdict
    
    def __getstate__(self):
        '''returns the data to be pickled.  Ignores the subprocess's Popen 
        object and sets old_child to true.  If we reload from this data, the
        child process is not recoverable.

        '''
        retdict = self.get_dict()
        retdict['old_child'] = True
        return retdict

    def __setstate__(self, state):
        self.from_dict(state)


class BasePreexec(object):
    def __init__(self, child):
        self.label = child.label

    def do_first(self):
        try:
            #os.setpgrp()
            os.setsid()
        except Exception, e:
            _logger.error("%s: setting the process group and session id failed: %s", self.label, e)
            os._exit(255)

    def do_last(self):
        pass

    def __call__(self):
        try:
            self.do_first()
            self.do_last()
        except:
            _logger.error("%s: Unhandled exception in BasePreexec.")
            raise


class BaseForker (Component):
    
    """Generic implementation of the service-location component.
    
    Methods:
    fork -- takes a dictionary specifying parameters for the forked task (exposed)
    signal -- signal a child with the specified signame (exposed)
    active_list -- retrieve a list of children which are still running (exposed)
    get_status -- return a dictionary of status information for a finished process (exposed)
    wait -- wait on children and record their status (automatic)
    """
    
    # name = __name__.split('.')[-1]
    # implementation = name

    UNKNOWN_ERROR = 256
    
    __statefields__ = ['next_task_id', 'children']

    def __init__ (self, *args, **kwargs):
        """Initialize a new BaseForker.
        
        All arguments are passed to the component constructor.
        """
        Component.__init__(self, *args, **kwargs)

        global _logger
        _logger = self.logger

        self.children = {}
        self.active_runids = []
        self.id_gen = IncrID()

    def __getstate__(self):

        return {'next_task_id': self.id_gen.idnum+1,
                'children'  : self.children}
   
        #FIXME: Single threaded things don't need a lock but components do.
        #  It will do nothing, fortunately. Parent needs to be picked as well
        #  or whatever we eventually decide to do.

    def __setstate__(self, state):
        global _logger
        _logger = self.logger

        self.id_gen = IncrID()
        self.id_gen.set(state['next_task_id'])
        if state.has_key('children'):
            self.children = state['children']
        else:
            self.children = []
        self.lock = Lock()
        self.statistics = Statistics()
        self.active_runids = []

    def __save_me(self):
        '''Periodically save off a statefile.'''
        Component.save(self)
    __save_me = automatic(__save_me, 
            float(get_forker_config('save_me_interval', 10)))
        
    def _dummy_child(self):
        '''Generate a placeholder child should we somehow lose a child.

        '''
        c = Child()
        c.id = -1
        c.pid = -1
        c.label = "Unknown"
        c.exit_status = self.UNKNOWN_ERROR
        c.ignore_output = True 
        c.complete = True
        c.old_child = True 

        return c

    def child_completed(self, local_id):
        '''check to see if our child has completed.  This will store the
        retcode in the child, asuming we have one.

        '''

        try:
            child = self.children[local_id]
        except KeyError:
            _logger.warning("Could not find task id %s.  Assuming this "
                    "process died in an unknown error-state.", local_id)
            return self.UNKNOWN_ERROR

        if child.exit_status != None:
            #we're already done
            return child.exit_status
        #FIXME: Brian has pointed out that there is a possibility of this next section hanging due to waiting for stdout/err
        retcode = child.proc.poll() 
        if (retcode != None):
            child.exit_status = retcode
            if not child.ignore_output:
                child.stdout = child.proc.stdout.readlines()
                child.stderr = child.proc.stderr.readlines()
            child.complete = True
            return retcode
        return None
    child_completed = exposed(child_completed)

    def get_child_data(self, local_id):
        '''return a dict of child data. Return None if there is no
        data.

        '''
        if not self.children.has_key(local_id):
            _logger.warning("Task %s: Could not locate child process data "
                    "entry.  Returning a dummy child.", local_id)
            return self._dummy_child()
        return self.children[local_id].get_dict()
    get_child_data = exposed(get_child_data)

    def child_cleanup(self, local_ids):
        '''Let the forker know that we are done with the child process data.
        and clean up.  Only call this if you have some sort of return code.
        Operates on a list of ids

        '''
        for local_id in local_ids:
            if not self.children.has_key(local_id):
                continue
        
            #kill child if still running.  
            pg = self.children[local_id].proc
            pid = pg.pid
            pg.poll()
            if pg.returncode == None:
                try:
                    if pg.poll() == None:
                        os.kill(pid, signal.SIGTERM)
                        sleep(5)
                    if pg.poll() == None:
                        os.kill(pid, signal.SIGKILL)
                except OSError:
                    #apparently we're already dead.
                    pass
            #now that we're dead...
            if self.children[local_id].runid != None:
                self.active_runids.remove(self.children[local_id].runid)
            del self.children[local_id]

    child_cleanup = exposed(child_cleanup)

    def _fork(self, data=None):
        _logger.error("%s: _fork not implemented by base forker", child.label, child.id)
        return

    def fork(self, cmd, tag=None, label=None, env=None, preexec_data=None,
            runid=None):
        """Fork a child task.  
        cmd -- A list of strings: the command and relevant arguments.
        tag -- a tag identifying the type of job, such as a script
        label -- a label for logger lines.  Somehthing like "<jobid>/<pgid>"
        env -- A mapping of environemnt variables to be included in the child's
        environment. 
        data -- user data to interpreted by a more specialized forker
        runid -- an indentifier generated by the client and used by forker to
        prevent starting a task multiple times during XML-RPC communication
        failure / retry scenarios.
        
        if you use preexec, you are responsible for redirecting stdout/stderr
        as needed.

        returns the forker id of the child process object.

        """

        try:
            #make sure that a job isn't retrying because the XML-RPC hung.
            if (runid != None) and (runid in self.active_runids):
                _logger.warning("%s: Attempting to start a task that is "\
                        "already running. Returning running child id." % label)
                for child,child_obj in self.children.iteritems():
                    if child_obj.runid == runid:
                        return child_obj.id 
    
            child = Child()
            child.id = self.id_gen.next() #this would be the 'local_id'
            child.tag = tag
            child.label = "%s/%s" % (label, child.id)
            child.cmd = cmd[0]
            child.args = cmd[1:]
            child.env = env
            child.runid = runid

            # os.environ silently calls putenv().  It also shallow-copies.
            # I'm checking here to make sure user-environments don't leak
            # back into forker's environment.  --PMR
            
            #only should do this for user jobs, we're not using this for
            #helper scripts.
            orig_env = copy.deepcopy(os.environ)
            child_env_dict = copy.deepcopy(os.environ.data)
            
            try:
                self._fork(child, preexec_data)
                if child.proc == None:
                    raise Exception("no process")
            except:
                _logger.error("%s: failed to start child process", child.label, exc_info=True)

            if orig_env != os.environ:
                _logger.error("forker environment changed during"
                        " task initialization.")

            if child.proc != None:
                self.children[child.id] = child
                self.active_runids.append(runid)
                return child.id
            else:
                return None
        except Exception, e:
            _logger.error("%s: failed due to an unexpected exception: %s", child.label, e, exc_info=True)
            raise

    fork = exposed(fork)
    
    def signal (self, local_id, signame):
        """Signal a child process.
        
        Arguments:
        local_id -- id of the child to signal
        signame -- signal name
        """
        if not self.children.has_key(local_id):
            _logger.error("signal found no child with id %s", local_id)
            return

        kid = self.children[local_id]
        _logger.info("%s: sending %s to pid %s", kid.label, 
                signame, kid.pid)
        try:
            os.kill(kid.pid, getattr(signal, signame))
        except OSError:
            _logger.error("%s: signal failure", kid.label, 
                    exc_info=True)

    signal = exposed(signal)
    
    def active_list (self, tag=None):
        """Retrieve the list of running child processes.
        If a tag is supplied, return active_processes with
        only that tag, otherwise, return all running processes.

        """
        #return only if we match the tag, the job is still running
        #and we haven't lost the process due to a restart.

        ret = []
        if tag != None:
            ret = [kid.id for kid in self.children.itervalues()
                    if (kid.exit_status is None) and
                       (kid.tag == tag) and
                       (kid.old_child == False)]

            keys = self.children.keys()
            for key in keys:
                if ((self.children[key].old_child == True) and
                    (self.children[key].tag == tag)):
                    del self.children[key]
        else:
            for kid in self.children.itervalues():
                if ((kid.exit_status is None) and
                    (kid.old_child == False)):

                    ret.append(kid.id)
   
            #once reported, we can delete.
            keys = self.children.keys()
            for key in keys:
                if self.children[key].old_child == True:
                    del self.children[key]

        return ret
    active_list = exposed(active_list)
    
    def get_status (self, local_id):
        """Signal a child process.
        
        Arguments:
        local_id -- id of the child to signal
        """

        _logger.info("status requested for task id %s", local_id)
        if self.children.has_key(local_id):
            dead = self.children[local_id]
            if dead.exit_status is not None:
                del self.children[local_id]
                _logger.info("%s: status returned: %s", dead.label, dead.exit_status)
                return dead.__dict__
            else:
                _logger.info("%s: still running", dead.label)
        else:
            _logger.info("task id %s: not found", local_id)
            
        return None
    get_status = exposed(get_status)


    def wait(self):
        """Call os.waitpid to status of dead processes.
        """
        while True:
            try:
                pid, status = os.waitpid(-1, os.WNOHANG)
            except OSError: # there are no child processes
                break
            # this is how waitpid + WNOHANG reports things are running
            # but not yet dead
            if pid == 0:
                break
            signum = 0
            core_dump = False
            exit_status = None
            if os.WIFEXITED(status):
                exit_status = os.WEXITSTATUS(status)
            elif os.WIFSIGNALED(status):
                signum = os.WTERMSIG(status)
                if os.WCOREDUMP(status):
                    core_dump = True
                exit_status = 128 + signum
                
            if exit_status is None:
                _logger.info("pid %s died but had no status", pid)
                break
            
            if signum:
                _logger.info("pid %s died with status %s and signal %s; coredump=%s", 
                        pid, exit_status, signum, core_dump)
            else:
                _logger.info("pid %s died with status %s", pid, exit_status)
            for each in self.children.itervalues():
                if each.pid == pid:
                    _logger.info("task %s: dead pid %s matches", 
                            each.label, pid)
                    each.exit_status = exit_status
                    each.core_dump = core_dump
                    each.signum = signum
    wait = automatic(wait)


if __name__ == "__main__":

    print "Initiating forker unit tests"
    test_count = IncrID()
    
    forker = BaseForker()

    init_pid = forker.fork("/bin/ls", runid=1)
    print test_count.next(),":", "forked process with pid %s" % init_pid
    assert (init_pid == 1), "init_id wrong"
    pid_2 = forker.fork("/bin/ls", runid=2)
    assert (pid_2 == 2), "pid_2 wrong"
    print test_count.next(),":", "forked process with pid %s" % pid_2
    pid_3 = forker.fork("/bin/ls", runid=1)
    print test_count.next(),":", "forked process with pid %s" % pid_3

    print forker.active_runids
    print forker.children
    forker.child_cleanup([init_pid, pid_2, pid_3])

    print forker.active_runids
    print forker.children
    pid_4 = forker.fork("/bin/ls", runid=1)
    pid_5 = forker.fork("/bin/ls")
    print pid_4
    forker.child_cleanup([pid_4])

