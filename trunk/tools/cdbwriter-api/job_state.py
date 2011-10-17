# job_state.py
#
# cheetah@anl.gov
# r1.0.x
#
# All non-trivial job state processing is done here, including
# wait time calculations, hold status and other job attributes
# which may be derived from job_prog events. Retrieval of job_prog
# events is external to this module.
#
# datetime objects are used for all representation of time
# timedelta objects are used for differential time
# end_window must be a datetime object in the same timezone as other related objects
#
# Two DAOs are instantiated in this module, one each for JOB_EVENTS and JOB_EVENT_CLASSES,
# as the the need for data from those tables is trivial.

import copy
import db2util
import datetime
import sys
from error import error
from job_events import *

##
##
##

class job_prog_error(error):
	def __init__(self, msg, error_list = []):
		self.msg = msg
		self.error_list = error_list
	
class job_prog_soft_error(job_prog_error):
	def __str__(self):
		return ("Job Progress Soft Error: %s" % self.msg)

class job_prog_hard_error(job_prog_error):
	def __str__(self):
		return ("Job Progress Hard Error: %s" % self.msg)

##
##
##

class _analysis_template(object):
	"""Job event analysis container.  Includes methods for basic job state.

	Duration computations for non-terminal jobs are subject to when
	the analysis was performed.  The time used for the 'cutoff' is the
	end_window time, as described in attributes.

	Attributes:
		end_window       - Cutoff for duration calculations if job not terminal (datetime)
		queue_time       - Job queued/created time (datetime)
		start            - Job start time (datetime)
		end              - Last observed terminal event (datetime)
		started          - Did the job ever reach running state? (bool)
		running          - Job presently running? (bool)
		ran              - Did the job ever reach running state? (bool)
		terminal         - Job reached terminal state? (bool)
		failed           - Any failure events observed? (bool)
		events_by_ID     - Map event names by event ID
		state            - Last observed job EVENT_TYPE, by name, except holds (str)
		total_hold       - Total walltime in hold.  Multiple simultaneous do not 'stack' (timedelta)
		holds            - Dictionary of hold data containers by hold event ID
		soft_errors      - List of soft errors found during job event analysis"""

	class __hold_data(object):
		"""Hold data container.  Instantiated for each type of hold per analysis container.

		Attributes:
			count	 - How many times was this hold entered? (int)
			active	 - Is hold presently active? (bool)
			duration - How long in this hold? (timedelta)"""

		def __init__(self):
			self.count = 0							# How many times entering hold?
			self.active = False						# Is hold presently active?
			self.duration = datetime.timedelta(0)	# How long in this hold?

	def __init__(self, events_by_ID, hold_event_IDs):
		# events_by_ID:		{event_ID : event_name} (for debug output and app convenience)
		# hold_event_IDs:	list of hold event IDs

		self.end_window = None					# Cutoff for duration calculations if job not terminal (datetime)
		self.queue_time = None					# Job queued/created (datetime)
		self.start = None						# Job started (datetime)
		self.end = None							# Last observed terminal event (datetime)
		self.running = False					# Job presently running?
		self.ran = False						# Job reached running state?
		self.terminal = False					# Job reached terminal state?
		self.failed = False						# Any failure events observed?
		self.events_by_ID = events_by_ID		# Map event names by event ID
		self.state = None						# Last observed job EVENT_TYPE, by name, except holds (str)
		self.total_hold = datetime.timedelta(0)	# Total walltime in hold.  Multiple simultaneous do not 'stack'
		# Dictionary of hold data containers by hold event ID
		self.holds = dict([(id, self.__hold_data()) for id in hold_event_IDs])
		self.soft_errors = []

	@property
	def started(self):
		"""Did the job reach the starting state? (bool)"""
		return self.start != None

	@property
	def in_hold(self):
		"""Is the job in any kind of hold? (bool)"""

		for hold in self.holds:
			if self.holds[hold].active:
				return True
		return False

	@property
	def total_queued_time(self):
		"""Total time in queue

		datetime.timedelta between creation time and start time
		
		Subject to end_window if job has not started,
		returns None if job went terminal prior to starting (job killed in queue)"""

		if self.terminal and not self.started:
			return None

		# If job has not started, compute from end_window
		if self.start:
			return self.start - self.queue_time
		else:
			if (self.end_window < self.queue_time):
				raise job_prog_hard_error('end_window prior to queue_time')
			return self.end_window - self.queue_time

	@property
	def eligible_queued_time(self):
		"""Total time in queue where job was not in any type of hold (timedelta)
		
		Subject to end_window if job has not started,
		returns None if job went terminal prior to starting (job killed in queue)"""

		if self.terminal and not self.started:
			return None

		#assert (self.total_queued_ti	= self.total_hold)

		return self.total_queued_time - self.total_hold

	@property
	def run_time(self):
		"""Run time:

		datetime.timedelta between the first starting event and the last terminal event

		Subject to end_window if job has not ended, and returns timedelta(0) if job has not started,
		returns None if job went terminal prior to starting (job killed in queue)"""

		if self.terminal and not self.started:
			return None

		if not self.start:
			return datetime.timedelta(0)
		if not self.end:
			if (self.end_window < self.start):
				raise job_prog_hard_error('end_window prior to start time')
			return self.end_window - self.start
		else:
			return self.end - self.start

	def debug(self):
		sys.stderr.write('Queued at:       %s\n' % (self.queue_time))
		sys.stderr.write('Start:           %s\n' % (self.start))
		sys.stderr.write('End:             %s\n' % (self.end))
		sys.stderr.write('End window:      %s\n' % (self.end_window))
		sys.stderr.write('State:           %s\n' % (self.events_by_ID[self.state]))
		sys.stderr.write('Started:         %s\n' % (str(self.started)))
		sys.stderr.write('Running:         %s\n' % (str(self.running)))
		sys.stderr.write('Ran:             %s\n' % (str(self.ran)))
		sys.stderr.write('Failed:          %s\n' % (str(self.failed)))
		sys.stderr.write('Terminal:        %s\n' % (str(self.terminal)))
		sys.stderr.write('Total Queued:    %24s\n' % (self.total_queued_time))
		sys.stderr.write('Total Eligible:  %24s\n' % (self.eligible_queued_time))
		sys.stderr.write('Total Holds:     %24s\n' % (self.total_hold))
		sys.stderr.write('Run Time:        %24s\n' % (self.run_time))
		sys.stderr.write('Hold by type:\n')
		for hold in self.holds:
			sys.stderr.write('[%3d] Hold: %-20s  Count: %2d  Active: %-5s  Duration: %24s\n' % (hold,
																				self.events_by_ID[hold],
																				self.holds[hold].count,
																				str(self.holds[hold].active),
																				self.holds[hold].duration))
		if self.soft_errors:
			sys.stderr.write("WARNING: %d soft error(s) found: %s\n" % (len(self.soft_errors), ', '.join([str(i) for i in self.soft_errors])))

##
## - figure out orphans (will never run)
##

class events(object):
	"""Job events processor"""

	def __init__(self, db, schema):
		"""args:
			db		- db handle
			schema	- schema name where cobaltDB tables reside (str)"""

		self.events_DAO = db2util.dao(db, schema, "JOB_EVENTS")
		self.event_classes_DAO = db2util.dao(db, schema, "JOB_EVENT_CLASSES")

		# Populated in __configure_events():
		self.__by_class = {}			# { event_class : [ event_IDs_for_class ] }
		self.__by_ID = None				# { event_ID : event_name }
		self.__by_name = None			# { event_name : event_ID }
		self.__hold_table = None		# { hold_ID : False } - see note in __configure_events()
		self.__release_table = None		# { hold_ID : release_ID_for_hold_ID }
		self.__configure_events()		# Populate foregoing

		# List of all hold and release IDs
		self.__hold_release_IDs = self.__release_table.keys() + self.__release_table.values()


	# Properties return copies to protect this object's canonical version

	@property
	def by_ID(self):
		"""{ event_ID : event_name }"""
		return copy.copy(self.__by_ID)

	@property
	def by_name(self):
		"""{ event_name : event_ID }"""
		return copy.copy(self.__by_name)

	@property
	def release_table(self):
		"""{ hold_ID : release_ID_for_hold_ID }"""
		return copy.copy(self.__release_table)

	def hold_table(self):
		"""Convenience method: Returns copy of all hold IDs mapped { hold_ID : False }"""
		return copy.copy(self.__hold_table)

	def __configure_events(self):
		# All event names and IDs are assumed to be unique
		#
		# A hold event's corrosponding release name is found
		# by appending HOLD_RELEASE_LABEL

		# Map class 'ID' to class name.  str() for possible unicode conversion
		event_classes = dict([(str(r.v.CLASS), str(r.v.NAME)) for r in self.event_classes_DAO.allRecords()])

		# Validate that the class names we care about exist:
		for class_name in CLASS_NAMES_USED:
			if class_name not in event_classes.values():
				raise job_prog_hard_error('Unable to find job class name %s' % (class_name))

		# Obtain all job_events records
		event_records = self.events_DAO.allRecords()

		# Create and populate __by_class (all IDs for each event class) 
		self.__by_class = dict([(class_name, []) for class_name in event_classes.values()])
		for record in event_records:
			self.__by_class[event_classes[record.v.CLASS]].append(record.v.ID)

		# Job event names by ID
		self.__by_ID = dict([(r.v.ID,r.v.NAME) for r in event_records])
		self.__by_ID[None] = 'Unknown'

		# Job event IDs by name
		self.__by_name = dict([(name, id) for id, name in self.__by_ID.iteritems()])

		# hold_table used as template to track hold state or other hold attributes
		self.__hold_table = dict([(id, False) for id in self.__by_class[E_HOLD]])
			# Map release events to hold by event name

		# release_table allows mapping a hold release to the inital hold event
		# derived by finding each hold's event name + HOLD_RELEASE_LABEL
		self.__release_table = {}

		for id in self.__hold_table.keys():
			self.__release_table[self.__by_name[self.__by_ID[id] + HOLD_RELEASE_LABEL]] = id

	def _state_analysis(self, job_object, end_window, allow_soft_errors = True):
		"""Processes a job event list, determines durations and current job state.

		args:
			job_object - object to analyze.
			                NB.  object prog events must be presorted chronologically
			end_window - datetime used to determine durations of jobs not in terminals state.
			allow_soft_errors	- supress raising an error for soft errors found in job_prog
								  defaults to True
						 
		returns:
			job analysis object"""

		event_list = [(r.v.ENTRY_TIME, r.v.EVENT_TYPE) for r in job_object._prog]

		# Calling this code from anywhere other than user code is not suggested due to soft
		# error handling

		if not event_list:
			raise job_prog_hard_error('No job progress events provided')

		analysis = _analysis_template(self.__by_ID, self.__hold_table.keys())
		analysis.end_window = end_window			# Cutoff for nonterminal jobs
		hold_times = self.hold_table()				# Stores datetime when holds go into effect

		# Stores datetime when first of a series of holds go into effect
		all_hold_dt = None							

		last_event_dt = datetime.datetime.min

		for dt, event in event_list:
			if dt < last_event_dt:
				raise job_prog_hard_error("prog records not in chronological order")
			else:
				last_event_dt = dt

			if not analysis.queue_time:						# Assume first event is when queued
				analysis.queue_time = dt					# Not checking for starting class record as
															# lack of a start record is DOOM, so we'll
															# take what we can get

			if event in self.__by_class[E_TERMINAL]:		# Multiple terminal events possible
				analysis.terminal = True					
				analysis.end = dt							# Record the last observed terminal event

			if event in self.__by_class[E_FAILURE]:			# Record any observed failures
				analysis.failed = True

			if event in self.__by_class[E_RUNNING]:			# Brute force flagging running state
				analysis.running = True
				analysis.ran = True
			else:
				analysis.running = False
				
								# Should not see multiple starts, but account for just in case
								# ... except preemption
			if event in self.__by_class[E_STARTING] and not analysis.start:
				analysis.start = dt
				if analysis.in_hold:						# Hold Cleanup
					if not allow_soft_errors:
						raise job_prog_soft_error("Job started while in hold")

					analysis.soft_errors.append("Job started while in hold")

					# move this code (repeated below as well) into analysis object
					for hold_released in self.__release_table.values():
						if analysis.holds[hold_released].active:
							analysis.holds[hold_released].duration += dt - hold_times[hold_released]
							analysis.holds[hold_released].active = False	# Clear hold flag
							analysis.holds[hold_released].active = False	# Clear datetime this hold started

					assert(all_hold_dt != None)
					analysis.total_hold += dt - all_hold_dt
					all_hold_dt = None
				
			if event not in self.__hold_release_IDs and event != self.__by_name[ALL_HOLDS_CLEAR]:		# Update state if not a hold
				analysis.state = event
			elif not analysis.started:						# process holds if we've not already started
				if event in self.__by_class[E_HOLD]:		# Entering/reasserting hold
					if not all_hold_dt:						# Keep track of total time in hold
						all_hold_dt = dt

					if analysis.holds[event].active:		# Already in that hold
						pass
					else:									# Not in hold already
						hold_times[event] = dt						# Set datetime we started this hold
						analysis.holds[event].active = True			# Flag in hold
						analysis.holds[event].count += 1			# Increment hold counter
				else:										# Exiting hold
					# Check ALL_HOLDS_CLEAR for cleanup
					# All hold releases should be caught, except for dep_failed followed by a modify
					# that clears the dep_fail.  The only indication the dep_hold was released is all_holds_cleared
					if event == self.__by_name[ALL_HOLDS_CLEAR]:
						release_list = self.__release_table.values()		# All release events
					else:
						release_list = [self.__release_table[event]]		# Map release event back to hold event

					for hold_released in release_list:
						if not analysis.holds[hold_released].active:		# Released hold we weren't already in (oops!)
							if event != self.__by_name[ALL_HOLDS_CLEAR]:	# ... unless we're in ALL_HOLDS_CLEAR cleanup
								if allow_soft_errors:
									analysis.soft_errors.append("Invalid hold release - no prior hold found")
								else:
									raise job_prog_soft_error("Invalid hold release - no prior hold found")
						else:												# Add to total time in given hold
							analysis.holds[hold_released].duration += dt - hold_times[hold_released]
							analysis.holds[hold_released].active = False	# Clear hold flag
							hold_times[hold_released] = None				# Clear datetime this hold started
							if not analysis.in_hold:						# Increment total hold duration if no other holds in effect
								analysis.total_hold += dt - all_hold_dt		 
								all_hold_dt = None
			else:											# Invalid state - hold observed after running
				if allow_soft_errors:
					analysis.soft_errors.append("Invalid post-start hold found")
				else:
					raise job_prog_soft_error("Invalid post-start hold found")

		# Account for any unclosed holds:
		if analysis.in_hold:
			for hold in analysis.holds:
				if analysis.holds[hold].active:
					if (end_window < hold_times[hold]):
						raise job_prog_hard_error('end_window prior to start of hold (%s)' % (str(hold)))
					analysis.holds[hold].duration += end_window - hold_times[hold]
			if (end_window < all_hold_dt):
				raise job_prog_hard_error('end_window prior to start of first hold')
			analysis.total_hold += end_window - all_hold_dt
				
		return analysis
