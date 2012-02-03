/*General Hardware object definitions:

These get inherited by other hardware-entities:
Midplane
Cable
Switch
Nodeboard
Node
IOLink

Make sure to check these, if you alter this set of structures.

These have been moved up and out of this file to avoid certain issues
with SWIG and when these can show up in code.

*/

%{
#include <bgsched/Hardware.h>
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/Hardware.h"

%extend bgsched::Hardware{

    int getStateValue(){
        return ($self->getState()).toValue();
    }

    std::string getStateString(){
        bgsched::Hardware::State v = ($self->getState()).toValue();
        switch(v){
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Hardware, Available)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Hardware, Missing)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Hardware, Error)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Hardware, Service)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Hardware, SoftwareFailure)
            default:
                return std::string("UnknownState");
        }
    
        return std::string("UnknownState");
    }
    
    const char *__str__(){
        return $self->toString().c_str();
    }
    
}

%pythoncode %{
Hardware.getState = Hardware.getStateValue
%}

