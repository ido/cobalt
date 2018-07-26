#!/usr/bin/env python
import os
import sys
import time
import uuid
import logging
import Cobalt
from Cobalt.Components.base import run_component
from Cobalt.Components.base import Component, exposed, automatic, locking
from Cobalt.Proxy import ComponentProxy
from Cobalt.Server import XMLRPCServer
from Cobalt.Server import find_intended_location
from Cobalt.Util import get_config_option

logger = logging.getLogger('hammer')


class Hammer(Component):
    """Hammer"""
    name = 'hammer'
    implementation = __name__.split('.')[-1]
    logger = logger

    def __init__(self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)

    def loop(self):
        self.logger.info("Hammer Time!")
        count = 1
        # ComponentProxy("service-location").unregister(self.name)
        # ComponentProxy("service-location").register(self.name, self.url)
        while count > 0:
            #component_name = "service-location"
            #slp = ComponentProxy(component_name)
            #address = slp.locate(component_name)
            #self.logger.info("Got reference to the %s: %s", component_name, slp)
            #address = slp.locate(self.name)
            nail = ComponentProxy('nail')
            self.logger.info("Got reference to the nail: %s", nail)
            id = nail.get_an_id()
            self.logger.info("Got newly minted hammer with serial number %s.  Filing off serial number...", id)
            count -= 1

    # The locking decorator as named is somewhat misleading.  It indicates that the specified function is responsible for
    # explicitly acquiring the base component mutex, as needed, and that the base component mutex will not automatically be
    # acquired on on its behalf before the function is called.  The decorator is used here to eliminate the deadlock between
    # loop() and get_and_id(), which loop() calls via RPC.
    loop = locking(automatic(loop, period=0.05))
    #loop = automatic(loop, period=0.1)

def main():
    from threading import Thread
    class WorkThread(Thread):
        def __init__(self):
            self.done = False
            Thread.__init__(self)

        def run(self):
            time.sleep(10)
            while not self.done:
                logger.info("work starts!")
                nail = ComponentProxy('nail')
                logger.info("Got reference to the nail: %s", nail)
                nail.do_work()
                logger.info("work done!")
            logger.info("works complete!")
            return

    thread = WorkThread()
    thread.start()

    run_component(Hammer, register=True, time_out=10.0, sleeptime=0.0)
    thread.done = True
    thread.join()

if __name__ == "__main__":
    main()
