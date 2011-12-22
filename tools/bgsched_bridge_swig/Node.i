/* Definitions for BG/Q Nodes.  This follows the "standard"
hardware-type object format.  

Translators provided for enums, since enums don't scan well in python.

*/

%module pybgsched

%{
#include <bgsched/Node.h>
%}

%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/Node.h"

