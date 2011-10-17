#!/bin/csh

source cobalt-db-config

set FILE = "cobalt-db-ddl"
set SOURCE = "${FILE}.src"
set OUTPUT = "${FILE}.sql"

if ( "x${TABLESPACE}" == "x" ) then
    set TABLESPACE_STR = ""
else
    set TABLESPACE_STR = 'IN "'"${TABLESPACE}"'"'
endif

echo "Creating ${OUTPUT}.  With correctly set db2 environment (is db2cshrc"
echo "or db2profile sourced?), run:"
echo "\ndb2 -tf ${OUTPUT}\n"

sed -e "s/##COBALT_SCHEMA##/${COBALT_SCHEMA}/g" \
    -e "s/##DATABASE##/${DATABASE}/g" \
    -e "s/##TABLESPACE##/${TABLESPACE_STR}/g" \
    -e "s/##DB_ADMIN##/${DB_ADMIN}/g" \
    -e "s/##RO_SUPPORT##/${RO_SUPPORT}/g" \
    -e "s/##RO_USER##/${RO_USER}/g" \
    -e "s/##COBALT_USER##/${COBALT_USER}/g"  $SOURCE > ${OUTPUT}
