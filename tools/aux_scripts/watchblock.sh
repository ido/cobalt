#!/bin/bash

LOG=$HOME/cron/log/watchblock.log
MSG=$HOME/cron/log/message_$(date +"%F-%T_TZ%z")
cdate=$(date)
LOCK=$HOME/cron/log/watchblock.lock
CONSOLE_CMDS=/tmp/$$.bgcons

#
# try lock, exit if locked
#
(
flock -x -n 200
if [ $? -ne 0 ];
then
    echo "$cdate : script locked" >> $LOG
    exit 1;
fi

#
# connect to db
#
/dbhome/bgqsysdb/sqllib/bin/db2 connect to bgdb0 user bgqsysdb using db24bgq > /dev/null
if [ $? -ne 0 ];
then
    echo "$cdate : db connection failed" >> $LOG
    exit 1
fi

count=$(/dbhome/bgqsysdb/sqllib/bin/db2 -x "select count(*) from bgqnode where status='F'")
if [ $count -gt 0 ];
then
    query=$(/dbhome/bgqsysdb/sqllib/bin/db2 "select * from bgqnode where status='F'")

    echo "Total: $count nodes found in failed state" > $MSG
    echo "Query Results:" >> $MSG
    echo "$query" >> $MSG
    echo "Recovery Action:" >> $MSG

    jobs=$(/dbhome/bgqsysdb/sqllib/bin/db2 -x "select id from bgqjob")
    if [ -n "$jobs" ]
    then
	echo "select_block R00-M0-N00-128"  >> $CONSOLE_CMDS
	for job in $jobs
	do
	    echo "kill_job $job" >> $CONSOLE_CMDS
	done
    fi
    cat $HOME/cron/recover_block.cmds >> $CONSOLE_CMDS
    cat $CONSOLE_CMDS >> $MSG
    echo "Command Results" >> $MSG 
    /bgsys/drivers/ppcfloor/bin/bg_console -e < $CONSOLE_CMDS >> $MSG 2>&1
    rm $CONSOLE_CMDS
    echo "$cdate : block reset : $? : $MSG" >> $LOG
fi

#
# disconnect from db
#
/dbhome/bgqsysdb/sqllib/bin/db2 disconnect bgdb0 > /dev/null

) 200>$LOCK

exit 0
