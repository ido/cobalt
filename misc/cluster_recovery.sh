#!/bin/bash


echo "#!/bin/bash" > recover_cobalt.sh
./mk_queues.py >> recover_cobalt.sh
./mk_nodes.py >> recover_cobalt.sh
./mk_reservations.py >> recover_cobalt.sh
./mk_jobs.py >> recover_cobalt.sh

echo "recover_cobalt.sh created.  Run this file to restore state after upgrade."


