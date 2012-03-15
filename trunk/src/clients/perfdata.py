#!/usr/bin/env python

import sys

import Cobalt.Logging
from Cobalt.Proxy import ComponentProxy
from Cobalt.Exceptions import ComponentLookupError
from Cobalt.Util import print_tabular

if __name__ == '__main__':
    components = sys.argv[1:]
    to_print = [('Name', 'Min', 'Max', 'Mean')]
    for component in components:
        c = ComponentProxy(component, defer=False)
        data = c.get_statistics()
        for key, value in data.iteritems():
            to_print.append(("%s.%s" % (component, key), ) + tuple(value))
    print_tabular(to_print)

