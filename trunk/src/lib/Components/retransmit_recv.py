#!/usr/bin/env python

"""Reciever to test re-transmit code. 

Should cause timeouts and multiple unacknowledged message transmissions

"""

from time import sleep, ctime
from Cobalt.Components.base import Component, run_component, exposed, automatic

class RetransRecv(Component):

    name = "RetRecv"
    implementation = "RetRecv"

    def __init__ (self, *args, **kwargs):

        Component.__init__(self, *args, **kwargs)
    
    @exposed
    def catchMessage(self, msg):
        
        #sleep(30)
        print "I got a message: %s" % msg
        #raise RuntimeError("BQQM!")


    def delay(self):
        print "starting sleep cycle"
        print ctime()
        sleep(300)
        #i = 0
        #while(i < 100000000):
        #     i += 1.0
        print "sleep cycle complete"
        print ctime()
    #delay = automatic(delay, 10)

if __name__ == "__main__":
    try:
        run_component(RetransRecv, single_threaded=True)
    except KeyboardInterrupt:
        sys.exit(1)
