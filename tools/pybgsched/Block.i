/*This one has to be modified by us. 
    Let's hear it for nested classes! 
    I'll see if a more recent version of SWIG can be put on the simulator and EAS.
    Could alleviate this.
*/
%module pybgsched

%warnfilter(325) bgsched::Block::Connectivity;


%exception bgsched::Block{
    try{
        $action;
    }
    catch(bgsched::InputException &e){
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;    
    }
}

%exception bgsched::Block::update{
    try{
        $action;
    }
    catch(bgsched::InputException &e){
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;    
    }
    catch(bgsched::DatabaseException &e){
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;    
    }
    catch(bgsched::InternalException &e){
        PyErr_SetString(PyExc_RuntimeError, const_cast<char *>(e.what()));
        return NULL;    
    }
}


%exception bgsched::Block::add{
    try{
        $action;
    }
    catch(bgsched::InputException &e){
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;    
    }
    catch(bgsched::DatabaseException &e){
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;    
    }
    catch(bgsched::RuntimeException &e){
        PyErr_SetString(PyExc_RuntimeError, const_cast<char *>(e.what()));
        return NULL;    
    }
}

/*Do this for SWIG's benefit.  This doesn't really exist in the C++ code */
struct Connectivity{
    enum Value {
        Torus,
        Mesh
    };
};

struct Action{
  enum Value {
    None = 0,
    Boot,
    Free
  };
};

%{
#include <bgsched/Block.h>
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/Block.h"

%{
typedef bgsched::Block::Connectivity Connectivity;
typedef bgsched::Block::Action Action;
%}

%extend bgsched::Block{

    int getStatusValue(){
        return ($self->getStatus()).toValue();
    }

    std::string getStatusString(){
        bgsched::Block::Status v = ($self->getStatus()).toValue();
        switch(v){
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Block, Allocated)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Block, Booting)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Block, Free)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Block, Initialized)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Block, Terminating)
            default:
                return std::string("UnknownState");
        }
        return std::string("UnknownState");
    }
}

%pythoncode{
Block.getStatus = Block.getStatusValue
}


