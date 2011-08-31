#!/usr/bin/env python

"""Tests the pm functions"""

import optparse
import sys
import Cobalt
import Cobalt.Util
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

if __name__ == "__main__":
    p = optparse.OptionParser(usage="%prog [--wait]")
    p.add_option("--wait", action="store_true", dest="wait",
                 help="Wait on terminated processes")
    opt, args = p.parse_args()

    try:
        pm = ComponentProxy("system", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "Failed to connect to system"
        raise SystemExit(1)
    if opt.wait:
        pm.wait_process_groups([{"state":"terminated"}])
    pgroups = pm.get_process_groups([{"id":"*", "user":"*", "state":"*", "location":"*"}])
    header = [['Id', 'User', 'State', 'Location']]
    # build output list
    output = []
    for pg in pgroups:
        output.append([pg["id"], pg["user"], pg["state"], pg["location"]])
    Cobalt.Util.printTabular(header + output)
