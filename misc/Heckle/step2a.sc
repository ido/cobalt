#!/bin/bash +x

#Script to copy files to bblogin

#copy source code to site packages and dist packages


COBALT_COMP_PATH=$HOME/cobalt/trunk/src/lib/Components

COBALT_REFERENCE_PATH=$HOME/cobalt/trunk/src/components

SYSTEM_COMP_PATH=/usr/lib/python2.6/site-packages/Cobalt/Components

SYSTEM_BIN_PATH=/usr/local/bin

cd ~/cobalt/trunk
svn update
cd ~

for component in heckle_system.py heckle_system2.py heckle_processgroup.py heckle_lib.py heckle_resource.py; do
     sudo cp $COBALT_COMP_PATH/$component $SYSTEM_COMP_PATH/$component
     echo "Did $component"
done

for component in heckle_system.py heckle_system2.py; do
     sudo cp $COBALT_REFERENCE_PATH/$component $SYSTEM_BIN_PATH/$component
     sudo chmod +x $SYSTEM_BIN_PATH/$component
     echo "Did reference $component"
done
