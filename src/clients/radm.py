#!/usr/bin/env python

"""Radm can manage the resources in the system (add, modify, remove, etc)"""

import sys, optparse

from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError

if __name__ == "__main__":
    p = optparse.OptionParser(usage="%prog [options] r1 r2 ... rN")
    p.add_option("--add", action="store_true", dest="add",
                 help="add resources named r1, r2, etc")
    p.add_option("--remove", action="store_true", dest="remove",
                 help="remove resources named r1, r2, etc")
    p.add_option("--func", action="store_true", dest="func",
                 help="mark r1, r2, etc as functional")
    p.add_option("--nonfunc", action="store_true", dest="nonfunc",
                 help="mark r1, r2, etc as non-functional")
    p.add_option("--sched", action="store_true", dest="sched",
                 help="mark r1, r2, etc as schedulable")    
    p.add_option("--nonsched", action="store_true", dest="nonsched",
                 help="mark r1, r2, etc as non-schedulable")
    p.add_option("--attr", action="store", dest="attr",
                 help="set other attributes of r1, r2, etc to ATTR" + \
                     "(enter ATTR as \"key1:val1 key2:val2 key3:val3 etc\")")
    p.add_option("--queue", action="store", dest="queue",
                 help="set r1, r2, etc queues to QUEUE")
    p.add_option("--state", action="store", dest="state",
                 help="Set r1, r2, etc states to STATE (idle, busy, blocked)")

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit()

    opt, args = p.parse_args()

    try:
        system = ComponentProxy("system", defer=False)
    except ComponentLookupError:
        print >> sys.stderr, "failed to connect to system component"
        sys.exit(1)

    if opt.add and opt.remove:
        print >> sys.stderr, "--add and --remove can't be used toegether"
        sys.exit(1)

    if opt.func and opt.nonfunc:
        print >> sys.stderr, "--func and --nonfunc can't be used together"
        sys.exit(1)

    if opt.sched and opt.nonsched:
        print >> sys.stderr, "--sched and --nonsched can't be used together"
        sys.exit(1)

    def namesort(resource):
        """Helper function to sort by resource name"""
        return resource["name"]

    # Adding/Removing are single operations (can't set attributes at same time)
    if opt.add:
        if len(args) == 0:
            print >> sys.stderr, "Must specify at least one resource name"
            sys.exit(1)
        specs = [{"name":name} for name in args]
        added = system.add_resources(specs)
        added.sort(key=namesort)
        if added == "KeyError":
            print >> sys.stderr, "One or more of the given names already exist"
            sys.exit(1)
        for r in added:
            print "Added resource with name '%s'" % r["name"]
        sys.exit(0)
    elif opt.remove:
        specs = [{"name":name} for name in args]
        removed = system.remove_resources(specs)
        removed.sort(key=namesort)
        for r in removed:
            print "Removed resource with name '%s'" % r["name"]
        sys.exit(0)

    # May change multiple attributes at a time
    if opt.func:
        specs = [{"name":name, "functional":False} for name in args]
        newattrs = {"functional":True}
        changed = system.set_attributes(specs, newattrs)
        changed.sort(key=namesort)
        print "Resources marked functional:"
        for r in changed:
            print "    %s" % r["name"]
    elif opt.nonfunc:
        specs = [{"name":name, "functional":True} for name in args]
        newattrs = {"functional":False}
        changed = system.set_attributes(specs, newattrs)
        changed.sort(key=namesort)
        print "Resources marked non-functional:"
        for r in changed:
            print "    %s" % r["name"]

    if opt.sched:
        specs = [{"name":name, "scheduled":False} for name in args]
        newattrs = {"scheduled":True}
        changed = system.set_attributes(specs, newattrs)
        changed.sort(key=namesort)
        print "Resources marked as schedulable:"
        for r in changed:
            print "    %s" % r["name"]
    elif opt.nonsched:
        specs = [{"name":name, "scheduled":True} for name in args]
        newattrs = {"scheduled":False}
        changed = system.set_attributes(specs, newattrs)
        changed.sort(key=namesort)
        print "Resources marked as non-schedulable:"
        for r in changed:
            print "    %s" % r["name"]
    
    if opt.queue:
        specs = [{"name":name} for name in args]
        newattrs = {"queue":opt.queue}
        changed = system.set_attributes(specs, newattrs)
        changed.sort(key=namesort)
        print "Resources with changed queues:"
        for r in changed:
            print "    %s" % r["name"]

    if opt.state:
        if not (opt.state == "idle" or opt.state == "busy" \
                    or opt.state == "blocked"):
            print "STATE must be 'idle', 'busy', or 'blocked'"
            sys.exit(1)
        specs = [{"name":name} for name in args]
        newattrs = {"state":opt.state}
        changed = system.set_attributes(specs, newattrs)
        changed.sort(key=namesort)
        print "Resources with changed state:"
        for r in changed:
            print "    %s" % r["name"]
    
    # Handle opt.attr
    if opt.attr != None:
        attr = opt.attr.split()
        attrdict = {}
        for a in attr:
            try:
                key, val = a.split(":")
            except ValueError:
                print >> sys.stderr, "Attributes not formatted correctly"
                sys.exit(1)
            attrdict[key] = val
        specs = [{"name":name} for name in args]
        newattrs = {"attributes":attrdict}
        changed = system.set_attributes(specs, newattrs)
        changed.sort(key=namesort)
        print "Resources with changed attributes:"
        for r in changed:
            print "    %s" % r["name"]
