#!/bin/bash -xe

SITE_ADDR=$1
SITE_PATH=$2
mkdir -p ./html
for FILE_PATH in ${@:3}
do
  FILE=$( basename $FILE_PATH )
  echo $FILE
  man2html -H $SITE_ADDR -M /$SITE_PATH -p $FILE_PATH  | sed -r 's/'${SITE_PATH}'\/([A-Za-z0-9]+)\+([A-Za-z0-9]+)/'${SITE_PATH}'\/\2.\1.html/' > ./html/${FILE}.html
done
