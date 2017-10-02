import tempfile
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.

import Cobalt

fd, config_file = tempfile.mkstemp()
fp = open(config_file, "w")
fp.write("""
[bgpm]
mpirun: /usr/bin/mpirun

[bgsystem]
bgkernel: false

[cqm]
log_dir: /tmp

[bgsched]
utility_file: /dev/null
""")
fp.close()

Cobalt.CONFIG_FILES = [config_file]
