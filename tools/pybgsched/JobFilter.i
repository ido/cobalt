%module pybgsched

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
