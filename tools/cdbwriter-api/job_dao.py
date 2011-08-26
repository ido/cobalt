import db2util
import jr_common
import job_sql
from db2util.helpers import list_to_str
from db2util.helpers import toList
from db2util.helpers import fromList
from db2util.helpers import intToBool
from db2util import SRCHCMP
from jr_common import DATA_LOAD

####
####
#### Todo: what to do about fields not in summary when summary load was performed
####
####
####


# ****** Ensure SQL sorts by chronological order

class data_dao(db2util.dao):
	def __init__(self, db, schema):
		self.db = db

		metaoverride = {"ATTR":		{	"validator":	self.validate_attr },
						"DEPS":		{	"validator":	self.validate_deps },
						"RUN_USERS":{	"validator":	self.validate_run_users }}

		self.table = db2util.table(db, schema, "JOB_DATA", metaoverride)
		self.attr_dao = jr_common.data_child_table_dao(db, schema, "JOB_ATTR", "JOB_DATA_ID")
		self.deps_dao = jr_common.data_child_table_dao(db, schema, "JOB_DEPS", "JOB_DATA_ID")
		self.run_users_dao = jr_common.data_child_table_dao(db, schema, "JOB_RUN_USERS", "JOB_DATA_ID")

		self.summary_fields = [	'ID',
								'JOBID',
								'JOB_TYPE',
								'JOB_USER',
								'WALLTIME',
								'PROCS',
								'NODES',
								'PROJECT',
								'LOCATION',
								'MODE',
								'QUEUE',
								'DEP_FRAC',
								'COMMENT',
								'RESID',
								'EXIT_STATUS' ]

	def set_summary_fields(self, field_list):
		if not set(field_list).issubset(set(['ID', 'JOBID'])):
			raise ValueError("Field List for set_summary_fields must contain 'ID' and 'JOBID'")

		if not set(field_list).issubset(set(self.summary_fields)):
			raise ValueError("Field List for set_summary_fields contains an unknown field name")

		self.summary_fields = field_list

	def validate_attr(self, value, meta):
		if type(value) != dict:
			return False

		# We'll coerce dictionaries into strings on insert/update

		#for k, v in value.iteritems()
		#	if type(k) not in [str, unicode] or type(v) not in [str, unicode]:
		#		return False

		return True

	def validate_deps(self, value, meta):
		# Deps: { dep_on_id (int) : satisfied (bool) }
		if type(value) != dict:
			return False

		for dep_on_id, satisfied in value.iteritems():
			if type(dep_on_id) not in [int, long] or type(satisfied) != bool:
				return False

		return True

	def validate_run_users(self, value, meta):
		if type(value) != list:
			return False

		for item in value:
			if type(item) not in [str, unicode]:
				return False

		return True

	def __get_virtual(self, record):
		id = record.v.ID		# TODO:  Use primaryKey()?

		record.v.ATTR = dict([(r.v.KEY, r.v.VALUE) for r in self.attr_dao.by_data_id(id)])
		record.v.DEPS = dict([(int(r.v.DEP_ON_ID), intToBool(r.v.SATISFIED)) for r in self.deps_dao.by_data_id(id)])
		record.v.RUN_USERS = [r.v.USER_NAME for r in self.run_users_dao.by_data_id(id)]

	def getID(self, id, data_load = DATA_LOAD.ALL):
		# default is ALL to indicate full load desired by default
		search_id = toList(id)

		if data_load in [DATA_LOAD.LAST_SUMMARY, DATA_LOAD.ALL_SUMMARY]:
			results = super(data_dao, self).getID(search_id, self.summary_fields, self.table)
		else:
			results = super(data_dao, self).getID(search_id, "*", self.table)

		if results:
			for record in results:
				if data_load not in [DATA_LOAD.LAST_SUMMARY, DATA_LOAD.ALL_SUMMARY]:
					self.__get_virtual(record)
				
		if type(id) == list:
			return results
		else:
			if results:
				return results[-1]
			else:
				return None

	def delete(self, record):
		raise Exception('delete not yet implemented')
		# 

	def update(self, record):
		# remember to cast k & v to str in attrs
		raise Exception('update not yet implemented')
		# 

	def insert(self, record):
		# remember to cast k & v to str in attrs
		raise Exception('insert not yet implemented')
		# TODO: This should be an atomic operation
		# id = db2util.dao.insert(self, record)
		# self.insertVirtualFields(record)


class prog_dao(db2util.dao):
	def __init__(self, db, schema):
		super(prog_dao, self).__init__(db, schema, "JOB_PROG_JOBID")

	# override parent method for TS-DT conversion
	def processSQL(self, SQL, SQLargs = tuple()):
		rList = super(prog_dao, self).processSQL(SQL, SQLargs)

		db2util.helpers.cvtRecordsTStoDT(rList)

		return rList

	def cobaltid(self, jobid):
		return self.searchFields([("JOBID", SRCHCMP.IN, toList(jobid))], orderSet = [("ENTRY_TIME", "+")])

	def active_by_daterange(self, start, end):
		SQL = job_sql.prog_by_active_daterange(self.table.schema, start, end)
		return self.processSQL(SQL)

	def running(self):
		SQL = job_sql.running_prog_records(self.table.schema)
		return self.processSQL(SQL)

	def nonterminal(self):
		SQL = job_sql.nonterminal_prog_records(self.table.schema)
		return self.processSQL(SQL)

	def min_jobid(self, jobid):
		SQL = job_sql.prog_by_min_jobid(self.table.schema, jobid)
		return self.processSQL(SQL)

class job_dao(jr_common._jr_dao):
	def __init__(self, db, schema):
		self.db = db
		self.schema = schema
		self.data = data_dao(self.db, self.schema)
		self.prog = prog_dao(self.db, self.schema)
		self._C_ID_NAME = "JOBID"
		self._DATA_FK_FIELD = 'JOB_DATA_ID'             # FK field name from Prog -> Data

	def running(self, data_load):
		prog_set = self._process_bulk_prog(self.prog.running())
		return self._finalize_prog_set(prog_set, data_load)

	def nonterminal(self, data_load):
		prog_set = self._process_bulk_prog(self.prog.nonterminal())
		return self._finalize_prog_set(prog_set, data_load)

	def min_jobid(self, jobid, data_load):
		prog_set = self._process_bulk_prog(self.prog.min_jobid(jobid))
		return self._finalize_prog_set(prog_set, data_load)
