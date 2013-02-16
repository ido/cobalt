%module pybgsched

typedef unsigned int uint32_t;
typedef unsigned long uint64_t;

/*SWIG includes*/
%include "std_string.i"
%ignore std::vector<bgsched::Shape>::vector(size_type);
%ignore std::vector<bgsched::Shape>::resize(size_type);
%include "std_vector.i"
%include "std_map.i"
%include "std_set.i"
%include "boost_shared_ptr.i"
%include "exception.i"
%include "cpointer.i"

%pointer_functions(uint32_t, uint32_tp)
%pointer_functions(uint64_t, uint64_tp)

/*interface includes */
%include "pybgsched_swig_macros.i"

/*generic exception handling.  Keep exceptions from killing cobalt*/
%exception  {
    PyThreadState *_save;
    _save = PyEval_SaveThread();
    try{
        $action
        PyEval_RestoreThread(_save);
    }
    catch(std::exception &e){
        PyEval_RestoreThread(_save);
        SWIG_exception(SWIG_RuntimeError, e.what());
    }
}

/*boost shared pointer declarations*/
%shared_ptr(bgsched::Hardware)
%shared_ptr(bgsched::ComputeHardware)
%shared_ptr(bgsched::NodeBoard)
%shared_ptr(bgsched::Midplane)
%shared_ptr(bgsched::Node)
%shared_ptr(bgsched::Switch)
%shared_ptr(bgsched::IOLink)
%shared_ptr(bgsched::IONode)
%shared_ptr(bgsched::IODrawer)
%shared_ptr(bgsched::Cable)
%shared_ptr(bgsched::Job)
%shared_ptr(bgsched::Block)
%shared_ptr(bgsched::IOBlock)
%shared_ptr(bgsched::Shape)

/*bridge includes*/
%include "types.i"
%include "EnumWrapper.i"
%include "SortOrder.i"
%include "Dimension.i"
%include "Coordinates.i"
%include "Job.i"
%include "JobSort.i"
%include "JobFilter.i"
%include "Hardware.i"
%include "Node.i"
%include "IONode.i"
%include "Shape.i"
%include "Cable.i"
%include "IOLink.i"
%include "SwitchSettings.i"
%include "Switch.i"
%include "NodeBoard.i"
%include "IODrawer.i"
%include "Midplane.i"
%include "Documentation.i"
%include "ComputeHardware.i"
%include "IOHardware.i"
%include "DatabaseException.i"
%include "BlockSort.i"
%include "IOBlockSort.i"
%include "Exception.i"
%include "Block.i"
%include "BlockFilter.i"
%include "IOBlock.i"
%include "IOBlockFilter.i"
%include "SchedUtil.i"
%include "InitializationException.i"
%include "InternalException.i"
%include "InputException.i"
%include "TimeInterval.i"
%include "RuntimeException.i"
%include "AllocatorEventListener.i"
%include "ResourceSpec.i"
%include "Midplanes.i"
%include "Model.i"
%include "LiveModel.i"
%include "Allocator.i"
%include "bgsched.i"
%include "core.i"
%include "kill.i"

/*Python convenience functions*/
%pythoncode %{
def SWIG_vector_to_list(vec):
    ret_list = []
    for i in range(0, vec.size()):
        ret_list.append(vec[i])
    return ret_list

def hardware_in_error_state(hw):

    hw_error_list = [Hardware.Error,
                     Hardware.Missing,
                     Hardware.Service,
                     Hardware.SoftwareFailure,
                    ]

    v = hw.getState()
    if v in hw_error_list:
        return True
    return False

%}


PYBGSCHED_SHARED_PTR_VECTORS(NodeBoard)
PYBGSCHED_SHARED_PTR_VECTORS(Midplane)
PYBGSCHED_SHARED_PTR_VECTORS(Node)
PYBGSCHED_SHARED_PTR_VECTORS(Switch)
PYBGSCHED_SHARED_PTR_VECTORS(IOLink)
PYBGSCHED_SHARED_PTR_VECTORS(IONode)
PYBGSCHED_SHARED_PTR_VECTORS(IODrawer)
PYBGSCHED_SHARED_PTR_VECTORS(Cable)
PYBGSCHED_SHARED_PTR_VECTORS(Job)
PYBGSCHED_SHARED_PTR_VECTORS(Block)
PYBGSCHED_SHARED_PTR_VECTORS(IOBlock)
PYBGSCHED_SHARED_PTR_VECTORS(Shape)
%template(ShapeVector) std::vector<bgsched::Shape>;
%template(BlockStatusSet) std::set<bgsched::Block::Status>;
%template(DimensionConnectivityMap) std::map<bgsched::Dimension, bgsched::Block::Connectivity::Value>;
%template(StringVector) std::vector<std::string>;




