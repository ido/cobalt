#!/usr/bin/env python

import ConfigParser, glob, re, math, datetime
import Cobalt.Util

# get current day
current_day = datetime.date.today().strftime("%Y-%m-%d")

done_re = re.compile("(?P<time>"+current_day+" \d+:\d+:\d+),\d{,3};Job (?P<jobid>\d+)/(?P<user>\w+) on (?P<nodes>\d+) nodes done. queue:(?P<queuetime>\d+\.\d+)s user:(?P<usertime>\d+\.\d+)s*")

_config = ConfigParser.ConfigParser()

_config.read('/etc/cobalt.conf')

cqm_section = _config._sections['cqm']

logfiles = glob.glob(cqm_section['log_dir']+'/*')

logfiles.sort()
logfiles.reverse()

output = []

thefile = open(logfiles[0], 'r')
for line in thefile:
    p = done_re.match(line)
    if p:
        # format usertime
        minutes, seconds = divmod(float(p.group('usertime')), 60)
        hours, minutes = divmod(minutes, 60)
        usertime = "%02d:%02d:%02d" % (hours, minutes, seconds)

        # format queuetime
        minutes, seconds = divmod(float(p.group('queuetime')), 60)
        hours, minutes = divmod(minutes, 60)
        queuetime = "%02d:%02d:%02d" % (hours, minutes, seconds)

        output.append([p.group('time'), p.group('jobid'), p.group('user'), \
                       p.group('nodes'), queuetime, usertime])

thefile.close()

header = [['Time completed', 'JobID', 'User', 'Nodes', 'QueueTime', 'RunTime']]

uniqified = []

for line in output:
    if uniqified.count(line) == 0:
        uniqified.append(line)

Cobalt.Util.print_tabular([tuple(x) for x in header + uniqified])
