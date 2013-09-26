#!/usr/bin/env python

import sys
import os
import optparse
import errno

class ExtendOptions(optparse.Option):
    '''extend optparse to handle concatinating options.'''

    ACTIONS = optparse.Option.ACTIONS + ('extend',)
    STORE_ACTIONS = optparse.Option.STORE_ACTIONS + ('extend',)
    TYPED_ACTIONS = optparse.Option.TYPED_ACTIONS + ('extend',)
    ALWAYS_TYPED_ACTIONS = optparse.Option.ALWAYS_TYPED_ACTIONS + ('extend',)

    def take_action(self, action, dest, opt, value, values, parser):
        if action == 'extend':
            values.ensure_value(dest, []).append(value)
        else:
            optparse.Option.take_action(self, action, dest, opt, value, values, parser)

def main():
    p = optparse.OptionParser(option_class=ExtendOptions)

    p.add_option("--cwd", action="store", dest="cwd", help="current working directory to use")
    p.add_option("--jobid", action="store", dest="jobid", help="jobid")
    p.add_option("--nf", action="store", dest="nodefile", help="nodefile")
    p.add_option("--env", action="extend", dest="envs", help="environment variables")

    if len(sys.argv) == 1:
        p.print_help()
        sys.exit(1)

    p.disable_interspersed_args()
    opt, args = p.parse_args()

    os.environ['COBALT_JOBID'] = opt.jobid
    os.environ['COBALT_NODEFILE'] = opt.nodefile
    if opt.envs is not None:
        for pair in opt.envs:
            key = pair.split('=')[0]
            val = '='.join(pair.split('=')[1:])
            os.environ[key] = val

    os.chdir(opt.cwd)

    #assume rest of args are to go to the executable and have the user script deal with it
    arg_tuple = tuple(args)

    try:
        os.execvpe(arg_tuple[0], arg_tuple, os.environ)
    except OSError, exc:
        print >> sys.stderr, str(exc)
        if exc.errno in [errno.EACCES, errno.EPERM]:
            sys.exit(126)
        elif exc.errno in [errno.ENOENT]:
            sys.exit(127)
        else:
            sys.exit(1)

    # We somehow got past an exec!?
    print >> sys.stderr, "Exec bypassed!? Exiting now!"
    sys.exit(1)


if __name__ == '__main__':
    main()
