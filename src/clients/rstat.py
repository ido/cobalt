#!/usr/bin/env python
"""Prints out information about the resources"""

import sys
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

if __name__ == "__main__":
    try:
        system = ComponentProxy("system", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "failed to connect to system component"
        sys.exit(1)

    specs = [{"name":"*", "functional":"*", "scheduled":"*", "state":"*",
              "queue":"*", "attributes":"*"}]
    status = system.get_resources(specs)

    header = [['Name', 'Queue', 'State', 'Attributes']]
    #build output list
    output = []
    def namesort(item):
        """Helper function to sort resources by name"""
        return item["name"]
    status.sort(key=namesort)
    for resource in status:
        if resource["functional"]:
            if resource["scheduled"]:
                state = resource["state"]
            else:
                state = "non-schedulable"
        else:
            state = "non-functional"
        output.append([resource["name"], resource["queue"], state,
                       resource["attributes"]])
    Cobalt.Util.printTabular(header + output)
