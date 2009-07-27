"""Test cases for the BBSystem component"""
from Cobalt.Components.bb import BBSystem
from Cobalt.Exceptions import DataCreationError

__all__ = ["TestBBSystem"]

class TestBBSystem():
    """Test class for BBSystem component"""
    
    def __init__(self):
        self.bb = None

    def setup(self):
        """Sets up the test component"""
        self.bb = BBSystem()
        self.setup_resources()

    def setup_resources(self):
        """Sets up the resources for the test component"""
        # Test adding resources
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == 0
        self.bb.add_resources(
            [{"name":"bb01", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":2,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb02", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":2,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb03", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":2,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb04", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":2,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb05", "functional":True, "scheduled":True,
              "attributes":{"speed":"slow", "NumProc":2,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb06", "functional":True, "scheduled":True,
              "attributes":{"speed":"slow", "NumProc":2,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb07", "functional":True, "scheduled":True,
              "attributes":{"action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb08", "functional":True, "scheduled":True,
              "attributes":{"action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb09", "functional":True, "scheduled":True,
              "attributes":{"speed":"slow", "NumProc":4,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb10", "functional":True, "scheduled":True,
              "attributes":{"speed":"slow", "NumProc":4,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb11", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":4,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb12", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":4,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb13", "functional":True, "scheduled":True,
              "attributes":{"action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb14", "functional":True, "scheduled":True,
              "attributes":{"action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb15", "functional":True, "scheduled":True,
              "attributes":{"NumProc":4,
                            "action":"idle", "mac":"00:11:22:33:44:55"}},
             {"name":"bb16", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast",
                            "action":"idle", "mac":"00:11:22:33:44:55"}}]
            )
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == 16
        # Test key error for adding resource with same name
        keyerr = self.bb.add_resources([{"name":"bb01"}])
        assert keyerr == "KeyError"
        # Test removing resources
        self.bb.add_resources([{"name":"bb1013", "functional":True}])
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == 17
        self.bb.remove_resources([{"name":"bb1013", "functional":False}])
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == 17
        self.bb.remove_resources([{"name":"bb1013", "functional":True}])
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == 16
        assert "bb1013" not in [r.name for r in num_resources]
        

    def test_find_job_location(self):
        """Tests the component method find_job_location()"""
        job_loc_args = [{"jobid":"1", "nodes":3, "queue":"default",
                         "utility_score":1,
                         "attrs":{"speed":"fast"}},
                        {"jobid":"2", "nodes":2, "queue":"default",
                         "utility_score":1,
                         "attrs":{"speed":"slow"}},
                        {"jobid":"3", "nodes":2, "queue":"default",
                         "utility_score":1},
                        {"jobid":"4", "nodes":3, "queue":"default",
                         "utility_score":1,
                         "attrs":{"NumProc":4}},
                        {"jobid":"5", "nodes":2, "queue":"default",
                         "utility_score":1,
                         "attrs":{"speed":"slow", "NumProc":2}},
                        {"jobid":"6", "nodes":4, "queue":"default",
                         "utility_score":1}]
        job_locs = self.bb.find_job_location(job_loc_args, None)
        assert len(job_locs) == 5
        assert len(self.bb.get_resources([{"state":"idle"}])) == 2
        assert len(self.bb.get_resources([{"state":"busy"}])) == 14

    def test_set_and_remove_attributes(self):
        """Tests the methods set_attributes() and remove_attributes()"""
        specs = [{"name":"bb13"}, {"name":"bb14"}]
        newattrs = {"attrTrue":True, "attrFalse":False, "attrInt":1013}
        self.bb.set_attributes(specs, newattrs)
        resources = self.bb.get_resources(specs)
        for r in resources:
            assert r.attrTrue == True
            assert r.attrFalse == False
            assert r.attrInt == 1013
        newattrs = {"attributes":{"speed":"fast", "myrinet":True}}
        self.bb.set_attributes(specs, newattrs)
        resources = self.bb.get_resources(specs)
        for r in resources:
            assert "speed" in r.attributes
            assert r.attributes["speed"] == "fast"
            assert "myrinet" in r.attributes
            assert r.attributes["myrinet"] == True
        attrs = ["speed"]
        self.bb.remove_attributes(specs, attrs)
        resources = self.bb.get_resources(specs)
        for r in resources:
            assert not hasattr(r, "speed")
            assert not hasattr(r, "myrinet")
            assert "speed" not in r.attributes
            assert "myrinet" in r.attributes and r.attributes["myrinet"] == True

    def test_add_process_groups(self):
        """Tests the method add_process_groups()"""
        specs = [{"id":"1013", "user":"carlson",
                  "location":["bb01", "bb02", "bb10", "bb13"]}]
        try:
            pg_added = self.bb.add_process_groups(specs)
            assert False
        except DataCreationError:
            assert True
        specs0 = [{"user":"carlson", "location":["bb10", "bb13"]}]
        specs1 = [{"user":"carlson", "location":["bb01"]}]
        specs2 = [{"user":"carlson", "location":["bb02"]}]
        specs3 = [{"user":"carlson", "location":["bb03"]}]
        specs4 = [{"user":"carlson", "location":["bb04"]}]
        specs5 = [{"user":"carlson", "location":["bb05"]}]
        specs6 = [{"user":"carlson", "location":["bb06"]}]
        specs7 = [{"user":"carlson", "location":["bb07"]}]
        specs8 = [{"user":"carlson", "location":["bb08", "bb09"]}]
        specs9 = [{"user":"carlson", "location":["bb11", "bb12"]}]
        specscombo = specs0 + specs1 + specs2
        pg_added = self.bb.add_process_groups(specscombo)
        self.bb.add_process_groups(specs3 + specs4 + specs5 + specs6)
        self.bb.add_process_groups(specs7 + specs8)
        self.bb.add_process_groups(specs9)
        pgs = self.bb.get_process_groups([{"id":"*"}])
        assert len(pgs) == 10
