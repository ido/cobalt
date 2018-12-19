/* Definitions for BG/Q Nodes.  This follows the "standard"
// Copyright 2017 UChicago Argonne, LLC. All rights reserved.
// Licensed under a modified BSD 3-clause license. See LICENSE for details.
hardware-type object format.  

Translators provided for enums, since enums don't scan well in python.

*/

%module pybgsched

%{
#include <bgsched/Node.h>
%}

%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/Node.h"

