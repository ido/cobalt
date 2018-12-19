#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

'''Cobalt queue converter script'''
__revision__ = '$Revision: 313 $'

__helpmsg__ ="""This script converts scheduler data to the 0.97.0 format, and is
intended to be run after installing 0.97. It takes no arguments, and
makes a backup copy of the old bgsched data in
'/var/spool/cobalt/bgsched.save' and saves the new bgsched data in
'/var/spool/cobalt/bgsched'.

If you installed bgsched.py in a location other than '/usr/sbin', then you
will need to modify line 25 of this script to reflect the location of
cqm.py.

Make sure there are no jobs running in the queue before you run this
script."""

import sys, cPickle, shutil

if '-h' in sys.argv or '--help' in sys.argv:
    print __helpmsg__
    raise SystemExit, 1

sys.path.append('/usr/sbin')
try:
    from bgsched import Partition, PartitionSet, Job
except Exception, msg:
    print '''Cannot find bgsched.py. Please specify the directory where bgsched.py can
be found in line 25 of this script, or in your $PYTHONPATH.'''
    print msg
    raise SystemExit, 1

if __name__ == '__main__':
    # make backup of old pickle
    shutil.copyfile('/var/spool/cobalt/bgsched', '/var/spool/cobalt/bgsched.save')

    partitions = cPickle.loads(open('/var/spool/cobalt/bgsched').read())[0]

    jobs = []
    savedata = tuple([partitions, jobs])
    cPickle.dump(savedata, open('/var/spool/cobalt/bgsched', 'w'))
