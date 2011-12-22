%module pybgsched


%include "std_vector.i"

%shared_ptr(bgsched::NodeBoard)

%{
#include <bgsched/NodeBoard.h>
%}


%include "/bgsys/drivers/ppcfloor/hlcs/include/bgsched/NodeBoard.h"


%extend bgsched::NodeBoard{

    
    int getQuadrantValue(){
        return $self->getQuadrant().toValue();
    } 

    std::string getQuadrantString(){

        bgsched::NodeBoard::Quadrant v = $self->getQuadrant().toValue();
        if (v == bgsched::NodeBoard::Q1)
            return std::string("Q1");
        else if (v == bgsched::NodeBoard::Q2)
            return std::string("Q2");
        else if (v == bgsched::NodeBoard::Q3)
            return std::string("Q3");
        else if (v == bgsched::NodeBoard::Q4)
            return std::string("Q4");    

        return std::string("UnknownState");

    }

}


%pythoncode %{
NodeBoard.getQuadrant = NodeBoard.getQuadrantValue
%}

