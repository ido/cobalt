#!/bin/bash

#This is going to require a reorg to be run afterwards.

DATABASE=$1
USER=$2
PASS=$3
SCHEMA=$4

db2 "connect to $DATABASE user $USER using $PASS"
#future proofing changes: Blue Gene max is 255 for Q, however, no garuntee that this doesn't change
#This is based on a Linux argument limit
db2 "ALTER TABLE $SCHEMA.JOB_DATA ADD COLUMN ION_KERNEL CLOB(4096)"
db2 "ALTER TABLE $SCHEMA.JOB_DATA ADD COLUMN ION_KERNELOPTIONS CLOB(4096)"
#Dimensionality can be contained in 13 characters at this point.  16 seems a bit more sane for
#future
db2 "ALTER TABLE $SCHEMA.JOB_DATA ADD COLUMN GEOMETRY VARCHAR(16)"
#A Bool, a Bool, my kingdom for a bool.
db2 "ALTER TABLE $SCHEMA.RESERVATION_DATA ADD COLUMN BLOCK_PASSTHROUGH INTEGER"
db2 terminate
