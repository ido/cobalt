from db2util.helpers import whereIn
from db2util.helpers import commaList

# comma separated string literals

STARTING_EVENTS = "'activating'"
# TODO: released events don't record deactivating, 'released' should be removed when bug fixed
ENDING_EVENTS = "'deactivating', 'released'"
# cobaltDB writer isn't inserting terminated events in cycling reservations
# need to fix db manually
#TERMINAL_EVENTS = "'deferred', 'terminated'"
TERMINAL_EVENTS = "'terminated'"

def last_state_all_reservations(schema):
	# Last state for all reservations
	#
	# Query returns ID, RES_DATA_ID, RESID, EVENT_TYPE (where ID is the prog ID)
	return ("""
		select
			t.PROG_ID as ID,
			t.RES_DATA_ID,
			t.RESID,
			p.EVENT_TYPE
		from
			(
				select
					max(p.ID) as PROG_ID,
					max(d.ID) as RES_DATA_ID,
					d.RESID
				from
					%s.RESERVATION_DATA as d,
					%s.RESERVATION_PROG as p
				where
					d.ID = p.RES_DATA_ID
				group by
					d.RESID
			) as t,
			%s.RESERVATION_PROG as p
		where
			t.PROG_ID = p.ID
	""" % (schema, schema, schema))

def res_ids_by_event_list(schema, event_list):
	# single numeric event id or list of ids
	return ("""
		select
			t1.RESID
		from
			(%s) as t1
		where
			t1.EVENT_TYPE in (%s)
	""") % (last_state_all_reservations(schema), commaList(event_list))

def prog_by_data_field(schema, field, values):
	# single numeric resid or list of resids
	return("""
		select
			p.*,
			d.RESID
		from
			%s.RESERVATION_PROG as p,
			(
				select
					ID,
					RESID
				from
					%s.RESERVATION_DATA
				where
					%s in (%s)
			) as d
		where
			p.RES_DATA_ID = d.ID
		order by
			p.ENTRY_TIME
	""") % (schema, schema, field, commaList(values))

def prog_by_resid(schema, resid):
	return prog_by_data_field(schema, "RESID", resid)

def prog_by_dataid(schema, dataid):
	return prog_by_data_field(schema, "RES_DATA_ID", dataid)

def prog_by_current_event(schema, event_list):
	return prog_by_resid(schema, res_ids_by_event_list(schema, event_list))

def prog_by_resid_subquery(schema, subquery):
	return ("""
		select
			*
		from
			%s.RESERVATION_PROG_RESID
		where
			RESID in (%s)
		order by
			RESID, ENTRY_TIME
	""" % (schema, subquery))

def events_by_name(schema, event_names):
    return ("""
		select
			ID
		from
			%s.RESERVATION_EVENTS
		where
			name in (%s)
	""" % (schema, event_names))

def active_resids(schema):
	return ("""
		select
			distinct RESID
		from
			%s.RESERVATION_PROG_RESID
		where
			EVENT_TYPE in (%s)
			and RESID not in
			(
				select
					RESID
				from
					%s.RESERVATION_PROG_RESID
				where
					EVENT_TYPE in (%s)
			)
	""" % (schema,
			events_by_name(schema, STARTING_EVENTS),
			schema,
			events_by_name(schema, ENDING_EVENTS + ',' + TERMINAL_EVENTS)))

# BUG WORKAROUND (TODO: REMOVE)
# ENDING_EVENTS also includes TEMRINAL_EVENTS as cobalt is failing to write out deactivated records on release

def nonterminal_resids(schema):
	return ("""
		select
			distinct RESID
		from
			%s.RESERVATION_DATA
		where
			RESID not in
			(
				select
					RESID
				from
					%s.RESERVATION_PROG_RESID
				where
					EVENT_TYPE in (%s)		-- terminal events (deferred/terminated)
			)
	""" % (schema, schema, events_by_name(schema, TERMINAL_EVENTS)))
	
def active_resids_by_daterange(schema, start, end):
	# Reservations active between start/end
	return ("""
		select
			distinct RESID
		from
			%s.RESERVATION_PROG_RESID
		where
			RESID in
			(
				select
					RESID
				from 
					%s.RESERVATION_PROG_RESID
				where
					EVENT_TYPE in (%s)		-- start events
					and ENTRY_TIME < '%s'
			) and
			(
				(
					EVENT_TYPE in (%s)		-- ending events
					and ENTRY_TIME >= '%s'
				) or
				RESID in (%s)				-- still active reservations
			)
	""" % (schema,
			schema,
			events_by_name(schema, STARTING_EVENTS),
			end,
			events_by_name(schema, ENDING_EVENTS),
			start,
			active_resids(schema)))

def prog_by_active_daterange(schema, start, end):
	# start/end in db2 TS format
	return prog_by_resid_subquery(schema, active_resids_by_daterange(schema, start, end))

def active_prog_records(schema):
	return prog_by_resid_subquery(schema, active_resids(schema))

def nonterminal_prog_records(schema):
	return prog_by_resid_subquery(schema, nonterminal_resids(schema))
