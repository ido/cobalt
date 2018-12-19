%warnfilter(325) bgsched::core::IOBlockSort::Field;
// Copyright 2017 UChicago Argonne, LLC. All rights reserved.
// Licensed under a modified BSD 3-clause license. See LICENSE for details.

struct IOBlockSort_Field {
    enum Value {
        IONodeCount,
        CreateDate,
        Name,
        Owner,
        User,
        Status,
        StatusLastModified
    };

};

%{
#include <bgsched/core/IOBlockSort.h>
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/core/IOBlockSort.h"

%{
typedef bgsched::core::IOBlockSort::Field IOBlockSort_Field;
%}
