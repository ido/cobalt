/*Class to wrap function pointer and track callback status from outside C++*/
#include <boost/bind.hpp>

namespace bgsched {
  class IONBootCompletedFunc {

    public:
      std::string IOBlockName;
      std::string location;
      bool called;
      bool hasException;
      boost::exception_ptr exc;
      IOBlock::RebootIONodeCallbackFn callback;

      IONBootCompletedFunc(std::string IOBlockName, std::string location){
        //constructor.  Make sure we have the location and block name
        this->IOBlockName = IOBlockName;
        this->location = location;
        called = 0;
        hasException = 0;
        exc = boost::exception_ptr();
        callback = boost::bind(&bgsched::IONBootCompletedFunc::do_callback, this, _1);
      }

      void do_callback(boost::exception_ptr exc_ptr){
        called = 1;
        if (exc_ptr != NULL){
          hasException = 1;
          exc = exc_ptr;
        }
        return;
      }

      void throwIfHasExc(){
        if(hasException){
          boost::rethrow_exception(exc);
        }
        return;
      }
  };
};
