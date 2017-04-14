#!/usr/bin/env python2.7

import sys
import ast
AVAILABLE_MCDRAM = ['cache', 'equal', 'split', 'flat']
AVAILABLE_NUMA = ['a2a', 'snc2', 'snc4', 'hemi', 'quad']

PRESET_QUEUES = {'debug-flat-quad': ('flat', 'quad'),
                 'debug-cache-quad': ('cache', 'quad'),
                }


def main():

    attrs = {}
    mcdram = None
    numa = None
    queue = None
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
            attrs = attr_dict
        elif key == 'queue':
            if val in PRESET_QUEUES.keys():
                mcdram = PRESET_QUEUES[val][0]
                numa = PRESET_QUEUES[val][1]
                queue = val
        else:
            pass

    if mcdram is not None and numa is not None:
        attrs['mcdram'] = mcdram
        attrs['numa'] = numa
        print >> sys.stderr, "Memory mode set to %s %s for queue %s" % (mcdram, numa, queue)
        print "attrs=%s" % attrs

    return 0

if __name__ == '__main__':
   sys.exit(main())
