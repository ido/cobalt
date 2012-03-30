import logging

import Cobalt.Components.bgqsystem 
from Cobalt.Components.bgqsystem import BGSystem
#from test_base import TestComponent

class TestBGQSystem(object):
    
    def setup (self):
        #TestComponent.setup(self)
        self.bgqsystem = BGSystem()


    def test_parse_subblock_config_empty(self):

        ret = self.bgqsystem.parse_subblock_config('Empty')
        assert {} == ret, "Failed: String 'Empty' did not return empty dict."

    def test_parse_subblock_config_none(self):
        ret = self.bgqsystem.parse_subblock_config(None)
        assert {} == ret, "Failed: Passing in None did not return empty dict."

    
    def test_parse_subblock_config_empty_str(self):
        ret = self.bgqsystem.parse_subblock_config('')
        assert {} == ret, "Failed: Passing in empty string did not return empty dict."

    def test_parse_subblock_cofng_str(self):

        ok_dict ={'TEST-00000-11331-128':32,
                  'TEST1-22000-33331-128':64,
                  'TEST2-00040-11331-128':1}
        ret = self.bgqsystem.parse_subblock_config(
                'TEST-00000-11331-128:32,TEST1-22000-33331-128:64,TEST2-00040-11331-128:1')
        assert ok_dict == ret, "Failed: Incorrect parsing of test string."

    
