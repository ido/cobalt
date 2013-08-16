# res_state.py
#
# cheetah@anl.gov
#
# All non-trivial res state processing is done here
# Retrieval of prog events is external to this module.
#
# datetime objects are used for all representation of time
# timedelta objects are used for differential time
# end_window must be a datetime object in the same timezone as other related objects
#
# One DAO is instantiated in this module for RES EVENTS
# as the the need for data from those tables is trivial.

import copy
import db2util
import datetime
import sys
from error import error
from db2util import helpers

# Literal Event Names
# Used as constants instead of dict for code clarity
E_CREATING = 'creating'
E_ACTIVATING = 'activating'
E_TERMINATED = 'terminated'
E_CYCLING = 'cycling'
E_MODIFYING = 'modifying'
E_DEFERRED = 'deferred'
E_DEACTIVATING = 'deactivating'
E_RELEASED = 'released'

##
##
##

class res_prog_error(error):
	def __init__(self, msg, error_list = []):
		self.msg = msg
		self.error_list = error_list
	
class res_prog_soft_error(res_prog_error):
	def __str__(self):
		return ("Job Progress Soft Error: %s" % self.msg)

class res_prog_hard_error(res_prog_error):
	def __str__(self):
		return ("Job Progress Hard Error: %s" % self.msg)

##
##
##

class _mod_history(object):
	"""Reservation modification segment.

	Each occasion a reservation is modified is represented by a _mod_history object.
	Examining these objects in sequence allows determining how a reservation was
	changed in low level detail.
	
	Attributes:
		dt         - datetime modification was made
		user       - username responsible for modification

	Available yet extremely low level attributes:
		data_record   - raw db2util reservation data record associated with this segement"""

	def __init__(self, dt, user, record):
		self.dt = dt
		self.user = user
		self.data_record = record

class _analysis_template(object):
	"""Reservation event analysis container.  Includes methods for basic reservation state.

	Duration computations for non-terminal jobs are subject to when
	the analysis was performed.  The time used for the 'cutoff' is the
	end_window time, as described in attributes.

	Attributes:
		end_window            - Cutoff for duration calculations if reservation not terminal (datetime)
		segments              - List of reservation segment objects (see _res_segment docs)
		modify_history        - List of reservation modification objects (see _mod_history docs)
		created               - datetime reservation was created
		creator               - who created reservation
		end_user              - who (if anyone) released or deferred reservation
		first_requested_start - datetime reservation was originally requested to begin
		start                 - datetime reservation actually first started
		last_requested_start  - datetime reservation was ultimatly requested to begin
		requested_end         - datetime reservation was ultimatly requested to end
		end                   - datetime reservation last ended
		discontiguous         - Was the reservation's active duration discontiguous? (bool)
		cycled                - Was the reservation created by cycling? (bool)
		ever_active           - Was the reservation ever active? (bool)
		active                - Is the reservation active? (bool)
		deferred              - Was the reservation ended by deferral? (bool) *
		released              - Was the reservation ended by release? (bool)
		terminal              - Is the reservation terminal? (bool)
		active_time           - Total active duration (timedelta)      
		soft_errors           - List of soft errors found during event analysis

	* If a cycling reservation has yet to go active and is deferred, the pre-active
	deferral on its own will not cause the deferred attribute to be True"""

	def __init__(self, events_by_ID):
		# events_by_ID:		{event_ID : event_name} (for debug output and app convenience)

		self.end_window = None					# Cutoff for duration calculations if not terminal (datetime)
		self.segments = []
		self.modify_history = []
		self.created = None
		self.creator = None
		self.end_user = None
		self.first_requested_start = None
		self.last_requested_start = None
		self.discontiguous = False
		self.cycled = False
		self.ever_active = False
		self.active = False
		self.deferred = False					# Likely depricated
		self.released = False
		self.terminal = False
		self.duration = None
		self.soft_errors = []

	@property
	def start(self):
		if self.segments:
			return self.segments[0].start
		else:
			return None

	@property
	def end(self):
		if self.segments:
			return self.segments[-1].end
		else:
			return None

	@property
	def active_time(self):
		td = datetime.timedelta(0)

		for s in self.segments:
			if s.end:
				td += s.end - s.start
			else:
				td += self.end_window - s.start

		return td
		#return helpers.TDtoSec(td)

	@property
	def requested_end(self):
		return self.last_requested_start + self.requested_duration

	def _update(self, event_record, data_record):
		self.last_requested_start = data_record.v.START
		self.requested_duration = datetime.timedelta(seconds = data_record.v.DURATION)

		self.modify_history.append(_mod_history(event_record.v.ENTRY_TIME, event_record.v.EXEC_USER, data_record))

	def debug(self):
		sys.stderr.write('Created at:               %s\n' % (self.created))
		sys.stderr.write('Creator:                  %s\n' % (self.creator))
		sys.stderr.write('First Requested Start:    %s\n' % (self.requested_start))
		sys.stderr.write('First Start:              %s\n' % (self.start))
		sys.stderr.write('Requested End:            %s\n' % (self.requested_end))
		sys.stderr.write('Last End:                 %s\n' % (self.end))
		sys.stderr.write('Ended by:                 %s\n' % (self.end_user))
		sys.stderr.write('Requested Duration:       %s\n' % (self.requested_duration))
		sys.stderr.write('Actual Duration:          %s\n' % (self.active_time))
		sys.stderr.write('Discontiguous?            %s\n' % (self.discontiguous))
		sys.stderr.write('Created by cycle?         %s\n' % (self.cycled))
		sys.stderr.write('Active?                   %s\n' % (self.active))
		sys.stderr.write('Ever Active?              %s\n' % (self.ever_active))
		sys.stderr.write('Ended by defferal?        %s\n' % (self.deferred))
		sys.stderr.write('Ended by release?         %s\n' % (self.released))
		sys.stderr.write('Terminal?                 %s\n' % (self.terminal))

		for s in self.segments:
			s.debug()

		for r in self.modify_history:
			sys.stderr.write("Modify Record %d: %s by %s\n" % (r.data_record.v.ID, r.dt, r.user))
			#r.data_record.stdout()

		if self.soft_errors:
			sys.stderr.write("WARNING: %d soft error(s) found: %s\n" % (len(self.soft_errors), ', '.join([str(i) for i in self.soft_errors])))

class _res_segment(object):
	"""Reservation segment container.

	Reservations may be modified to change effective time, users and partitions during
	the lifetime of a reservation.  Each distinct timespan with consistent attributes
	is represented as a segment.  A simple reservation which is created, eventually starts
	then ends with no futher modification will only have one segment.

	Attributes:
		start         - datetime this segment starts
		end           - datetime this segment ends
		end_window    - end_window used for duration computation
		exec_user     - username (if any) responsible for modification resulting in new segment
		discontiguous - does this segement start discontiguous to the prior segment?
		duration      - duration for this segment (timedelta)
		partitions    - list of partitions for this segment
		user_list     - list of users for this segment

	Available yet extremely low level attributes:

		data_ID       - reservation data record ID associated with this segment
		data_record   - raw db2util reservation data record associated with this segement"""

	def __init__(self, start_DT, exec_user, data_record, end_window, discontiguous = False):
		self.start = start_DT
		self.end = None
		self.end_window = end_window
		self.exec_user = exec_user
		self.data_record = data_record
		self.discontiguous = discontiguous

	@property
	def duration(self):
		if self.end:
			return self.end - self.start
		else:
			return self.end_window - self.start

	@property
	def partitions(self):
		return self.data_record.v.PARTS

	@property
	def user_list(self):
		return self.data_record.v.USERS

	@property
	def data_ID(self):
		return self.data_record.v.ID

	def _set_end(self, dt, new_segment = False):
		# new_segment indicates passed dt is actually start of a new
		# segmenent.  Apply logic to avoid overlapping segment times
		if new_segment:
			if self.start == dt:
				self.end = dt
			else:
				#self.end = dt - datetime.timedelta.resolution
				self.end = dt
		else:
			self.end = dt

	def debug(self):
		if self.discontiguous:
			flag = "*D*"
		else:
			flag = "   "
		sys.stderr.write('  %s %s -> %s @ %s (users: %s) (by: %s)\n' % (flag, self.start, self.end, helpers.commaList(self.partitions, ':'), helpers.commaList(self.user_list, ':'), self.exec_user))

class events(object):
	"""Reservation events processor"""

	def __init__(self, db, schema):
		"""args:
			db		- db handle
			schema	- schema name where cobaltDB tables reside (str)"""

		self.events_DAO = db2util.dao(db, schema, "RESERVATION_EVENTS")

		# Populated in __configure_events():
		self.__by_ID = None				# { event_ID : event_name }
		self.__by_name = None			# { event_name : event_ID }
		self.__configure_events()		# Populate foregoing

	# Properties return copies to protect this object's canonical version

	@property
	def by_ID(self):
		"""{ event_ID : event_name }"""
		return copy.copy(self.__by_ID)

	@property
	def by_name(self):
		"""{ event_name : event_ID }"""
		return copy.copy(self.__by_name)

	def __configure_events(self):
		# All event names and IDs are assumed to be unique

		# TODO - validate event names
		# Validate that the class names we care about exist:
		#for class_name in CLASS_NAMES_USED:
		#	if class_name not in event_classes.values():
		#		raise res_prog_hard_error('Unable to find job class name %s' % (class_name))

		# Obtain all event records
		event_records = self.events_DAO.allRecords()

		# Event names by ID
		self.__by_ID = dict([(r.v.ID,r.v.NAME) for r in event_records])
		self.__by_ID[None] = 'Unknown'

		# Event IDs by name
		self.__by_name = dict([(name, id) for id, name in self.__by_ID.iteritems()])

	def _state_analysis(self, res_object, end_window, allow_soft_errors = True, segment_on_user_change = False):
		"""Processes a reservation event list.

		args:
			res_object - res object to analyze
			             res object prog events must be presorted chronologically
			end_window - datetime used to determine durations of jobs not in terminals state.
			allow_soft_errors	- supress raising an error for soft errors found in job_prog
								  defaults to True
						
		returns:
			reservation analysis object"""

		# Calling this code from anywhere other than user code is not suggested due to soft
		# error handling

		# ENTRY_TIMES exepected to be converted to DT on db read

		if not res_object._prog:
			raise res_prog_hard_error('No reservation progress events')

		# Force progress records into chronological order
		#res_object._prog.sort(key = lambda prog_rec: prog_rec.v.ENTRY_TIME)

		analysis = _analysis_template(self.__by_ID)
		analysis.end_window = end_window			# Cutoff for nonterminal reservations

		last_event_dt = datetime.datetime.min

		for event_record in res_object._prog:
			if event_record.v.ENTRY_TIME < last_event_dt:
				raise res_prog_hard_error("prog records not in chronological order")
			else:
				last_event_dt = event_record.v.ENTRY_TIME

			event_type = event_record.v.EVENT_TYPE
			data_record = res_object._data_record(event_record.v.RES_DATA_ID)

			if event_type == self.__by_name[E_CREATING]:
				analysis.created = event_record.v.ENTRY_TIME
				analysis.creator = event_record.v.EXEC_USER
				analysis.requested_start = data_record.v.START
				analysis._update(event_record, data_record)

			# Cycling events are the equivalent of the create event for cycling reservations
			elif event_type == self.__by_name[E_CYCLING]:
				analysis.created = event_record.v.ENTRY_TIME
				analysis.creator = event_record.v.EXEC_USER
				analysis.requested_start = data_record.v.START
				analysis.cycled = True
				analysis._update(event_record, data_record)

			elif event_type == self.__by_name[E_ACTIVATING]:
				# Possible to have multiple activating events in reservation (eg, start modified into future)
				if analysis.ever_active:
					analysis.discontiguous = True
					analysis.segments.append(_res_segment(event_record.v.ENTRY_TIME, event_record.v.EXEC_USER, data_record, end_window, discontiguous = True))
				else:
					analysis.ever_active = True
					analysis.segments.append(_res_segment(event_record.v.ENTRY_TIME, event_record.v.EXEC_USER, data_record, end_window, discontiguous = False))
				
				analysis.active = True

			elif event_type == self.__by_name[E_MODIFYING]:
				analysis._update(event_record, data_record)
				if analysis.active:
					# Create new segment only if reservation geometry or user list changed
					if analysis.segments[-1].partitions != data_record.v.PARTS or \
						(segment_on_user_change and set(analysis.segments[-1].user_list) != set(data_record.v.USERS)):
						analysis.segments[-1]._set_end(event_record.v.ENTRY_TIME, new_segment = True)
						analysis.segments.append(_res_segment(event_record.v.ENTRY_TIME,  event_record.v.EXEC_USER, data_record, end_window))

			elif event_type == self.__by_name[E_DEFERRED]:
				if analysis.ever_active:
					analysis.deferred = True
					analysis.end_user = event_record.v.EXEC_USER

				# Deferred cycling reservations won't have a terminal event until released on a future resid
				# ^^^ that is a bug.  All reservation instances need a terminal event, even if it's followed
				# by cycling a new reservation.  Otherwise it really breaks reservations which haven't yet
				# activated getting deferred into the future
				# analysis.terminal = True

			elif event_type == self.__by_name[E_DEACTIVATING]:
				if analysis.active:
					analysis.segments[-1]._set_end(event_record.v.ENTRY_TIME, new_segment = False)
				else:
					if allow_soft_errors:
						analysis.soft_errors.append("Deactivated event found while not active")
					else:
						raise res_prog_soft_error("Deactivated event found while not active")

				analysis.active = False

			elif event_type == self.__by_name[E_RELEASED]:
				analysis.released = True
				analysis.end_user = event_record.v.EXEC_USER

			elif event_type == self.__by_name[E_TERMINATED]:
				analysis.terminal = True
				
				# TODO: Remove after bugfix
				# cdbwriter doesn't generate deactiving event on release

				if analysis.active:
					analysis.segments[-1]._set_end(event_record.v.ENTRY_TIME, new_segment = False)
					if allow_soft_errors:
						analysis.soft_errors.append("Terminated without prior deactivation")
					else:
						raise res_prog_soft_error("Terminated without prior deactivation")

					analysis.active = False

			else:
				raise res_prog_hard_error("Unknown event in res analysis")

		return analysis
