#!/usr/bin/env python
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
import hotshot, hotshot.stats

if __name__ == "__main__":
    stats = hotshot.stats.load("qsim.profile")
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    stats.print_stats(30)
