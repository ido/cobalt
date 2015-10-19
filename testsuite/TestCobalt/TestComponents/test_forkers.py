'''Tests for the forker components

'''

CQM_CONFIG_FILE_ENTRY = """
[forker]
foo = bar

[logging]
to_syslog = True
syslog_level = DEBUG
to_console = True
console_level = DEBUG

"""

# override the cobalt config file before the cqm component is loaded
import Cobalt
import TestCobalt
import ConfigParser
import time

config_file = Cobalt.CONFIG_FILES[0]
config_fp = open(config_file, "w")
config_fp.write(CQM_CONFIG_FILE_ENTRY)
config_fp.close()
config_fp.close()
config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)


from mock import Mock, MagicMock, patch

import Cobalt.Components.base_forker
from Cobalt.Components.user_script_forker import UserScriptForker
from Cobalt.Components.user_script_forker import UserScriptChild
Cobalt.Components.base_forker.config = config

class TestChild(Cobalt.Components.base_forker.BaseChild):

    def preexec_first(self):
        pass

    def preexec_last(self):
        pass

class TestBaseForker(object):

    def setup_base_forker(self):
        self.child_id = None
        self.bf = Cobalt.Components.base_forker.BaseForker()
        self.bf.child_cls = TestChild

    def test_wait_SIGTERM(self):
        # make sure SIGTERM gets sent when marked for death
        self.setup_base_forker()
        self.child_id = self.bf.fork(['/bin/sleep','60'])
        time.sleep(1)
        assert self.child_id != None, "No child id returned"
        self.bf.marked_for_death[self.child_id] = self.bf.children[self.child_id]
        self.bf._wait() #SIGTERM fires now
        time.sleep(1)
        self.bf._wait() #SIGKILL and we're done
        assert self.bf.children[self.child_id].signum == 15, 'Job not SIGTERMed'

    def test_wait_SIGKILL(self):
        # if SIGTERM fails, make sure a SIGKILL is delivered.
        self.setup_base_forker()
        self.bf.DEATH_TIMEOUT = 2
        self.child_id = self.bf.fork(['testsuite/TestCobalt/TestComponents/ignore_sigterm.py','60'])
        time.sleep(1)
        assert self.child_id != None, "No child id returned"
        self.bf.marked_for_death[self.child_id] = self.bf.children[self.child_id]
        self.bf._wait() #SIGTERM (IGNORED) and start timer
        time.sleep(3)
        self.bf._wait() #SIGKILL (give a moment to propigate)
        time.sleep(1) #If we're not dead by now we're in trouble something has gone wrong
        self.bf._wait() #SIGKILL and we're done
        assert self.bf.children[self.child_id].signum == 9, 'Job not SIGKILLed'


class TestUserScriptForker(object):

    @patch('Cobalt.os.killpg')
    @patch('Cobalt.os.kill')
    def test_signal_pgroup(self, mock_kill, mock_killpg):
        #send a killpg to a script process group
        usf = UserScriptForker()
        usf.children[1] = UserScriptChild(data={'nodect':512, 'args':[],
            'cwd':'/dev/null', 'location':'foo', 'jobid':2, 'executable':'bar',
            'user':'frodo', 'size':512})
        usf.children[1].pid = 1234
        usf.signal(1, "SIGTERM")
        mock_killpg.assert_called_with(1234, 15)
        mock_kill.assert_not_called()


    @patch('Cobalt.os.killpg')
    @patch('Cobalt.os.kill')
    def test_signal_nokillpg(self, mock_kill, mock_killpg):
        #use kill if appropriate attr set.
        usf = UserScriptForker()
        usf.children[1] = UserScriptChild(data={'nodect':512, 'args':[],
            'cwd':'/dev/null', 'location':'foo', 'jobid':2, 'executable':'bar',
            'user':'frodo', 'size':512, 'attrs':{'nopgkill': True}})
        usf.children[1].pid = 1234
        usf.signal(1, "SIGTERM")
        mock_kill.assert_called_with(1234, 15)
        mock_killpg.assert_not_called()


    @patch('Cobalt.os.killpg')
    @patch('Cobalt.os.kill')
    def test_signal_no_pid_no_kill(self, mock_kill, mock_killpg):
        usf = UserScriptForker()
        usf.children[1] = UserScriptChild(data={'nodect':512, 'args':[],
            'cwd':'/dev/null', 'location':'foo', 'jobid':2, 'executable':'bar',
            'user':'frodo', 'size':512, 'attrs':{'nopgkill': True}})
        usf.signal(1, "SIGTERM")
        mock_kill.assert_not_called()
        mock_killpg.assert_not_called()
