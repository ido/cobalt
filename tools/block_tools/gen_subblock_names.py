#!/usr/bin/env python

import Cobalt
from Cobddalt.Components.bgq_base_system import node_position_exp, nodecard_exp, midplane_exp, rack_exp
from Cobalt.Components.bgq_base_system import NODECARD_A_DIM_MASK, NODECARD_B_DIM_MASK, NODECARD_C_DIM_MASK, NODECARD_D_DIM_MASK, NODECARD_E_DIM_MASK
from Cobalt.Components.bgq_base_system import A_DIM, B_DIM, C_DIM, D_DIM, E_DIM
from Cobalt.Components.bgq_base_system import get_extents_from_size
from Cobalt.Components.bgqsystem import parse_subblock_config

import sys



def gen_subblock_names(parent_name, min_size):

    retnames = []
    curr_size = 128

    bg_block_filter = pybgsched.BlockFilter()
    bg_block_filter.setName(parent_name)
    bg_block_filter.setExtendedInfo(True)
    bg_parent_block = pybgsched.getBlocks(bg_block_filter)[0]
    bgpb_nodeboards = SWIG_vector_to_list(bg_parent_block.getNodeBoards())
    #FIXME: make MAX_NODEBOARD or the like.
    nodecard_pos = 15
    for nb in bgpb_nodeboards:
        nb_pos = int(nodecard_exp.search(nb).groups()[0])
        nodecard_pos = min(nodecard_pos, nb_pos)
    midplane_hw_loc = SWIG_vector_to_list(bg_parent_block.getMidplanes())[0]
    midplane_pos = int(midplane_exp.search(midplane_hw_loc).groups()[0])
    rack_pos = int(rack_exp.search(midplane_hw_loc).groups()[0])
    #get parent midplane information.  we only need this once:
    midplane = self.compute_hardware_vec.getMidplane(midplane_hw_loc)
    midplane_logical_coords = pybgsched.getMidplaneCoordinates(midplane_hw_loc)
    
    subblock_prefix = get_config_option("bgsystem", "subblock_prefix", "COBALT")
    
    
    ret_blocks = []
    while (curr_size >= min_size):
        if curr_size >= 128:
            curr_size = 64
            continue
        
        if curr_size == 64:
            extents = get_extents_from_size(curr_size)
            #corner_node_j_loc_list = get_corner_nodes_for_size(rack_pos, midplane_pos, nodecard_pos, curr_size)
            for i in range(0,2):
                #curr_name = "%sR%02d-M%d-N%02d-64" % (rack_pos, midplane_pos, nodecard_pos+(2*i))
                #nodecard_list = []
                curr_nb_pos = nodecard_pos + (2*i)
                a_corner = midplane_logical_coords[A_DIM]*4 + int(bool(NODECARD_A_DIM_MASK & curr_nb_pos))*2
                b_corner = midplane_logical_coords[B_DIM]*4 + int(bool(NODECARD_B_DIM_MASK & curr_nb_pos))*2
                c_corner = midplane_logical_coords[C_DIM]*4 + int(bool(NODECARD_C_DIM_MASK & curr_nb_pos))*2
                d_corner = midplane_logical_coords[D_DIM]*4 + int(bool(NODECARD_D_DIM_MASK & curr_nb_pos))*2
                e_corner = 0

                curr_name = '%s-%d%d%d%d%d-%d%d%d%d%d-%d' % (subblock_prefix,
                        a_corner, b_corner, c_corner, d_corner, e_corner,
                        a_corner + extents[A_DIM] - 1,
                        b_corner + extents[B_DIM] - 1,
                        c_corner + extents[C_DIM] - 1,
                        d_corner + extents[D_DIM] - 1,
                        e_corner + extents[E_DIM] - 1,
                        curr_size)

                retnames.append(curr_name) 
        elif curr_size == 32:
         
            extents = get_extents_from_size(curr_size)
            for i in range(0,4):
                curr_nb_pos = nodecard_pos + i
                a_corner = midplane_logical_coords[A_DIM]*4 + int(bool(NODECARD_A_DIM_MASK & curr_nb_pos))*2
                b_corner = midplane_logical_coords[B_DIM]*4 + int(bool(NODECARD_B_DIM_MASK & curr_nb_pos))*2
                c_corner = midplane_logical_coords[C_DIM]*4 + int(bool(NODECARD_C_DIM_MASK & curr_nb_pos))*2
                d_corner = midplane_logical_coords[D_DIM]*4 + int(bool(NODECARD_D_DIM_MASK & curr_nb_pos))*2
                e_corner = 0

                curr_name = '%s-%d%d%d%d%d-%d%d%d%d%d-%d' % (subblock_prefix,
                        a_corner, b_corner, c_corner, d_corner, e_corner,
                        a_corner + extents[A_DIM] - 1,
                        b_corner + extents[B_DIM] - 1,
                        c_corner + extents[C_DIM] - 1,
                        d_corner + extents[D_DIM] - 1,
                        e_corner + extents[E_DIM] - 1,
                        curr_size)
                 
                retnames.append(curr_name) 
    
        else:
             extents = get_extents_from_size(curr_size)
            
             #yes, do these for each nodecard.
             for curr_nb_pos in range(nodecard_pos, nodecard_pos + 4):
                 for i in range(0, (32/curr_size)):
                
                     #Yes these bitmasks are important.
                     a_corner = midplane_logical_coords[A_DIM]*4 + int(bool(NODECARD_A_DIM_MASK & curr_nb_pos))*2 + (int(bool(i & 1)))
                     b_corner = midplane_logical_coords[B_DIM]*4 + int(bool(NODECARD_B_DIM_MASK & curr_nb_pos))*2 + (int(bool(i & 2)))
                     c_corner = midplane_logical_coords[C_DIM]*4 + int(bool(NODECARD_C_DIM_MASK & curr_nb_pos))*2 + (int(bool(i & 4)))
                     d_corner = midplane_logical_coords[D_DIM]*4 + int(bool(NODECARD_D_DIM_MASK & curr_nb_pos))*2 + (int(bool(i & 8)))
                     e_corner = int(bool(i & 16))
 
                     curr_name = '%s-%d%d%d%d%d-%d%d%d%d%d-%d' % (subblock_prefix,
                             a_corner, b_corner, c_corner, d_corner, e_corner,
                             a_corner + extents[A_DIM] - 1,
                             b_corner + extents[B_DIM] - 1,
                             c_corner + extents[C_DIM] - 1,
                             d_corner + extents[D_DIM] - 1,
                             e_corner + extents[E_DIM] - 1,
                             curr_size)
                     
                     retnames.append(curr_name) 
                 # for i
             # for curr_nb_pos

        curr_size = curr_size / 2
        
    return retnames

if __name__ == '__main__':

    spec_string = sys.args[1]

    specs = parse_subblock_config(spec_string)


    block_names = []

    for spec in specs.keys():
        block_names.extend(gen_subblock_names)
    
    print "\n".join(block_names)

    sys.exit(0)
