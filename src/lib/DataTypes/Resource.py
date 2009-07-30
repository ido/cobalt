"""Contains the Resource and ResourceDict Data Types"""

__revision__ = "$Revision$"



from Cobalt.Data import Data, DataDict



class Resource(Data):
    """A resource unit for a system
    
    Attributes:
    tag -- defines what this Data object is (default "Resource")
    functional -- Whether the resource is functional (default False)
    name -- canonical name
    queue -- Name of the queue which this resource is in (default "default")
    scheduled -- Whether the resource can be scheduled on (default False)
    size -- The size of the resource (depends on system type)
    state -- "idle", "busy", or "blocked"
    attributes -- a dictionary of other attributes of this resource
    """

    fields = Data.fields + ["functional", "name", "queue", "scheduled",
                            "size", "state", "attributes"]

    required = Data.required + ["name"]

    def __init__(self, spec):
        Data.__init__(self, spec)
        self.tag = "Resource"
        self.functional = spec.get("functional", False)
        self.name = spec.get("name", None)
        self.queue = spec.get("queue", "default")
        self.scheduled = spec.get("scheduled", False)
        self.size = 1
        self.state = spec.get("state", "idle")
        self.attributes = spec.get("attributes", {})

    def match_attributes(self, attrs):
        """Returns true if the 'attributes' attribute of the resource
        contains the provided attributes in 'attrs' (a dictionary)"""
        for key, val in attrs.iteritems():
            if not key in self.attributes or self.attributes[key] != val:
                return False
        return True



class ResourceDict(DataDict):
    """A container for resources, keyed by name"""

    item_cls = Resource
    key = "name"

    def get_attr_matched_resources(self, specs, attrs):
        """Get those resources that have matching specs, including
        matching attrs to the other "attributes" attribute

        Arguments:
        specs -- list of dictionaries with details of resource to match
        attrs -- dictionary with other "attributes" resource must match

        Returns a list of resources that matched specs and attrs"""
        resources = self.q_get(specs)
        for r in resources[:]:
            if not r.match_attributes(attrs):
                resources.remove(r)
        return resources
