#!/usr/bin/env python2.7

import sys
import ast
AVAILABLE_MCDRAM = ['cache', 'hybrid', 'half', 'flat']
AVAILABLE_NUMA = ['a2a', 'snc2', 'snc4', 'hemi', 'quad']

def main():

    for arg in sys.argv:
        try:
            splitarg = arg.split('=')
            key = splitarg[0]
            val = '='.join(splitarg[1:])
        except (IndexError, ValueError, TypeError):
            print >> sys.stderr, "Missing or badly formatted args."
            return 1
        if key == 'attrs':
            attr_dict = ast.literal_eval(val)
            for akey, aval in attr_dict.items():
                if akey == 'mcdram':
                    if not  aval.lower() in AVAILABLE_MCDRAM:
                        print >> sys.stderr, "%s is an invalid MCDRAM mode" % aval
                        return 1
                elif akey == 'numa':
                    if not aval.lower() in AVAILABLE_NUMA:
                        print >> sys.stderr, "%s is an invalid NUMA mode" % aval
                        return 1
                else:
                    pass
        else:
            pass

    return 0

if __name__ == '__main__':
   sys.exit(main())
