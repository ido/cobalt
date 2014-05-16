/*This one has to be modified by us. 
    Let's hear it for nested classes! 
    I'll see if a more recent version of SWIG can be put on the simulator and EAS.
    Could alleviate this.
*/
%module pybgsched

/* Swig doesn't handle nested structs automatically by default, and will throw warnings
despite a workaround being put in place.*/
%warnfilter(325) bgsched::Block::Connectivity;
%warnfilter(325) bgsched::Block::Action;
/* 314:This supresses a warning about renaming none.  Since we can't rename
the variable in the libary, this is a known deviation.*/
%warnfilter(314);

%exception bgsched::Block{

    try{
        $action;
    }
    catch(bgsched::InputException &e){
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;
    }
    catch(std::exception &e){
        SWIG_exception(SWIG_RuntimeError, e.what());
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
    catch(std::exception &e){
        SWIG_exception(SWIG_RuntimeError, e.what());
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
    catch(std::exception &e){
        SWIG_exception(SWIG_RuntimeError, e.what());
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

  int getActionValue(){
       return ($self->getAction()).toValue();
  }

  std::string getActionString(){
    int v = ($self->getAction()).toValue();
    switch(v){
      PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Block::Action, None)
      PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Block::Action, Boot)
      PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::Block::Action, Free)
      default:
        return std::string("UnknownState");
    }
    return std::string("UnknownState");
  }

}

%pythoncode{
Block.getStatus = Block.getStatusValue
Block.getAction = Block.getActionValue
}

%warnfilter(+314);
