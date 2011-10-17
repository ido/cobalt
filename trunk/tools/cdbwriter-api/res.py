import jr_common
import res_state
import res_dao
from jr_common import DATA_LOAD
from jr_common import DATA_LOAD_DEFAULT

class res_wrangler(jr_common._wrangler):
	def __init__(self, db, schema):
		self.events = res_state.events(db, schema)				# Analysis class, required below

		# Required by parent class:
		self.dao = res_dao.res_dao(db, schema)					# DAO for res related tables
		self._cobalt_object = jr_common._jr_obj					# reservation object
		self._analysis = self.events._state_analysis			# analysis function

	def _run_analysis(self, cobalt_objects, end = None, user_segment = False):
		return super(res_wrangler, self)._run_analysis(cobalt_objects, end, segment_on_user_change = user_segment)

	def cobaltid(self, cobaltid, data_load = DATA_LOAD.ALL):
		return super(res_wrangler, self).cobaltid(cobaltid, data_load)

	def resid(self, resid, data_load = DATA_LOAD.ALL):
		return self.cobaltid(resid, data_load)

	def active(self):
		return self._load_cobalt_objects(self.dao.active())

	def nonterminal(self):
		return self._load_cobalt_objects(self.dao.nonterminal())

	def all(self):
		return self._run_analysis(self._load_cobalt_objects(self.dao.all()))
