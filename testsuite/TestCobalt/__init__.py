import tempfile

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
