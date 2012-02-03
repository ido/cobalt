#include <iostream>
#include <exception>

#include "bgsched/bgsched.h"


int main (){

    try {
        bgsched::init("../../bg.properties");
        std::cout << "INIT OK" << std::endl;
        bgsched::refreshConfiguration();
    }
    catch (std::exception& e){
        std::cout << "BOOM!"<< std::endl << e.what() << std::endl;
    }

    try {
        bgsched::init("/home/richp/bg.properties");
        std::cout << "INIT OK" << std::endl;
        bgsched::refreshConfiguration();
    }
    catch (std::exception& e){
        std::cout << "BOOM!"<< std::endl << e.what() << std::endl;
    }
    std::cout << "EXITING." << std::endl;
    return 0;
}
