#!/bin/bash +x

#Script to copy files to bblogin

#copy source code to site packages and dist packages

COBALT_PATH=$HOME/cobalt/trunk

COBALT_COMP_PATH=$COBALT_PATH/src/lib/Components
COBALT_REFERENCE_PATH=$COBALT_PATH/src/components

COBALT_MISC_PATH=$HCOBALT_PATH/misc/Heckle

SYSTEM_LIB_PATH=/usr/lib/python2.6/site-packages/Cobalt
SYSTEM_COMP_PATH=$SYSTEM_LIB_PATH/Components
SYSTEM_DATATYPES_PATH=$SYSTEM_COMP_PATH/DataTypes

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

sudo cp $COBALT_MISC_PATH/heckle_forker.py $SYSTEM_COMP_PATH/heckle_forker.py
echo "Did $component"
sudo cp $COBALT_MISC_PATH/heckle_sched.py $SYSTEM_COMP_PATH/heckle_sched.py
echo "Did $component"
sudo cp $COBALT_MISC_PATH/heckle_temp_Data.py $SYSTEM_LIB_PATH/heckle_temp_Data.py
echo "Did $component"
sudo cp $COBALT_MISC_PATH/heckle_temp_ProcessGroup.py $SYSTEM_DATATYPES_PATH/lib/DataTypes/
echo "Did $component"


for component in
     sudo cp $COBALT_MISC_PATH/$component $SYSTEM_BIN_PATH/$component
     sudo chmod +x $SYSTEM_BIN_PATH/$component
     echo "Did reference $component"
done

cp $COBALT_MISC_PATH/step2a.sc $HOME/step2a.sc