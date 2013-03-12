%warnfilter(325) bgsched::core::IOBlockSort::Field;

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
