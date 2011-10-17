import copy
import datetime
import db2util
from db2util.helpers import toList
from db2util.helpers import enum
from db2util import SRCHCMP

DATA_LOAD = db2util.helpers.enum("DATA_LOAD_TYPE", [	"NONE",
														"LAST",
														"LAST_SUMMARY",
														"ALL",
														"ALL_SUMMARY" ] )
DATA_LOAD_DEFAULT = DATA_LOAD.LAST_SUMMARY

# objects common to jobs and reservations

def default_end_window():
	return datetime.datetime.now()

class data_child_table_dao(db2util.dao):
	def __init__(self, db, tableSchema, tableName, dataID_field_name):
		super(data_child_table_dao, self).__init__(db, tableSchema, tableName)
		self.dataID_field_name = dataID_field_name

	def by_data_id(self, data_id):
		return self.searchFields([(self.dataID_field_name, SRCHCMP.IN, toList(data_id))])

class _jr_obj(object):
	# _prog list must always be sorted chronologically
	def __init__(self, cobaltid, prog_callback, data_callback, analysis_callback, fk_fieldname, defer_prog_load = False):
		self.cobaltid = cobaltid
		self._prog = []
		self._prog_callback = prog_callback
		self._data = {}									# Should *not* be used outside this funtion (use _data_record instead)
		self._data_callback = data_callback
		self._analysis_callback = analysis_callback
		self._data_fk_field = fk_fieldname
		self._last_analysis = None
		self._last_analysis_dt = datetime.datetime.min

		if not defer_prog_load:
			self._refresh_prog()

	def __getattr__(self, name):
		if name.upper() == 'ID':
			return self._last_prog.valueByName('ID')

		if name.upper() in self._last_prog.fieldNames:
			return self._last_prog.valueByName(name.upper())

		if name.upper() in self._last_data.fieldNames:
			# Force db load if asking for non-summary field
			if self._last_data.s.partial_load and name not in self._last_data.s.partial_fields:
				self.refresh()

			return self._last_data.valueByName(name.upper())

		raise AttributeError("object '_jr_obj' has no attribute '%s'" % (name))

	@property
	def dynamic_attrs(self):
		return [str(f) for f in self._last_prog.fieldNames + self._last_data.fieldNames]

	@property
	def valid(self):
		if self._prog:
			return True
		return False

	@property
	def _last_data(self):
		return self._data_record(self._last_data_id)

	@property
	def _last_prog(self):
		return self._prog[-1]

	@property
	def _last_data_id(self):
		return self._prog[-1].valueByName(self._data_fk_field)

	@property
	def prog_changed(self):
		test_prog = self._prog_callback(self.cobaltid)
		return (test_prog == self._prog)

	def purge_data(self):
		self._data = self._data.fromkeys(self._data.keys())

	def refresh(self, reanalyze = True):
		self._refresh_prog()
		# Force next request for most recent data to be reloaded
		# Consider using purge_data instead to knock over all data
		self._data[self._last_data_id] = None

		if reanalyze:
			# Rerun analysis
			if self._last_analysis:
				self.analysis(self._last_analysis_dt)

	def _bulk_load(self, prog_records, data_records = {}):
		# Use with 'defer_prog_load'
		# data dictionary need not be complete
		self._refresh_prog(prog_records)
		self._data.update(data_records)

	def _data_record(self, data_id):
		if not self._data[data_id]:
			self._data[data_id] = self._data_callback(data_id)

		return self._data[data_id]
		
	def _get_prog(self):
		return self._prog_callback(self.cobaltid)

	def _refresh_prog(self, prog_records = []):
		if prog_records:
			self._prog = copy.copy(prog_records)
		else:
			self._prog = self._get_prog()

		for r in self._prog:
			if r.valueByName(self._data_fk_field) not in self._data:
				self._data[r.valueByName(self._data_fk_field)] = None

	def analysis(self, end_window = None, **kwargs):
		if end_window:
			# We used to check if end_window has changed since last call
			# This doesn't work so well, as calling function may ask for analysis refresh
			# with same end_window
			self._last_analysis_dt = end_window

			self._last_analysis = self._analysis_callback(self, end_window, **kwargs)
		else:
			if not self._last_analysis:
				raise Exception('analysis() method not previously called with end_window')

		return self._last_analysis

class _jr_dao(db2util.dao):
	# children need self.prog and self.data daos defined
	# self.prog needs	: self.prog.cobaltid
	#					: self.prog.active_by_daterange

	class __record_container(object):
		# Stores a related set of progress record objects and data record objects
		def __init__(self, prog_set, data_set = {}):
			self.prog_set = prog_set
			self.data_set = data_set

	# converting bulk records to sets by resid/jobid requires knowledge of table structure
	# otherwise _process_bulk really ought to be in the wrangler

	def _process_bulk_prog(self, bulk_prog_records):
		# Given a list of progress record objects, return the dictionary:
		# { cobaltid : [ prog, prog... ] }

		# self._C_ID_NAME is field name for cobaltid (eg, RESID/JOBID)

   		prog_set = {}

		for record in bulk_prog_records:
			if record.valueByName(self._C_ID_NAME) not in prog_set:
				prog_set[record.valueByName(self._C_ID_NAME)] = [record]
			else:
				prog_set[record.valueByName(self._C_ID_NAME)].append(record)

		return prog_set

	def _process_bulk_data(self, bulk_data_records):
		# Given a list of data record objects, return the dictionary:
		# { cobaltid : { record.ID : record, record.ID : record... } }

		# self._C_ID_NAME is field name for cobaltid (eg, RESID/JOBID)

		data_set = {}

		for record in bulk_data_records:
			if record.valueByName(self._C_ID_NAME) not in data_set:
				data_set[record.valueByName(self._C_ID_NAME)] = {}
			data_set[record.valueByName(self._C_ID_NAME)][record.id] = record

		return data_set

	def _last_data_id_for_prog_set(self, prog_set):
		# given a prog set, return a list containing the last data record ID for
		# every cobaltid in the prog set.

		# *** RECORDS WITHIN PROG SET MUST BE SORTED CHRONOLOGICALLY ***

		data_ids = []

		for cobaltid in prog_set:
			data_ids.append(prog_set[cobaltid][-1].valueByName(self._DATA_FK_FIELD))

		return data_ids

	def _all_data_ids_for_prog_set(self, prog_set):
		# given a prog set, return a detuplicated list containing all data record IDs

		data_ids = []

		# iteritems variety was hard to read!
		for cobaltid in prog_set:
			data_ids.extend([record.valueByName(self._DATA_FK_FIELD) for record in prog_set[cobaltid]])

		return list(set(data_ids))

	def get_data(self, prog_set, data_load = DATA_LOAD.LAST):
		# given a prog_set, return a data_set

		# Entirely possible for get_data to be called with an empty prog_set
		# If so, pass in empty result set to _process_bulk_data for compatiblity
		if prog_set:
			# Need all data rows or just last data rows?
			if data_load in [DATA_LOAD.ALL, DATA_LOAD.ALL_SUMMARY]:
				data_row_IDs = self._all_data_ids_for_prog_set(prog_set)
			else:
				data_row_IDs = self._last_data_id_for_prog_set(prog_set)
	
			data_records = self.data.getID(data_row_IDs, data_load)
		else:
			data_records = {}
	
		return self._process_bulk_data(data_records)
				

	def _finalize_prog_set(self, prog_set, data_load = DATA_LOAD.NONE):
		# Appears to associate data with progress records
		# perhaps where to put standard fields requiring computation?

		if data_load == DATA_LOAD.NONE:
			return self.__record_container(prog_set, {})
		else:
			return self.__record_container(prog_set, self.get_data(prog_set, data_load))

	def cobaltid(self, cobaltid, data_load = DATA_LOAD.NONE):
		# given list or single cobaltid (jobid/resid), return a record container
		# for given cobaltid(s).  Data records optional.

		prog_set = self._process_bulk_prog(self.prog.cobaltid(cobaltid))

		return self._finalize_prog_set(prog_set, data_load)

	def active_by_daterange(self, start_DT, end_DT, data_load):
		# API side expects python DT object; db2 expects timestamps
		start = db2util.DTtoTS(start_DT)
		end = db2util.DTtoTS(end_DT)

		prog_set = self._process_bulk_prog(self.prog.active_by_daterange(start, end))
		return self._finalize_prog_set(prog_set, data_load)

class _wrangler(object):
	# Adapts cobalt concepts and methods to database DAOs
	# DAOs should return prog and data sets, this class returns cobalt objects
	# DAOs must define the following:
	# self._DATA_FK_FIELD = 'JOB_DATA_ID'			# FK field name from Prog -> Data

	# Children need to define the following:
	# self.dao = job_dao.job_dao(db, schema)
	# self._cobalt_object = _job_obj				# Class to instantiate new cobalt object
	# self._analysis = self.events._state_analysis	# Method to call for analysis, if any (otherwise None)

	# General strategy for creating cobalt objects:
	# - Use DAO method to return raw data in record container format
	# - Record container provides prog records and optionally one or more data records
	# - Use _load_cobalt_objects to create cobalt objects and populate with available data
	#
	# While creating a cobalt object without any prog or data records is possible, most searches
	# for the desired record(s) would return prog/data anyway.  Might as well keep those rows
	# and populate right away

	def _load_cobalt_objects(self, raw_data):
		# Given a prog_set, return a list of cobalt objects loaded with prog records
		# Also load data record(s) if provided

		prog = raw_data.prog_set	# { cobaltid : [ prog, prog... ] }
		data = raw_data.data_set	# { cobaltid : { record.ID : record, record.ID : record... } }

		cobalt_objects = []

		for cobaltid in prog:
			cobalt_objects.append(self._cobalt_object( cobaltid,					# cobalt ID (jobid/resid)
														self.dao.prog.cobaltid,		# callback to load prog records by cobaltid
														self.dao.data.getID,		# callback to load data records by data row ID
														self._analysis,				# callback for analysis
														self.dao._DATA_FK_FIELD,	# FK field name from Prog -> Data
														defer_prog_load = True))	# Defer loading progress data (no autoload)

			# Bulk load progress records, and optionally data records if they were supplied
			if cobaltid in data:
				cobalt_objects[-1]._bulk_load(prog[cobaltid], data[cobaltid])
			else:
				cobalt_objects[-1]._bulk_load(prog[cobaltid])

		return cobalt_objects

	def _run_analysis(self, cobalt_objects, end = None, **kwargs):
		# perform analysis() on a list of cobalt_objects
		# returns passed list for convenience

		if not end:
			end = default_end_window()

		for o in cobalt_objects:
			o.analysis(end, **kwargs)
		
		return cobalt_objects

	def cobaltid(self, cobaltid, data_load = DATA_LOAD.NONE):
		return self._load_cobalt_objects(self.dao.cobaltid(cobaltid, data_load))

	def active_by_daterange(self, start_DT, end_DT, data_load = DATA_LOAD_DEFAULT):
		# Must specify a valid end_DT

		cobalt_objects = self._load_cobalt_objects(self.dao.active_by_daterange(start_DT, end_DT, data_load))

		return self._run_analysis(cobalt_objects, default_end_window())
