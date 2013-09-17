#!/bin/sh

msg_error()
{
    echo ""
    echo "ERROR: $*"
    echo ""
    exit 1
}

msg_warn()
{
    echo "WARNING: $*"
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

if test -z "${COBALT_CONFIG_FILES}" ; then
    msg_error "COBALT_CONFIG_FILES not set."
fi

if test ! -d "${COBALT_SOURCE_DIR}/src/Cobalt" ; then
    msg_error "$COBALT_SOURCE_DIR/src/Cobalt does not exist."
fi

PYTHONPATH="${COBALT_SOURCE_DIR}/src:${PYTHONPATH}"
export PYTHONPATH

case $COBALT_SYSTEM_TYPE in
    EAS)
	components="slp user_script_forker bg_runjob_forker system_script_forker cqm bgqsystem bgsched"
	if test ! -f ${COBALT_SOURCE_DIR}/src/components/simulator.xml ; then
	    msg_error "${COBALT_SOURCE_DIR}/src/components/simulator.xml does not exist."
	fi
	;;
    BG)
	components="slp user_script_forker bg_mpirun_forker system_script_forker cqm bgsystem bgsched"
	if test -f ${COBALT_RUNTIME_DIR}/lib/libsched.so ; then
	    LD_LIBRARY_PATH="${COBALT_RUNTIME_DIR}/lib:${LD_LIBRARY_PATH}"
	    export LD_LIBRARY_PATH
	else
	    msg_warn "${COBALT_RUNTIME_DIR}/lib/libsched.so does not exist."
	fi

	if test ! -d /bgsys/drivers/ppcfloor/lib64 ; then
	    msg_error "/bgsys/drivers/ppcfloor/lib64 does not exist."
	fi
	LD_LIBRARY_PATH=/bgsys/drivers/ppcfloor/lib64:${LD_LIBRARY_PATH}
	export LD_LIBRARY_PATH
	MPIRUN_VERBOSE=2
	export MPIRUN_VERBOSE
	;;
    BGSIM)
	components="slp user_script_forker bg_mpirun_forker system_script_forker cqm brooklyn bgsched"
	if test ! -f ${COBALT_SOURCE_DIR}/src/components/simulator.xml ; then
	    msg_error "${COBALT_SOURCE_DIR}/src/components/simulator.xml does not exist."
	fi
	;;
    DA)
	components="slp bgforker cluster_system bgsched scriptm"
	;;
    "")
	msg_error "COBALT_SYSTEM_TYPE not set."
	;;
    *)
	msg_error "${COBALT_SYSTEM_TYPE} is not a supported system type."
	;;
esac

if test ! -f "${COBALT_RUNTIME_DIR}/etc/cobalt.conf" ; then
    msg_error "${COBALT_RUNTIME_DIR}/etc/cobalt.conf does not exist."
fi
mkdir "${COBALT_RUNTIME_DIR}/var" >/dev/null 2>&1
mkdir "${COBALT_RUNTIME_DIR}/var/log" >/dev/null 2>&1
mkdir "${COBALT_RUNTIME_DIR}/var/log/cobalt" >/dev/null 2>&1
mkdir "${COBALT_RUNTIME_DIR}/var/run" >/dev/null 2>&1
mkdir "${COBALT_RUNTIME_DIR}/var/run/cobalt" >/dev/null 2>&1
mkdir "${COBALT_RUNTIME_DIR}/var/spool" >/dev/null 2>&1
mkdir "${COBALT_RUNTIME_DIR}/var/spool/cobalt" >/dev/null 2>&1
mkdir "${COBALT_RUNTIME_DIR}/tmp" >/dev/null 2>&1

start_component()
{
    cat <<EOF >>"${COBALT_RUNTIME_DIR}/var/log/cobalt/$1.out"

===============================================================================

starting $1 component on `date`

EOF
    cd "${COBALT_SOURCE_DIR}/src/components"
    ($PYTHON_EXE $1.py -d --config-files ${COBALT_CONFIG_FILES} ) \
      >>"${COBALT_RUNTIME_DIR}/var/log/cobalt/$1.out" 2>&1 &
    if test $? -eq 0 ; then
	echo "$1 component started; pid $!"
	echo "$!" >"${COBALT_RUNTIME_DIR}/var/run/cobalt/$1"
    else
	echo "ERROR: $1 component failed to start!" >>"${COBALT_RUNTIME_DIR}/var/log/cobalt/$1.out"
	msg_error "$1 component failed to start!"
    fi
}

if test -n "$*" ; then
    components=$*
fi

for component in $components ; do
    if [ $component = bgqsystem ]
    then
        . /home/bgqsysdb/sqllib/db2profile
    fi
    start_component $component
done
