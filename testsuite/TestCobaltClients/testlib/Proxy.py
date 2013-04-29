import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import time
import pwd
import os
import getpass
import testutils

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

fn = 'stub.out'
fd = open(fn,'w')
logbuf       = ''
vbuf         = ''
logwrite     = True

USERS    = ['james', 'land' , 'house', 'dog', 'cat', 'henry', 'king', 'queen', 'girl'  , 'boy']
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

def logdiclist(diclist):
    for dic in diclist: logdic(dic)

def gen_partitions(specs,updates,whoami):
    logmsg('whoami: %s' % str(whoami))
    logdiclist(specs)
    if updates:
        logdic(updates)
    parts = []
    i = 0
    for spec in specs:
        parts.append({'name':PARTS[i],'queue':QUEUES[i],'children':'a', 'size':i, 
                      'node_geometry':['48','48','48','48','48'],'relatives':'b','passthrough_blocks':'A',
                      'draining':False,'state':'idle','functional':True, 'scheduled':True})
        for s in specs:
            for k in s:
                parts[i][k] = s[k]
        if updates:
            for k in updates:
                parts[i][k] = updates[k]
        i += 1
    return parts

def genplist(specs):
    logdiclist(specs)
    plist = []
    for s in specs:
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
                parts.append({'name':p2,'queue':QUEUES[i],'children':['a'], 'size':i,'parents':['a','b','c'],
                              'node_geometry':['48','48','48','48','48'],'relatives':['b'],'passthrough_blocks':['A'],
                              'draining':False,'state':'idle','functional':True, 'scheduled':True})
                i += 1
            break
        parts.append({'name':p1['name'],'queue':QUEUES[i],'children':['a'], 'size':i,'parents':['a','b','c'],
                      'node_geometry':['48','48','48','48','48'],'relatives':['b'],'passthrough_blocks':['A'],
                      'draining':False,'state':'idle','functional':True, 'scheduled':True})
        i += 1
    return parts

class SystemStub(object):

    def initiate_proxy_boot(s,block, user, jobid):
        logmsg("\nINITIATE_PROXY_BOOT\n")
        logmsg("block: %s" % block)
        logmsg("user: %s" % user)
        logmsg("jobid: %s" % str(jobid))
        return True

    def initiate_proxy_free(s,block, user, jobid):
        logmsg("\nINITIATE_PROXY_FREE\n")
        logmsg("block: %s" % block)
        logmsg("user: %s" % user)
        logmsg("jobid: %s" % str(jobid))
        return True

    def get_boot_statuses_and_strings(s,block):
        logmsg("\nGET_BOOT_STATUSES_AND_STRINGS\n")
        logmsg("block: %s" % block)
        boot_id        = 1
        status         = 'complete'
        status_strings = ['status 1','status 2','status 3']
        return (boot_id, status, status_strings)

    def reap_boot(s,block):
        logmsg("\nREAP_BOOT\n")
        logmsg("block: %s" % block)
        return True
        
    def get_block_bgsched_status(s,block):
        logmsg("\nGET_BLOCK_BGSCHED_STATUS\n")
        logmsg("block: %s" % block)
        return 'Free'
        
    def get_block_bgsched_status(s,block):
        logmsg("\nGET_BLOCK_BGSCHED_STATUS\n")
        logmsg("block: %s" % block)
        return 'Free'
        
    def validate_job(s,opts):
        disable_logwrite()
        logmsg("\nVALIDATE_JOB\n")
        logdic(opts)
        enable_logwrite()
        return opts

    def get_partitions(s,plist):
        logmsg("\nGET_PARTITIONS\n")
        return get_parts(plist)

    def get_blocks(s,plist):
        logmsg("\nGET_BLOCKS\n")
        return get_parts(plist)

    def verify_locations(s,location_list):
        logmsg("\nVERIFY_LOCATIONS\n")
        logmsg('location list: '+str(location_list))
        return location_list

    def add_partitions (s, specs, user_name=None):
        logmsg("\nADD_PARTITION\n")
        return genplist(specs)

    def del_partitions (s, specs, user_name=None):
        logmsg("\nDEL_PARTITION\n")
        return genplist(specs)

    def set_partitions (s, specs, updates, user_name=None):
        logmsg("\nSET_PARTITION\n")
        return genplist(specs)

    def generate_xml(s):
        logmsg("\nGENERATE_XML\n")
        return genplist([{'name':'*'}])

    def fail_partitions(s, specs, user_name=None):
        logmsg("\nFAIL_PARTITION\n")
        return genplist(specs)

    def unfail_partitions(s, specs, user_name=None):
        logmsg("\nUNFAIL_PARTITION\n")
        return genplist(specs)

    def save(s,filename):
        logmsg("\nSAVE\n")
        logmsg('filename:'+str(filename))
        return get_parts([{'name':'*'}])

    def halt_booting(s,user_name=None):
        logmsg("\nHALT_BOOTING\n")
        logmsg('whoami: %s' % str(user_name))
        return True

    def resume_booting(s,user_name=None):
        logmsg("\nRESUME_BOOTING\n")
        logmsg('whoami: %s' % str(user_name))
        return True

    def booting_status(s):
        logmsg("\nBOOTING_STATUS\n")
        return False

    def set_cleaning(s,part,var2,user_name):
        logmsg("\nSET_CLEANING\n")
        logmsg("part: %s" % part)
        logmsg("var2 : %s" % var2)
        logmsg('whoami: %s' % str(user_name))
        return True

    def get_implementation(s):
        logmsg("\nGET_IMPLEMENTATION\n")
        return 'cluster_system'

    def nodes_down(s,args,whoami):
        logmsg("\nNODES_DOWN\n")
        logmsg("whoami: %s" % whoami)
        for a in args:
            logmsg(a)
        return ["D1","D2","D3","D4","D5"]

    def nodes_up(s,args,whoami):
        logmsg("\nNODES_UP\n")
        logmsg("whoami: %s" % whoami)
        logmsg("args: %s" % str(args))
        return ["U1","U2","U3","U4","U5"]

    def get_idle_blocks(s,block_loc, query_size,geo_list):
        logmsg("\nGET_IDLE_BLOCKS\n")
        logmsg("block location: %s" % str(block_loc))
        logmsg("query size: %s" % str(query_size))
        geo = ''
        if geo_list != None: 
            for g in geo_list:
                geo += str(g) + 'x'
            geo = geo[:-1]
        logmsg("geoometry: %s" % geo)
        return ["I1","I2","I3","I4","I5"]

    def get_node_status(s):
        logmsg("\nGET_NODES_STATUS\n")
        return [ ['D1','good'],['D2','bad'],['D3','ugly'],['U1','one'],['U2','two'],['U3','three']]

    def get_queue_assignments(s):
        logmsg('\nGET_QUEUE_ASSIGNMENTS\n')
        ret = {'QU1':'U1','QD1':'D1','QU2':'U2','QD2':'D2','QU3':'U3','QD3':'D3'}
        return ret

    def set_queue_assignments(s,queues,args,whoami):
        logmsg('\nGET_QUEUE_ASSIGNMENTS\n')
        logmsg("whoami: %s" % whoami)
        logmsg("args: %s" % str(args))
        logmsg("queues: %s" % str(queues))
        ret = queues
        return ret

def change_jobs(ojoblist, newjob,user):
    logmsg("\nOriginal Jobs:\n")
    logdiclist(ojoblist)
    logmsg("\nNew Job Info:\n")
    if type(newjob) == type([]) or type(newjob) == type({}):
        logdic(newjob)
    else:
        logmsg(str(newjob))
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
    
    def set_jobid(s,jobid, whoami):
        logmsg("\nSET_JOBID\n")
        logmsg('jobid:'+str(jobid))
        logmsg('whoami:'+str(whoami))
        return True

    def save(s,filename):
        logmsg("\nSAVE\n")
        logmsg('filename:'+str(filename))
        return True
        
    def set_queues(s,jobslist, qdata, whoami):
        logmsg("\nSET_QUEUES\n")
        logmsg('queue data:'+str(qdata))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        return True

    def del_queues(s,jobslist,force,whoami):
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

    def add_queues(s,jobslist,whoami):
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

    def get_queues(s,jobslist):
        logmsg("\nGET_QUEUES\n")
        logdiclist(jobslist)
        queues = []
        for i in range(10):
            queue = {'maxtime'      : None,
                     'mintime'      : None,
                     'name'         : QUEUES[i],
                     'users'        : USERS[i],
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

    def preempt_jobs(s,jobslist,whoami,force):
        logmsg("\nPREEMPT_JOBS\n")
        logmsg('force:'+str(force))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        return True

    def del_jobs(s,jobslist,force,whoami):
        logmsg("\nDEL_JOBS\n")
        logmsg('force:'+str(force))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        return jobslist

    def run_jobs(s,jobslist,location,whoami):
        logmsg("\nRUN_JOBS\n")
        logmsg('location:'+str(location))
        logmsg('whoami:'+str(whoami))
        logdiclist(jobslist)
        return True

    def add_jobs(s,jobslist):
        global logbuf
        logmsg("\nADD_JOBS\n")
        logdiclist(jobslist)
        if logbuf != '':
            logmsg(logbuf)
            logbuf = ''
        return [{'jobid':1}]
        
    def set_jobs(s,ojoblist, newjob,user):
        logmsg("\nSET_JOBS\n")
        return change_jobs(ojoblist,newjob,user)

    def adjust_job_scores(s,ojoblist, newjob,user):
        logmsg("\nADJUST_JOB_SCORES\n")
        return change_jobs(ojoblist,newjob,user)

    def get_jobs(s,job_specs):
        if len(job_specs) == 0: return
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
            if 'state' in job:
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
            _job['location']      = '/tmp'
            _job['submittime']    = 60
            _job['envs']          = {}
            _job['args']          = ''
            _job['user_list']     = [u for u in USERS]
            _job['geometry']      = None
            _job['score']         = SCORES[ndx]
            ndx += 1
            _job_specs.append(_job)
            wtime += 5
            nodes += 512
        enable_logwrite()
        return _job_specs

    def define_user_utility_functions(s,whoami):
        logmsg("\nDEFINE_USER_UTILITY_FUNCTION\n")
        logmsg('whoami: %s' % str(whoami))

class SchedStub(object):

    def save(s,filename):
        logmsg("\nSAVE\n")
        logmsg('filename:'+str(filename))
        return True

    def force_res_id(s,id):
        logmsg("\nFORCE_RES_ID\n")
        logmsg('id: ' + str(id))
        return id

    def set_res_id(s,id):
        logmsg("\nSET_RES_ID\n")
        logmsg('id: ' + str(id))
        return id

    def force_cycle_id(s,id):
        logmsg("\nFORCE_CYCLE_ID\n")
        logmsg('id: ' + str(id))
        return id

    def set_cycle_id(s,id):
        logmsg("\nSET_CYCLE_ID\n")
        logmsg('id: ' + str(id))
        return id

    def get_reservations(s,query):
        logmsg("\nGET_RESERVATIONS\n")
        logdiclist(query)
        res_list = []
        ct   = 300
        d    = 500
        st   = 1000000
        res  = query[0]
        sz   = 100
        if 'name' in res:
            _res = {'queue':QUEUES[0],'name':res['name'],'cycle':ct,'duration':d,'start':st,'active':True,
                    'partitions':':'.join(PARTS),'block_passthrough':True,'cycle_id':10,'users':USERS[0],
                    'project':'proj','res_id':'id'}
            res_list.append(_res)
        else:
            for q in QUEUES:
                ct += 300
                d  += 500
                st += 1000000
                sz -= 1
                res_list.append({'queue':q,'name':q,'cycle':ct,'duration':d,'start':st,'active':True,
                                 'partitions':':'.join(PARTS),'block_passthrough':True,'project':'proj','res_id':'id'})
            
        return res_list

    def set_reservations(s,res_list,spec,user):
        logmsg("\nSET_RESERVATIONS\n")
        logdiclist(res_list)
        logdic(spec)
        logmsg('user: '     + str(user))
        return True

    def add_reservations(s,specs,user):
        logmsg("\nADD_RESERVATIONS\n")
        logdiclist(specs)
        logmsg('user: '     + str(user))
        return True

    def check_reservations(s):
        logmsg("\nCHECK_RESERVATIONS\n")
        return True

    def sched_status(s):
        logmsg("\nSCHED_STATUS\n")
        return True

    def disable(s,whoami):
        logmsg("\nDISABLE\n")
        logmsg('whoami: %s' % str(whoami))

    def enable(s,whoami):
        logmsg("\nENABLE\n")
        logmsg('whoami: %s' % str(whoami))

class SlpStub(object):

    def get_services(s,query):
        logmsg("\nGET_SERVICES\n")
        logdiclist(query)
        tinfo = testutils.get_testinfo()
        if tinfo.find("NO SERVICES") != -1:
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
        
