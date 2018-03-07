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

[system]
size: 10
elogin_hosts: foo:bar
""")
fp.close()

Cobalt.CONFIG_FILES = [config_file]
