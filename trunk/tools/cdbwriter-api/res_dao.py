import db2util
import jr_common
from jr_common import DATA_LOAD
import res_sql
from db2util.helpers import list_to_str
from db2util.helpers import toList
from db2util.helpers import fromList
from db2util.helpers import intToBool
from db2util import SRCHCMP

class data_dao(db2util.dao):
	def __init__(self, db, schema):
		self.db = db

		metaoverride = {"PARTS":	{	"validator":	self.validate_parts },
						"USERS":	{	"validator":	self.validate_users }}

		self.table = db2util.table(db, schema, "RESERVATION_DATA", metaoverride)
		self.parts_dao = jr_common.data_child_table_dao(db, schema, "RESERVATION_PARTS", "RES_DATA_ID")
		self.users_dao = jr_common.data_child_table_dao(db, schema, "RESERVATION_USERS", "RES_DATA_ID")

	# override parent method for TS-DT conversion
	def processSQL(self, SQL, SQLargs = tuple()):
		rList = super(data_dao, self).processSQL(SQL, SQLargs)

		db2util.helpers.cvtRecordsTStoDT(rList)

		return rList

	def validate_parts(self, value, meta):
		if type(value) != list:
			return False

		for item in value:
			if type(item) not in [str, unicode]:
				return False

		return True

	def validate_users(self, value, meta):
		if type(value) != list:
			return False

		for item in value:
			if type(item) not in [str, unicode]:
				return False

		return True

	def __get_virtual(self, record):
		id = record.v.ID

		record.v.PARTS = [r.v.NAME for r in self.parts_dao.by_data_id(id)]
		record.v.USERS = [r.v.NAME for r in self.users_dao.by_data_id(id)]

	def getID(self, id, data_load = None):
		# data_load exists for compatibility with calls in jr_common
		# reservation records are small enough that we always load all fields from a data row

		search_id = toList(id)

		results = super(data_dao, self).getID(search_id, table = self.table)

		if results:
			for record in results:
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
		raise Exception('update not yet implemented')
		# 

	def insert(self, record):
		raise Exception('insert not yet implemented')
		# TODO: This should be an atomic operation
		# id = db2util.dao.insert(self, record)
		# self.insertVirtualFields(record)

class prog_dao(db2util.dao):
	def __init__(self, db, schema):
		super(prog_dao, self).__init__(db, schema, "RESERVATION_PROG_RESID")

	# override parent method for TS-DT conversion
	def processSQL(self, SQL, SQLargs = tuple()):
		rList = super(prog_dao, self).processSQL(SQL, SQLargs)

		db2util.helpers.cvtRecordsTStoDT(rList)

		return rList

	def cobaltid(self, resid):
		return self.searchFields([("RESID", SRCHCMP.IN, toList(resid))], orderSet = [("ENTRY_TIME", "+")])

	def active(self):
		SQL = res_sql.active_prog_records(self.table.schema)
		return self.processSQL(SQL)

	def nonterminal(self):
		SQL = res_sql.nonterminal_prog_records(self.table.schema)
		return self.processSQL(SQL)

	def active_by_daterange(self, start, end):
		SQL = res_sql.prog_by_active_daterange(self.table.schema, start, end)
		return self.processSQL(SQL)

	def all(self):
		return self.searchFields([("ID", SRCHCMP.GTE, [0])], orderSet = [("ENTRY_TIME", "+")])

class res_dao(jr_common._jr_dao):
	def __init__(self, db, schema):
		self.db = db
		self.schema = schema
		self.data = data_dao(self.db, self.schema)
		self.prog = prog_dao(self.db, self.schema)
		self._C_ID_NAME = "RESID"
		self._DATA_FK_FIELD = "RES_DATA_ID"

	def active(self):
		prog_set = self._process_bulk_prog(self.prog.active())
		return self._finalize_prog_set(prog_set, DATA_LOAD.ALL)

	def nonterminal(self):
		prog_set = self._process_bulk_prog(self.prog.nonterminal())
		return self._finalize_prog_set(prog_set, DATA_LOAD.ALL)

	def all(self):
		prog_set = self._process_bulk_prog(self.prog.all())
		return self._finalize_prog_set(prog_set, DATA_LOAD.ALL)
