"""Hardware abstraction layer for the system on which process groups are run.

Classes:
NodeCard -- node cards make up Partitions
Block -- atomic set of nodes
BlockDict -- default container for blocks
ProcessGroup -- virtual process group running on the system
ProcessGroupDict -- default container for process groups
BGBaseSystem -- base system component
"""

import sys
import time
import xmlrpclib
import copy
import Cobalt
import re
import Cobalt.Util
from Cobalt.Data import Data, DataDict
from Cobalt.Exceptions import JobValidationError, ComponentLookupError
from Cobalt.Components.base import Component, exposed, automatic, query, locking
import thread, ConfigParser
from Cobalt.Proxy import ComponentProxy
from Cobalt.DataTypes.ProcessGroup import ProcessGroupDict


__all__ = [
    "Node"
    "NodeCard",
    "Block",
    "BlockDict",
    "BGBaseSystem",
]

#try:
#    Cobalt.Util.init_cobalt_config()
#except:
#    print ERROR: Problem reading config.
#    sys.exit(1)
CP = ConfigParser.ConfigParser()
CP.read(Cobalt.CONFIG_FILES)
try:
    max_drain_hours = float(CP.get('bgsystem', 'max_drain_hours'))
except:
    max_drain_hours = float(sys.maxint)

#you'd think that this would be in the control system database somewhere, but it's not.
#this generates the node locations for N00 in a midplane.  So far as I know (and I can 
#be proven wrong here) these are consistient between midplanes.

#Also, when moving between nodes, the B and E dimensions seem to like to reverse together.
#No I don't know why.

def generate_base_node_map():

    ret_map = [[0,0,0,0,0]]
    
    __transform_subcube(ret_map)
    ret_map.append(__transform_dim(('b','d'), ret_map[len(ret_map)-1])) 
    __transform_subcube(ret_map)
    ret_map.append(__transform_dim(('a','b','c'), ret_map[len(ret_map)-1]))
    __transform_subcube(ret_map)
    ret_map.append(__transform_dim(('b','d'), ret_map[len(ret_map)-1]))  
    __transform_subcube(ret_map)

    return ret_map

def __transform_subcube(coord_map):

    coord_map.append(__transform_dim(('c',), coord_map[len(coord_map)-1]))
    coord_map.append(__transform_dim(('b',), coord_map[len(coord_map)-1]))
    coord_map.append(__transform_dim(('c',), coord_map[len(coord_map)-1]))
    coord_map.append(__transform_dim(('e',), coord_map[len(coord_map)-1]))
    coord_map.append(__transform_dim(('c',), coord_map[len(coord_map)-1]))
    coord_map.append(__transform_dim(('b',), coord_map[len(coord_map)-1]))
    coord_map.append(__transform_dim(('c',), coord_map[len(coord_map)-1]))

    return

def __transform_dim(dims, dim_tuple):
   
    ret = [i for i in dim_tuple]
    
    if 'a' in dims:
        ret[0] = ret[0] ^ 1 
    if 'b' in dims:
        ret[1] = ret[1] ^ 1 
    if 'c' in dims:
        ret[2] = ret[2] ^ 1 
    if 'd' in dims:
        ret[3] = ret[3] ^ 1 
    if 'e' in dims:
        ret[4] = ret[4] ^ 1 
    
    return ret

#these allow us to translate from NXX positons in the midplane
#to the correct local coord for a nodecard.
#NOTE: if you flip the B-dim flip the E as well...
NODECARD_A_DIM_MASK = 4
NODECARD_B_DIM_MASK = 8
NODECARD_C_DIM_MASK = 1
NODECARD_D_DIM_MASK = 2
NODECARD_E_DIM_MASK = 8

A_DIM = 0
B_DIM = 1
C_DIM = 2
D_DIM = 3
E_DIM = 4

#generate this once.  Everything else is just this transposed.
base_node_map = generate_base_node_map()

nodes_per_nodecard = 32
subrun_only_size = 128

node_position_exp  = re.compile(r'-J(?P<pos>[0-9][0-9])')
nodecard_exp = re.compile(r'-N(?P<pos>[0-9][0-9])')
midplane_exp = re.compile(r'-M(?P<pos>[0-9])')
rack_exp = re.compile(r'R(?P<pos>[0-9][0-9])')

def get_node_coords(node_pos, nodecard_pos):

    ret_coords = list(base_node_map[node_pos])
    if bool(nodecard_pos & NODECARD_A_DIM_MASK):
        ret_coords[0] = ret_coords[0] ^ 1
    if bool(nodecard_pos & NODECARD_B_DIM_MASK):
        ret_coords[1] = ret_coords[1] ^ 1
    if bool(nodecard_pos & NODECARD_C_DIM_MASK):
        ret_coords[2] = ret_coords[2] ^ 1
    if bool(nodecard_pos & NODECARD_D_DIM_MASK):
        ret_coords[3] = ret_coords[3] ^ 1
    if bool(nodecard_pos & NODECARD_E_DIM_MASK):
        ret_coords[4] = ret_coords[4] ^ 1
    return ret_coords

def verify_extents_for_size(coords, size):
    '''Return true if the extents do not go beyond the maximum for a midplane, for subblock use.

       Must be < 512 nodes for now.

    '''
    extents = _get_extents_from_size(size)

    for i in range(0,5):
        if (coords[i] + extents[i]) > 4:
            return False
    return True

def _get_extents_from_size(size):
    '''Given a size, generate the extents for BG/Q subblock job use.

    '''
    left = int(size)
    count = 0
    ret_extents = [1,1,1,1,1]
    dim_order = []

    if size <= 512 and size >= 64:
        ret_extents = [2,2,2,2,2]
        dim_order = [2,3,0,1,-1] #nodecard in midplane order #c,d,a,b
            #E dimension doens't figure in, should cause an error
        left /= 32

    
    #for the subnodeboard shape 32 or less
    elif size <= 32:
        dim_order = [0,3,4,1,2] #Order for nodecards: c,b,e,d,a
    else:
        raise ValueError(("Size %s to get_extents_from_size outside of proper range." % size))

    while left != 1:
        ret_extents[dim_order[count]] *= 2
        count += 1
        left /= 2

    return ret_extents


class Node (object):

    def __init__(self, spec):
        #can be invoked with a spec string from the bridge API
        self.nodeboard = spec.get("nodeboard")
        self.name = spec.get("name") # RXX-MY-NZZ-JAA
        self.nodecard_pos = spec.get("nodecard_pos") #NZZ
        self.node_pos = spec.get("position") # JAA
        self.status = spec.get("status", "A")
        #Available, Failed
        self.reverse_A = bool(self.nodecard_pos & NODECARD_A_DIM_MASK)
        self.reverse_B = bool(self.nodecard_pos & NODECARD_B_DIM_MASK)
        self.reverse_C = bool(self.nodecard_pos & NODECARD_C_DIM_MASK)
        self.reverse_D = bool(self.nodecard_pos & NODECARD_D_DIM_MASK)
        self.reverse_E = bool(self.nodecard_pos & NODECARD_E_DIM_MASK)
        self.in_use = False
        self.coords = base_node_map[self.node_pos]
        if self.reverse_A:
            self.coords[0] = self.coords[0] ^ 1
        if self.reverse_B:
            self.coords[1] = self.coords[1] ^ 1
        if self.reverse_C:
            self.coords[2] = self.coords[2] ^ 1
        if self.reverse_D:
            self.coords[3] = self.coords[3] ^ 1
        if self.reverse_E:
            self.coords[4] = self.coords[4] ^ 1

    def set_status(self, status):
        #TODO: put in valid statuses in here, exception on bad statuses
        self.status = status

    def mark_in_use(self):
        self.in_use = True

    def mark_free(self):
        self.in_use = False

    def report_dict(self):
        return {'coords': self.coords,
                'in_use': self.in_use,
                'status': self.status,
                'name': self.name,
                }

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s id=%r>" % (self.__class__.__name__, self.name)

    def __eq__(self, other):
        return self.name == other.name

class NodeCard (object):
    """node boards make up midplanes
   
       they are also something we can fake-control without the control system.
    """
    def __init__(self, name, state="idle"):
        self.name = name
        self.nodecard =  int(nodecard_exp.search(name).groups()[0])#NXX
        self.rack = 0 #get from control system, for EAS this is fine
        self.midplane = 0 #get from control system, for EAS this is fine
        self.used_by = '' #Block(s) that is/are using the nodeboard
        self.reserved_by = '' #jobid reserving this
        self.state = state
        self.in_use = False
        #will be able to pull from the control system later, for now generate this:
        self.nodes = []
        for i in range(0, 32):
            self.nodes.append( Node({'nodecard_pos': self.nodecard,
                             'position': i,
                             'status': 'A',
                             'name': 'R%02d-M%d-N%02d-J%02d' % (self.rack,  
                                 self.midplane, self.nodecard, i),
                             }))

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<%s id=%r>" % (self.__class__.__name__, self.name)


    def __eq__(self, other):
        return self.id == other.id

    #def _update_nodes(self):
        
    #TODO: make sure to check my nodes to see if they have failed, if they've tanked, I've tanked.
       
    def extract_nodes_by_extent(self, corner, extents):
        '''Get a list of nodes that are included by a corner and extent on this board.

        corner: [a,b,c,d,e] integer coordinates.
        extents: [a,b,c,d,e] integer extents, constrained to 4x4x4x4x2.

        Return: List of Nodes: Return an empty list and raise an error if you have a mismatch.

        '''

        ret_nodes = []
        
        #Note that nodes can be anywhere on the nodeboard in a block.  I think we have to scan each time.
        for node in self.nodes:
            for i in range(0,5):
                mismatch = False
                if not (node.coords[i] >= corner[i] and
                        node.coords[i] < (corner[i] + extents[i])):
                    mismatch = True
                    break
            if not mismatch:
                ret_nodes.append(node)

        extent_size = 1
        for e in extents:
            extent_size *= e

        if len(ret_nodes) != extent_size:
            #we are looking for nodes not on this nodeboard.  That is likely an error.
            raise RuntimeError("bgq_base_system.NodeCard: Mismatch in extent size and number of nodes returned. Size: %s, Nodes: %s" % (extent_size, len(ret_nodes)))

        return ret_nodes


block_states = ['idle', #nodeboard is idle and can be used in scheduling decisions
                'allocated', #nodeboard is booted by control system, nothing running on it
                'reserved', #nodeboard is a part of a reservation
                'disabled', #admin has disabled the nodebaord in question
                'busy', #control system reporting block busy
                ]



class Block (Data):
    
    """An atomic set of nodes.
    
    Blocks can be reserved to run process groups on.
    
    Attributes:
    tag -- block or pseudoblock
    scheduled -- ? (default False)
    name -- canonical name
    functional -- the block is available for scheduling
    queue -- ?
    parents -- super(containing)-blocks
    children -- sub-blockss
    size -- number of nodes in the block
    
    Properties:
    state -- "idle", "busy", or "blocked"
    """
    
    fields = Data.fields + [
        "tag", "scheduled", "name", "functional",
        "queue", "size", "parents", "children", "state", 
        "backfill_time",
    ]
    
    def __init__ (self, spec):
        """Initialize a new block."""
        Data.__init__(self, spec)
        spec = spec.copy()
        self.scheduled = spec.pop("scheduled", False)
        self.name = spec.pop("name", None)
        self.functional = spec.pop("functional", False)
        self.queue = spec.pop("queue", "default")
        self.size = int(spec.pop("size", None))
        # these hold Partition objects
        self.state = spec.pop("state", "idle")
        self.tag = spec.get("tag", "partition")
        self.bridge_block = None
        self.node_cards = spec.get("node_cards", [])
        self.nodes = spec.get("nodes", []) 
        self.switches = spec.get("switches", [])
        self.reserved_until = False
        self.reserved_by = None
        self.used_by = None
        self.cleanup_pending = False

        # this holds block names
        self._wiring_conflicts = set()
        self.backfill_time = None
        self.draining = False

        self._relatives = [] #list of blocks that have overlapping resources with this one
        self._parents = [] #relatives that are a superset of me
        self._childeren = [] #relatives that are proper subsets of me
         
        self.admin_failed = False #set this to true if a partadm --fail is issued

        self._update_node_cards()

        if self.size < subrun_only_size:
            #we have to make a pseudoblock
            self.block_type = "pseudoblock"
        else:
            self.block_type = "normal"

        if self.block_type == "normal":
            for nc in self.node_cards:
                self.nodes.extend(nc.nodes)
        elif self.block_type == "pseudoblock":
            #these are not being tracked by the control system, and are not allocated by it
            #these are just subrun targets.
            if self.size >= nodes_per_nodecard:
                for nc in self.node_cards:
                    self.nodes.extend(nc.nodes)
            else:
                #parse name to get corner node
                node_pos = int(node_position_exp.search(self.name).groups()[0])
                nodecard_pos = int(nodecard_exp.search(self.name).groups()[0])
                #sanity check extents
                corner_coords = get_node_coords(node_pos, nodecard_pos)
                stat = verify_extents_for_size(corner_coords, self.size)
                if not stat:
                    raise RuntimeError("Invalid corner node for chosen block size.")
                #pull in all nodenames by coords from nodecard.
                nc = self.node_cards[0] #only one node_card is in use in this case.
                self.nodes.extend(nc.extract_nodes_by_extent(corner_coords, _get_extents_from_size(self.size)))

    def _update_node_cards(self):
        if self.state != "idle":
            for nc in self.node_cards:
                nc.used_by = self.name
        else:
            for nc in self.node_cards:
                nc.used_by = ''
   
    def _update_nodes(self):
        if self.state != "idle":
            for node in self.nodes:
                node.in_use = True
        else:
            for node in self.nodes:
                node.in_use = False

    def _get_relatives (self):
        return [r.name for r in self._relatives]
    
    relatives = property(_get_relatives)
    
    def _get_node_card_names (self):
        return [nc.name for nc in self.node_cards]
    
    node_card_names = property(_get_node_card_names)
    
    def _get_parents(self):
        return [block.name for block in self._relatives if block.is_superblock(self)]
    parents = property(_get_parents)
    
    def _get_childeren(self):
        return [block.name for block in self._relatives if block.is_subblock(self)]
    children = property(_get_childeren)

    def _get_node_names (self):
        return [n.name for n in self.nodes]
    
    node_names = property(_get_node_names)

    def __str__ (self):
        return self.name
    
    def __repr__ (self):
        return "<%s name=%r>" % (self.__class__.__name__, self.name)

    def does_block_overlap(self, block):
        '''Determines if blocks overlap.  Does not add block to relatives if 
        it does. Just a test.

        '''

        if self.name == block.name:
            return False #don't overlap with yourself.
        
        b1_nc_names = set(self.node_card_names)
        b2_nc_names = set(block.node_card_names)
    
        if not (b1_nc_names & b2_nc_names):
            return False
        
        b1_node_names = set(self.node_names)
        b2_node_names = set(block.node_names)

        if not (b1_node_names & b2_node_names):
            return False
        
        return True

    def mark_if_overlap(self, block):
        '''Mark both blocks if they are relatives of eachother.

        Returns True if an overlap is detected, otherwise false.

        '''
        if self.does_block_overlap(block):
            if self not in block._relatives:
                self._relatives.append(block)
                block._relatives.append(self)
            return True
        else:
            if self in block._relatives:
                self._relatives.remove(block)
                block._relatives.remove(self)

        return False

    def is_superblock(self, block):

        if self.name == block.name:
            return False
        
        b1_nc_names = set(self.node_card_names)
        b2_nc_names = set(block.node_card_names)
        if not (b1_nc_names >= b2_nc_names):
            return False
        if len(b1_nc_names ^ b2_nc_names) == 0:
            b1_node_names = set(self.node_names)
            b2_node_names = set(block.node_names)

            if not (b1_node_names >= b2_node_names): 
                return False

        return True
    
    def is_subblock(self, block):
        if self.name == block.name:
            return False
        return not self.is_superblock(block)


class BlockDict (DataDict):
    """Default container for blocks.
    
    Keyed by block name.
    """
    
    item_cls = Block
    key = "name"



class BGProcessGroupDict(ProcessGroupDict):
    """ProcessGroupDict modified for Blue Gene systems"""

    def __init__(self):
        ProcessGroupDict.__init__(self)

    def find_by_jobid(self, jobid):
        """Find process groups by jobid"""
        for id, pg in self.iteritems():
            if pg.jobid == jobid:
                return pg
        return None



class BGBaseSystem (Component):
    """base system class. 
    
    Methods:
    add_blocks -- tell the system to manage blocks (exposed, query)
    get_blocks -- retrieve blocks in the simulator (exposed, query)
    del_blocks -- tell the system not to manage blocks (exposed, query)
    set_blocks -- change random attributes of blocks (exposed, query)
    update_relatives -- should be called when blocks are added and removed from the managed list
    
    *_partitions are also exposed so that external components don't have to be rewritten.

    Note: This class uses Python's threading module.

    """
    
    def __init__ (self, *args, **kwargs):
        Component.__init__(self, *args, **kwargs)
        self._blocks = BlockDict()
        self._managed_blocks = set()
        self.process_groups = BGProcessGroupDict()
        self._blocks_lock = thread.allocate_lock()
        
        #bridge interaction
        self.bridge_in_error = False
        
        self.cached_blocks = None
        self.offline_blocks = []

    def _get_blocks (self):
        return BlockDict([
            (block.name, block) for block in self._blocks.itervalues()
            if block.name in self._managed_blocks
        ])
    
    blocks = property(_get_blocks)

    def add_blocks (self, specs, user_name=None):
        """Add a block to the managed block list.

        """
        self.logger.info("%s called add_blocks(%r)", user_name, specs)
        self.logger.info("%s", self._managed_blocks)
        specs = [{'name':spec.get("name")} for spec in specs]
        self._blocks_lock.acquire()
        try:
            blocks = [
                block for block in self._blocks.q_get(specs)
                if block.name not in self._managed_blocks
            ]
        except:
            blocks = []
            self.logger.error("error in add_blocks", exc_info=True)
        self._blocks_lock.release()
        
        self._managed_blocks.update([
            block.name for block in blocks
        ])
        self.update_relatives()
        return blocks
    add_block = exposed(query(add_blocks))
    add_partitions = exposed(query(add_blocks))

    def get_blocks (self, specs):
        """Query blocks on simulator.
        
        """
        self._blocks_lock.acquire()
        try:
            blocks = self.blocks.q_get(specs)
        except:
            blocks = []
            self.logger.error("error in get_blocks", exc_info=True)
        self._blocks_lock.release()
        
        return blocks
    get_blocks = exposed(query(get_blocks))
    get_partitions = exposed(query(get_blocks))
    
    def verify_locations(self, location_list):
        """Providing a system agnostic interface for making sure a 'location string' is valid
        
        """
        parts = self.get_blocks([{'name':l} for l in location_list])
        return [ p.name for p in parts ]
    verify_locations = exposed(verify_locations)

    def del_blocks (self, specs, user_name=None):
        """Remove blocks from the list of managed blocks
        
        """
        self.logger.info("%s called del_blocks(%r)", user_name, specs)
        
        self._blocks_lock.acquire()
        try:
            blocks = [
                block for block in self._blocks.q_get(specs)
                if block.name in self._managed_blocks
            ]
        except:
            blocks = []
            self.logger.error("error in del_blocks", exc_info=True)
        self._blocks_lock.release()
        
        self._managed_blocks -= set( [block for block in blocks] )
        import copy
        
        self.update_relatives()
        return blocks
    del_blocks = exposed(query(del_blocks))
    del_partitions = exposed(query(del_blocks))

    def set_blocks (self, specs, updates, user_name=None):
        """Update random attributes on matching blocks
        
        """
        def _set_blocks(block, newattr):
            self.logger.info("%s updating block %s: %r", user_name, block.name, newattr)
            block.update(newattr)
            
        self._blocks_lock.acquire()
        try:
            blocks = self._blocks.q_get(specs, _set_blocks, updates)
        except:
            blocks = []
            self.logger.error("error in set_blocks", exc_info=True)
        self._blocks_lock.release()
        return blocks
    set_blocks = exposed(query(set_blocks))
    set_partitions = exposed(query(set_blocks))

    def update_relatives(self):
        """ Update a block's relatives.  A block is a relative of another 
        block iff it shares resources with the other block (nodecards, nodes, wires, &c.)

        This method should always be called when we change the contests of self._managed_blocks.
        Perhaps self._managed_blocks should be altered to always invoke this?

        """
        #TODO: This needs to be changed so that more overlapping 
        #resources can be determined. More granularity may be needed.

        #partial overlaps are being tracked, not sure what to do about paternity.

        for b_name in self._managed_blocks:
            b = self._blocks[b_name]

            # toss the wiring dependencies in with the parents
            for dep_name in b._wiring_conflicts:
                #no wiring dependencies to determine yet
                pass

            for other in self._blocks.itervalues():
                if b.name == other.name:
                    continue
                b.mark_if_overlap(other)
            
            b._parents = [block for block in b._relatives if block.is_superblock(b)]
            b._children = [block for block in b._relatives if block.is_subblock(b)]

    def validate_job(self, spec):
        """validate a job for submission

        Arguments:
        spec -- job specification dictionary
        """
        # spec has {nodes, walltime*, procs, mode, kernel}
        
        max_nodes = max([int(p.size) for p in self._blocks.values()])
        try:
            sys_type = CP.get('bgsystem', 'bgtype')
        except:
            sys_type = 'bgq'
        if sys_type == 'bgq':
            job_types = ['c1', 'c2', 'c4', 'c8','c16','c32','c64', 'script']
        else:
            raise JobValidationError("[bgq_base_system]: Unsupported System Type.")
        try:
            spec['nodecount'] = int(spec['nodecount'])
        except:
            raise JobValidationError("Non-integer node count")
        if not 0 < spec['nodecount'] <= max_nodes:
            raise JobValidationError("Node count out of realistic range")
        if float(spec['time']) < 5:
            raise JobValidationError("Walltime less than minimum")
        if not spec['mode']:
            if sys_type == 'bgq':
                spec['mode'] = 'c1'
        if spec['mode'] not in job_types:
            raise JobValidationError("Invalid mode")
        if spec['attrs'].has_key("location"):
            p_name = spec['attrs']['location']
            if not self.blocks.has_key(p_name):
                raise JobValidationError("Partition %s not found" % p_name)
        spec['proccount'] = spec['nodecount']
        #if not spec['proccount']:
        #    if spec.get('mode', 'co') == 'vn':
        #        if sys_type == 'bgl':
        #            spec['proccount'] = str(2 * int(spec['nodecount']))
        #        elif sys_type == 'bgp':
        #            spec['proccount'] = str(4 * int(spec['nodecount']))
        #        else:
        #            self.logger.error("Unknown bgtype %s" % (sys_type))
        #    elif spec.get('mode', 'co') == 'dual':
        #        spec['proccount'] = 2 * int(spec['nodecount'])
        #    else:
        #        spec['proccount'] = spec['nodecount']
        #else:
        #    try:
        #        spec['proccount'] = int(spec['proccount'])
        #    except:
        #        JobValidationError("non-integer proccount")
        #    if spec['proccount'] < 1:
        #        raise JobValidationError("negative proccount")
        #    if spec['proccount'] > spec['nodecount']:
        #        if spec['mode'] not in ['vn', 'dual']:
        #            raise JobValidationError("proccount too large")
        #        if sys_type == 'bgl' and (spec['proccount'] > (2 * spec['nodecount'])):
        #            raise JobValidationError("proccount too large")
        #        elif sys_type == ' bgp'and (spec['proccount'] > (4 * spec['nodecount'])):
        #            raise JobValidationError("proccount too large")
        
        # have to set ranks per node based on mode:

        if spec['mode'] == 'script':
            spec['ranks_per_node'] = None
        else: #remember c1 is default, so ranks_per_node defaults to 1
            rpn_re  = re.compile(r'c(?P<pos>[0-9]*)')
            spec['ranks_per_node'] = int(rpn_re.match(spec['mode']).groups()[0])
        # need to handle kernel
        return spec
    validate_job = exposed(validate_job)
        

    def fail_blocks(self, specs, user_name=None):
        '''Manually put a block into a failed state by admin-action

        '''
        self.logger.info("%s failing block %s", user_name, specs)
        blocks = self.get_blocks(specs)
        if not blocks:
            ret = "no matching blocks found\n"
        else:
            ret = ""
        for b in blocks:
            #mark the block as admin-failed?
            if not b.admin_failed:
                ret += "failing %s\n" % b.name
                b.admin_failed = True
            else:
                ret += "%s is already marked as failing\n" % p.name

        return ret
    fail_blocks = exposed(fail_blocks)
    
    def unfail_blocks(self, specs, user_name=None):
        '''Bring a block out of a failed state that was entered by an admin action.


        '''
        self.logger.info("%s unfailing block %s", user_name, specs)
        block = self.get_blocks(specs)
        if not parts:
            ret = "no matching blocks found\n"
        else:
            ret = ""
        for b in self.get_blocks(specs):
            if b.admin_failed:
                ret += "unfailing %s\n" % b.name
                b.admin_failed = False
            else:
                ret += "%s is not currently failing\n" % p.name
        
        return ret
    unfail_blocks = exposed(unfail_blocks)
    
    def _find_job_location(self, args, drain_blocks=set(), backfilling=False):
        jobid = args['jobid']
        nodes = args['nodes']
        queue = args['queue']
        utility_score = args['utility_score']
        walltime = args['walltime']
        #walltime_p = args.get('walltime_p', walltime)  #*AdjEst* 
        forbidden = args.get("forbidden", [])
        required = args.get("required", [])
       
        #if walltime_prediction_enabled:  # *Adj_Est*
        #    runtime_estimate = float(walltime_p)  
        #else:
        #    runtime_estimate = float(walltime)
        
        best_score = sys.maxint
        best_block = None
        
        available_blocks = set()
        
        requested_location = None
        if args['attrs'].has_key("location"):
            requested_location = args['attrs']['location']
                
        if required:
            # whittle down the list of required blocks to the ones of the proper size
            # this is a lot like the stuff in _build_locations_cache, but unfortunately, 
            # reservation queues aren't assigned like real queues, so that code doesn't find
            # these
            for p_name in required:
                available_blocks.add(self.cached_blocks[p_name])
                available_blocks.update(self.cached_blocks[p_name]._children)

            possible = set()
            for p in available_blocks:            
                possible.add(p.size)
                
                
            desired_size = 0
            job_nodes = int(nodes)
            for psize in sorted(possible):
                if psize >= job_nodes:
                    desired_size = psize
                    break
            for p in available_blocks.copy():
                if p.size != desired_size:
                    available_blocks.remove(p)
                elif p.name in self._not_functional_set:
                    available_blocks.remove(p)
                elif requested_location and p.name != requested_location:
                    available_blocks.remove(p)
            
        else:
            for p in self.possible_locations(nodes, queue):
                skip = False
                for bad_name in forbidden:
                    if p.name==bad_name or bad_name in p.relatives:
                        skip = True
                        break
                if not skip:
                    if (not requested_location) or (p.name == requested_location):
                        available_blocks.add(p)
        
        available_blocks -= drain_blocks
        now = time.time()
        
        for block in available_blocks:
            # if the job needs more time than the block currently has available, look elsewhere    
            if backfilling: 
                               
                if block.reserved_by:
                    #if the block is reserved, we don't use predicted walltime to backfill
                    runtime_estimate = float(walltime)
                
         #       if 60 * runtime_estimate > (block.backfill_time - now):      # *Adj_Est*
         #           continue
                
                if 60*float(walltime) > (block.backfill_time - now):
                    continue
                
            if block.state == "idle":
                # let's check the impact on blocks that would become blocked
                score = 0
                for p in block.parents:
                    if self.cached_blocks[p].state == "idle" and self.cached_blocks[p].scheduled:
                        score += 1
                
                # the lower the score, the fewer new blocks will be blocked by this selection
                if score < best_score:
                    best_score = score
                    best_block = block        

        if best_block:
            return {jobid: [best_block.name]}


    def _find_drain_block(self, job):
        # if the user requested a particular block, we only try to drain that one
        if job['attrs'].has_key("location"):
            target_name = job['attrs']['location']
            return self.cached_blocks.get(target_name, None)
        
        drain_block = None
        locations = self.possible_locations(job['nodes'], job['queue'])
        
        for p in locations:
            if not drain_block:
                drain_block = p
            else:
                if p.backfill_time < drain_block.backfill_time:
                    drain_block = p
        
        if drain_block:
            # don't try to drain for an entire weekend 
            hours = (drain_block.backfill_time - time.time()) / 3600.0
            if hours > max_drain_hours:
                drain_block = None

        return drain_block


    def possible_locations(self, job_nodes, q_name):
        desired_size = 0
        job_nodes = int(job_nodes)
        if self._defined_sizes.has_key(q_name):
            for psize in self._defined_sizes[q_name]:
                if psize >= job_nodes:
                    desired_size = psize
                    break

        if self._locations_cache.has_key(q_name):
            return self._locations_cache[q_name].get(desired_size, [])
        else:
            return []

    # this function builds three things, namely a pair of dictionaries keyed by queue names, and a set of 
    # block names which are not functional
    #
    # self._defined_sizes maps queue names to an ordered list of block sizes available in that queue
    #     for all schedulable blocks (even if currently offline and not functional)
    # self._locations_cache maps queue names to dictionaries which map block sizes to block objects;
    #     this structure will only contain blocks which are fully online, so we don't try to drain a
    #     broken block
    # self._not_functional_set contains names of blocks which are not functional (either themselves, or
    #     a parent or child) 
    def _build_locations_cache(self):
        per_queue = {}
        defined_sizes = {}
        not_functional_set = set()
        for target_block in self.cached_blocks.itervalues():
            usable = True
            if target_block.name in self.offline_blocks:
                usable = False
            else:
                for part in self.cached_blocks.itervalues():
                    if not part.functional:
                        not_functional_set.add(part.name)
                        if target_block.name in part.children or target_block.name in part.parents:
                            usable = False
                            not_functional_set.add(target_block.name)
                            break

            for queue_name in target_block.queue.split(":"):
                if not per_queue.has_key(queue_name):
                    per_queue[queue_name] = {}
                if not defined_sizes.has_key(queue_name):
                    defined_sizes[queue_name] = set()
                if target_block.scheduled:
                    defined_sizes[queue_name].add(target_block.size)
                if target_block.scheduled and target_block.functional and usable:
                    if not per_queue[queue_name].has_key(target_block.size):
                        per_queue[queue_name][target_block.size] = []
                    per_queue[queue_name][target_block.size].append(target_block)
        
        for q_name in defined_sizes:
            defined_sizes[q_name] = sorted(defined_sizes[q_name])
        
        self._defined_sizes = defined_sizes
        self._locations_cache = per_queue
        self._not_functional_set = not_functional_set
    
    def find_job_location(self, arg_list, end_times):
        ''' get the best location for a job.

        '''
        
        best_block_dict = {}
        
        if self.bridge_in_error:
            #TODO: Make a bridge so that it can be in error.
            return {}
        
        self._blocks_lock.acquire()
        try:
            self.cached_blocks = copy.deepcopy(self.blocks)
        except:
            self.logger.error("error in copy.deepcopy", exc_info=True)
            return {}
        finally:
            self._blocks_lock.release()

        # build the cached_blocks structure first
        self._build_locations_cache()

            
        # first, figure out backfilling cutoffs per block (which we'll also use for picking which block to drain)
        job_end_times = {}
        for item in end_times:
            job_end_times[item[0][0]] = item[1]
            
        now = time.time()
        for p in self.cached_blocks.itervalues():
            if p.state == "idle":
                p.backfill_time = now
            else:
                p.backfill_time = now + 5*60
            p.draining = False
        
        for p in self.cached_blocks.itervalues():    
            if p.name in job_end_times:
                if job_end_times[p.name] > p.backfill_time:
                    p.backfill_time = job_end_times[p.name]
                
                for parent_name in p.parents:
                    parent_block = self.cached_blocks[parent_name]
                    if p.backfill_time > parent_block.backfill_time:
                        parent_block.backfill_time = p.backfill_time
        
        for p in self.cached_blocks.itervalues():
            if p.backfill_time == now:
                continue
            
            for child_name in p.children:
                child_block = self.cached_blocks[child_name]
                if child_block.backfill_time == now or child_block.backfill_time > p.backfill_time:
                    child_block.backfill_time = p.backfill_time

        
        # first time through, try for starting jobs based on utility scores
        drain_blocks = set()
        
        for job in arg_list:
            block_name = self._find_job_location(job, drain_blocks)
            if block_name:
                best_block_dict.update(block_name)
                break
            
            location = self._find_drain_block(job)
            if location is not None:
                for p_name in location.parents:
                    drain_blocks.add(self.cached_blocks[p_name])
                for p_name in location.children:
                    drain_blocks.add(self.cached_blocks[p_name])
                    self.cached_blocks[p_name].draining = True
                drain_blocks.add(location)
                #self.logger.info("job %s is draining %s" % (winning_job['jobid'], location.name))
                location.draining = True
        
        # the next time through, try to backfill, but only if we couldn't find anything to start
        if not best_block_dict:
            
            # arg_list.sort(self._walltimecmp)

            for args in arg_list:
                block_name = self._find_job_location(args, backfilling=True)
                if block_name:
                    self.logger.info("backfilling job %s" % args['jobid'])
                    best_block_dict.update(block_name)
                    break

        # reserve the stuff in the best_block_dict, as those blocks are allegedly going to 
        # be running jobs very soon
        #
        # also, this is the only part of finding a job location where we need to lock anything
        self._blocks_lock.acquire()
        try:
            for p in self.blocks.itervalues():
                # push the backfilling info from the local cache back to the real objects
                p.draining = self.cached_blocks[p.name].draining
                p.backfill_time = self.cached_blocks[p.name].backfill_time
                
            for jobid, block_list in best_block_dict.iteritems():
                part = self.blocks[block_list[0]]
                part.used_by = int(jobid)
                part.reserved_until = time.time() + 5*60
                part.state = "allocated"  
                for p in part._parents:
                    if p.state == "idle":
                        p.state = "blocked (%s)" % (part.name,)
                for p in part._children:
                    if p.state == "idle":
                        p.state = "blocked (%s)" % (part.name,)
        except:
            self.logger.error("error in find_job_location", exc_info=True)
        self._blocks_lock.release()
        
        return best_block_dict
    find_job_location = locking(exposed(find_job_location))
    
    def _walltimecmp(self, dict1, dict2):
        return -cmp(float(dict1['walltime']), float(dict2['walltime']))


    def find_queue_equivalence_classes(self, reservation_dict, active_queue_names):
        '''Make reservations equivalent to their queues, and set a block such 
        that jobs outside the reservation aren't scheduled on reserved resources.

        '''

        equiv = []
        for part in self.blocks.itervalues():
            if part.functional and part.scheduled:
                part_active_queues = []
                for q in part.queue.split(":"):
                    if q in active_queue_names:
                        part_active_queues.append(q)

                # go on to the next block if there are no running
                # queues using this block
                if not part_active_queues:
                    continue
                
                found_a_match = False
                for e in equiv:
                    if e['data'].intersection(part.node_card_names):
                        e['queues'].update(part_active_queues)
                        e['data'].update(part.node_card_names)
                        found_a_match = True
                        break
                if not found_a_match:
                    equiv.append( { 'queues': set(part_active_queues), 'data': set(part.node_card_names), 'reservations': set() } ) 
        
        real_equiv = []
        for eq_class in equiv:
            found_a_match = False
            for e in real_equiv:
                if e['queues'].intersection(eq_class['queues']):
                    e['queues'].update(eq_class['queues'])
                    e['data'].update(eq_class['data'])
                    found_a_match = True
                    break
            if not found_a_match:
                real_equiv.append(eq_class)

        equiv = real_equiv
                
        for eq_class in equiv:
            for res_name in reservation_dict:
                skip = True
                for b_name in reservation_dict[res_name].split(":"):
                    b = self.blocks[b_name]
                    if eq_class['data'].intersection(b.node_card_names):
                        eq_class['reservations'].add(res_name)
                    for dep_name in b._wiring_conflicts:
                        if self.blocks.has_key(dep_name):
                            if eq_class['data'].intersection(self.blocks[dep_name].node_card_names):
                                eq_class['reservations'].add(res_name)
                                break

            for key in eq_class:
                eq_class[key] = list(eq_class[key])
            del eq_class['data']
        
        return equiv
    find_queue_equivalence_classes = exposed(find_queue_equivalence_classes)
    
    
    def can_run(self, target_block, node_count, block_dict):
        '''Determine if a block is in a runable state.

           Should this go into the Block class? probably.
        '''
        if target_block.state != "idle":
            return False
        desired = sys.maxint
        for block in block_dict.itervalues():
            if not block.functional:
                if target_block.name in block.children or target_block.name in block.parents:
                    return False
            else:
                if block.scheduled:
                    if int(node_count) <= int(block.size) < desired:
                        desired = int(block.size)
        return target_block.scheduled and target_block.functional and int(target_block.size) == desired

    def reserve_resources_until(self, location, new_time, jobid):
        rc = False
        block_name = location[0]
        pg = self.process_groups.find_by_jobid(jobid)
        try:
            self._blocks_lock.acquire()
            used_by = self.blocks[block_name].used_by
            if new_time:
                if used_by == jobid:
                    self.blocks[block_name].reserved_until = new_time
                    self.blocks[block_name].reserved_by = jobid
                    self.logger.info("job %s: block '%s' now reserved until %s", jobid, block_name,
                        time.asctime(time.gmtime(new_time)))
                    rc = True
                else:
                    self.logger.error("job %s wasn't allowed to update the reservation on block %s (owner=%s)",
                        jobid, block_name, used_by)
            else:
                if used_by == jobid or used_by == None:
                    self.blocks[block_name].reserved_until = False
                    self.blocks[block_name].reserved_by = None
                    self.logger.info("reservation on block '%s' has been removed", block_name)
                    rc = True
                else:
                    self.logger.error("job %s wasn't allowed to clear the reservation on block %s (owner=%s)",
                        jobid, block_name, used_by)
        except:
            self.logger.exception("an unexpected error occurred will adjusting the block reservation time")
        finally:
            self._blocks_lock.release()
        return rc
    reserve_resources_until = exposed(reserve_resources_until)



