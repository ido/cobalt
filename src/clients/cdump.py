#!/usr/bin/env python

'''Cobalt state dump and load command'''
__revision__ = '$Revision: 427 $'
__version__ = '$Version$'

import sys, xmlrpclib, xml.dom.minidom
import Cobalt.Logging, Cobalt.Proxy, Cobalt.Util, Cobalt.Data, Cobalt.Component

__helpmsg__ = 'Usage: cqdump [--dump] [--load xmlfile]'

def get_version():
    '''determines cobalt version from lib imports'''
    version_dict = {('202', '154', '101', '170', '170'):'0.96.2',
                    ('202', '388', '262', '499', '392'):'current'}
    this_version = [x.__revision__.split()[1] for x in Cobalt.Component,
                    Cobalt.Data, Cobalt.Logging, Cobalt.Proxy, Cobalt.Util]
    print 'this version', this_version
    print version_dict[tuple(this_version)]

def get_queues(cqm_conn):
    '''gets queues from cqmConn'''
    info = [{'tag':'queue', 'name':'*', 'state':'*', 'users':'*',
             'maxtime':'*', 'mintime':'*', 'maxuserjobs':'*',
             'maxqueued':'*', 'maxrunning':'*', 'adminemail':'*',
             'totalnodes':'*', 'cron':'*', 'policy':'*', 'stamp':'*'}]
    return cqm_conn.GetQueues(info)

def get_jobs(cqm_conn):
    '''gets jobs from cqm_conn'''
    long_header    = ['JobID', 'JobName', 'User', 'WallTime', 'QueuedTime',
                      'RunTime', 'Nodes', 'State', 'Location', 'Mode', 'Procs',
                      'Queue', 'StartTime', 'Index', 'SubmitTime', 'Path',
                      'OutputDir', 'Envs', 'Command', 'Args', 'Kernel', 'KernelOptions',
                      'Project', 'Stamp']
    query = [{'tag':'job', 'jobid':'*'}]
    for q in query:
        for h in long_header:
            if h == 'JobName':
                q.update({'outputpath':'*'})
            elif h != 'JobID':
                q.update({h.lower():'*'})
    return cqm_conn.GetJobs(query)

def get_partitions(bgsched_conn):
    '''gets all partition info'''
    query = [{'tag':'partition', 'scheduled':'*', 'name':'*', 'stamp':'*',
              'reservations':'*', 'functional':'*', 'queue':'*', 'state':'*',
              'deps':'*', 'db2':'*', 'size':'*'}]
    return bgsched_conn.GetPartition(query)

def maketree(xmlnode, elements):
    '''appends children to xmlnode from members of elements dictionary'''
    for attr in elements:
        newattr = doc.createElement(attr)
        if isinstance(elements.get(attr), bool):
            newtype = "bool"
        elif isinstance(elements.get(attr), int):
            newtype = "int"
        elif isinstance(elements.get(attr), list):
            newtype = "list"
            elements[attr] = xmlrpclib.dumps(tuple(elements.get(attr)))        
        elif isinstance(elements.get(attr), float):
            newtype = "float"
        else:
            newtype = "str"
        newattr.setAttribute("type", newtype)
        xmlnode.appendChild(newattr)
        attrtext = doc.createTextNode(str(elements.get(attr)))
        newattr.appendChild(attrtext)

def makedict(xmlnodes):
    nodelist = []
    for node in xmlnodes[0].childNodes:
        #print job.childNodes
        newdict = {}
        for attr in node.childNodes:
            if not attr.hasChildNodes():
                element_data = ''
            else:
                element_data = attr.childNodes[0].data
#             print attr.nodeName, element_data
            attr_type = attr.getAttribute('type')
            if attr_type == 'bool':
                element_data = bool(element_data)
            elif attr_type == 'int':
                element_data = int(element_data)
            elif attr_type == 'float':
                element_data = float(element_data)
            elif attr_type == 'list':
                # load list data using xmlrpc marshalling
                element_data = list(xmlrpclib.loads(element_data)[0])
            newdict.update({attr.nodeName:element_data})
        nodelist.append(newdict)
    return nodelist

if __name__ == '__main__':
    if '--version' in sys.argv:
        print "cdump %s" % __revision__
        print "cobalt %s" % __version__
        raise SystemExit, 0

    options = {'dump':'dump', 'd':'debug'}
    doptions = {'load':'load'}

    (opts, args) = Cobalt.Util.dgetopt_long(sys.argv[1:], options,
                                            doptions, __helpmsg__)

    if opts['dump'] or not sys.argv[1:]:
        #TODO: check version
#         this_version = get_version()

        #new xml dom
        doc = xml.dom.minidom.Document()
        cobalt_xml = doc.createElement('cobalt')
        doc.appendChild(cobalt_xml)

        try:
            cqm = Cobalt.Proxy.queue_manager()
        except Cobalt.Proxy.CobaltComponentError:
            print "Failed to connect to queue manager"
            raise SystemExit, 1

        #get the next jobid
        try:
            next_jobid = cqm.GetJobID()
            next_jobid_xml = doc.createElement('nextjobid')
            cobalt_xml.appendChild(next_jobid_xml)
            next_jobid_text = doc.createTextNode(str(next_jobid))
            next_jobid_xml.appendChild(next_jobid_text)
        except xmlrpclib.Fault:
            #cqm version must not have GetJobID()
            pass

        #dump queues
        queues = doc.createElement('queues')
        cobalt_xml.appendChild(queues)
        for q in get_queues(cqm):
            newq = doc.createElement('queue')
            queues.appendChild(newq)
            maketree(newq, q)

        #dump jobs
        jobs = doc.createElement('jobs')
        cobalt_xml.appendChild(jobs)
        for job in get_jobs(cqm):
            newjob = doc.createElement('job')
            jobs.appendChild(newjob)
            maketree(newjob, job)

        # make connection to scheduler
        try:
            bgsched = Cobalt.Proxy.scheduler()
        except Cobalt.Proxy.CobaltComponentError:
            print "Failed to connect to scheduler"
            raise SystemExit, 1

        #get partition stuff
        partitions = doc.createElement('partitions')
        cobalt_xml.appendChild(partitions)
        for part in get_partitions(bgsched):
            newpart = doc.createElement('partition')
            partitions.appendChild(newpart)
            maketree(newpart, part)

        #print unformatted xml to stdout
        print doc.toxml()
#         print >>sys.stderr, doc.toprettyxml(indent='    ')

    elif opts['load']:
        #TODO: check version
        
        # make queue manager connection, and fetch current jobs and queues
        try:
            cqm = Cobalt.Proxy.queue_manager()
            current_jobs = cqm.GetJobs([{'tag':'job', 'jobid':'*'}])
            current_queues = cqm.GetQueues([{'tag':'queue', 'name':'*'}])
        except Cobalt.Proxy.CobaltComponentError:
            print "Failed to connect to queue manager"
            raise SystemExit, 1

        # load xml from arguments
        xmldoc = xml.dom.minidom.parse(opts['load'])

        # get queues from xml dom
        queues = xmldoc.getElementsByTagName('queues')
        queuequery = makedict(queues)
        current_queue_names = [cq.get('name') for cq in current_queues]
        existing_queues = [queue for queue in queuequery if queue.get('name') in current_queue_names]
        new_queues = [queue for queue in queuequery if queue.get('name') not in current_queue_names]

        print 'Setting queues:'
        if not opts['debug']:
            response = cqm.AddQueue(new_queues)
            if response:
                for r in response:
                    print 'added %s' % r.get('name')
            else:
                for r in response:
                    print 'failed to add %s' % r.get('name')

        for eq in existing_queues:
            query = [{'tag':'queue', 'name':eq.get('name')}]
            for eq_key in eq.keys():
                if eq_key == 'name' or eq_key == 'tag':
                    del eq[eq_key]
            if not opts['debug']:
                [response] = cqm.SetQueues(query, eq)
                if response:
                    print 'updated %s' % response.get('name')
                else:
                    print 'failed to update %s' % query[0].get('name')

        # get jobs from xml dom
        jobs = xmldoc.getElementsByTagName('jobs')
        jobquery = makedict(jobs)

        current_job_names = [cj.get('jobid') for cj in current_jobs]
        existing_jobs = [job for job in jobquery if job.get('jobid') in current_job_names]
        new_jobs = [job for job in jobquery if job.get('jobid') not in current_job_names]
        print "\nSetting jobs:"
        for jq in new_jobs:
            if not opts['debug']:
                [response] = cqm.AddJob(jq)
                if response:
                    print "added job %s/%s" % (response.get('jobid'), jq.get('user'))
                else:
                    print "failed to add job %s/%s" % (jq.get('jobid'), jq.get('user'))

        for ej in existing_jobs:
            query = [{'tag':'job', 'jobid':ej.get('jobid')}]
            for ej_key in ej.keys():
                if ej_key == 'jobid' or ej_key == 'tag':
                    del ej[ej_key]
            if not opts['debug']:
                [response] = cqm.SetJobs(query, ej)
                if response:
                    print 'updated %s/%s' % (response.get('jobid'), ej.get('user'))
                else:
                    print 'failed to update %s/%s' % (query[0].get('jobid'), ej.get('user'))

        # get next jobid
        nextjobid = xmldoc.getElementsByTagName('nextjobid')
        if nextjobid:
#         print nextjobid[0].childNodes[0].data
            print "\nSetting next jobid:"
            print nextjobid[0].childNodes[0].data
            if not opts['debug']:
                cqm.SetJobID(int(nextjobid[0].childNodes[0].data))

        # restore partitions
        partitions = xmldoc.getElementsByTagName('partitions')
        partquery = makedict(partitions)

        # make scheduler connection, fetch current partitions
        try:
            bgsched = Cobalt.Proxy.scheduler()
            current_partitions = bgsched.GetPartition([{'tag':'partition', 'name':'*'}])
        except Cobalt.Proxy.CobaltComponentError:
            print "Failed to connect to scheduler"
            raise SystemExit, 1

        current_names = [cp.get('name') for cp in current_partitions]
        existing_partitions = [part for part in partquery if part.get('name') in current_names]
        new_partitions = [part for part in partquery if part.get('name') not in current_names]

        print "\nSetting partitions:"
        # new partitions
        if not opts['debug']:
            result = bgsched.AddPartition(new_partitions)
            if result:
                for p in new_partitions:
                    print "added %s" % p.get('name')
            else:
                for p in new_partitions:
                    print "failed to add %s" % p.get('name')
        # existing partitions
        for part in existing_partitions:
            query = [{'tag':'partition', 'name':part.get('name')}]
            for p in part.keys():
                if p == 'tag' or p == 'name':
                    del part[p]
            if not opts['debug']:
                result = bgsched.Set(query, part)
                if result:
                    print 'updated %s' % query[0].get('name')
                else:
                    print 'failed to update %s' % query[0].get('name')
        
