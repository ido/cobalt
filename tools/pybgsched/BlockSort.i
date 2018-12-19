
// Copyright 2017 UChicago Argonne, LLC. All rights reserved.
// Licensed under a modified BSD 3-clause license. See LICENSE for details.
%warnfilter(325) bgsched::core::BlockSort::Field;

struct BlockSort_Field {
    enum Value {
        ComputeNodeCount,
        CreateDate,
        Name,
        Owner,
        User,
        Status,
        StatusLastModified
    };
};


%{
#include <bgsched/core/BlockSort.h>
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/core/BlockSort.h"

%{
typedef bgsched::core::BlockSort::Field BlockSort_Field;
%}
