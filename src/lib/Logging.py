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
import sys
import termios
import types
import linecache
import Cobalt
import ConfigParser
import threading
import time
import Queue


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
            for line in record.getMessage().split('\n'):
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

def setup_logging(procname, to_console=TO_CONSOLE, to_syslog=TO_SYSLOG, syslog_facility=SYSLOG_FACILITY, level=0):
    '''setup logging for bcfg2 software'''
    if hasattr(logging, 'already_setup'):
        return 
    # add the handler to the root logger
    if to_console:
        log_to_stderr(logging.root)
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

def log_to_stderr (logger_name, level=CONSOLE_LEVEL):
    """Set up console logging."""
    try:
        logger = logging.getLogger(logger_name)
    except:
        # assume logger_name is already a logger
        logger = logger_name
    handler = logging.StreamHandler() # sys.stderr is the default stream
    handler.setLevel(level)
    handler.setFormatter(TermiosFormatter()) # investigate this formatter
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





#TODO: Wrap up the safety stuff in this.  Also, make sure to get the fifo from
#a config file on the cobalt side

class DatabaseWriter(object):

    """I am intending this to involve a singleton IO thread going to the
    database"""
    
    initialized = False
    write_thread = None
    off = False
    
    def __init__(self, output_filename):
        
        
        self.output_filename = output_filename
        
        if not self.__class__.initialized:
            self.__class__.write_thread = ThreadedWrite(output_filename,
                                                        name="db_writer")
            
            #Turning this off in trunk until I can figure out why
            #this is not shutting down correctly.
            #self.__class__.write_thread.start()
            #self.thread_name = DatabaseWriter.write_thread.name
            

            self.__class__.initialized = True
        self.__class__.off = True

    @classmethod              
    def write(cls,data):
        #append a newline.  It makes the decoding behave a
        #a lot better
        if not cls.initialized:
            raise RuntimeError("Attempted to write to database before writer initialized.")
            #until I figure out a better way, do nothing, since this can be
            #turned off.
        if cls.off:
            if cls.write_thread.is_alive():
                cls.write_thread.send("Terminate\n")
            return
        
        cls.write_thread.send((data +"\n"))

    
    @classmethod
    def close(cls):
        cls.write("Terminate")
    

db_log_to_file = DatabaseWriter.write
#TODO: no I don't want to rewrite a bunch of code right now, why do you ask?
#dump this in favor of DatabaseWriter.write



class ThreadedWrite(threading.Thread):
    
    def __init__(self, output_filename, *args, **kwargs):
        threading.Thread.__init__(self,*args,**kwargs)
        self.msg_queue = Queue.Queue()
        self.terminating = False
        self.output_filename = output_filename
        self.missed_timeouts = 0
        self.max_missed_timeouts = 20
        #self.daemon = True

    def run(self):
        
        print "Database writing disabled."
        return
        
        while not self.terminating:
            try:
                queue_data = self.msg_queue.get(block=False)
                self.missed_timeouts = 0
            except Queue.Empty:               
                time.sleep(1)
                continue
            
            out_file = open(os.path.join(self.output_filename), "a")
            out_file.write(queue_data)
            out_file.close()
            self.msg_queue.task_done()
            
        #TODO: set up a fail-over file.
        #drain the queue and then terminate.
        print "Writer thread terminating."
        while not self.msg_queue.empty():
            queue_data = self.msg_queue.get(block=False)
            out_file = open(os.path.join(self.output_filename), "a")
            out_file.write(queue_data)
            out_file.close()
            self.msg_queue.task_done()
        
        return

    def send(self, data):

        """catches messages.  If "Terminate" message is caught, kill the
           writer thread."""
        if not isinstance(data, str):
            raise TypeError("Non-string data passed to the database writer")
        if self.terminating:
            raise RuntimeError("Attempted to queue a message after writer has been sent a terminate message.")
        if data == "Terminate\n":
            self.terminating = True
            self.close()
            return
        self.msg_queue.put(data, block=False)

    def close(self):
        self.msg_queue.join()
        self.join()
        

