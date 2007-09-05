#!/usr/bin/env python

'''this is the simple cluster scheduler'''
__revision__ = '$Revision'

import Cobalt.Component, Cobalt.Data, Cobalt.Logging, Cobalt.Proxy
import re, time, signal, logging, sys, xmlrpclib, ConfigParser

MAX_DATE = 2147483647
logger = logging.getLogger('csched')
comm = Cobalt.Proxy.CommDict()

class TimerException(Exception):
    '''a set of exceptions currently unused'''
    pass

class Timer(object):
    '''a generic timer'''
    def __init__(self):
        '''initialize the timer'''
        self.start = time.time()
        self.stop = time.time()
        pass
    
    def Start(self):
        '''start the timer'''
        self.start = time.time()
        
    def Stop(self):
        '''stop the timer'''
        self.stop = time.time()
            
    def Check(self):
        '''check the timer to see the current status'''
        try:
            return self.stop-self.start
        except:
            raise TimerException, "StateError"
        
    def Elapsed(self):
        '''get the elapsed time of the timer'''
        try:
            return time.time()-self.start
        except:
            raise TimerException, "StateError" 

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

class ComputeNode(Cobalt.Data.Data):
    '''object for nodes in the system'''
    def __init__(self, element):
        '''initialize the object with default values'''
        Cobalt.Data.Data.__init__(self, element)
        #name and attributes will have to be coded into the object that comes in.
        #maybe even the queue will want to be determined ahead of time.
        self.set('state', 'idle')
        self.set('reservation', '')
        #this may become optional. it depends on how the Nodelist is prebuilt?
        self.set('queue', 'default')
        #this is a temporary haxor to get things running without a ton of modification
        self.set('attributes', ['compute'])

    def isUsable( self, attribute, queue ):
        return self.isAvailable() and self.hasAttribute(attribute) and self.inQueue(queue)

    def hasAttribute(self, attribute):
        '''get the nodes attributes'''
        return [ attr for attr in self.get('attributes') if attr == attribute ]

    def isAvailable(self):
        '''is the node currently available to be scheduled'''
        return self.get('scheduled') and self.get('state') == "idle"

    def isReserved(self, reservation):
        return self.get('reservation') == reservation

    def notReserved(self):
        return self.get('reservation') == ""
        
    def inQueue(self, queue):
        return self.get('queue') == queue

class NodeList(Cobalt.Data.DataSet):
    __object__ = ComputeNode
    _configfields = []
    _config = ConfigParser.ConfigParser()
    if '-C' in sys.argv:
        _config.read(sys.argv[sys.argv.index('-C') + 1])
    else:
        _config.read('/etc/cobalt.conf')
    if not _config._sections.has_key('csched'):
        print '''"csched" section missing from cobalt config file'''
        raise SystemExit, 1
    config = _config._sections['csched']
    mfields = [field for field in _configfields if not config.has_key(field)]
    if mfields:
        print "Missing option(s) in cobalt config file: %s" % (" ".join(mfields))
        raise SystemExit, 1
    if not _config._sections.has_key('csched-queue'):
        print '''csched-queue section missing from config file'''
        raise SystemExit, 1
    qconfig = _config._sections['csched-queue']
    qpolicy = {'default':'PlaceFIFO', 'short':'PlaceShort'}

    def __init__(self):
        '''Initialize the object and create the actual list data'''
        Cobalt.Data.DataSet.__init__(self)
        #this maybe totally obsolete due to the fact that I want to be able to modify,store and reread the configs, through restart.
        #this is actually going to be fully replaced with add get del functions and the data will be stored in the regular dump and load
        #functionality. I will have to make sure there is a client tool to do that interaction not sure partadm.py will be the right thing.

    def setReservation(self, spec, name):
        '''this will find all node matching the spec and then assign name to the nodes reservation field'''
        for node in self.matchNodes(spec):
            node.set('reservation', name)
        
    def matchNodes(self, regex):
        '''create a node list for the job from a regular expression'''
        noderegex = re.compile(regex)
        return [ node for node in self.data if re.match(noderegex, node.get('name')) ]

    def enoughNodes(self, numOfNodes, attribute, queue ):
        '''returns a list of nodes if there are enough nodes available to be scheduled'''
        listofnodes = []
        mynodelist = []
        #check for reservation first of all.. and also that there is enough nodes in the reservation to run
        mynodelist = [ node.get('name') for node in self.data if node.isUsable( attribute, queue ) ]
        if len(mynodelist) >= int(numOfNodes):
            listofnodes = mynodelist[:int(numOfNodes)]
        return listofnodes

    def markUsed(self, job, nodelist):
        '''mark the node as used by a job or reservation'''
        for node in self.data:
            if node.get('name') in nodelist:
                node.set('state', job)

    def markFree(self, jobid):
        '''mark the node as free or available to be scheduled'''
        for node in self.data:
            if node.get('state') == jobid:
                node.set('state', "idle")
                                            
class Scheduler(Cobalt.Component.Component):
    '''Core Object for the actual scheduler'''
    __implementation__ = 'csched'
    __name__  =  'scheduler'
    __statefields__ = ['nodes']
    __schedcycle__ = 10
    async_funcs = ['assert_location', 'RunQueue']
        
    def __init__(self,setup):
        '''setup the object with default values'''
        self.nodes = NodeList()
        Cobalt.Component.Component.__init__(self,setup)
        self.adminlist = ['bradshaw', 'desai', 'alusk', 'root']
        self.jobs = []
        #I may want to make reservations an entire class of stuff that have fancy methods and what not
        self.reservations = {}
        self.qmconnect = FailureMode("QM Connection")
        self.lastrun = 0
        self.register_function(lambda address, data:self.nodes.Get(data), "GetPartition")
        self.register_function(lambda address, data:self.nodes.Add(data), "AddPartition")
        self.register_function(lambda address, data:self.nodes.Del(data), "DelPartition")
        self.register_function(lambda address, data, updates:
                               self.nodes.Get(data, lambda part, newattr:part.update(newattr), updates),
                               'Set')
        self.register_function(self.AddReservation, "AddReservation")
        self.register_function(self.ReleaseReservation, "DelReservation")


    def AddReservation(self, _, spec, name, user, start, duration):
        '''Add a reservation to matching partitions'''
        nodes = self.nodes.match(spec)
        self.reservations[name] = (user, start, duration, nodes)
        return self.reservation[name]
    
    def ReleaseReservation(self, _, spec, name):
        '''Release specified reservation'''
        return self.reservations.pop(name)
                            
    def RunQueue(self):
        '''Process changes to the cqm queue'''
        since = time.time() - self.lastrun
        if since < self.__schedcycle__:
            return
        try:
            jobs = comm['qm'].GetJobs([{'tag':'job', 'nodes':'*', 'location':'*', 'jobid':'*', 'state':'*',
                                        'walltime':'*', 'queue':'*', 'user':'*'}])
        except xmlrpclib.Fault:
            self.qmconnect.Fail()
            return 0
        except:
            self.logger.error("Unexpected fault during queue fetch", exc_info=1)
            return 0
        self.qmconnect.Pass()
        active = [job.get('jobid') for job in jobs]
        for job in [j for j in self.jobs if j.get('jobid') not in active]:
            logger.info("Job %s/%s: gone from qm" % (job.get('jobid'), job.get('user')))
            self.nodes.markFree(job.get('jobid'))
            self.jobs.remove(job)
        # known is jobs that are already registered
        known = [job.get('jobid') for job in self.jobs]

        newjobs = [job for job in jobs if job.get('jobid') not in known]
        self.jobs += newjobs

        #this will have to change a bit due to the fact I don't have that structure currently.
        placements = self.Schedule()
        if '-t' not in sys.argv:
            for (jobid, nodes) in placements:
                try:
                    comm['qm'].RunJobs([{'tag':'job', 'jobid':jobid}], nodes)
                    pass
                except:
                    logger.error("failed to connect to the queue manager to run job %s" % (jobid))
        else:
            print "Jobs would be placed on:", placements
        self.lastrun = time.time()


    def Schedule(self):
        '''this will return a list of tuples of (jobid,[nodes]) that can run right now'''
        placements = []
        #get all the jobs not running
        for job in [ job for job in self.jobs if job.get('state') == 'queued' ]:
            nodes = self.nodes.enoughNodes( job.get('nodes'), 'compute', job.get('queue') )
            if nodes:
                placements.append((job.get('jobid'),nodes))
                self.nodes.markUsed(job.get('jobid'), nodes)
        return placements

        
if __name__ == '__main__':
    from getopt import getopt, GetoptError
    try:
        opts = getopt(sys.argv[1:], 'dC:D:', [])[0]
    except GetoptError, msg:
        print "%s\nUsage:\ncsched.py [-d] [-C <configfile>] [-D <pidfile>]" % (msg)
        raise SystemExit, 1
    try:
        daemon = [x[1] for x in opts if x[0] == '-D'][0]
    except:
        daemon = False
    level = 10
    if len([x for x in opts if x[0] == '-d']):
        level = 0
    Cobalt.Logging.setup_logging('cqm', level=20)
    server = Scheduler({'configfile':'/etc/cobalt.conf', 'daemon':daemon})
    server.serve_forever()
