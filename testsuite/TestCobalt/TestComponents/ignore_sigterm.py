#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

import signal
import sys
import time

if __name__ == "__main__":

    #Ignore the sigterm signal
    signal.signal(signal.SIGTERM, signal.SIG_IGN)

    time.sleep(float(sys.argv[1]))

