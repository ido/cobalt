import logging
import os
import sys
import pwd
import signal
import subprocess

import Cobalt
import Cobalt.Components.pg_forker
PGChild = Cobalt.Components.pg_forker.PGChild
PGForker = Cobalt.Components.pg_forker.PGForker
import Cobalt.Util
from Cobalt.Util import init_cobalt_config, get_config_option, expand_num_list

from cray_messaging import BasilRequest
from cray_messaging import parse_response, ALPSError

exposed = Cobalt.Components.base.exposed
convert_argv_to_quoted_command_string = Cobalt.Util.convert_argv_to_quoted_command_string


_logger = logging.getLogger(__name__.split('.')[-1])

#CONFIG POINT TO ALPS

init_cobalt_config()
BASIL_PATH = get_config_option('alps', 'basil', '/opt/cray/alps/default/bin/apbasil')
DEFAULT_DEPTH = int(get_config_option('alps', 'default_depth', 72))

class ALPSScriptChild (PGChild):
    def __init__(self, id = None, **kwargs):
        PGChild.__init__(self, id=id, **kwargs)
        self.pagg_id = None
        self.alps_res_id = None
        try:
            self.bg_partition = self.pg.location[0]
        except IndexError:
            _logger.error("%s: no partition was specified", self.label)
            raise

        data = kwargs['data']
        if data.has_key('nodect'):
            self.pg.nodect = data['nodect']
        else:
            self.pg.nodect = self.pg.size

    def __getstate__(self):
        state = {}
        state.update(PGChild.__getstate__(self))
        return state

    def __setstate__(self, state):
        PGChild.__setstate__(self, state)

    def preexec_first(self):
        PGChild.preexec_first(self)

        try:
            user_info = pwd.getpwnam(self.pg.user)
            shell = user_info.pw_shell
            homedir = user_info.pw_dir
        except:
            _logger.error("%s: unable to obtain account information for user %s", self.label, self.pg.user)
            self.print_clf_error("unable to obtain account information for user %s", self.pg.user)
            raise

        if not self.cwd:
            self.cwd = homedir

        self.env = {}
        self.env.update(self.pg.env)
        self.env['HOME'] = homedir
        self.env['USER'] = self.pg.user
        self.env['LOGNAME'] = self.pg.user
        self.env['SHELL'] = shell
        self.env["COBALT_PARTNAME"] = self.bg_partition
        self.env["COBALT_PARTSIZE"] = str(self.pg.nodect)
        self.env["COBALT_JOBSIZE"] = str(self.pg.size)
        self.env["COBALT_PARTCORES"] = str(DEFAULT_DEPTH)
        self.env["COBALT_PROJECT"] = str(self.pg.project)
        self.env["COBALT_QUEUE"] = str(self.pg.queue)
        #used for "simulation modes"
        if os.environ.has_key('COBALT_CONFIG_FILES'):
            self.env['COBALT_CONFIG_FILES'] = os.environ['COBALT_CONFIG_FILES']
        if os.environ.has_key('COBALT_SOURCE_DIR'):
            self.env['COBALT_SOURCE_DIR'] = os.environ['COBALT_SOURCE_DIR']
        if os.environ.has_key('COBALT_RUNTIME_DIR'):
            self.env['COBALT_RUNTIME_DIR'] = os.environ['COBALT_RUNTIME_DIR']

        #Confirm the ALPS reservation -- may need to regenerate the reservation.
        if not self._confirm_alps_reservation():
            _logger.error('%s: Unable to confirm ALPS reservation.  Terminating.',
                    self.pg.label)
            sys.exit(1)

        # One last bit of mangling to prevent premature splitting of args
        # quote the argument strings so the shell doesn't eat them.
        self.cmd_string = convert_argv_to_quoted_command_string(self.args)
        self.exe = shell
        self.args = ["-", "-c", "exec " + self.cmd_string]


    def _confirm_alps_reservation(self):
        '''confirm the alps reservation.  If needed, replace the ALPS
        reservation.  Cobalt's already holding these resources.

        If resources can't be confirmed, treat as a "boot failure" and
        terminate child.

        '''
        rc = False
        success = self._send_confirm()
        #success = False
        #if a failure, re-reserve.  Use child data to reassociate reservation
        #with hardware in system componient.
        if not success :
            _logger.warning('Re-reservation required for %s', self.pg.label)
            #rereserve
            params = {}
            params['user_name'] = self.pg.user
            params['batch_id'] = self.pg.jobid
            params['width'] = int(self.pg.nodect) * int(DEFAULT_DEPTH)
            params['nppn'] = int(DEFAULT_DEPTH) #FIXME fix this.  Pass this in from qsub. FIXME
            params['node_list'] = expand_num_list(self.pg.location[0])
            params['depth'] = None
            params['npps'] = None
            params['nspn'] = None
            params['reservation_mode'] = 'EXCLUSIVE'
            params['nppcu'] = None
            params['p-state'] = None
            params['p-govenor'] = None
            reserve_request = BasilRequest('RESERVE', params=params)
            basil = subprocess.Popen(BASIL_PATH, stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = basil.communicate(str(reserve_request))
            if basil.returncode == 0:
                try:
                    response = parse_response(stdout)
                    #won't need the response itself beyond that we were successful.
                except ALPSError:
                    _logger.warning('%s: unable to reserve nodes in ALPS: %s',
                            self.pg.label, self.pg.location)
                else:
                    _logger.warning('%s: New reservation %s created.',
                            self.pg.label, response['reservation_id'])
                    self.pg.alps_res_id = response['reservation_id']
                    success = self._send_confirm()
                    if success:
                        rc = True
            else:
                #Can't re-reserve.  We're dead at this point.  Exit child
                #process now.
                _logger.error('%s re-resevation failed.\n%s\n%s', self.pg.label,
                        stdout, stderr)
        else:
            _logger.info('%s: ALPS reservation %s confirmed', self.pg.label,
                    self.pg.alps_res_id)
            rc = True
        return rc

    def _send_confirm(self):
        success = False
        params = {'reservation_id': self.pg.alps_res_id,
                  'pagg_id': os.getpgid(0)}
        confirm_request = BasilRequest('CONFIRM', params=params)
        #call alps
        #if confirmed, we should have the process group as pagg_id
        basil = subprocess.Popen(BASIL_PATH, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        #couldn't confirm, log message and let failure happen
        stdout, stderr = basil.communicate(str(confirm_request))
        if basil.returncode == 0:
            #if we get a nonzero, that's a failure, fall through to return no
            #success
            try:
                response = parse_response(stdout)
                #won't need the response itself beyond that we were successful.
            except ALPSError:
                _logger.warning('%s: unable to confirm ALPS reservation %s',
                        self.pg.label, self.pg.alps_res_id)
            else:
                _logger.info('%s: confirmed alps_reservation %s', self.pg.label,
                        self.pg.alps_res_id)
                success = True
        else:
            _logger.error('%s: Child exited with stderr: %s', self.pg.label,
                    stderr)

        return success

    def preexec_last(self):
        PGChild.preexec_last(self)

    def signal(self, signum, pg=True):
        #due to how cleanup happens, pg must always be true.
        pg = True
        PGChild.signal(self, signum, pg)



class ALPSScriptForker (PGForker):
    """Component for starting script jobs"""

    name = __name__.split('.')[-1]
    implementation = name

    child_cls = ALPSScriptChild

    logger = _logger

    def __init__ (self, *args, **kwargs):
        """Initialize a new user script forker.

        All arguments are passed to the base forker constructor.
        """
        PGForker.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return PGForker.__getstate__(self)

    def __setstate__(self, state):
        PGForker.__setstate__(self, state)

    def signal(self, child_id, signame):
        """
        Signal a child process.

        Arguments:
        child_id -- id of the child to signal
        signame -- signal name
        """

        _logger.debug("Using overridden signal method.")

        if not self.children.has_key(child_id):
            _logger.error("Child %s: child not found; unable to signal", child_id)
            return

        child = self.children[child_id]
        try:
            signum = getattr(signal, signame)
        except AttributeError:
            _logger.error("%s: %s is not a valid signal name; child not signaled",
                          child.label, signame)
            raise
        #pg = True
        #if self.children[child_id].pg.attrs.has_key('nopgkill'):
        #    pg = False
        #super(ALPSScriptChild, self.children[child_id]).signal(signum, pg=pg)
        child.signal(signum, pg=True)
    signal = exposed(signal)
