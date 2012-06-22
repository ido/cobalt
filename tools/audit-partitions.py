#!/usr/bin/env python

import Cobalt
from Cobalt.Proxy import ComponentProxy
import sys

def get_size(name):
    name_chunks = name.split('-')
    return int(name_chunks[len(name_chunks)-1])

if __name__ == '__main__':

    partitions = ComponentProxy('system').get_partitions([{'name':'*','parents':'*',
        'children':'*','switch_list':'*','wiring_conflicts':'*','node_card_list':'*',
        'size':'*'}])

    error = False
    part_dict = {}
    for part in partitions:
        part['parents'] = set(part['parents'])
        part['children'] =  set(part['children'])
        part['wiring_conflicts'] = set(part['wiring_conflicts'])
        part['node_card_list'] = set(part['node_card_list'])
        part['switch_list'] = set(part['switch_list'])
        part_dict[part['name']] = part

    for part in part_dict.itervalues():
        #Children are defined as blocks that are proper subsets of this block in terms of nodecards.
        #Children are always smaller than their parents.
        #Children are always fully overlapped by their parents
        for child in part['children']:
            child_part = part_dict[child]
            if child_part['size'] >=  part['size']:
                print "ERROR", child_part['name'], "is larger than parent", part['name']
                error = True
            else:
                if not child_part['node_card_list'].issubset(part['node_card_list']):
                    print "ERROR", child_part['name'], "has nodecards not in parent", part['name'],":"
                    print (child_part['node_card_list'] - part['node_card_list'])
                    error = True

        #Parents are all blocks with resources that intersect with this block's.  Any partial overlap
        #goes here.  Wiring conflicts end up here.
        #if we are a wiring conflict, we have no nodecards in common but we do share switches.

        for parent in part['parents']:
            parent_dict = part_dict[parent]
            if parent in part['wiring_conflicts']:
                if not parent_dict['node_card_list'].isdisjoint(part['node_card_list']):
                    print "ERROR", parent_dict['name'], "wiring conflict and nodecards in common", part['name']
                    error = True
            elif parent_dict['node_card_list'] > part['node_card_list']:
                #this is proper, no further tests needed.
                pass
            elif parent_dict['node_card_list'] < part['node_card_list']:
                #if a proper subset, then we have a child in parents
                print "ERROR", parent_dict['name'], "child found in parents set in partition", part['name']
                error = True
            elif  ((parent_dict['node_card_list'] - part['node_card_list']) and 
                  (part['node_card_list'] - parent_dict['node_card_list']) and
                  not part['node_card_list'].isdisjoint(parent_dict['node_card_list'])):
                #partial overlaps are ok, and belong here 
                pass
            else:
                print "ERROR", parent_dict['name'], "has an improper paternal relationship with", part['name']
                error = False

    if error:
        print 'FAILED'
    else:
        print 'SUCCESS'

    sys.exit(0)

