#!/usr/bin/env python
import hotshot, hotshot.stats

if __name__ == "__main__":
    stats = hotshot.stats.load("qsim.profile")
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    stats.print_stats(30)
