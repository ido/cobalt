'''Utility funtions for Cobalt programs'''
__revision__ = '$Revision$'

import os
import types
import smtplib
import socket
import time
import ConfigParser
import popen2
from datetime import date, datetime
from getopt import getopt, GetoptError
import logging

import Cobalt

logger = logging.getLogger('Util')

def dgetopt(arglist, opt, vopt, msg):
    '''parse options into a dictionary'''
    ret = {}
    for optname in opt.values() + vopt.values():
        ret[optname] = False
    gstr = "".join(opt.keys()) + "".join([longopt+':' for longopt in vopt.keys()])
    gstr += 'C:'
    try:
        (opts, args) = getopt(arglist, gstr)
    except GetoptError, gerr:
        print gerr
        print msg
        raise SystemExit, 1
    for (gopt, garg) in opts:
        option = gopt[1:]
        if opt.has_key(option):
            ret[opt[option]] = True
        elif option == 'C':
            contine
        else:
            ret[vopt[option]] = garg
    return ret, list(args)

def dgetopt_long(arglist, opt, vopt, msg):
    '''parse options into a dictionary, long and short options supported'''
    ret = {}
    for optname in opt.values() + vopt.values():
        ret[optname] = False
    long_opts = []
    gstr = ''

    # options that don't require args
    for o in opt.keys():
        if len(o) > 1:
            long_opts.append(o)
        else:
            gstr = gstr + o
    # options that require args
    for o in vopt.keys():
        if len(o) > 1:
            long_opts.append(o + '=')
        else:
            gstr = gstr + o + ':'

    gstr += 'C:'
    try:
        (opts, args) = getopt(arglist, gstr, long_opts)
    except GetoptError, gerr:
        print gerr
        print msg
        raise SystemExit, 1

    for (gopt, garg) in opts:
        option = gopt.split('-')[-1]
        if opt.has_key(option):
            ret[opt[option]] = True
        elif option == 'C':
            continue
        else:
            ret[vopt[option]] = garg

    return ret, list(args)

def print_vertical(rows):
    '''print data in horizontal format'''
    hmax = max([len(str(x)) for x in rows[0]])
    hformat = '    %%-%ds: %s' % (hmax+1, '%s')
    for row in rows[1:]:
        for x in range(len(row)):
            if x == 0:
                print "%s: %s" % (rows[0][x], row[x])
            else:
                print hformat % (rows[0][x], row[x])
        print

def print_tabular(rows):
    '''print data in tabular format'''
    cmax = tuple([-1 * max([len(str(row[index])) for row in rows]) for index in xrange(len(rows[0]))])
    fstring = ("%%%ss  " * len(cmax)) % cmax
    print fstring % rows[0]
    print ((-1 * sum(cmax))  + (len(cmax) * 2)) * '='
    for row in rows[1:]:
        try:
            print fstring % row
        except IOError:
            return

def printTabular(rows, centered = []):
    '''print data in tabular format'''
    for row in rows:
        for index in xrange(len(row)):
            if isinstance(row[index], types.BooleanType):
                if row[index]:
                    row[index] = 'X'
                else:
                    row[index] = ''
    total = 0
    for column in xrange(len(rows[0])):
        width = max([len(str(row[column])) for row in rows])
        for row in rows:
            if column in centered:
                row[column] = row[column].center(width)
            else:
                row[column] = str(row[column]).ljust(width)
        total += width + 2
    try:
        print '  '.join(rows[0])
        print total * '='
        for row in rows[1:]:
            print '  '.join(row)
    except IOError:
        return

def print_dtab(dtab, fields = []):
    '''print dictionary data in tabular format'''
    if not fields:
        fields = dtab[0].keys()
    fieldlen = [(field, max([len(str(drow[field])) for drow in dtab] + [len(field)])) for field in fields]
    fstring = ''
    for key, value in fieldlen:
        fstring += '%%(%s)%ss  ' % (key, (-1 * value))
    header = "".join([("%" + str(value) + "s  ")%(key) for key, value in fieldlen])
    print header
    print (sum([value for key, value in fieldlen]) + (2 * len(fieldlen))) * '='
    for drow in dtab:
        print fstring % drow

def buildRackTopology(partlist):
    '''Build a dict of partition -> (parents, children)'''
    partinfo = {}
    partport = {}
    for part in partlist:
        partport[part['name']] = part
        partinfo[part['name']] = ([], [])
    for part in partlist:
        parents = [ppart['name'] for ppart in partlist if part['name'] in ppart['deps']]
        while parents:
            next = parents.pop()
            partinfo[part['name']][0].append(next)
            ndp = [ppart['name'] for ppart in partlist if next in ppart['deps']]
            parents += ndp
        children = part['deps'][:]  # copy because popping this below would
                                    # clear the deps list, and all children
                                    # are not added properly
        while children:
            next = children.pop()
            partinfo[part['name']][1].append(next)
            children += partport[next]['deps']
    return partinfo

def sendemail(toaddr, subj, msg, smtpserver = 'localhost'):
    '''Sends an email'''
    msgstr = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % ('cobalt@%s' % socket.getfqdn(), (',').join(toaddr), subj))
    try:
        server = smtplib.SMTP(smtpserver)
    except Exception, e:
        print "Problem sending mail", e
        return
    try:
        server.sendmail('cobalt@%s' % socket.getfqdn(), toaddr, msgstr + msg)
    except Exception, msg:
        print 'Problem sending mail', msg
    server.quit()
    
def runcommand(cmd):
    '''Execute command, returning rc, stdout, stderr'''
    cmdp = popen2.Popen3(cmd, True)
    out = []
    err = []
    status = cmdp.wait()
    out += cmdp.fromchild.readlines()
    err += cmdp.childerr.readlines()
    return (status, out, err)

class AccountingLog:
    def __init__(self, name):
        CP = ConfigParser.ConfigParser()
        CP.read(Cobalt.CONFIG_FILES)
        try:
            self.logdir = CP.get('cqm', 'log_dir')
        except ConfigParser.NoOptionError:
            self.logdir = '/var/log/cobalt-accounting'
        self.date = None
        self.logfile = open('/dev/null', 'w+')
        self.name = name
    def RotateLog(self):
        if self.date != time.localtime()[:3]:
            self.date = time.localtime()[:3]
            date_string = "%s_%02d_%02d" % self.date
            logfile = "%s/%s-%s.log" % (self.logdir, self.name, date_string)
            try:
                self.logfile = open(logfile, 'a+')
            except IOError:
                self.logfile = open("/dev/null", 'a+')
    def LogMessage(self, message):
        self.RotateLog()
        timenow = time.strftime("%Y-%m-%d %T", time.localtime())
        self.logfile.write("%s %s\n" % (timenow, message))
        self.logfile.flush()

class FailureMode(object):
    '''FailureModes are used to report (and supress) errors appropriately
    call Pass() on success and Fail() on error'''
    def __init__(self, name):
        self.name = name
        self.status = True

    def Pass(self):
        '''Check if status was previously failure and report OK status if needed'''
        if not self.status:
            logger.error("Failure %s cleared" % (self.name))
            self.status = True

    def Fail(self):
        '''Check if status was previously success and report failed status if needed'''
        if self.status:
            logger.error("Failure %s occured" % (self.name))
            self.status = False

class PBSLog (object):
    
    """Manage a log using the PBS accounting log file format.
    
    Properties:
    logfile -- The (open) file to log messages to.
        
    For more information see section 10.3 of the PBS Pro. 7 Admin Guide.
    """
    
    def __init__ (self, id_string=None):
        """Initialize a new PBS-style log generator."""
        self.id_string = id_string
        # Get the log directory from a config file.
        config = ConfigParser.ConfigParser()
        config.read(Cobalt.CONFIG_FILES)
        try:
            self.logdir = config.get('cqm', 'log_dir')
        except ConfigParser.NoOptionError:
            self.logdir = "/var/log/cobalt-accounting"
        # The date of the last log entry.
        self._last_date = None
        # The active (open) log file.
        self._last_file = None
    
    def _get_logfile (self):
        """Return an appropriate open file for logging."""
        if self._last_date == date.today():
            # The date has not changed, so reuse
            # the previous file.
            return self._last_file
        else:
            # The date has changed, so open a new
            # file.
            self._last_date = date.today()
            format = "%Y%m%d" # ccyymmdd
            filename = os.path.join(
                self.logdir,
                self._last_date.strftime(format),
            )
            try:
                self._last_file = open(filename, "a")
            except IOError:
                self._last_file = open("/dev/null", "a")
            return self._last_file
    logfile = property(_get_logfile)
    
    def reset (self):
        """Reset the open log file."""
        self._last_date = None
        self._last_file = None
    
    def _prep_key (self, key):
        # replace __dot__ with '.'
        key = str(key)
        key = key.replace("__dot__", ".")
        return key
    
    def _prep_value (self, value):
        # automatically quote values containing spaces
        if " " in str(value):
            value = '"%s"' % value
        return value
    
    def log (self, record_type, id_string=None, datetime=datetime.now, **messages):
        
        """Add a log entry.
        
        Arguments:
        id_string -- The job, reservation, or reservation-job identifier. (default self.id_string)
        record_type -- A single character indicating the type of record.
        
        Keyword arguments:
        datetime -- Either a datetime, or a callable that returns a datetime. (default datetime.now)
        
        Additional keyword arguments may be specified to set messages.
        """
        
        try:
            datetime = datetime()
        except:
            pass # assume datetime is already a datetime
        format = "%m/%d/%Y %H:%M:%S" # mm/dd/ccyy hh:mm:ss
        
        assert record_type in ("A", "B", "C", "D", "E", "F", "K",
                               "k", "Q", "R", "S", "T", "U", "Y")
        
        assert id_string or self.id_string
        
        message_text = " ".join([
            "%s=%s" % (self._prep_key(key), self._prep_value(value))
            for key, value in messages.iteritems()
        ])
        
        self.logfile.write("%s;%s;%s;%s\n" % (
            datetime.strftime(format),
            record_type,
            id_string or self.id_string,
            message_text,
        ))
        
        self.logfile.flush()
