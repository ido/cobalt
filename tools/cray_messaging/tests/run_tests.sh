#!/bin/bash -e

export OLD_PYTHONPATH=$PYTHONPATH
export PYTHONPATH=`pwd`/../lib

nosetests "${@:1}" ./test_cray_messages.py

export PYTHONPATH=$OLD_PYTHONPATH
