import copy
import ConfigParser
import logging
import os
import sys

import Cobalt
import Cobalt.Components.pg_forker
PGChild = Cobalt.Components.pg_forker.PGChild
PGForker = Cobalt.Components.pg_forker.PGForker

_logger = logging.getLogger(__name__.split('.')[-1])


class _Config (object):
    _bgpm_configfields = ['mpirun', 'mmcs_server_ip']

    _config = ConfigParser.ConfigParser()
    _config.read(Cobalt.CONFIG_FILES)
    if not _config._sections.has_key('bgpm'):
        print '''"bgpm" section missing from cobalt config file'''
        sys.exit(1)

    bgpm = _config._sections['bgpm']
    _mfields = ['bgpm::%s' % (field,) for field in _bgpm_configfields if not bgpm.has_key(field)]

    if _mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(_mfields))
        sys.exit(1)


class BGMpirunChild (PGChild):
    def __init__(self, id = None, **kwargs):
        PGChild.__init__(self, id=id, **kwargs)

        try:
            self.bg_partition = self.pg.location[0]
        except IndexError:
            _logger.error("%s: no partition was specified", self.label)
            raise

    def __getstate__(self):
        state = {}
        state.update(PGChild.__getstate__(self))
        return state

    def __setstate__(self, state):
        PGChild.__setstate__(self, state)

    def preexec_first(self):
        PGChild.preexec_first(self)

        # FIXME: we really shouldn't be copying all of root's environment, should we?
        self.env = copy.deepcopy(os.environ)

        # export subset of MPIRUN_* variables to mpirun's environment
        # we explicitly state the ones we want since some are "dangerous"
        exportenv = [ 'MPIRUN_CONNECTION', 'MPIRUN_KERNEL_OPTIONS',
                      'MPIRUN_MAPFILE', 'MPIRUN_START_GDBSERVER',
                      'MPIRUN_LABEL', 'MPIRUN_NW', 'MPIRUN_VERBOSE',
                      'MPIRUN_ENABLE_TTY_REPORTING', 'MPIRUN_STRACE']

        app_envs = []
        for key, value in self.pg.env.iteritems():
            if key in exportenv:
                self.env[key] = value
            else:
                app_envs.append((key, value))

        self.args = [
            os.path.expandvars(_Config.bgpm['mpirun']),
            '-host', _Config.bgpm['mmcs_server_ip'],
            '-np', str(self.pg.size),
            '-partition', self.bg_partition,
            '-mode', self.pg.mode,
            '-cwd', self.pg.cwd,
            '-exe', self.pg.executable]
        if self.pg.args:
            self.args.extend(['-args', " ".join(self.pg.args)])
        if len(app_envs) > 0:
            self.args.extend(['-env', " ".join(["%s=%s" % x for x in app_envs])])
        if self.pg.kerneloptions:
            self.args.extend(['-kernel_options', self.pg.kerneloptions])

    def preexec_last(self):
        PGChild.preexec_last(self)


class BGMpirunForker (PGForker):
    
    """Component for starting mpirun jobs on the Blue Gene"""
    
    name = __name__.split('.')[-1]
    implementation = name

    child_cls = BGMpirunChild

    logger = _logger

    def __init__ (self, *args, **kwargs):
        """Initialize a new BG mpirun forker.
        
        All arguments are passed to the base forker constructor.
        """
        PGForker.__init__(self, *args, **kwargs)

    def __getstate__(self):
        return PGForker.__getstate__(self)

    def __setstate__(self, state):
        PGForker.__setstate__(self, state)
