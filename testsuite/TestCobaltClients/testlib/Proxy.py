import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import time
import pwd
import os
import getpass

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
PARTS    = ['A','B','C','D','E','F','G','H','I','J']

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

class SystemStub(object):
    def validate_job(s,opts):
        disable_logwrite()
        logmsg("\nVALIDATE_JOB\n")
        logdic(opts)
        enable_logwrite()
        return opts

    def get_partitions(s,plist):
        logmsg("\nGET_PARTITIONS\n")
        logmsg('plist: '+str(plist))
        parts = []
        i = 0
        for p in PARTS:
            parts.append({'name':p,'queue':QUEUES[i],'children':'a','size':i,'node_geometry':['48','48','48','48','48'],
                          'draining':False,'state':'idle','functional':True,'scheduled':True})
            i += 1
        return parts

    def verify_locations(s,location_list):
        logmsg("\nVERIFY_LOCATIONS\n")
        logmsg('location list: '+str(location_list))
        return location_list

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
        logmsg("\nOriginal Jobs:\n")
        logdiclist(ojoblist)
        logmsg("\nNew Job Info:\n")
        logdic(newjob)
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
            for key in newjob:
                _job[key] = newjob[key]
            _job_specs.append(_job)
            wtime += 5
            nodes += 512
            ndx += 1
        return _job_specs

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

class SchedStub(object):

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
            _res = {'queue':QUEUES[0],'name':res['name'],'cycle':ct,'duration':d,'start':st,
                    'active':True,'partitions':':'.join(PARTS)}
            res_list.append()
        else:
            for q in QUEUES:
                ct += 300
                d  += 500
                st += 1000000
                sz -= 1
                res_list.append({'queue':q,'name':q,'cycle':ct,'duration':d,'start':st,'active':True,
                                 'partitions':':'.join(PARTS)})
            
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

system    = SystemStub()
cqm       = CqmStub()
scheduler = SchedStub()

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
        
