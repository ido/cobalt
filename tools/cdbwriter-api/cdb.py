import job
import res

class cobaltDB(object):
	def __init__(self, db, schema):
		self.schema = schema
		self.db = db

		self.job = job.job_wrangler(self.db, schema)
		self.res = res.res_wrangler(self.db, schema)
