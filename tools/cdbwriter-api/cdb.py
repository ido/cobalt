import job
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
import res

class cobaltDB(object):
	def __init__(self, db, schema):
		self.schema = schema
		self.db = db

		self.job = job.job_wrangler(self.db, schema)
		self.res = res.res_wrangler(self.db, schema)
