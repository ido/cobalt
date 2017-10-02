%module pybgsched
// Copyright 2017 UChicago Argonne, LLC. All rights reserved.
// Licensed under a modified BSD 3-clause license. See LICENSE for details.

%warnfilter(325) bgsched::core::JobSort::Field;


struct JobSort_Field {
/*here for SWIG.  Internal struct to the JobSort classs*/
    enum Value {
         Id,
         User,
         Block,
         Executable,
         StartTime,
         EndTime,
         ExitStatus,
         Status,
         ComputeNodesUsed,
         RanksPerNode
    };
};

%{
#include <bgsched/core/JobSort.h>
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/core/JobSort.h"

%{
typedef bgsched::core::JobSort::Field JobSort_Field;
%}

