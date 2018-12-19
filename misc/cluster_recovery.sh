#!/bin/bash
# Copyright 2017 UChicago Argonne, LLC. All rights reserved.
# Licensed under a modified BSD 3-clause license. See LICENSE for details.


echo "#!/bin/bash" > recover_cobalt.sh
./mk_queues.py >> recover_cobalt.sh
./mk_nodes.py >> recover_cobalt.sh
./mk_reservations.py >> recover_cobalt.sh
./mk_jobs.py >> recover_cobalt.sh

echo "recover_cobalt.sh created.  Run this file to restore state after upgrade."


