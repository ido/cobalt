#!/bin/sh

msg_error()
{
    echo ""
    echo "ERROR: $*"
    echo ""
    exit 1
}

if test -z "$PYTHON_EXE" ; then
    export PYTHON_EXE=""
fi

if test -z "${COBALT_SOURCE_DIR}" ; then
    msg_error "ERROR: COBALT_SOURCE_DIR not set."
fi

if test -z "${COBALT_RUNTIME_DIR}" ; then
    msg_error "COBALT_RUNTIME_DIR not set."
fi

if test ! -d ${COBALT_SOURCE_DIR}/src/Cobalt ; then
    msg_error "$COBALT_SOURCE_DIR/src/Cobalt does not exist."
fi

if test -n "$1" ; then
    partlist_file=$1
else
    partlist_file="$COBALT_RUNTIME_DIR/etc/partlist.txt"
fi

if test ! -f $partlist_file && [ $partlist_file != 'all' ] ; then
    msg_error "$partlist_file does not exist."
fi

$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/partadm.py -d '*'

if [ $partlist_file == 'all' ] ; then
    $PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/partadm.py -a '*'
    $PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/partadm.py --enable '*'
    $PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/partadm.py --activate '*'
else
    for p in `cat $partlist_file` ; do
	$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/partadm.py -a $p
	$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/partadm.py --enable $p
	$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/partadm.py --activate $p
    done
fi

$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/partadm.py -l

$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/cqadm.py --delq default
$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/cqadm.py --addq default
$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/cqadm.py --start default
$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/cqadm.py --getq
$PYTHON_EXE $COBALT_SOURCE_DIR/src/clients/cqstat.py -q
