#!/usr/bin/env python

"""Sender to test re-transmit code. 

Should cause timeouts and multiple unacknowledged message transmissions

"""

from time import sleep
from Cobalt.Components.base import Component, run_component, exposed, automatic
from Cobalt.Proxy import ComponentProxy

class RetransSend(Component):

    name = "RetSend"
    implementation = "RetSend"

    def __init__ (self, *args, **kwargs):

        Component.__init__(self, *args, **kwargs)
        self.count = 0
    

    def sendMessage(self):

        self.count += 1
        print "Sending Message: seq %d" % self.count
        ComponentProxy("RetRecv", defer=False, retry=False).catchMessage("messgae %d caught." % self.count)

    sendMessage = automatic(sendMessage, 10)


if __name__ == "__main__":
    try:
        run_component(RetransSend)
    except KeyboardInterrupt:
        sys.exit(1)
