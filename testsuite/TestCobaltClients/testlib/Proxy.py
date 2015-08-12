import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import time
import pwd
import os
import getpass
import testutils
import socket

def stub_time():
    return 1364335099.14

def stub_getpwuid(x):
    return ('gooduser', '********', 501, 20, 'Good User', '/home/gooduser', '/bin/bash')

def stub_getpwnam(user):
    if user == 'naughtyuser':
        raise KeyError
    return (user, '********', 501, 20, '%s %s' % (user,user), '/home/%s' % user, '/bin/bash')

def stub_getcwd():
    return '/tmp'

def stub_getuser():
    return stub_getpwuid(1)[0]

def stub_system(cmd):
    return 0

def stub_gethostname():
    return "foo.bar"

# redefine the standard time() function
time.time = stub_time

# redefine the  pwd.getpwuid
pwd.getpwuid = stub_getpwuid

# redefine the  pwd.getpwuid
pwd.getpwnam = stub_getpwnam

# redefine path
os.environ['PATH'] = '/tmp'

# redefine getting the current working directory
os.getcwd = stub_getcwd

# redfine getuser 
getpass.getuser = stub_getuser

# redfine system
os.system = stub_system

#redefine gethostname, so this is host agnostic -PMR
socket.gethostname = stub_gethostname

fn = 'stub.out'
fd = open(fn,'w')
logbuf       = ''
vbuf         = ''
logwrite     = True

USERS    = ['james', 'land' , 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl'  , 'boy']
GROUPS   = [None, None, None, None, 'foo', 'bar', 'wheel', None, None, None,]
QUEUES   = ['kebra', 'jello', 'bello', 'aaa', 'bbb', 'hhh'  , 'dito', 'myq'  , 'yours' , 'zq' ]
SCORES   = [ 45    ,  50    ,  55    ,  40  ,  60  ,  30    ,  20   ,  25    ,  35     ,  2   ]
PARTS    = ['P1','P2','P3','P4','P5','P6','P7','P8','P9','P10']

def enable_logwrite():
    global logwrite
    logwrite = True

def disable_logwrite():
    global logwrite
    logwrite = False

def logmsg(msg):
    global logbuf
    global logwrite
    if logwrite:
        fd.write(msg + '\n')
    else:
        logbuf = logbuf + msg + '\n'

def logdic(dic):
    keylist = []
    for key in dic:
        keylist.append(key)
    keylist.sort()
    for key in keylist:
        logmsg(str(key) + ':' + str(dic[key]))
        logmsg(str(key) + ' type: ' + str(type(dic[key])))

def logdiclist(diclist):
    for dic in diclist: logdic(dic)

def gen_partitions(specs,updates,whoami):
    logmsg('whoami: %s' % str(whoami))
    logdiclist(specs)
    if updates:
        logdic(updates)
    parts = []
    for i in range(len(specs)):
        parts.append({'name':PARTS[i],'queue':QUEUES[i],'children':'a', 'size':i, 
                      'node_geometry':['48','48','48','48','48'],'relatives':'b','passthrough_blocks':'A',
                      'draining':False,'state':'idle','functional':True, 'scheduled':True})
        for s in specs:
            for k in s:
                parts[i][k] = s[k]
        if updates:
            for k in updates:
                parts[i][k] = updates[k]
    return parts

def genplist(parts):
    logdiclist(parts)
    plist = []
    for s in parts:
        if s['name'] == '*':
            for p in PARTS:
                plist.append(p)
            break
        plist.append(s['name'])
    return plist

def get_parts(plist):
    logmsg('plist: '+str(plist))
    parts = []
    i = 0
    for p1 in plist:
        if p1['name'] == '*':
            for p2 in PARTS:
                parts.append({'name':p2,'queue':QUEUES[i],'children':['a','b','c','d'], 'size':i,'parents':['a','b','c'],
                              'node_geometry':['48','48','48','48','48'],'relatives':['b'],'passthrough_blocks':['A'],
                              'draining':False,'state':'idle','functional':True, 'scheduled':True, 'status': 'OK', 
                              'block_computes_for_reboot': True, 'autoreboot' : True} )
                i += 1
            break
        parts.append({'name':p1['name'],'queue':QUEUES[i],'children':['a','b','c','d'], 'size':i,'parents':['a','b','c'],
                      'node_geometry':['48','48','48','48','48'],'relatives':['b'],'passthrough_blocks':['A'],
                      'draining':False,'state':'idle','functional':True, 'scheduled':True, 'status': 'OK',
                      'block_computes_for_reboot': True, 'autoreboot' : True} )
        i += 1
    return parts

class SystemStub(object):

    def interactive_job_complete(self, jobid):
        logmsg("\INTERACTIVE_JOB_COMPLETE\n")
        logmsg("jobid: %s, type = %s" % (str(jobid), str(type(jobid))))
        return True

    def initiate_proxy_boot(self,block, user, jobid, resid=None, timeout=None):
        logmsg("\nINITIATE_PROXY_BOOT\n")
        logmsg("block: %s, type = %s" % (block, str(type(block))))
        logmsg("user: %s" % user)
        logmsg("jobid: %s, type = %s" % (str(jobid), str(type(jobid))))
        return True

    def initiate_proxy_free(self,block, user, jobid):
        logmsg("\nINITIATE_PROXY_FREE\n")
        logmsg("block: %s, type = %s" % (block, str(type(block))))
        logmsg("user: %s" % user)
        logmsg("jobid: %s, type = %s" % (str(jobid), str(type(jobid))))
        return True

    def get_boot_statuses_and_strings(self,block):
        logmsg("\nGET_BOOT_STATUSES_AND_STRINGS\n")
        logmsg("block: %s, type = %s" % (block, str(type(block))))
        boot_id        = 1
        status         = 'complete'
        status_strings = ['status 1','status 2','status 3']
        return (boot_id, status, status_strings)

    def reap_boot(self,block):
        logmsg("\nREAP_BOOT\n")
        logmsg("block: %s, type = %s" % (block, str(type(block))))
        return True

    def get_block_bgsched_status(self,block):
        logmsg("\nGET_BLOCK_BGSCHED_STATUS\n")
        logmsg("block: %s, type = %s" % (block, str(type(block))))
        return 'Free'

    def validate_job(self,opts):
        disable_logwrite()
        logmsg("\nVALIDATE_JOB\n")
        logdic(opts)
        if not opts['mode']:
            opts['mode'] = 'c1'
        if not opts['proccount']:
            opts['proccount'] = str(512)
        opts['nodecount'] = int(opts['nodecount'])
        opts['ranks_per_node'] = 10
        enable_logwrite()
        return opts

    def get_partitions(self,plist):
        logmsg("\nGET_PARTITIONS\n")
        return get_parts(plist)

    def get_blocks(self,plist):
        logmsg("\nGET_BLOCKS\n")
        return get_parts(plist)

    def get_io_blocks(self, plist):
        logmsg("\nGET_IO_BLOCKS\n")
        return get_parts(plist)

    def verify_locations(self,location_list):
        logmsg("\nVERIFY_LOCATIONS\n")
        logmsg('location list: '+str(location_list))
        return location_list

    def add_partitions (self, parts, user_name=None):
        logmsg("\nADD_PARTITION\n")
        logmsg('user name: %s' % str(user_name))
        logdiclist(parts)
        return genplist(parts)

    def add_io_blocks(self, parts, user_name=None):
        logmsg("\nADD_IO_BLOCKS\n")
        logmsg('user name: %s' % str(user_name))
        logdiclist(parts)
        return genplist(parts)

    def del_partitions (self, parts, user_name=None):
        logmsg("\nDEL_PARTITION\n")
        logmsg('user name: %s' % str(user_name))
        logdiclist(parts)
        return genplist(parts)

    def del_io_blocks(self, parts, user_name=None):
        logmsg("\nDEL_IO_BLOCKS\n")
        logmsg('user name: %s' % str(user_name))
        logdiclist(parts)
        return genplist(parts)

    def set_partitions (self, parts, updates, user_name=None):
        logmsg("\nSET_PARTITION\n")
        logmsg('user name: %s' % str(user_name))
        logdiclist(parts)
        logdic(updates)
        return genplist(parts)

    def generate_xml(self):
        logmsg("\nGENERATE_XML\n")
        return genplist([{'name':'*'}])

    def fail_partitions(self, parts, user_name=None):
        logmsg("\nFAIL_PARTITION\n")
        logmsg('user name: %s' % str(user_name))
        logmsg('part list: %s' % str(parts))
        return genplist(parts)

    def unfail_partitions(self, parts, user_name=None):
        logmsg("\nUNFAIL_PARTITION\n")
        logmsg('user name: %s' % str(user_name))
        logmsg('part list: %s' % str(parts))
        return genplist(parts)

    def save(self,filename):
        logmsg("\nSAVE\n")
        logmsg('filename:'+str(filename))
        return get_parts([{'name':'*'}])

    def halt_booting(self,user_name=None):
        logmsg("\nHALT_BOOTING\n")
        logmsg('whoami: %s' % str(user_name))
        return True

    def resume_booting(self,user_name=None):
        logmsg("\nRESUME_BOOTING\n")
        logmsg('whoami: %s' % str(user_name))
        return True

    def booting_status(self):
        logmsg("\nBOOTING_STATUS\n")
        return False

    def set_cleaning(self,part,var2,user_name):
        logmsg("\nSET_CLEANING\n")
        logmsg("part: %s" % part)
        logmsg("var2 : %s, type = %s" % (var2, str(type(var2))))
        logmsg('whoami: %s' % str(user_name))
        return True

    def get_implementation(self):
        logmsg("\nGET_IMPLEMENTATION\n")
        return 'cluster_system'

    def nodes_down(self,args,whoami):
        logmsg("\nNODES_DOWN\n")
        logmsg("whoami: %s" % whoami)
        for a in args:
            logmsg(a)
        return ["D1","D2","D3","D4","D5"]

    def nodes_up(self,args,whoami):
        logmsg("\nNODES_UP\n")
        logmsg("whoami: %s" % whoami)
        logmsg("args: %s" % str(args))
        return ["U1","U2","U3","U4","U5"]

    def get_idle_blocks(self,block_loc, query_size,geo_list):
        logmsg("\nGET_IDLE_BLOCKS\n")
        logmsg("block location: %s, type = %s" % (str(block_loc), str(type(block_loc))))
        logmsg("query size: %s, type = %s" % (str(query_size), str(type(queue_size))))
        geo = ''
        if geo_list != None: 
            for g in geo_list:
                geo += str(g) + 'x'
            geo = geo[:-1]
        logmsg("geoometry: %s" % geo)
        return ["I1","I2","I3","I4","I5"]

    def get_node_status(self):
        logmsg("\nGET_NODES_STATUS\n")
        return [ ['D1','good'],['D2','bad'],['D3','ugly'],['U1','one'],['U2','two'],['U3','three']]

    def get_queue_assignments(self):
        logmsg('\nGET_QUEUE_ASSIGNMENTS\n')
        ret = {'QU1':'U1','QD1':'D1','QU2':'U2','QD2':'D2','QU3':'U3','QD3':'D3'}
        return ret

    def set_queue_assignments(self,queues,args,whoami):
        logmsg('\nGET_QUEUE_ASSIGNMENTS\n')
        logmsg("whoami: %s" % whoami)
        logmsg("args: %s" % str(args))
        logmsg("queues: %s" % str(queues))
        ret = queues
        return ret

    def initiate_io_boot(self, parts, whoami):
        logmsg('\nINITIATE_IO_BOOT\n')
        logmsg("whoami: %s" % whoami)
        logmsg('parts: %s' % str(parts))
        return True

    def initiate_io_free(self, parts, force, whoami):
        logmsg('\nINITIATE_IO_BOOT\n')
        logmsg("whoami: %s" % whoami)
        logmsg("force: %s, type = %s" % (str(force),str(type(force)) ))
        logmsg('parts: %s' % str(parts))
        return True

    def set_autoreboot(self, parts, user):
        logmsg('\nSET_AUTOREBOOT\n')
        logmsg("whoami: %s" % user)
        logmsg('parts: %s' % str(parts))
        return True

    def unset_autoreboot(self, parts, user):
        logmsg('\nUNSET_AUTOREBOOT\n')
        logmsg("whoami: %s" % user)
        logmsg('parts: %s' % str(parts))
        return True

    def enable_io_autoreboot(self):
        logmsg("\nENABLE_IO_AUTOREBOOT\n")
        return True

    def disable_io_autoreboot(self):
        logmsg("\nDISABLE_IO_AUTOREBOOT\n")
        return 

    def get_io_autoreboot_status(self):
        logmsg("\nGET_IO_AUTOREBOOT_STATUS\n")
        return True

    def get_backfill_windows(self):
        logmsg("\nGET_BACKFILL_WINDOWS\n")
        return {}

def change_jobs(ojoblist, newjob,user):
    logmsg("\nOriginal Jobs:\n")
    logmsg("user: %s" % user)
    logdiclist(ojoblist)
    logmsg("\nNew Job Info:\n")
    if type(newjob) == type([]) or type(newjob) == type({}):
        logdic(newjob)
    else:
        logmsg(str(newjob) + ', type = ' + str(type(newjob)))
    _job_specs = []
    wtime = 5
    nodes = 512
    ndx = 0
    for job in ojoblist:
        _job = {}
        _job['tag']           = 'job'
        _job['user']          = USERS[ndx]
        _job['jobid']         = job['jobid']
        _job['project']       = 'my_project'
        _job['notify']        = 'myemag@gmail.com'
        _job['walltime']      = wtime
        _job['procs']         = nodes
        _job['nodes']         = nodes
        _job['is_active']     = False
        _job['queue']         = QUEUES[ndx]
        _job['mode']          = 'smp'
        _job['errorpath']     = '/tmp'
        _job['errorpath']     = '/tmp'
        _job['outputpath']    = '/tmp'
        _job['user_hold']     = False
        _job['has_completed'] = False
        if type(newjob) == type([]):
            for key in newjob:
                _job[key] = newjob[key]
        _job_specs.append(_job)
        wtime += 5
        nodes += 512
        ndx += 1
    return _job_specs

class CqmStub(object):
    
    def set_jobid(self,jobid, whoami):
        logmsg("\nSET_JOBID\n")
        logmsg('jobid:'+str(jobid))
        logmsg('whoami:'+str(whoami))
        return True

    def save(self,filename):
        logmsg("\nSAVE\n")
        logmsg('filename:'+str(filename))
        return True
        
    def set_queues(self,jobslist, qdata, whoami):
        logmsg("\nSET_QUEUES\n")
        logmsg('queue data:'+str(qdata))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        return True

    def del_queues(self,jobslist,force,whoami):
        logmsg("\nDEL_QUEUES\n")
        logmsg('force:'+str(force))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        queues = [{'maxtime'      : None,
                   'mintime'      : None,
                   'name'         : job['name'],
                   'user'         : 'gooduser',
                   'maxrunning'   : 20,
                   'maxqueued'    : 20,
                   'maxusernodes' : 20,
                   'maxnodehours' : 20,
                   'totalnodes'   : 100,
                   'adminemail'   : 'myemail@gmail.com',
                   'state'        : 'deleted',
                   'cron'         : 'whocares',
                   'policy'       : 'mypolicy',
                   'priority'     : 'urgent'} for job in jobslist]
        return queues

    def add_queues(self,jobslist,whoami):
        logmsg("\nADD_QUEUES\n")
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        queues = [{'maxtime'      : None,
                   'mintime'      : None,
                   'name'         : job['name'],
                   'user'         : 'gooduser',
                   'maxrunning'   : 20,
                   'maxqueued'    : 20,
                   'maxusernodes' : 20,
                   'maxnodehours' : 20,
                   'totalnodes'   : 100,
                   'adminemail'   : 'myemail@gmail.com',
                   'state'        : 'running',
                   'cron'         : 'whocares',
                   'policy'       : 'mypolicy',
                   'priority'     : 'urgent'} for job in jobslist]
        return queues

    def get_queues(self,jobslist):
        logmsg("\nGET_QUEUES\n")
        logdiclist(jobslist)
        queues = []
        for i in range(10):
            queue = {'maxtime'      : None,
                     'mintime'      : None,
                     'name'         : QUEUES[i],
                     'users'        : USERS[i],
                     'groups'       : GROUPS[i],
                     'maxrunning'   : 20,
                     'maxqueued'    : 20,
                     'maxusernodes' : 20,
                     'maxnodehours' : 20,
                     'totalnodes'   : 100,
                     'adminemail'   : 'myemail@gmail.com',
                     'state'        : 'running',
                     'cron'         : 'whocares',
                     'policy'       : 'mypolicy',
                     'priority'     : 'urgent'}
            queues.append(queue)
        return queues

    def preempt_jobs(self,jobslist,whoami,force):
        logmsg("\nPREEMPT_JOBS\n")
        logmsg('force:'+str(force))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        return True

    def del_jobs(self,jobslist,force,whoami):
        logmsg("\nDEL_JOBS\n")
        logmsg('force:'+str(force))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        return jobslist

    def run_jobs(self,jobslist,location,whoami):
        logmsg("\nRUN_JOBS\n")
        logmsg('location:'+str(location))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        return True

    def add_jobs(self,jobslist):
        global logbuf
        logmsg("\nADD_JOBS\n")
        logdiclist(jobslist)
        if logbuf != '':
            logmsg(logbuf)
            logbuf = ''
        return [{'jobid':1}]
        
    def set_jobs(self,ojoblist, newjob,user):
        logmsg("\nSET_JOBS\n")
        return change_jobs(ojoblist,newjob,user)

    def adjust_job_scores(self,ojoblist, newscore,user):
        logmsg("\nADJUST_JOB_SCORES\n")
        logdiclist(ojoblist)
        logmsg('new score: %s, type = %s' % (str(newscore), str(type(newscore))))
        jobids = [j['jobid'] for j in ojoblist]
        return jobids

    def get_jobs(self,job_specs):
        if len(job_specs) == 0: return

        # get hooks f
        thook = testutils.get_testhook()
        job_running = True if thook.find("JOB_RUNNING") != -1 else False

        logmsg("\nGET_JOBS\n")
        logdiclist(job_specs)
        _job_specs = []
        wtime = 5
        nodes = 512
        jobid = 100
        ndx = 1
        for job in job_specs:
            if type(job['jobid']) != type(1):
                j = jobid
                jobid += 1
            else:
                j = job['jobid']
                
            if job_running:
                state = 'running'
            elif 'state' in job:
                state = job['state']
            else:
                state = 'user_hold'

            _job = {}
            _job['tag']           = 'job'
            _job['user']          = USERS[ndx]
            _job['state']         = state
            _job['jobid']         = j
            _job['project']       = 'my_project'
            _job['notify']        = 'myemail@gmail.com'
            _job['walltime']      = str(wtime)
            _job['procs']         = str(nodes)
            _job['nodes']         = str(nodes)
            _job['is_active']     = True if job_running else False
            _job['queue']         = QUEUES[ndx]
            _job['mode']          = 'smp'
            _job['errorpath']     = '/tmp'
            _job['errorpath']     = '/tmp'
            _job['outputpath']    = '/tmp'
            _job['user_hold']     = False
            _job['has_completed'] = False
            _job['location']      = '/tmp'
            _job['submittime']    = str(60)
            _job['envs']          = {}
            _job['args']          = ''
            _job['user_list']     = [u for u in USERS]
            _job['geometry']      = None
            _job['resid']         = None
            _job['score']         = SCORES[ndx]
            ndx += 1
            _job_specs.append(_job)
            wtime += 5
            nodes += 512
        enable_logwrite()
        return _job_specs

    def define_user_utility_functions(self,whoami):
        logmsg("\nDEFINE_USER_UTILITY_FUNCTION\n")
        logmsg('whoami: %s' % str(whoami))

class SchedStub(object):

    def save(self,filename):
        logmsg("\nSAVE\n")
        logmsg('filename:'+str(filename))
        return True

    def force_res_id(self,res_id):
        logmsg("\nFORCE_RES_ID\n")
        logmsg('id: ' + str(res_id) + ', type: ' + str(type(res_id)))
        return id

    def set_res_id(self,res_id):
        logmsg("\nSET_RES_ID\n")
        logmsg('id: ' + str(res_id) + ', type: ' + str(type(res_id)))
        return id

    def force_cycle_id(self,cycle_id):
        logmsg("\nFORCE_CYCLE_ID\n")
        logmsg('id: ' + str(cycle_id) + ', type: ' + str(type(cycle_id)))
        return id

    def set_cycle_id(self,cycle_id):
        logmsg("\nSET_CYCLE_ID\n")
        logmsg('id: ' + str(cycle_id) + ', type: ' + str(type(cycle_id)))
        return id

    def get_reservations(self,query):
        logmsg("\nGET_RESERVATIONS\n")
        logdiclist(query)
        res_list = []

        # get hooks f
        thook = testutils.get_testhook()

        ct   = 300
        d    = 500
        st   = 1000000

        if thook.find("BOGUS USER") != -1:
            u = 'bogususer'
        else:
            u = 'gooduser'

        for res in query:
            if 'name' in res:
                if thook.find("NO CYCLE") != -1:
                    _res = {'queue':QUEUES[0],'name':res['name'],'cycle':None,'duration':d,'start':st,'active':True,
                            'partitions':':'.join(PARTS),'block_passthrough':True,'cycle_id':10,'users':u,
                            'project':'proj','res_id':'id'}
                else:
                    _res = {'queue':QUEUES[0],'name':res['name'],'cycle':ct,'duration':d,'start':st,'active':True,
                            'partitions':':'.join(PARTS),'block_passthrough':True,'cycle_id':10,'users':u,
                            'project':'proj','res_id':'id'}
                res_list.append(_res)
            else:
                for q in QUEUES:
                    ct += 300
                    d  += 500
                    st += 1000000
                    res_list.append({'queue':q,'name':q,'cycle':ct,'duration':d,'start':st,'active':True,
                                     'partitions':':'.join(PARTS),'block_passthrough':True,'project':'proj','res_id':'id'})
        return res_list

    def set_reservations(self,res_list,spec,user):
        logmsg("\nSET_RESERVATIONS\n")
        logdiclist(res_list)
        logdic(spec)
        logmsg('user: '     + str(user))
        return True

    def release_reservations(self,spec,user):
        logmsg("\RELEASE_RESERVATIONS\n")
        logdiclist(spec)
        logmsg('user: '     + str(user))
        return [{'name': r['name'], 'partitions': 'p1:p2' } for r in spec]

    def del_reservations(self,spec,user):
        logmsg("\RELEASE_RESERVATIONS\n")
        logdiclist(spec)
        logmsg('user: '     + str(user))
        return ['one','two','three']

    def add_reservations(self,specs,user):
        logmsg("\nADD_RESERVATIONS\n")
        logdiclist(specs)
        logmsg('user: '     + str(user))
        return True

    def check_reservations(self):
        logmsg("\nCHECK_RESERVATIONS\n")
        return True

    def sched_status(self):
        logmsg("\nSCHED_STATUS\n")
        return True

    def disable(self,whoami):
        logmsg("\nDISABLE\n")
        logmsg('whoami: %s' % str(whoami))

    def enable(self,whoami):
        logmsg("\nENABLE\n")
        logmsg('whoami: %s' % str(whoami))
    
    def get_backfill_list(self,whoami):
        logmsg("\nGET_BACKFILL_LIST\n")
        logmsg('whoami: %s' % str(whoami))

class SlpStub(object):

    def get_services(self,query):
        logmsg("\nGET_SERVICES\n")
        logdiclist(query)
        thook = testutils.get_testhook()
        if thook.find("NO SERVICES") != -1:
            return []
        services = []
        for i in range(5):
            services.append({'name':'S'+str(i), 'location':'P'+str(i),'stamp':1366668370.0+(i*10)})
        return services

system    = SystemStub()
cqm       = CqmStub()
scheduler = SchedStub()
slp       = SlpStub()

def ComponentProxy(component_name, **kwargs):
    """
    ComponentProxy stub
    """
    if component_name == "system":
        return system
    elif component_name == "queue-manager":
        return cqm
    elif component_name == "scheduler":
        return scheduler
    elif component_name == "service-location":
        return slp
        
