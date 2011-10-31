# select t.job_data_id, t.jobid, t.prog_id, p.event_type from (select max(d.id) as job_data_id, d.jobid, max (p.id) as prog_id from intrepid.job_data as d, intrepid.job_prog as p where d.id = p.job_data_id group by d.jobid) as t, intrepid.job_prog as p where t.prog_id = p.id" (Estimated Cost = 14270.824219) - last state for all jobs

from db2util.helpers import whereIn
from db2util.helpers import commaList

# in days
MAX_RUNNING_WINDOW = 5
MAX_QUEUED_WINDOW = 365

TERMINAL_CLASS = "T"
STARTING_CLASS = "S"
RUNNING_CLASS = "R"
FAILED_CLASS = "F"

##
## Support queries
##

def events_by_class(schema, event):
	return ("""
		select
			ID
		from
			%s.JOB_EVENTS
		where
			class = '%s'
	""" % (schema, event))

##
## Last state for all jobs
##

def last_state_all_jobs(schema):
	# Last state for all jobs
	#
	# Query returns ID, JOB_DATA_ID, JOBID, EVENT_TYPE (where ID is the prog ID)
	return ("""
		select
			t.PROG_ID as ID,
			t.JOB_DATA_ID,
			t.JOBID,
			p.EVENT_TYPE
		from
			(
				select
					max(p.ID) as PROG_ID,
					max(d.ID) as JOB_DATA_ID,
					d.JOBID
				from
					%s.JOB_DATA as d,
					%s.JOB_PROG as p
				where
					d.ID = p.JOB_DATA_ID
				group by
					d.JOBID
			) as t,
			%s.JOB_PROG as p
		where
			t.PROG_ID = p.ID
	""" % (schema, schema, schema))
##
## Queries returning JOB_DATA IDs
##

def data_ids_by_min_jobid(schema, jobid):
	return ("""
		select
			ID
		from
			%s.JOB_DATA
		where
			JOBID >= %s
	""" % (schema, str(jobid)))

def data_ids_by_jobid_subquery(schema, subquery):
	return ("""
		select
			ID
		from
			%s.JOB_DATA
		where
			JOBID in (%s)
	""" % (schema, subquery))

##
## Queries returning JOB IDs
##

def running_jobids(schema):
	return ("""
		select
			t.JOBID
		from
			(%s) as t
		where
			t.EVENT_TYPE in (%s)
	""" % (last_state_all_jobs(schema), events_by_class(schema, RUNNING_CLASS)))
					
def terminal_jobids(schema):
	return ("""
		select
			distinct JOBID
		from
			%s.JOB_PROG_JOBID
		where
			EVENT_TYPE in (%s)
	""" % (schema, events_by_class(schema, TERMINAL_CLASS)))
					
def nonterminal_jobids(schema):
	return ("""
		select
			distinct JOBID
 		from
			%s.JOB_DATA
		where
			JOBID not in (%s)
	""" % (schema, terminal_jobids(schema)))

def active_jobids_by_daterange(schema, start, end):
	# Jobs active between start/end
	return ("""
		select
			distinct JOBID
		from
			%s.JOB_PROG_JOBID
		where
			JOBID in
			(
				select
					JOBID
				from 
					%s.JOB_PROG_JOBID
				where
					EVENT_TYPE in (%s)		-- start events
					and entry_time < '%s'
			) and
			(
				(
					EVENT_TYPE in (%s)		-- terminal events
					and entry_time >= '%s'
				) or
				JOBID in (%s)				-- non-terminal jobs
			)
	""" % (schema,
			schema,
			events_by_class(schema, STARTING_CLASS),
			end,
			events_by_class(schema, TERMINAL_CLASS),
			start,
			nonterminal_jobids(schema)))

##
## More support
##

def prog_by_data_id_subquery(schema, subquery):
	return ("""
		select
			*
		from
			%s.JOB_PROG_JOBID
		where
			JOB_DATA_ID in (%s)
		order by
			JOBID, ENTRY_TIME
	""" % (schema, subquery))

def prog_by_jobid_subquery(schema, subquery):
	return ("""
		select
			*
		from
			%s.JOB_PROG_JOBID
		where
			JOBID in (%s)
		order by
			JOBID, ENTRY_TIME
	""" % (schema, subquery))

def running_prog_records(schema):
	return prog_by_data_id_subquery(schema, data_ids_by_jobid_subquery(schema, running_jobids(schema)))
					
def nonterminal_prog_records(schema):
	return prog_by_data_id_subquery(schema, data_ids_by_jobid_subquery(schema, nonterminal_jobids(schema)))

def prog_by_jobid(schema, jobid):
	if type(jobid) != list:
		job_list = [jobid]
	else:
		job_list = jobid

	return prog_by_data_id_subquery(schema, data_ids_by_jobid_subquery(schema, commaList(job_list)))

def prog_by_min_jobid(schema, jobid):
	return prog_by_data_id_subquery(schema, data_ids_by_min_jobid(schema, jobid))

def prog_by_active_daterange(schema, start, end):
	# start/end in db2 TS format
	return prog_by_jobid_subquery(schema, active_jobids_by_daterange(schema, start, end))
