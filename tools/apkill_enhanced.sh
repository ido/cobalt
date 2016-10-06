#!/bin/bash
# For those times when politely asking an applicaiton to terminate isn't
# sufficient.  This first sends the passed signal through to apkill, then waits
# 5 minutes for termination. Then sends another apkill -SIGKILL.  This is as big
# a hammer as we have for termination.


apkill_cmd='/opt/cray/alps/default/bin/apkill'
apstat_cmd='/opt/cray/alps/default/bin/apstat'
if [[ "$#" -lt "2" ]]
then
  echo "Usage: enhanced_apkill -[signal] [pidlist]"
  exit 1
fi

$apkill_cmd $1 ${@:2}
sleep 300
for apid in ${@:2}
do
  found_apid=`awk "/$apid/ {print \\$0}" <((apstat -a $apid 2> /dev/null))`
  if [ -n "$found_apid" ]
  then
    echo Sending SIGKILL to $apid
    $apkill_cmd -9 $apid
  fi
done
