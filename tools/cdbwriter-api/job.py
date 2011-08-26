import jr_common
import job_dao
import job_state
from jr_common import DATA_LOAD
from jr_common import DATA_LOAD_DEFAULT

##
## todo:  possible to call for analysis with no _prog
## -- entire dynamic _prog should be transparent
##


class job_wrangler(jr_common._wrangler):
	def __init__(self, db, schema):
		self.events = job_state.events(db, schema)		# Analysis class, required below

		# Required by parent class:
		self.dao = job_dao.job_dao(db, schema)			# DAO for res related tables
		self._cobalt_object = jr_common._jr_obj			# job object
		self._analysis = self.events._state_analysis	# analysis function

	@property
	def summary_fields(self):
		return self.dao.data.summary_fields

	def set_summary_fields(self, field_list):
		self.dao.data.set_summary_fields(field_list)
		
	def jobid(self, jobid, data_load = DATA_LOAD_DEFAULT):
		return self.cobaltid(jobid, data_load)

	def running(self, data_load = DATA_LOAD_DEFAULT):
		return self._run_analysis(self._load_cobalt_objects(self.dao.running(data_load)))

	def nonterminal(self, data_load = DATA_LOAD_DEFAULT):
		return self._run_analysis(self._load_cobalt_objects(self.dao.nonterminal(data_load)))

	def min_jobid(self, jobid, data_load = DATA_LOAD_DEFAULT):
		return self._run_analysis(self._load_cobalt_objects(self.dao.min_jobid(jobid, data_load)))
