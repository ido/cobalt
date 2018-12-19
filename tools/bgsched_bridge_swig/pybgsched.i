%module pybgsched
// Copyright 2017 UChicago Argonne, LLC. All rights reserved.
// Licensed under a modified BSD 3-clause license. See LICENSE for details.

typedef unsigned int uint32_t;

/*SWIG includes*/
%include "std_string.i"
%include "boost_shared_ptr.i"

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
%include "Shape.i"
%include "Cable.i"
%include "SwitchSettings.i"
%include "Switch.i"
%include "NodeBoard.i"
%include "Midplane.i"
%include "Documentation.i"
%include "ComputeHardware.i"
%include "DatabaseException.i"
%include "BlockSort.i"
%include "BlockFilter.i"
%include "IOLink.i"
%include "Exception.i"
%include "BlockFilter.i" 
%include "Block.i"
%include "BlockFilter.i"
%include "SchedUtil.i"
%include "InitializationException.i"
%include "InternalException.i"
%include "InputException.i"
%include "TimeInterval.i"
%include "RuntimeException.i"
%include "bgsched.i"
%include "core.i"
