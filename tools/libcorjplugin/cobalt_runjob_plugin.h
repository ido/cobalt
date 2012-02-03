#ifndef __COBALT_RUNJOB_PLUGIN_H
#define __COBALT_RUNJOB_PLUGIN_H

#include <bgsched/runjob/Plugin.h>

#include <boost/thread/mutex.hpp>

/******************************************************************************
 * class: CobaltRunjobPlugin
 * Any mangling that needs to go to job arguments should likely go here, 
 * especially if they need to be intercepted for all runjob calls
 *****************************************************************************/

class CobaltRunjobPlugin : public bgsched::runjob::Plugin{

public:
    CobaltRunjobPlugin();
    ~CobaltRunjobPlugin();
    void execute(bgsched::runjob::Verify &data);
    void execute(const bgsched::runjob::Started &data);
    void execute(const bgsched::runjob::Terminated &data);

private:
    boost::mutex _mutex;
};

typedef struct block_info_t{
    std::string loc_id;
    int rack_id;
    int midplane_id;
    int node_board_id;
    int node_id;
    int size;
    std::string parent_block;
} block_info;

block_info *parse_block_info(std::string block_id);
void get_extents_from_size(int size, int extents[5]);

/* Useful defines for getting our dimensions right*/
static int NODEBOARD_A_DIM_MASK = 4;
static int NODEBOARD_B_DIM_MASK = 8;
static int NODEBOARD_C_DIM_MASK = 1;
static int NODEBOARD_D_DIM_MASK = 2;
static int NODEBOARD_E_DIM_MASK = 8;

static int A_DIM = 0;
static int B_DIM = 1;
static int C_DIM = 2;
static int D_DIM = 3;
static int E_DIM = 4;

#define NODES_PER_NODEBOARD 32
#define NUM_DIMS 5

std::vector< std::vector< int > >base_node_map;
#endif
