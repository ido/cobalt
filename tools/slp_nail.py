#!/usr/bin/env python
import os
import sys
import time
import uuid
import logging
import random
import Cobalt
from Cobalt.Components.base import run_component
from Cobalt.Components.base import Component, exposed, automatic, locking
from Cobalt.Proxy import ComponentProxy
from Cobalt.Server import XMLRPCServer
from Cobalt.Server import find_intended_location
from Cobalt.Util import get_config_option

logger = logging.getLogger('nail')


class Nail(Component):
    """Nail"""
    name = 'nail'
    implementation = __name__.split('.')[-1]
    logger = logger

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)

    def get_an_id(self):
        """Generate a new ID"""
        self.logger.info("Nail.get_an_id() called")
        id = uuid.uuid4().hex
        self.logger.info("Nail.get_an_id() returning id %s", id)
        return id
    get_an_id = locking(exposed(get_an_id))

    def do_work(self):
        """Work!"""
        self.logger.info("Starting Work")
        worktime = 100000000
        for x in range(worktime):
            uuid.uuid4().hex
            random.random()
        self.logger.info("Ending Work")
    do_work = locking(exposed(do_work))

def main():
    run_component(Nail, register=True, time_out=10.0, sleeptime=0.0)

if __name__ == "__main__":
    main()
