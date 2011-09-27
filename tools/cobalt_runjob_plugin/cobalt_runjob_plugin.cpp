#include <iostream>
#include <algorithm>
#include <iterator>
#include <string>
#include <vector>
#include <map>

#include <boost/foreach.hpp>

#include "cobalt_runjob_plugin.h"
//#include "ProcessTree.h"

#include <string.h>
#include <stdlib.h>
#include <stdio.h>

/*get midplane information*/

using std::cout;
using std::endl;
using std::string;

block_info *parse_block_info(string block_id){
    
    block_info *ret = new block_info();
    std::vector<string> tokens;
    const char *delim = "-";
    unsigned int pos = 0;
    unsigned int lastpos = 0;
    unsigned int maxlen = block_id.size();
    do{
        lastpos = block_id.find_first_not_of(delim, pos);
        pos = block_id.find_first_of(delim, lastpos);
        tokens.push_back(block_id.substr(lastpos, pos - lastpos));
    } while (pos < maxlen && lastpos < maxlen);

    //ret->loc_id = tokens[0];
    ret->rack_id = atoi(tokens[0].erase(0,1).c_str()); 
    ret->midplane_id = atoi(tokens[1].erase(0,1).c_str()); 
    ret->node_board_id = atoi(tokens[2].erase(0,1).c_str()); 
    if(tokens.size() > 4)
        ret->node_id = atoi(tokens[3].erase(0,1).c_str());
    else{
        /*this would be the expedient solution.  Actual computation will be ported later */
        switch (ret->node_board_id){
            case 0:
                ret->node_id = 0;
                break;
            case 1:
                ret->node_id = 1;
                break;
            case 2:
                ret->node_id = 12;
                break;
            case 3:
                ret->node_id = 13;
                break;

        }
    } 
    ret->size = atoi(tokens[tokens.size() - 1].c_str());
    
    
    //const char *block_fmt = "EAS-R%02d-M%d-N%02d-%d";
    //const char *pseudo_block_fmt = "EAS-R%02d-M%d-N%02d-J%02d-%d";
    
    /*input already sanitized by runjob itself.*/
    //char loc_str[4];


    //cout << "Chopping string: " << block_id.c_str() << endl;

    //if (!(EOF == sscanf(block_id.c_str(), pseudo_block_fmt,  ret->rack_id, 
    //           ret->midplane_id, ret->node_board_id, ret->node_id, ret->size))){
    //        ret->loc_id = string("EAS");    
   // }
    //else{
        /*scan what looks like a normal block name*/
    //    sscanf(block_id.c_str(), block_fmt, loc_str, ret->rack_id, ret->midplane_id,
    //            ret->node_board_id, ret->size);
    //    if (ret->size == 32){
    //        if(ret->node_board_id == 1)
    //            ret->node_id = 1;
     //       else{
     //           ret->node_id = 0;
     //       }
     //   }
     //   else{
     //       ret->node_id = -1;
     //   }
     //   ret->loc_id = string(loc_str);    
   // }
   
    //cout << "Chop complete" << endl;
    const char *parent_block_fmt = "R%02d-M%d-N%02d-128";
    char pb_name[32];
    sprintf(pb_name, parent_block_fmt,  ret->rack_id,
            ret->midplane_id, (ret->node_board_id/4 * 4) );
    ret->parent_block = string(pb_name);

    //cout << "Parent Block: " << pb_name <<endl;
    //cout << "Loc: " << ret->loc_id << endl;
    //cout << "Rack: " << ret->rack_id << endl;
    //cout << "Midplane: " << ret->midplane_id << endl;
    //cout << "Nodeboard: " << ret->node_board_id << endl;
    //cout << "Node: " << ret->node_id << endl;
    //cout << "Size: " << ret->size << endl;

    return ret;
}

void get_extents_from_size(int size, unsigned int extents[5]){
    /* generate valid subblock extents from a given size, we should get:
     * 128 = 2,2,4,4,2
     * 64  = 2,2,4,2,2
     * 32  = 2,2,2,2,2
     * 16  = 2,2,1,2,2
     * ...
     * see ALCF2 wiki documentation for more info on subblock extents
     */
    int left = size;
    int count =  0;
    int extents_len = 5;
    int i;
    
    for(i =0; i < extents_len; ++i){
        extents[i] = 1;
    }
    int dim_order[5];

    if (size <= 512 && size >= 64){
        for(i=0;i<extents_len;++i){
            extents[i]++;
        }
        dim_order[0] = 2;
        dim_order[1] = 3;
        dim_order[2] = 0;
        dim_order[3] = 1;
        dim_order[4] = -1;
        left /= 32;
    }
    else if(size <= 32){
        dim_order[0] = 0;
        dim_order[1] = 3;
        dim_order[2] = 4;
        dim_order[3] = 1;
        dim_order[4] = 2;
    }

    while (left > 1){
        extents[dim_order[count]] *= 2;
        count++;
        left /= 2;
    }

    return;
}


/* Plugin constructor */
CobaltRunjobPlugin::CobaltRunjobPlugin() : bgsched::runjob::Plugin(), _mutex(){
    std::cout << "Initializing Cobalt Runjob Plugin" << std::endl;
    return;
}

CobaltRunjobPlugin::~CobaltRunjobPlugin(){
    std::cout << "Finalizing Cobalt Runjob Plugin" << std::endl;
    return;
}

/*execute for job verification.  This verify reference is mutable. 
 * Modifies job data, so watch for locks.*/
void CobaltRunjobPlugin::execute(bgsched::runjob::Verify &data){
    cout << "starting job from pid: " << data.pid() << endl;
    cout << "exe: "<< data.exe() << endl;
    
    cout << "args: " << endl;
    cout << endl;
    
    cout << "block data:" << endl;
    
    //Attempt to extract block info and run subblock if we need
    string block_id = data.block();
    block_info *corner;
    corner = parse_block_info(data.block());
    cout << corner->node_board_id << endl;
    cout << corner->node_id << endl;
    cout << corner->size << endl;

    if (corner->size >=128){
        cout << "block name: "<< data.block() << endl;
        return;
    }

    data.block(corner->parent_block); 
        
    cout << "block name: "<< data.block() << endl;
        
    const char *corner_node_fmt = "R%02d-M%d-N%02d-J%02d";
    char corner_name[32];
    sprintf(corner_name, corner_node_fmt, corner->rack_id,
            corner->midplane_id, corner->node_board_id, corner->node_id);

    data.corner(bgsched::runjob::Corner().location(string(corner_name)));
   
    
     
    unsigned int shape_array[5] = {2,2,2,2,2};
    
    get_extents_from_size(corner->size, shape_array);

    data.shape(bgsched::runjob::Shape(shape_array));
    if (!data.corner().location().empty()){
        cout << "subblock corner: " <<  data.corner().location()  << endl;
        cout << "subblock shape: " <<  data.shape().value() << endl;
    }

    return;
}
       
void CobaltRunjobPlugin::execute(const bgsched::runjob::Started &data){
    boost::lock_guard<boost::mutex> lock( _mutex );
    std::cout << "runjob " << data.pid() << " started with ID " << data.job() << std::endl;

    return;
}

void CobaltRunjobPlugin::execute(const bgsched::runjob::Terminated &data){

    boost::lock_guard<boost::mutex> lock( _mutex );
    std::cout << "runjob " << data.pid() << " shadowing job " << data.job() << " finished with status " << data.status() << std::endl;
    // output failed nodes
    const bgsched::runjob::Terminated::Nodes& nodes = data.software_error_nodes();
    if ( !nodes.empty() ) {
        std::cout << nodes.size() << " failed nodes" << std::endl;
        BOOST_FOREACH( const bgsched::runjob::Node i, data.software_error_nodes() ) {
            std::cout << i.location() << std::endl;
        }
    }

    return;
}

extern "C" {
    
bgsched::runjob::Plugin *create(){
    return new CobaltRunjobPlugin();
}

void destroy(bgsched::runjob::Plugin *plugin){
    delete plugin;
    return;
}

} // extern "C"
