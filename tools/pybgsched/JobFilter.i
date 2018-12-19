%module pybgsched
// Copyright 2017 UChicago Argonne, LLC. All rights reserved.
// Licensed under a modified BSD 3-clause license. See LICENSE for details.

%warnfilter(325) bgsched::JobFilter::JobType;

struct JobType {
    enum Value {
        Active = 0, 
        Completed,  
        All        
    };
};

%{
#include <bgsched/JobFilter.h>
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/JobFilter.h"

%{
typedef bgsched::JobFilter::JobType JobType;
%}
