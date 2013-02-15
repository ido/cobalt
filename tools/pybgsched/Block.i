/*This one has to be modified by us. 
    Let's hear it for nested classes! 
    I'll see if a more recent version of SWIG can be put on the simulator and EAS.
    Could alleviate this.
*/
%module pybgsched

%warnfilter(325) bgsched::Block::Connectivity;
%warnfilter(325) bgsched::Block::Action;


%exception bgsched::Block{

    PyThreadState *_save;
    _save = PyEval_SaveThread();
    try{
        $action;
    }
    catch(bgsched::InputException &e){
        PyEval_RestoreThread(_save);
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;
    }
    catch(std::exception &e){
        PyEval_RestoreThread(_save);
        SWIG_exception(SWIG_RuntimeError, e.what());
        return NULL;
    }
    PyEval_RestoreThread(_save);
}


%exception bgsched::Block::update{
    PyThreadState *_save;
    _save = PyEval_SaveThread();
    try{
        $action;
    }
    catch(bgsched::InputException &e){
        PyEval_RestoreThread(_save);
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;
    }
    catch(bgsched::DatabaseException &e){
        PyEval_RestoreThread(_save);
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;
    }
    catch(bgsched::InternalException &e){
        PyEval_RestoreThread(_save);
        PyErr_SetString(PyExc_RuntimeError, const_cast<char *>(e.what()));
        return NULL;
    }
    catch(std::exception &e){
        PyEval_RestoreThread(_save);
        SWIG_exception(SWIG_RuntimeError, e.what());
        return NULL;
    }
    PyEval_RestoreThread(_save);
}


%exception bgsched::Block::add{
    PyThreadState *_save;
    _save = PyEval_SaveThread();
    try{
        $action;
    }
    catch(bgsched::InputException &e){
        PyEval_RestoreThread(_save);
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;
    }
    catch(bgsched::DatabaseException &e){
        PyEval_RestoreThread(_save);
        PyErr_SetString(PyExc_IOError, const_cast<char *>(e.what()));
        return NULL;
    }
    catch(bgsched::RuntimeException &e){
        PyEval_RestoreThread(_save);
        PyErr_SetString(PyExc_RuntimeError, const_cast<char *>(e.what()));
        return NULL;
    }
    catch(std::exception &e){
        PyEval_RestoreThread(_save);
        SWIG_exception(SWIG_RuntimeError, e.what());
        return NULL;
    }
    PyEval_RestoreThread(_save);
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


