'''Bcfg2 logging support'''
__revision__ = '$Revision$'

# import lxml.etree
import copy
import fcntl
import logging
import logging.handlers
import math
import os.path
import socket
import struct
import os
import sys
import termios
import types
import linecache
import Cobalt
import ConfigParser
import threading
import time
import Queue
import traceback

import Cobalt.JSONEncoders
import Cobalt.Proxy
from Cobalt.Exceptions import ComponentLookupError



SYSLOG_LEVEL_DEFAULT = "DEBUG"
CONSOLE_LEVEL_DEFAULT = "INFO"

LOGGING_LEVELS = {
    "DEBUG" : logging.DEBUG,
    "INFO" : logging.INFO,
    "WARNING" : logging.WARNING,
    "ERROR" : logging.ERROR,
    "CRITICAL" : logging.CRITICAL,
    }

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
try:
    TO_CONSOLE = config.get('logger', 'to_console').lower()
    if TO_CONSOLE == "false" or TO_CONSOLE == "0":
        TO_CONSOLE = False
    else:
        TO_CONSOLE = True
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
    TO_CONSOLE = True
try:
    CONSOLE_LEVEL = config.get('logger', 'console_level').upper()
    if LOGGING_LEVELS.has_key(CONSOLE_LEVEL):
        CONSOLE_LEVEL = LOGGING_LEVELS[CONSOLE_LEVEL]
    else:
        CONSOLE_LEVEL = int(CONSOLE_LEVEL)
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
    CONSOLE_LEVEL = LOGGING_LEVELS[CONSOLE_LEVEL_DEFAULT]
except ValueError:
    print >>sys.stderr, "set for console_level, \"%s\", is not valid; setting level to %s" % (CONSOLE_LEVEL, CONSOLE_LEVEL_DEFAULT)
    CONSOLE_LEVEL = LOGGING_LEVELS[CONSOLE_LEVEL_DEFAULT]
try:
    TO_SYSLOG = config.get('logger', 'to_syslog').lower()
    if TO_SYSLOG == "false" or TO_SYSLOG == "0":
        TO_SYSLOG = False
    else:
        TO_SYSLOG = True
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
    TO_SYSLOG = True
try:
    SYSLOG_LEVEL = config.get('logger', 'syslog_level').upper()
    if LOGGING_LEVELS.has_key(SYSLOG_LEVEL):
        SYSLOG_LEVEL = LOGGING_LEVELS[SYSLOG_LEVEL]
    else:
        SYSLOG_LEVEL = int(SYSLOG_LEVEL)
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
    SYSLOG_LEVEL = LOGGING_LEVELS[SYSLOG_LEVEL_DEFAULT]
except ValueError:
    print >>sys.stderr, "set for syslog_level, \"%s\", is not valid; setting level to %s" % (SYSLOG_LEVEL, SYSLOG_LEVEL_DEFAULT)
    SYSLOG_LEVEL = LOGGING_LEVELS[SYSLOG_LEVEL_DEFAULT]
try:
    SYSLOG_LOCATION = os.path.expandvars(config.get('logger', 'syslog_location'))
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
    SYSLOG_LOCATION = "/dev/log"
try:
    SYSLOG_FACILITY = config.get('logger', 'syslog_facility')
except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
    SYSLOG_FACILITY = "local0"

def print_attributes(attrib):
    ''' Add the attributes for an element'''
    return ' '.join(['%s="%s"' % data for data in attrib.iteritems()])

def print_text(text):
    ''' Add text to the output (which will need normalising '''
    charmap = {'<':'&lt;', '>':'&gt;', '&':'&amp;'}
    return ''.join([charmap.get(char, char) for char in text]) + '\n'
        
def xml_print(element, running_indent=0, indent=4):
    ''' Add an element and its children to the return string '''
    if (len(element.getchildren()) == 0) and (not element.text):
        ret = (' ' * running_indent)
        ret += '<%s %s/>\n' % (element.tag, print_attributes(element.attrib))
    else:
        child_indent = running_indent + indent
        ret = (' ' * running_indent)
        ret += '<%s%s>\n' % (element.tag, print_attributes(element))
        if element.text:                
            ret += (' '* child_indent) + print_text(element.text)
        for child in element.getchildren():
            ret += xml_print(child, child_indent, indent)
            ret += (' ' * running_indent) +  '</%s>\n' % (element.tag)
        if element.tail:
            ret += (' ' * child_indent) + print_text(element.tail)
    return ret

class TermiosFormatter(logging.Formatter):
    '''The termios formatter displays output in a terminal-sensitive fashion'''

    def __init__(self, fmt=None, datefmt=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        if sys.stdout.isatty():
            # now get termios info
            try:
                self.width = struct.unpack('hhhh', fcntl.ioctl(0, termios.TIOCGWINSZ,
                                                               "\000"*8))[1]
                if self.width == 0:
                    self.width = 80
            except:
                self.width = 80
        else:
            # output to a pipe
            self.width = 32768

    def format(self, record):
        '''format a record for display'''
        returns = []
        line_len = self.width
        if type(record.msg) in types.StringTypes:
            for line in logging.Formatter.format(self, record).split('\n'):
                if len(line) <= line_len:
                    returns.append(line)
                else:
                    inner_lines = int(math.floor(float(len(line)) / line_len))+1
                    for i in xrange(inner_lines):
                        returns.append("%s" % (line[i*line_len:(i+1)*line_len]))
        elif type(record.msg) == types.ListType:
            if not record.msg:
                return ''
            # getMessage() must be called so that arguments are substituted; eval() is used to turn the string back into a list
            msgdata = eval(record.getMessage())
            msgdata.sort()
            msgwidth = self.width
            columnWidth = max([len(str(item)) for item in msgdata])
            columns = int(math.floor(float(msgwidth) / (columnWidth+2)))
            lines = int(math.ceil(float(len(msgdata)) / columns))
            for lineNumber in xrange(lines):
                indices = [idx for idx in [(colNum * lines) + lineNumber
                                           for colNum in range(columns)] if idx < len(msgdata)]
                format = (len(indices) * (" %%-%ds " % columnWidth))
                returns.append(format % tuple([msgdata[idx] for idx in indices]))
        #elif type(record.msg) == lxml.etree._Element:
        #    returns.append(str(xml_print(record.msg)))
        else:
            returns.append(str(record.getMessage()))
        if record.exc_info:
            returns.append(self.formatException(record.exc_info))
        return '\n'.join(returns)

class FragmentingSysLogHandler(logging.handlers.SysLogHandler):
    '''This handler fragments messages into chunks smaller than 250 characters'''

    def __init__(self, procname, path, facility):
        self.procname = procname
        logging.handlers.SysLogHandler.__init__(self, path, facility)

    def emit(self, record):
        '''chunk and deliver records'''
        record.name = self.procname
        msgdata = record.getMessage()
        if len(msgdata) > 250:
            msgs = []
            error = record.exc_info
            record.exc_info = None
            while msgdata:
                newrec = copy.deepcopy(record)
                newrec.msg = msgdata[:250]
                newrec.args = ()
                msgs.insert(0,newrec)
                msgdata = msgdata[250:]
            msgs[0].exc_info = error
        else:
            msgs = [record]
        while msgs:
            newrec = msgs.pop()
            msg = self.log_format_string % (self.encodePriority(self.facility,
                                                                newrec.levelname.lower()), self.format(newrec))
            try:
                self.socket.send(msg)
            except socket.error:
                while True:
                    try:
                        if self.unixsocket:
                            self._connect_unixsocket(self.address)
                        else:
                            self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
                            self.socket.connect(self.address)
                        break
                    except socket.error:
                        continue
                    self.socket.send("Reconnected to syslog")
                    self.socket.send(msg)

def setup_logging(procname, to_console=TO_CONSOLE, to_syslog=TO_SYSLOG, syslog_facility=SYSLOG_FACILITY, level=0,
                  console_timestamp=False):
    '''setup logging for bcfg2 software'''
    if hasattr(logging, 'already_setup'):
        return 
    # add the handler to the root logger
    if to_console:
        log_to_stderr(logging.root, timestamp=console_timestamp)
    if to_syslog:
        try:
            syslog = FragmentingSysLogHandler(procname, SYSLOG_LOCATION, syslog_facility)
            syslog.setLevel(SYSLOG_LEVEL)
            syslog.setFormatter(logging.Formatter('%(name)s[%(process)d]: %(message)s'))
            logging.root.addHandler(syslog)
        except socket.error:
            logging.root.error("failed to activate syslogging")
    logging.root.setLevel(level)
    logging.already_setup = True

def trace_process (**kwargs):
    
    """Literally log every line of python code as it runs.
    
    Keyword arguments:
    log -- file (name) to log to (default stderr)
    scope -- base scope to log to (default Cobalt)"""
    
    file_name = kwargs.get("log", None)
    if file_name is not None:
        log_file = open(file_name, "w")
    else:
        log_file = sys.stderr
    
    scope = kwargs.get("scope", "Cobalt")
    
    def traceit (frame, event, arg):
        if event == "line":
            lineno = frame.f_lineno
            filename = frame.f_globals["__file__"]
            if (filename.endswith(".pyc") or
                filename.endswith(".pyo")):
                filename = filename[:-1]
            name = frame.f_globals["__name__"]
            line = linecache.getline(filename, lineno)
            print >> log_file, "%s:%s: %s" % (name, lineno, line.rstrip())
        return traceit
    
    sys.settrace(traceit)

def log_to_stderr (logger_name, level=CONSOLE_LEVEL, timestamp=False):
    """Set up console logging."""
    if timestamp:
        format = '%(asctime)s %(message)s'
        date_format = '%Y-%m-%d %H:%M:%S'
    else:
        format = None
        date_format = None
    try:
        logger = logging.getLogger(logger_name)
    except:
        # assume logger_name is already a logger
        logger = logger_name
    handler = logging.StreamHandler() # sys.stderr is the default stream
    handler.setLevel(level)
    handler.setFormatter(TermiosFormatter(format, date_format)) # investigate this formatter
    logger.addHandler(handler)

def log_to_syslog (logger_name, level=SYSLOG_LEVEL, format='%(name)s[%(process)d]: %(message)s'):
    """Set up syslog logging."""
    try:
        logger = logging.getLogger(logger_name)
    except:
        # assume logger_name is already a logger
        logger = logger_name
    # anticipate an exception somewhere below
    handler = logging.handlers.SysLogHandler() # investigate FragmentingSysLogHandler
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)


# Log-to-database utilities are below.
class dbwriter(object):

    """I am intending this to involve a singleton IO thread going to the
    database"""
    
    def __init__(self, logger, queue=None, overflow_filename=None,
                 max_queued=None):
        
        self.logger = logger
        self.enabled = False
        self.cdbwriter_alive = False
        self.cdbwriter = None
        self.flushing = False
        
        self.overflow = False
        self.overflow_filename = overflow_filename
        self.overflow_file = None
        self.clearing_overflow = False
        self.max_queued = max_queued    
        
        if queue:
            self.msg_queue = queue
        else:
            self.msg_queue = []
            


    def connect(self):
        if not self.enabled:
            return

        if self.cdbwriter_alive:
            self.logger.warning("Attempted to connect to cdbwriter when a conenction already exists.")
            return

        try:
            self.cdbwriter = Cobalt.Proxy.ComponentProxy('cdbwriter', defer=False)
            
            self.cdbwriter_alive = True
        except:
            self.logger.warning("Unable to connect to cdbwriter")
        
        
        
    def log_to_db(self, user, event, msg_type, obj):
        if not self.enabled:
            return

        #if a queue gets too large, save messages to disk for later writiing.
        if ((self.max_queued != None) and 
            (len(self.msg_queue) >= self.max_queued) and 
            not self.clearing_overflow):
            self.overflow = True
            self.open_overflow('a')
            if self.overflow_file == None:
                #we have too many messages and cannot write to disk.  
                #This message has to be dropped.
                #Of course, a lot of somethings would have to go critically 
                #wrong to need this.  The logfile message may fail as well.

                try:
                    message = Cobalt.JSONEncoders.ReportObject(user, event,
                                                               msg_type, obj).encode()
                except Exception as e:
                    self.logger.error("Error encoding message to send to cdbwriter.")
                    self.logger.error(traceback.format_exc())
                else:
                    #done just about all I can.  At this point, I don't have much choice.
                    self.logger.critical("MESSAGE DROPPED: %s" % message)
            else:
                self.queue_to_overflow()
                self.close_overflow()

        #end queue overflow handling

        try:
            message = Cobalt.JSONEncoders.ReportObject(user, event, 
                                                           msg_type, obj).encode()
        except Exception as e:
            self.logger.error("Error encoding message to send to cdbwriter.")
            self.logger.debug(traceback.format_exc())
            
        else:
            self.msg_queue.append(message)
        
        self.flush_queue()

 
    def flush_queue(self):
        """send a series of messages to the writer component."""
        if not (self.enabled or self.flushing or self.clearing_overflow):
            return

        self.flushing = True
        if not self.cdbwriter_alive:
            self.connect()
        
        #we're connected and have an "overflow file", we should flush 
        #that first.
        if self.overflow and self.cdbwriter_alive:
            self.clearing_overflow = True
            #Shove out as many to the writer component as we can.  Save the rest.
            self.open_overflow('r')
            if self.overflow_file:
                #we prepend to the message queue.
                overflow_queue = [line for line in self.overflow_file]
                overflow_queue.extend(self.msg_queue)
                self.msg_queue = overflow_queue
                self.close_overflow()
                self.del_overflow() #Now that it is back in memory, we dump if needed.
                self.overflow = False

        

        #drain the queue, if we have one.
        while self.msg_queue and self.cdbwriter_alive:
            msg = self.msg_queue[0]
            try:
               self.cdbwriter.add_message(msg)
            except:
                self.logger.error("dbwriter.flush_queue: Unable to contact "\
                        "database writer when sending message.")
                self.cdbwriter_alive = False
                
                #if the cdbwriter falls over while dealing with overflow.
                if ((self.max_queued != None) and
                    (len(self.msg_queue) >= self.max_queued)):
                    self.overflow = True
                    self.open_overflow('a')
                    if self.overflow_file != None:
                        self.queue_to_overflow()
                        self.close_overflow()
                break
            else:
                try:
                    self.msg_queue.pop(0)
                except IndexError:
                    self.logger.error("dbwriter.flush_queue: Queue already empty.")
        
        self.clearing_overflow = False
        self.flushing = False
       

    def open_overflow(self, mode):
        
        try:
            self.overflow_file = open(self.overflow_filename,mode)
        except:
            self.logger.critical("Unable to open overflow file!  Information to database will be lost!")

    def close_overflow(self):
        if self.overflow and self.overflow_file:
            self.overflow_file.close()
            self.overflow_file = None
    
    def del_overflow(self):
        os.remove(self.overflow_filename)
        

    def queue_to_overflow(self):
        
        elements_written = 0
        if len(self.msg_queue) == 0:
            return

        while self.msg_queue:
            msg = self.msg_queue.pop(0)
            try:
                self.overflow_file.write(msg+'\n')
                elements_written += 1
            except IOError:
                logger.error('Could only partially empty queue, %d messages written' % 
                             elements_written)
                self.msg_queue.insert(0, msg)
                
        if elements_written > 0:
            del self.msg_queue[0:elements_written-1] #empty the queue of what we have written
        
        return len(self.msg_queue)
        
