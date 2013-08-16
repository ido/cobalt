#!/usr/bin/env python

import signal
import sys
import time

if __name__ == "__main__":

    #Ignore the sigterm signal
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

    time.sleep(float(sys.argv[1]))

