/*This is another place where there are a lot of nested structs
Also, we have a function pointer return containning an exception
so that is also getting special handling*/
%module pybgsched

%warnfilter(325) bgsched::IOBlock::Action;
%warnfilter(314);


%exception bgsched::IONBootCompletedFunc {
    PyThreadState *_save;
    _save = pyEval_SaveThread();
    try{
      $action
    }
    catch(bgsched::InputException &e){
      PyEval_RestoreThread(_save);
      PyErr_SetString(PyExc_ValueError, const_cast<char *>(e.what()));
      return NULL;
    }
    catch(bgsched::RuntimeException &e){
      PyEval_RestoreThread(_save);
      PyErr_SetString(PyExc_RuntimeError, const_cast<char *>(e.what()));
      return NULL;
    }
    catch(std::exception &e){
      PyEval_RestoreThread(_save);
      PyErr_SetString(PyExc_RuntimeError, const_cast<char *>(e.what()));
      return NULL;
    }
    PyEval_RestoreThread(_save);
}

struct IOBlock_Action{
  enum Value {
    None = 0,
    Boot,
    Free
  };
};

/*The reboot nodes API takes a function pointer which is how it informs you that
an individual boot is done.  There is no query funciton for the ION state other
than the hardware should go from a SoftwareFailure state to Available (or Error
if the ION then blows on boot).  This is also the exception return mechanism.

Keep in mind that using this interface also means you're hitting mc_server in
addition to the database.  In a threaded call.

*/

%{
#include <bgsched/IOBlock.h>
#include "IONBootCompletedFunc.h"
%}
%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/IOBlock.h"
%include "IONBootCompletedFunc.h"


%extend bgsched::IOBlock{

    int getStatusValue(){
        return ($self->getStatus()).toValue();
    }

    std::string getStatusString(){
        bgsched::IOBlock::Status v = ($self->getStatus()).toValue();
        switch(v){
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::IOBlock, Allocated)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::IOBlock, Booting)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::IOBlock, Free)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::IOBlock, Initialized)
            PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::IOBlock, Terminating)
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
      PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::IOBlock::Action, None)
      PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::IOBlock::Action, Boot)
      PYBGSCHED_CASE_ENUM_TO_STRING(bgsched::IOBlock::Action, Free)
      default:
        return std::string("UnknownState");
    }
    return std::string("UnknownState");
  }

  static void rebootIONodeFromPython(bgsched::IONBootCompletedFunc *func_class){
    bgsched::IOBlock::rebootIONode(func_class->IOBlockName, func_class->location, func_class->callback);
    return;
  }
}

%{
typedef bgsched::IOBlock::Action IOBlock_Action;
%}

%pythoncode{
IOBlock.getStatus = IOBlock.getStatusValue
IOBlock.getAction = IOBlock.getActionValue
IOBlock.rebootIONode = IOBlock.rebootIONodeFromPython
}
%warnfilter(+314);
