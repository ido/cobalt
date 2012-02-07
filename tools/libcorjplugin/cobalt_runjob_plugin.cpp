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

void transform_dim(int dim, std::vector< std::vector < int > > &node_map){
    std::vector<int> coord;
    coord = node_map.back();
    coord[dim] = coord[dim] ^ 1;
    node_map.push_back(coord); 
    return;
}

void transform_cube( std::vector< std::vector < int > > &node_map){

    transform_dim(C_DIM, node_map);
    transform_dim(B_DIM, node_map);
    transform_dim(C_DIM, node_map);
    transform_dim(E_DIM, node_map);
    transform_dim(C_DIM, node_map);
    transform_dim(B_DIM, node_map);
    transform_dim(C_DIM, node_map);
    return;
}

void generate_base_node_map(std::vector < std::vector < int > > &node_map ){
    /*Yes, this is a magic bit of code.  This generates the node address (JXX
     * for 0 <= XX <= 31) to logical coordinate mapping for N00 on any given
     * midplane.  By xor-ing with a series of masks defined in the header file
     * you can generate a logical address for any of the nodeboards in a 
     * midplane.  These mappings are consistient from midplane to midplane.
     * --PMR
     */

    std::vector<int> coords;
    for (int i = 0; i < NUM_DIMS; i++){
        coords.push_back(0);
    }

    node_map.push_back(coords);
    transform_cube(node_map);

    coords = node_map.back();
    coords[B_DIM] = coords[B_DIM] ^ 1;
    coords[D_DIM] = coords[D_DIM] ^ 1;
    node_map.push_back(coords);
    
    transform_cube(node_map);
    
    coords = node_map.back();
    coords[A_DIM] = coords[A_DIM] ^ 1;
    coords[B_DIM] = coords[B_DIM] ^ 1;
    coords[C_DIM] = coords[C_DIM] ^ 1;
    node_map.push_back(coords);
    
    transform_cube(node_map);

    coords = node_map.back();
    coords[B_DIM] = coords[B_DIM] ^ 1;
    coords[D_DIM] = coords[D_DIM] ^ 1;
    node_map.push_back(coords);

    transform_cube(node_map);
    
    return;
}



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

    ret->size = atoi(tokens[tokens.size() - 1].c_str());
    
    /* take the actual size of the block, and don't do anything if the size is
     * >128.  Really, don't change the block name, it's a headache we don't want.
     */
    //ret->loc_id = tokens[0];
    if (ret->size >= 512){
        ret->rack_id = NULL;
        ret->midplane_id = NULL;
        ret->node_board_id = NULL;
        ret->node_id = NULL;
        return ret;
    }
    else if(ret->size >= 32){
        ret->rack_id = atoi(tokens[tokens.size()-4].erase(0,1).c_str()); 
        ret->midplane_id = atoi(tokens[tokens.size()-3].erase(0,1).c_str());
        ret->node_board_id = atoi(tokens[tokens.size()-2].erase(0,1).c_str()); 
    
        /* Take the nodes from the base node map, apply a series of masks based
         * on the nodeboard hardware address (the NXX value) to determine which 
         * dimensions are "reversed." Since a nodeboard is size 2 in all dims
         * an xor takes care of this.
         * */
        bool a,b,c,d,e;
        for (int i = 0; i < NODES_PER_NODEBOARD; i++){

            a = base_node_map[i][A_DIM] ^ bool(NODEBOARD_A_DIM_MASK & ret->node_board_id);
            b = base_node_map[i][B_DIM] ^ bool(NODEBOARD_B_DIM_MASK & ret->node_board_id);
            c = base_node_map[i][C_DIM] ^ bool(NODEBOARD_C_DIM_MASK & ret->node_board_id);
            d = base_node_map[i][D_DIM] ^ bool(NODEBOARD_D_DIM_MASK & ret->node_board_id);
            e = base_node_map[i][E_DIM] ^ bool(NODEBOARD_E_DIM_MASK & ret->node_board_id);
            
            if (! (a||b||c||d||e)){   
                ret->node_id = i;
                break;
            }
        }

        cout << "tokens:" << tokens.size() << tokens[0] <<endl;
        if (tokens.size() > 4){
            ret->loc_id = tokens[0];
        }
        else {
            ret->loc_id = "";
        }
    }
    else{
        ret->rack_id = atoi(tokens[tokens.size()-5].erase(0,1).c_str()); 
        ret->midplane_id = atoi(tokens[tokens.size()-4].erase(0,1).c_str());
        ret->node_board_id = atoi(tokens[tokens.size()-3].erase(0,1).c_str()); 
        ret->node_id = atoi(tokens[tokens.size()-2].erase(0,1).c_str());
        if (tokens.size() > 5){
            ret->loc_id = tokens[0];
        }
        else {
            ret->loc_id = "";
        }
    } 
    
    /*we use 128's as our parent block for this plugin, smallest part size we have*/
    const char *parent_block_fmt = "R%02d-M%d-N%02d-128";
    const char *loc_parent_block_fmt =  "%s-R%02d-M%d-N%02d-128";
    
    char pb_name[32];
    cout << ret->loc_id << endl;
    if (!ret->loc_id.empty()){
        sprintf(pb_name, loc_parent_block_fmt, ret->loc_id.c_str() ,ret->rack_id,
            ret->midplane_id, (ret->node_board_id/4 * 4) );
    }
    else{
        sprintf(pb_name, parent_block_fmt,  ret->rack_id,
            ret->midplane_id, (ret->node_board_id/4 * 4) );
    }
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
    generate_base_node_map(base_node_map);
    return;
}

CobaltRunjobPlugin::~CobaltRunjobPlugin(){
    std::cout << "Finalizing Cobalt Runjob Plugin" << std::endl;
    return;
}

/*execute for job verification.  This verify reference is mutable. 
 * Modifies job data, so watch for locks.*/
void CobaltRunjobPlugin::execute(bgsched::runjob::Verify &data){
    /* we mangle the block to make subruns easier.  We may ultimately
     * change this down the road.
     */
    
    cout << "starting job from pid: " << data.pid() << endl;
    cout << "exe: "<< data.exe() << endl;
    cout << "args: ";
    for (unsigned int i = 0; i < data.args().size(); ++i){
        cout << data.args()[i] << ' ';
    }
    cout << endl;
    cout << "block data:" << endl;
    
    //Attempt to extract block info and run subblock if we need
    string block_id = data.block();
    block_info *corner;
    corner = parse_block_info(data.block());
    cout << "rack: " << corner->rack_id << endl;
    cout << "midplane: " << corner->midplane_id << endl;
    cout << "nodeboard: " << corner->node_board_id << endl;
    cout << "node: " << corner->node_id << endl;
    cout << "size: " << corner->size << endl;

    if (corner->size >=128){
        //if we're at or above base-block size don't do anything.
        cout << "block name: "<< data.block() << endl;
        return;
    }

    if (corner->size == 64 && 
        ((int(corner->node_board_id) % 2) != 0)){
        std::string errmsg = data.block();
        errmsg += " is an invalid subblock specification.";
        data.deny_job(errmsg);
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
        if (!data.shape().value().empty()) 
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
