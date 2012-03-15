%module pybgsched

%warnfilter(325) bgsched::SchedUtil::Errors;    

struct SchedUtil_Errors
    {
        /*!
         * \brief Error codes.
         */
        enum Value
        {
            InputVectorSizeMismatch = 1,
            VectorIndexOutOfBounds,
        };


        /*!
         * \brief Error message string.
         *
         * \return Error message string.
         */
        static std::string toString(Value v, const std::string& what);
    };



%{
#include <bgsched/SchedUtil.h>
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/SchedUtil.h"

%{
typedef bgsched::SchedUtil::Errors SchedUtil_Errors;
%}    
