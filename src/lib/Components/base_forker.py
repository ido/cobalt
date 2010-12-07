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


import Cobalt.Logging
from Cobalt.Components.base import Component, exposed, automatic
from Cobalt.Data import IncrID


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
        #keep the Popen object handle.
        self.proc = None

class job_preexec(object):
    '''Class for handling pre-exec tasks for a job.
    Initilaization takes a job-data object.  This allows id's to be set 
    properly and other bookkeeping tasks to be correctly set.

    '''

    def __init__(self, data):

        self.data = data

    def __call__(self):
        '''this is where the job-setting magic happens
        
        '''
        data = self.data
        label = "%s/%s" % (data["jobid"], data["id"])    
        try:
            # only root can call os.setgroups so we need to do this
            # before calling os.setuid
            try:
                os.setgroups([])
                os.setgroups(data["other_groups"])
            except:
                self.logger.error("task %s: failed to set supplementary groups",
                        label, exc_info=True)
            try:
                os.setgid(data["primary_group"])
                os.setuid(data["userid"])
            except OSError:
                self.logger.error("task %s: failed to change userid/groupid", 
                        label)
                os._exit(1)
                       
            if data["umask"] != None:
                try:
                    os.umask(data["umask"])
                except:
                    self.logger.error("task %s: failed to set umask to %s", 
                            label, data["umask"])

            for key, value in data["postfork_env"].iteritems():
                os.environ[key] = value
                    
            atexit._atexit = []
        
            try:
                stdin = open(data["stdin"] or "/dev/null", 'r')
            except (IOError, OSError, TypeError), e:
                self.logger.error("task %s: error opening stdin file %s: %s (stdin will be /dev/null)", label, data["stdin"], e)
                stdin = open("/dev/null", 'r')
            os.dup2(stdin.fileno(), 0)
                
            new_out = None
            try:
                stdout = open(data["stdout"], 'a')
            except (IOError, OSError, TypeError), e:
                self.logger.error("task %s: error opening stdout file %s: %s", 
                        label, data["stdout"], e)
                output_to_devnull = False
                try:
                    scratch_dir = get_forker_config("scratch_dir", None)
                    if scratch_dir:
                        new_out = os.path.join(scratch_dir, 
                                "%s.output" % data["jobid"])
                        self.logger.error("task %s: sending stdout to scratch_dir %s", label, new_out)
                        stdout = open(new_out, 'a')
                    else:
                        self.logger.error("set the scratch_dir option in the [forker] section of cobalt.conf to salvage stdout")
                        output_to_devnull = True
                except Exception, e:
                    output_to_devnull = True
                    self.logger.error("task %s: error opening stdout file %s: %s", label, new_out, e)
                                          
                if output_to_devnull:
                    stdout = open("/dev/null", 'a')
                    new_out = "/dev/null"
                    self.logger.error("task %s: sending stdout to /dev/null",
                            label)
            os.dup2(stdout.fileno(), sys.__stdout__.fileno())
                
            new_err = None
            try:
                stderr = open(data["stderr"], 'a')
            except (IOError, OSError, TypeError), e:
                self.logger.error("task %s: error opening stderr file %s: %s", label, data["stderr"], e)
                error_to_devnull = False
                try:
                    scratch_dir = get_forker_config("scratch_dir", None)
                    if scratch_dir:
                        new_err = os.path.join(scratch_dir, 
                                "%s.error" % data["jobid"])
                        self.logger.error("task %s: sending stderr to scratch_dir %s", label, new_err)
                        stderr = open(new_err, 'a')
                    else:
                        self.logger.error("set the scratch_dir option in the [forker] section of cobalt.conf to salvage stderr")
                        error_to_devnull = True
                except Exception, e:
                    error_to_devnull = True
                    self.logger.error("task %s: error opening stderr file %s: %s", label, new_err, e)
                                          
                if error_to_devnull:
                    stderr = open("/dev/null", 'a')
                    new_err = "/dev/null"
                    self.logger.error("task %s: sending stderr to /dev/null", label)
            os.dup2(stderr.fileno(), sys.__stderr__.fileno())
                
            cmd = data["cmd"]
            try:
                cobalt_log_file = open(data["cobalt_log_file"], "a")
                if new_out:
                    print >> cobalt_log_file, "failed to open %s" % data["stdout"]
                    print >> cobalt_log_file, "stdout sent to %s\n" % new_out
                if new_err:
                    print >> cobalt_log_file, "failed to open %s" % data["stderr"]
                    print >> cobalt_log_file, "stderr sent to %s\n" % new_err
                print >> cobalt_log_file, "%s\n" % " ".join(cmd[1:])
                print >> cobalt_log_file, "called with environment:\n"
                for key in os.environ:
                    print >> cobalt_log_file, "%s=%s" % (key, os.environ[key])
                print >> cobalt_log_file, "\n"
                cobalt_log_file.close()
            except:
                self.logger.error("task %s: unable to open cobaltlog file %s", 
                                 label, data["cobalt_log_file"])
        except:
            self.logger.error("task %s: Unhandled exception.")
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
    
    name = "forker"
    implementation = "bgforker"
    
    # A default logger for the class is placed here.
    # Assigning an instance-level logger is supported,
    # and expected in the case of multiple instances.
    logger = module_logger
    
    def __init__ (self, *args, **kwargs):
        """Initialize a new BaseForker.
        
        All arguments are passed to the component constructor.
        """
        Component.__init__(self, *args, **kwargs)
        self.children = {}
        self.id_gen = IncrID()

    def __getstate__(self):
        return {'next_job_id': self.id_gen.idnum+1}
   
    def __setstate__(self):
        self.id_gen = IncrID()
        self.ig_gen.set(state['next_job_id'])

    def __save_me(self):
        '''Periodically save off a statefile.'''
        Component.save(self)
    __save_me = automatic(__save_me, 
            float(get_forker_config('save_me_interval', 10)))
        

    def child_completed(self, local_id):
        '''check to see if our child has completed.  This will store the
        retcode in the child, asuming we have one.

        '''
        
        retcode = self.children[local_id].subproc.poll()
        if retcode != None:
            self.children[local_id].exit_status = retcode
            return True
        return False
    child_completed = exposed(child_completed)

    def get_output(self, local_id):
        '''return a tupple of return code, stdout, stderr
           if None, None, None returned, then we're not done.

           if stdout or stderr are none and the process has exited, then 
           that output has been redirected to some other file, and not a 
           subprocess.PIPE.

        '''

        if self.children[local_id].exit_status != None:
            pg = self.childeren[local_id].proc
            stdout = None
            stderr = None
            if pg.stdout != None:
                stdout = pg.stdout.readlines()
            if pg.stderr != None:
                stderr = pg.stderr.readlines()
            return pg.exit_status, stdout, stderr
        return None,None,None

    get_output = exposed(get_output)

    
       
    def fork(self, cmd, tag=None, label=None, app_env=None, 
            data=None, preexec=None):
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

        try:
            env = os.environ
            if app_env != None:
                for key in app_env:
                    env[key] = app_env[key]

            if prefork == None:
                child.proc = subprocess.Popen(cmd, env=env, stdout=PIPE, 
                        stderr=PIPE)
                child.pid = child.proc.pid
            else:
                #As noted above.  Do not send stdout/stderr to a pipe.  User 
                #jobs routed to that would be bad.
                child.proc = subprocess.Popen(cmd, env=env, preexec_fn=preexec)
                child.pid = child.proc.pid
                self.logger.info("task %s: forked with pid %s", child.label, 
                    child.pid)
            self.childeren[child.id] = child
            return child.id
        except OSError as e:
            self.logger.error("%s Task %s failed to execute with a code of %s: %s", child.label, child.id, e.errno, e.strerr)
        except ValueError:
            self.logger.error("%s Task %s failed to run due to bad arguments.",
                    child.label, child.id)
        except Exception as e:
            self.logger.error("%s Task %s failed due to an %s exception.",
                    child.label, child.id, e)
            self.logger.debug("%s Parent Traceback:\n %s", child.label, 
                    format_exc())
            self.logger.debug("%s Child Traceback:\n %s", child_label,
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
        ret = []
        if tag != None:
            return [kid for kid in self.childeren.itervalues()
                    if (kid.exit_status is None) and
                       (kid.tag == tag)]
        else:
            for kid in self.children.itervalues():
                if kid.exit_status is None:
                    ret.append(kid.id)
                
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
