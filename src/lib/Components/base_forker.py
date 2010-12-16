"""Implementations of the forker component.

Classes:
BaseForker -- generic implementation

The forker component provides a single threaded component which can safely
fork new processes.

"""

import logging
import sys
import os
import signal
import socket
import time
import atexit
import ConfigParser
import subprocess
import shlex
from subprocess import PIPE
from traceback import format_exc

from threading import Lock
from Cobalt.Statistics import Statistics
import Cobalt.Logging
from Cobalt.Components.base import Component, exposed, automatic
from Cobalt.Data import IncrID
from Cobalt.Util import sleep


config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)

# A default logger for the component is instantiated here.
module_logger = logging.getLogger("Cobalt.Components.BaseForker")


def get_forker_config(option, default):
    try:
        value = config.get('forker', option)
    except Exception, e:
        if isinstance(e, ConfigParser.NoSectionError):
            module_logger.info("[forker] section missing from cobalt.conf")
            value = default
        elif isinstance(e, ConfigParser.NoOptionError):
            value = default
        else:
            raise e
    return value


__all__ = [
    "BaseForker",
]


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
        self.stdout = None
        self.stderr = None
        self.ignore_output = False
        self.complete = False
        self.old_child = False
        #keep the Popen object handle.
        self.proc = None
    
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




class BaseForker (Component):
    
    """Generic implementation of the service-location component.
    
    Methods:
    fork -- takes a dictionary specifying parameters for the forked task (exposed)
    signal -- signal a child with the specified signame (exposed)
    active_list -- retrieve a list of children which are still running (exposed)
    get_status -- return a dictionary of status information for a finished process (exposed)
    wait -- wait on children and record their status (automatic)
    """
    
    name = "forker"
    implementation = "bgforker"
    UNKNOWN_ERROR = 255
    
    # A default logger for the class is placed here.
    # Assigning an instance-level logger is supported,
    # and expected in the case of multiple instances.
    logger = module_logger
   
    __statefields__ = ['next_task_id', 'children']

    def __init__ (self, *args, **kwargs):
        """Initialize a new BaseForker.
        
        All arguments are passed to the component constructor.
        """
        Component.__init__(self, *args, **kwargs)
        self.children = {}
        self.id_gen = IncrID()

    def __getstate__(self):

        return {'next_task_id': self.id_gen.idnum+1,
                'children'  : self.children}
   
        #FIXME: Single threaded things don't need a lock but components do.
        #  It will do nothing, fortunately. Parent needs to be picked as well
        #  or whatever we eventually decide to do.

    def __setstate__(self, state):
        self.id_gen = IncrID()
        self.id_gen.set(state['next_task_id'])
        if state.has_key('children'):
            self.children = state['children']
        self.lock = Lock()
        self.statistics = Statistics()

    def __save_me(self):
        '''Periodically save off a statefile.'''
        Component.save(self)
    __save_me = automatic(__save_me, 
            float(get_forker_config('save_me_interval', 10)))
        
    def dummy_child(self):
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
            self.logger.warning("Could not find task id %s.  Assuming this "
                    "process died in an unknown error-state.", local_id)
            return self.UNKNOWN_ERROR

        if child.exit_status != None:
            #we're already done
            return child.exit_status

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
            self.logger.warning("Task %s: Could not locate child process data "
                    "entry.  Returning a dummy child.", local_id)
            return self.dummy_child()
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
                        pg.terminate()
                        sleep(5)
                    if pg.poll() == None:
                        pg.kill()
                except OSError:
                    #apparently we're already dead.
                    pass
            #now that we're dead...
            del self.children[local_id]

    child_cleanup = exposed(child_cleanup)
    
       
    def fork(self, cmd, tag=None, label=None, app_env=None, preexec=None):
        """Fork a child task.  
        cmd -- A list of strings: the command and relevant arguments.
        tag -- a tag identifying the type of job, such as a script
        label -- a label for logger lines.  Somehthing like "Job xxx/yyy:"
        env -- A mapping of environemnt variables to append to the child
        environment. 
        preexec -- a callable class containing code to execute in the child
        process after the fork, but before exec is called
        
        if you use preexec, you are responsible for redirecting stdout/stderr
        as needed.

        returns the forker id of the child process object.

        """

        child = Child()
        child.id = self.id_gen.next() #this would be the 'local_id'
        child.label = label
        child.tag = tag
        child.cmd = cmd[0]
        child.args = cmd[1:]


        try:
            env = os.environ
            if app_env != None:
                for key in app_env:
                    env[key] = app_env[key]

            if preexec == None:
                child.proc = subprocess.Popen(cmd, env=env, stdout=PIPE, 
                        stderr=PIPE)
                child.pid = child.proc.pid
            else:
                #As noted above.  Do not send stdout/stderr to a pipe.  User 
                #jobs routed to that would be bad.
                child.proc = subprocess.Popen(cmd, env=env, preexec_fn=preexec)
                child.pid = child.proc.pid
                child.ignore_output = True
                self.logger.info("task %s: forked with pid %s", child.label, 
                    child.pid)
            self.children[child.id] = child
            return child.id
        except OSError as e:
            self.logger.error("%s Task %s failed to execute with a code of "
                    "%s: %s", child.label, child.id, e.errno, e)
        except ValueError:
            self.logger.error("%s Task %s failed to run due to bad arguments.",
                    child.label, child.id)
        except Exception as e:
            self.logger.error("%s Task %s failed due to an %s exception.",
                    child.label, child.id, e)
            self.logger.debug("%s Parent Traceback:\n %s", child.label, 
                    format_exc())
            if e.__dict__.has_key('child_traceback'):
                self.logger.debug("%s Child Traceback:\n %s", child.label,
                    e.child_traceback)
            #It may be valuable to get the child traceback for debugging.
            raise

        #Well, this has blown up, There is no child, so nothing to return.
        return None
    fork = exposed(fork)
    
    def signal (self, local_id, signame):
        """Signal a child process.
        
        Arguments:
        local_id -- id of the child to signal
        signame -- signal name
        """
        if not self.children.has_key(local_id):
            self.logger.error("signal found no child with id %s", local_id)
            return

        kid = self.children[local_id]
        self.logger.info("task %s: sending %s to pid %s", kid.label, 
                signame, kid.pid)
        try:
            os.kill(kid.pid, getattr(signal, signame))
        except OSError:
            self.logger.error("task %s: signal failure", kid.label, 
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
            ret = [kid for kid in self.children.itervalues()
                    if (kid.exit_status is None) and
                       (kid.tag == tag) and
                       (kid.old_child == False)]

            keys = self.childeren.keys()
            for key in keys:
                if ((self.childeren[key].old_child == True) and
                    (self.childeren[key].tag == tag)):
                    del self.childeren[key]
        else:
            for kid in self.children.itervalues():
                if ((kid.exit_status is None) and
                    (kid.old_child == False)):

                    ret.append(kid.id)
   
            #once reported, we can delete.
            keys = self.childeren.keys()
            for key in keys:
                if self.childeren[key].old_child == True:
                    del self.childeren[key]

        return ret
    active_list = exposed(active_list)
    
    def get_status (self, local_id):
        """Signal a child process.
        
        Arguments:
        local_id -- id of the child to signal
        """

        self.logger.info("status requested for task id %s", local_id)
        if self.children.has_key(local_id):
            dead = self.children[local_id]
            if dead.exit_status is not None:
                del self.children[local_id]
                self.logger.info("task %s: status returned", dead.label)
                return dead.__dict__
            else:
                self.logger.info("task %s: still running", dead.label)
        else:
            self.logger.info("task id %s: not found", local_id)
            
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
                self.logger.info("pid %s died but had no status", pid)
                break
            
            if signum:
                self.logger.info("pid %s died with status %s and signal %s", 
                        pid, status, signum)
            else:
                self.logger.info("pid %s died with status %s", pid, status)
            for each in self.children.itervalues():
                if each.pid == pid:
                    self.logger.info("task %s: dead pid %s matches", 
                            each.label, pid)
                    each.exit_status = exit_status
                    each.core_dump = core_dump
                    each.signum = signum
    wait = automatic(wait)
