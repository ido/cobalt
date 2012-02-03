%module pybgsched

/* These get peppered throughout the code, and have to occur before any declaration/use.
So, we're getting this meta-stuff out of the way now. */
%include <boost_shared_ptr.i>

%template(ComputeHardware_ConstPtr) boost::shared_ptr<const bgsched::ComputeHardware>;
%template(ComputeHardware_Ptr) boost::shared_ptr<bgsched::ComputeHardware>;
%shared_ptr(ComputeHardware_Ptr)
%shared_ptr(ComputeHardware_ConstPtr)
