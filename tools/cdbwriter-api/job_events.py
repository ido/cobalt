# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.
HOLD_RELEASE_LABEL = '_release'		# literal found at end of event name for release events
ALL_HOLDS_CLEAR = 'all_holds_clear'

# Literal Event CLASS Names
# Used as constants instead of dict for code clarity
E_STARTING = 'Starting'
E_RUNNING = 'Running'
E_TERMINAL = 'Terminal'
E_HOLD = 'Hold'
E_FAILURE = 'Failure'

# Should include all E_* constants, used for validation
CLASS_NAMES_USED = [E_STARTING, E_RUNNING, E_TERMINAL, E_HOLD, E_FAILURE]
