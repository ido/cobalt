import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import time

def stub_time():
    return 1364335099.14

# redefine the standard time() function
time.time = stub_time


fn = 'stub.out'
fd = open(fn,'w')
logbuf       = ''
vbuf         = ''
logwrite     = True

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
        return 'P'

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
                   'user'         : 'georgerojas',
                   'maxrunning'   : 20,
                   'maxqueued'    : 20,
                   'maxusernodes' : 20,
                   'maxnodehours' : 20,
                   'totalnodes'   : 100,
                   'adminemail'   : 'george@therojas.com',
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
                   'user'         : 'georgerojas',
                   'maxrunning'   : 20,
                   'maxqueued'    : 20,
                   'maxusernodes' : 20,
                   'maxnodehours' : 20,
                   'totalnodes'   : 100,
                   'adminemail'   : 'george@therojas.com',
                   'state'        : 'running',
                   'cron'         : 'whocares',
                   'policy'       : 'mypolicy',
                   'priority'     : 'urgent'} for job in jobslist]
        return queues

    def get_queues(s,jobslist):
        logmsg("\nGET_QUEUES\n")
        logdiclist(jobslist)
        queues = [{'maxtime'      : None,
                   'mintime'      : None,
                   'name'         : 'queue1',
                   'users'        : 'rojas:rich',
                   'maxrunning'   : 20,
                   'maxqueued'    : 20,
                   'maxusernodes' : 20,
                   'maxnodehours' : 20,
                   'totalnodes'   : 100,
                   'adminemail'   : 'george@therojas.com',
                   'state'        : 'running',
                   'cron'         : 'whocares',
                   'policy'       : 'mypolicy',
                   'priority'     : 'urgent'},
                  {'maxtime'      : None,
                   'mintime'      : None,
                   'name'         : 'queue2',
                   'users'        : 'georgerojas',
                   'maxrunning'   : 21,
                   'maxqueued'    : 21,
                   'maxusernodes' : 21,
                   'maxnodehours' : 21,
                   'totalnodes'   : 101,
                   'adminemail'   : 'george@therojas.com',
                   'state'        : 'running',
                   'cron'         : 'whocares',
                   'policy'       : 'mypolicy',
                   'priority'     : 'urgent'}]
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
        for job in ojoblist:
            _job = {}
            _job['tag']           = 'job'
            _job['user']          = 'georgerojas'
            _job['jobid']         = job['jobid']
            _job['project']       = 'gdr_project'
            _job['notify']        = 'george@therojas.com'
            _job['walltime']      = wtime
            _job['procs']         = nodes
            _job['nodes']         = nodes
            _job['is_active']     = False
            _job['queue']         = 'default'
            _job['mode']          = 'smp'
            _job['errorpath']     = '/Users/georgerojas/mypython'
            _job['errorpath']     = '/Users/georgerojas/mypython'
            _job['outputpath']    = '/Users/georgerojas/mypython'
            _job['user_hold']     = False
            _job['has_completed'] = False
            for key in newjob:
                _job[key] = newjob[key]
            _job_specs.append(_job)
            wtime += 5
            nodes += 512
        return _job_specs

    def get_jobs(s,job_specs):
        if len(job_specs) == 0: return
        logmsg("\nGET_JOBS\n")
        logdiclist(job_specs)
        _job_specs = []
        wtime = 5
        nodes = 512
        jobid = 100
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
            _job['user']          = 'georgerojas'
            _job['state']         = state
            _job['jobid']         = j
            _job['project']       = 'gdr_project'
            _job['notify']        = 'george@therojas.com'
            _job['walltime']      = wtime
            _job['procs']         = nodes
            _job['nodes']         = nodes
            _job['is_active']     = False
            _job['queue']         = 'default'
            _job['mode']          = 'smp'
            _job['errorpath']     = '/Users/georgerojas/mypython'
            _job['errorpath']     = '/Users/georgerojas/mypython'
            _job['outputpath']    = '/Users/georgerojas/mypython'
            _job['user_hold']     = False
            _job['has_completed'] = False
            _job['location']      = '/Users/georgerojas/myphthon'
            _job['submittime']    = 60
            _job['envs']          = ''
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
        ct = 0
        d  = 0
        st = 0
        for res in query:
            ct += 300
            d  += 500
            st += 1000000
            res_list.append({'name':res['name'],'cycle':ct,'duration':d,'start':st})
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
        
