"""Test cases for the BBSystem component"""
from Cobalt.Components.bb import BBSystem

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
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == 0
        self.bb.add_resources(
            [{"name":"bb01", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":2}},
             {"name":"bb02", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":2}},
             {"name":"bb03", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":2}},
             {"name":"bb04", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":2}},
             {"name":"bb05", "functional":True, "scheduled":True,
              "attributes":{"speed":"slow", "NumProc":2}},
             {"name":"bb06", "functional":True, "scheduled":True,
              "attributes":{"speed":"slow", "NumProc":2}},
             {"name":"bb07", "functional":True, "scheduled":True},
             {"name":"bb08", "functional":True, "scheduled":True},
             {"name":"bb09", "functional":True, "scheduled":True,
              "attributes":{"speed":"slow", "NumProc":4}},
             {"name":"bb10", "functional":True, "scheduled":True,
              "attributes":{"speed":"slow", "NumProc":4}},
             {"name":"bb11", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":4}},
             {"name":"bb12", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast", "NumProc":4}},
             {"name":"bb13", "functional":True, "scheduled":True},
             {"name":"bb14", "functional":True, "scheduled":True},
             {"name":"bb15", "functional":True, "scheduled":True,
              "attributes":{"NumProc":4}},
             {"name":"bb16", "functional":True, "scheduled":True,
              "attributes":{"speed":"fast"}}]
            )
        num_resources = self.bb.get_resources([{"name":"*"}])
        assert len(num_resources) == 16

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

    def test_set_attributes(self):
        """Tests the component method set_attributes()"""
        specs = [{"name":"bb13"}, {"name":"bb14"}]
        newattrs = {"attrTrue":True, "attrFalse":False, "attrInt":1013}
        self.bb.set_attributes(specs, newattrs)
        resources = self.bb.get_resources([{"name":"bb13"}, {"name":"bb14"}])
        for r in resources:
            assert r.attrTrue == True
            assert r.attrFalse == False
            assert r.attrInt == 1013
