"""Cobalt process manager."""

import logging

from Cobalt.Data import Job, Data, DataDict, IncrID, DataCreationError
from Cobalt.Proxy import ComponentProxy, ComponentLookupError
from Cobalt.Components.base import Component, exposed, automatic, query


__all__ = ["Job", "JobDict", "ProcessManager"]

logger = logging.getLogger(__name__)


class Job (Job):
    
    def __init__ (self, spec):
        for key in ["id", "user", "size", "executable", "cwd", "location"]:
            if "key" not in spec:
                raise DataCreationError("required key '%s' missing" % key)
        Data.__init__(self, spec)


class JobDict (DataDict):
    
    item_cls = Job
    key = "id"


class ProcessManager (Component):
    
    """Generic implementation of process-manager
    
    Methods:
    add_jobs -- add jobs to the process manager (exposed)
    get_jobs -- query jobs from the process manager (exposed)
    wait_jobs -- return and remove finished jobs (exposed)
    signal_jobs -- send a signal to jobs (exposed)
    check_jobs -- finish jobs that are no longer running on the system (automatic)
    """
    
    name = "process-manager"
    
    logger = logger

    def __init__ (self, **kwargs):
        Component.__init__(self, **kwargs)
        self.jobs = JobDict()
    
    def add_jobs (self, specs):
        """Add a job to the process manager."""
        self.logger.info("add_jobs(%r)" % (specs))
        jobs = self.jobs.q_add(specs)
        system_specs = \
            ComponentProxy("system").add_jobs([job.to_rx() for job in jobs])
        for system_spec in system_specs:
            job = self.jobs[system_spec['id']]
            job.state = "running"
        return jobs
    add_jobs = exposed(query(add_jobs))
    
    def get_jobs (self, specs):
        """Query jobs from the process mananger."""
        self.logger.info("get_jobs(%r)" % (specs))
        return self.jobs.q_get(specs)
    get_jobs = exposed(query(get_jobs))
    
    def wait_jobs (self, specs):
        """Removes and returns jobs that have finished."""
        self.logger.info("wait_jobs(%r)" % (specs))
        specs = [spec.copy() for spec in specs]
        for spec in specs:
            spec['state'] = "finished"
        return self.jobs.q_del(specs)
    wait_jobs = exposed(query(wait_jobs))
    
    def signal_jobs (self, specs, signame="SIGTERM"):
        """Send a signal to existing job processes."""
        self.logger.info("signal_jobs(%r, %r)" % (specs, signame))
        return ComponentProxy("system").signal_jobs(specs, signame)
    signal_jobs = exposed(signal_jobs)

    def check_jobs (self):
        """Finish jobs that are no longer running on the system."""
        self.logger.info("check_jobs()")
        local_job_specs = [job.to_rx(["id"]) for job in self.jobs.values() if job.state != 'finished']
        try:
            system_job_specs = ComponentProxy("system").get_jobs(local_job_specs)
        except ComponentLookupError:
            self.logger.error("check_jobs() [unable to contact system]")
            return
        system_job_ids = [spec['id'] for spec in system_job_specs]
        for job in self.jobs.values():
            if job.id not in system_job_ids and job.state != "finished":
                job.state = "finished"
    check_jobs = automatic(check_jobs)
