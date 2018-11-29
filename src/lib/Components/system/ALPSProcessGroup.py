# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
"""Process group for Cray systems.  The earliest system this targets is the
XC-40 running ALPS.  This adds server-side information for interactive job
launch that is unique to the ALPS environment and is necessary on systems using
eLogin nodes (formerly known as CDL nodes).

"""
import time
import logging

from Cobalt.Util import init_cobalt_config, get_config_option
from Cobalt.DataTypes.ProcessGroup import ProcessGroup

_logger = logging.getLogger(__name__)

init_cobalt_config()

PGROUP_STARTUP_TIMEOUT = float(get_config_option('alpssystem', 'pgroup_startup_timeout', 120.0))
USER_SESSION_HOSTS = [host.strip() for host in
        get_config_option('alpssystem', 'user_session_hosts', '').split(':')]

class ALPSProcessGroup(ProcessGroup):
    '''ALPS-specific PocessGroup modifications.'''

    def __init__(self, spec):
        super(ALPSProcessGroup, self).__init__(spec)
        self.alps_res_id = spec.get('alps_res_id', None)
        self.interactive_complete = False
        now = int(time.time())
        self.startup_timeout = int(spec.get("pgroup_startup_timeout",
            now + PGROUP_STARTUP_TIMEOUT))

    def start(self):
        '''Start the process group. The ALPS version also sets the host to use.
        This host is in a list provided by the configuration file.  If the host
        has an alps_script_forker instance running on it, those currently
        running jobs will be taken into account when selecting where to run.

        The forker host with the lowest number of locations

        Args:
            None

        Returns:
            None

        Raises:
            ProcessGroupStartupError: The start for the process group has failed
                                      and no child process id has been returned.

        Side Effects:
            Prompts the specified forker to start a job.  In the event of an
            interactive job, sets a fake head pid (1) and notes which host
            should be used for the interactive job launch.

        '''
        if self.mode == 'interactive':
            if len(USER_SESSION_HOSTS):
                pass
        return super(ALPSProcessGroup, self).start()
