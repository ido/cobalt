#!/usr/bin/env python

import ConfigParser, glob, re, math, datetime, sys, time, getopt
import Cobalt.Util


if __name__ == '__main__':
    (opts, command) = Cobalt.Util.dgetopt(sys.argv[1:], {'f':'full'}, {'d':'days'},
                                          "Usage: cqhist [-d days] [-f]")
    if not opts['days']:
        opts['days'] = 1
    # get day range
    day_range = [time.strftime("%Y-%m-%d", time.localtime(int(time.time() - d*24*3600))) for d in range(int(opts['days']))]
    day_range = '(' + '|'.join(day_range) + ')'

    # setup regex's
    user_re = "(?P<user>\w+)"
    jobid_re = "(?P<jobid>\d+)"
    location_re = "(?P<location>\S+)"

    done_re = re.compile("(?P<time>" + day_range + " \d+:\d+:\d+),\d{,3};Job " + \
                         jobid_re + "/" + user_re + " on (?P<nodes>\d+) nodes done. queue:(?P<queuetime>\d+\.\d+)s user:(?P<usertime>\d+\.\d+)s*")
    start_re = re.compile("(?P<time>" + day_range + " \d+:\d+:\d+),\d{,3};S;(?P<jobid>\d+);" + \
                          user_re + ";" + location_re + ";(\d+);(?P<nodes>\d+);(?P<processors>\d+);(?P<mode>\w+);(?P<walltime>\d+)")
    run_re = re.compile("(?P<time>" + day_range + " \d+:\d+:\d+),\d{,3};Job " + \
                        jobid_re + "/" + user_re + "/Q:" + "(?P<queue>\w+): Running job on " + location_re)

    _config = ConfigParser.ConfigParser()
    _config.read('/etc/cobalt.conf')
    cqm_section = _config._sections['cqm']

    logfiles = glob.glob(cqm_section['log_dir'] + '/cqm*.log')
    logfiles.sort()
    #logfiles.reverse()  # put most recent log first

    rundict = {}
    donedict = {}
    startdict = {}

    output = []

    for logfile in logfiles:
        thefile = open(logfile, 'r')
        for line in thefile:
            d = done_re.match(line)
            if d:
                # format usertime
                minutes, seconds = divmod(float(d.group('usertime')), 60)
                hours, minutes = divmod(minutes, 60)
                usertime = "%02d:%02d:%02d" % (hours, minutes, seconds)

                # format queuetime
                minutes, seconds = divmod(float(d.group('queuetime')), 60)
                hours, minutes = divmod(minutes, 60)
                queuetime = "%02d:%02d:%02d" % (hours, minutes, seconds)
                output.append([d.group('time'), d.group('jobid'), d.group('user'),
                               d.group('nodes'), queuetime, usertime])

            r = run_re.match(line)
            if r:
                rundict.update({r.group('jobid'):{ 'queue':r.group('queue'),
                                                   'location':r.group('location') } })

            s = start_re.match(line)
            if s:
                startdict.update({s.group('jobid'):{ 'processors':s.group('processors'),
                                                     'nodes':s.group('nodes'), 'mode':s.group('mode'),
                                                     'walltime':s.group('walltime') } })

        thefile.close()

    uniqified = []

    for line in range( len(output) ):

        jobid = output[line][1]

        if '-f' in sys.argv:
            if rundict.has_key(jobid):
                output[line] = output[line] + [rundict[jobid]['location']]
            else:
                output[line] = output[line] + ['-']

        if '-f' in sys.argv:
            if startdict.has_key(jobid):
                output[line] = output[line] + [ startdict[jobid]['processors'],
                                            startdict[jobid]['mode'] ]
            else:
                output[line] = output[line] + ['-', '-']

    for line in output:
        if uniqified.count(line) == 0:
            uniqified.append(line)

    if '-f' in sys.argv:
        header = [['Time completed', 'JobID', 'User', 'Nodes', \
                   'QueueTime', 'RunTime', 'Location', 'Proc', 'Mode']]
    else:
        header = [['Time completed', 'JobID', 'User', 'Nodes', 'QueueTime', 'RunTime']]

    Cobalt.Util.print_tabular([tuple(x) for x in header + uniqified])
