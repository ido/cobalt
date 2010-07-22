"""Test cases for the BBSystem component"""
import sys
import time
from Cobalt.Components.bb import BBSystem
from Cobalt.Exceptions import DataCreationError

__all__ = ["TestBBSystem"]

############################
## MODIFY THIS LIST OF NAMES
## TO THOSE THAT ARE
## ALLOCATED FOR TESTING
############################
names = []

class TestBBSystem():
    """Test class for BBSystem component"""
    
    def __init__(self):
        self.bb = None
        if len(names) == 0:
            print >> sys.stderr, "Must specify nodes for testing in global " + \
                "list 'names'"
            assert False

    def setup(self):
        """Sets up the test component"""
        self.bb = BBSystem()
        self.setup_resources()

    def setup_resources(self):
        """Sets up the resources for the test component"""
        # Test adding resources
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == 0
        specs = [{"name":name, "functional":True, "scheduled":True,
                  "attributes":{"action":"idle"}} for name in names]
        for spec in specs:
            if spec["name"] == "bb01":
                spec["attributes"]["mac"] = "00-17-31-F9-C8-7F"
            elif spec["name"] == "bb02":
                spec["attributes"]["mac"] = "00-17-31-71-99-C1"
            elif spec["name"] == "bb03":
                spec["attributes"]["mac"] = "00-17-31-71-99-9D"
            elif spec["name"] == "bb04":
                spec["attributes"]["mac"] = "00-17-31-71-99-50"
            elif spec["name"] == "bb05":
                spec["attributes"]["mac"] = "00-17-31-F9-C9-36"
            elif spec["name"] == "bb06":
                spec["attributes"]["mac"] = "00-17-31-71-99-6A"
            elif spec["name"] == "bb07":
                spec["attributes"]["mac"] = "00-17-31-71-99-6C"
            elif spec["name"] == "bb08":
                spec["attributes"]["mac"] = "00-17-31-F9-C9-31"
            elif spec["name"] == "bb09":
                spec["attributes"]["mac"] = "00-17-31-F9-C8-F2"
            elif spec["name"] == "bb10":
                spec["attributes"]["mac"] = "00-17-31-71-99-D0"
            elif spec["name"] == "bb11":
                spec["attributes"]["mac"] = "00-17-31-71-99-82"
            elif spec["name"] == "bb12":
                spec["attributes"]["mac"] = "00-17-31-71-99-EC"
            elif spec["name"] == "bb13":
                spec["attributes"]["mac"] = "00-17-31-71-99-E6"
            elif spec["name"] == "bb14":
                spec["attributes"]["mac"] = "00-17-31-71-99-E8"
            elif spec["name"] == "bb15":
                spec["attributes"]["mac"] = "00-17-31-71-99-E9"
            elif spec["name"] == "bb16":
                spec["attributes"]["mac"] = "00-17-31-71-99-89"
            elif spec["name"] == "bb17":
                spec["attributes"]["mac"] = "00-17-31-F9-C8-DE"
            elif spec["name"] == "bb18":
                spec["attributes"]["mac"] = "00-17-31-71-99-81"
            elif spec["name"] == "bb19":
                spec["attributes"]["mac"] = "00-1A-92-27-37-F0"
            elif spec["name"] == "bb20":
                spec["attributes"]["mac"] = "00-17-31-71-9A-0F"
            elif spec["name"] == "bb21":
                spec["attributes"]["mac"] = "00-17-31-71-99-6D"
            elif spec["name"] == "bb22":
                spec["attributes"]["mac"] = "00-17-31-71-99-74"
            elif spec["name"] == "bb23":
                spec["attributes"]["mac"] = "00-17-31-71-99-D4"
            elif spec["name"] == "bb24":
                spec["attributes"]["mac"] = "00-17-31-71-99-56"
            elif spec["name"] == "bb25":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-40"
            elif spec["name"] == "bb26":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-4E"
            elif spec["name"] == "bb27":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-44"
            elif spec["name"] == "bb28":
                spec["attributes"]["mac"] = "00-1F-C6-86-76-6C"
            elif spec["name"] == "bb29":
                spec["attributes"]["mac"] = "00-1F-C6-84-83-C6"
            elif spec["name"] == "bb30":
                spec["attributes"]["mac"] = "00-23-54-01-DD-D8"
            elif spec["name"] == "bb31":
                spec["attributes"]["mac"] = "00-1F-C6-86-76-72"
            elif spec["name"] == "bb32":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-46"
            elif spec["name"] == "bb33":
                spec["attributes"]["mac"] = "00-1F-C6-86-76-98"
            elif spec["name"] == "bb34":
                spec["attributes"]["mac"] = "00-23-54-44-47-CE"
            elif spec["name"] == "bb35":
                spec["attributes"]["mac"] = "00-1F-C6-0D-BC-54"
            elif spec["name"] == "bb36":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-38"
            elif spec["name"] == "bb37":
                spec["attributes"]["mac"] = "00-1F-C6-86-76-64"
            elif spec["name"] == "bb38":
                spec["attributes"]["mac"] = "00-1F-C6-86-76-76"
            elif spec["name"] == "bb39":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-3E"
            elif spec["name"] == "bb40":
                spec["attributes"]["mac"] = "00-1F-C6-86-76-7C"
            elif spec["name"] == "bb41":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-48"
            elif spec["name"] == "bb42":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-64"
            elif spec["name"] == "bb43":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-76"
            elif spec["name"] == "bb44":
                spec["attributes"]["mac"] = "00-1F-C6-84-83-94"
            elif spec["name"] == "bb45":
                spec["attributes"]["mac"] = "00-1F-C6-84-82-74"
            elif spec["name"] == "bb46":
                spec["attributes"]["mac"] = "00-23-54-A1-86-58"
            elif spec["name"] == "bb47":
                spec["attributes"]["mac"] = "00-1F-C6-84-83-8C"
            elif spec["name"] == "bb48":
                spec["attributes"]["mac"] = "00-23-54-44-47-CC"
        self.bb.add_resources(specs)
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == len(names)
        # Test key error for adding resource with same name
        keyerr = self.bb.add_resources([{"name":names[0]}])
        assert keyerr == "KeyError"
        # Test removing resources
        self.bb.add_resources([{"name":"bb1013", "functional":True}])
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == len(names) + 1
        self.bb.remove_resources([{"name":"bb1013", "functional":False}])
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == len(names) + 1
        self.bb.remove_resources([{"name":"bb1013", "functional":True}])
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == len(names)
        assert "bb1013" not in [r.name for r in num_resources]
        

    def test_find_job_location(self):
        """Tests the component method find_job_location()"""
        self.setup()
        self.bb.add_resources([{"name":"test1", "functional":True,
                                "scheduled":True,
                                "attributes":{"numProc":2, "speed":"slow"}},
                               {"name":"test2", "functional":True,
                                "scheduled":True,
                                "attributes":{"numProc":2, "speed":"slow"}},
                               {"name":"test3", "functional":True,
                                "scheduled":True,
                                "attributes":{"numProc":2, "speed":"fast"}},
                               {"name":"test4", "functional":True,
                                "scheduled":True,
                                "attributes":{"numProc":2, "speed":"fast"}},
                               {"name":"test5", "functional":True,
                                "scheduled":True,
                                "attributes":{"numProc":4, "speed":"fast"}},
                               {"name":"test6", "functional":True,
                                "scheduled":True,
                                "attributes":{"numProc":4, "speed":"fast"}}
                               ])
        job_loc_args = [{"jobid":"1", "nodes":3, "queue":"default",
                         "utility_score":1, "attrs":{"speed":"slow"}},
                        {"jobid":"2", "nodes":2, "queue":"default",
                         "utility_score":2, "attrs":{"speed":"slow"}},
                        {"jobid":"3", "nodes":1, "queue":"default",
                         "utility_score":1, "attrs":{"speed":"fast",
                                                     "numProc":4}},
                        {"jobid":"4", "nodes":3, "queue":"default",
                         "utility_score":2, "attrs":{"speed":"fast"}},
                        {"jobid":"5", "nodes":2, "queue":"default",
                         "utility_score":2, "attrs":{"numProc":2}}
                        ]
        job_locs = self.bb.find_job_location(job_loc_args, None)
        assert len(job_locs) == 3
        assert job_locs["3"] == ["test5"]
        assert job_locs["2"] == ["test1", "test2"]
        assert job_locs["4"] == ["test3", "test4", "test6"]
        assert len(self.bb.get_resources([{"state":"idle"}])) == len(names)
        assert len(self.bb.get_resources([{"state":"busy"}])) == 6

    def test_set_and_remove_attributes(self):
        """Tests the methods set_attributes() and remove_attributes()"""
        self.setup()
        specs = [{"name":"test1"}, {"name":"test2"}]
        newattrs = {"attrTrue":True, "attrFalse":False, "attrInt":1013}
        self.bb.add_resources(specs)
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
        self.setup()
        specs = [{"id":"1013", "user":"carlson",
                  "location":["bb01", "bb02", "bb10", "bb13"]}]
        try:
            pg_added = self.bb.add_process_groups(specs)
            assert False
        except DataCreationError:
            assert True
        specs = [{"user":"carlson", "location":[loc],
                  "executable":"test_bb_script",
                  "stdout":"test_bb_script_stdout"} for loc in names]
        pg_added = self.bb.add_process_groups(specs)
        assert len(pg_added) == len(names)
        pgs = self.bb.get_process_groups([{"id":"*"}])
        assert len(pgs) == len(names)
        specrun = [{"state":"running"}]
        count = 0
        while True:
            done = True
            PGs = self.bb.get_process_groups(specrun)
            for pg in PGs:
                if pg.building_nodes or pg.pinging_nodes:
                    done = False
            if not done:
                time.sleep(20)
                if count < len(names):
                    self.bb.node_done_building(names[count])
                    count = count + 1
                self.bb._check_builds_done()
            else:
                break
        time.sleep(10)
        done = self.bb.get_process_groups([{"state":"terminated"}])
        assert len(done) == len(names)
        resources = self.bb.get_resources([{"name":"*"}])
        assert len(resources) == len(names)
        for res in resources:
            res.state = "busy"
        wait = self.bb.wait_process_groups([{"state":"terminated"}])
        assert len(wait) == len(names)
        resources = self.bb.get_resources([{"name":"*"}])
        assert len(resources) == len(names)
        for res in resources:
            assert res.state == "idle"
        pgs = self.bb.get_process_groups([{"id":"*"}])
        assert len(pgs) == 0

    def test_signal_process_groups(self):
        """Tests the method signal_process_groups()"""
        self.setup()
        pgs = self.bb.get_process_groups([{"id":"*"}])
        assert len(pgs) == 0
        specs = [{"user":"carlson", "location":[loc],
                  "executable":"test_bb_script",
                  "stdout":"test_bb_script_stdout"} for loc in names]
        pg_added = self.bb.add_process_groups(specs)
        assert len(pg_added) == len(names)
        pgs = self.bb.get_process_groups([{"id":"*"}])
        assert len(pgs) == len(names)
        resources = self.bb.get_resources([{"name":"*"}])
        assert len(resources) == len(names)
        for res in resources:
            res.state = "busy"
        count = 0
        while True:
            done = True
            PGs = self.bb.get_process_groups([{"state":"running"}])
            for pg in PGs:
                if pg.building_nodes or pg.pinging_nodes:
                    done = False
            if not done:
                time.sleep(2)
                if count < len(names):
                    self.bb.node_done_building(names[count])
                    count = count + 1
                self.bb._check_builds_done()
            else:
                break
        while True:
            done = True
            PGs = self.bb.get_process_groups([{"state":"*"}])
            for pg in PGs:
                if not pg.head_pid:
                    done = False
            if not done:
                time.sleep(2)
            else:
                break
        count = 0
        while True:
            if count < 5:
                time.sleep(2)
                count = count + 1
            else:
                break
        self.bb.signal_process_groups([{"id":"*"}], "SIGINT")
        time.sleep(3)
        pgs = self.bb.get_process_groups([{"id":"*", "state":"*"}])
        assert len(pgs) == len(names)
        for pg in pgs:
            assert pg.state == "terminated"
        self.bb.wait_process_groups([{"id":"*", "state":"terminated"}])
        pgs = self.bb.get_process_groups([{"id":"*"}])
        assert len(pgs) == 0
        resources = self.bb.get_resources([{"name":"*"}])
        assert len(resources) == len(names)
        for res in resources:
            assert res.state == "idle"

    def test_node_done_building(self):
        """Tests the method node_done_building()"""
        self.setup()
        specs = [{"name":"test", "attributes":{"action":"build-default"}}]
        self.bb.add_resources(specs)
        self.bb.node_done_building("test")
        test = self.bb.get_resources([{"name":"test"}])
        assert test[0].attributes["action"] == "boot-default"
