#include <iostream>
#include <dlfcn.h>

#include "bgsched/runjob/Plugin.h"
#include "bgsched/runjob/Verify.h"
#include "cobalt_runjob_plugin.h"

int main(int argc, char **argv){

    std::cout << "Starting" << std::endl;
    void * handle = dlopen("/home/richp/cobalt_runjob_plugin/libcorjplugin.so", RTLD_LAZY);
    if (!handle){
        std::cout << "couldn't open lib" << std::endl;
    }
    std::cout << "plugin open." << std::endl;
    bgsched::runjob::Plugin *p = create();
    std::cout << "Created" << std::endl;
    parse_block_info(std::string("R00-M1-N02-J03-16"));
    parse_block_info(std::string("R00-M1-N01-32"));
    parse_block_info(std::string("R00-M1-N02-64"));
    destroy(p);
    std::cout << "Done." << std::endl;
    return 0;
}
