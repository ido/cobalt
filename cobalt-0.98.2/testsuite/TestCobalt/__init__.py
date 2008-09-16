import tempfile

import Cobalt

fd, config_file = tempfile.mkstemp()
open(config_file, "w").write("""
[bgpm]
mpirun: /usr/bin/mpirun

[cqm]
log_dir: /tmp
bgkernel: false

[bgsched]
utility_file: /tmp/asdf
""")

Cobalt.CONFIG_FILES = [config_file]
