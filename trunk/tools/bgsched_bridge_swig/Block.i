/*This one has to be modified by us. 
    Let's hear it for nested classes! 
    I'll see if a more recent version of SWIG can be put on the simulator and EAS.
    Could alleviate this.
*/
%module pybgsched

%warnfilter(325) bgsched::Block::Connectivity;

/*Do this for SWIG's benefit.  This doesn't really exist in the C++ code */
struct Connectivity{
    enum Value {
        Torus,
        Mesh
    }; 
}; 

%ignore boost::noncopyable;

namespace boost{
    class noncopyable {};
}
%{
#include <bgsched/Block.h>
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/Block.h"

%{
typedef bgsched::Block::Connectivity Connectivity;
%}

