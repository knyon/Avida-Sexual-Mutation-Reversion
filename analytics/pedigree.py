#! /Library/Frameworks/Python.framework/Versions/3.1/bin/python3

import re
import sys
from collections import deque

pedigree = {}

class pedigree_queue(deque):

    def __init__(self, *items):
        super(pedigree_queue, self).__init__(self)
        self.append(*items)

    def append(self, *items):
        for i in items:
            super(pedigree_queue, self).append(i)


def create_pedigree_from_detail_file(file_name):
    for line in open(file_name):
        entry = parse_detail_line(line) 
        if entry:
            add_genotype_to_pedigree(entry)

def parse_detail_line(detail):
    regex = re.compile(r"^(\d*)[\s\)\(:a-z]*(\d*),(\d*).*heads_sex\s([a-z]*)")
    matched_genotype_ids = regex.match(detail)

    if matched_genotype_ids:
        genotype_id = matched_genotype_ids.group(1)
        parent_a_id = matched_genotype_ids.group(2)
        parent_b_id = matched_genotype_ids.group(3)
        sequence = matched_genotype_ids.group(4)
        return (genotype_id, sequence, parent_a_id, parent_b_id)
    else:
        return ''

def add_genotype_to_pedigree(entry):
    key = entry[0]
    value = (entry[1], entry[2], entry[3])
    pedigree[key] = value

def pedigree_breadth_first_search(start_genotype_id, target_id):
    bfs_queue = pedigree_queue(start_genotype_id, None)
    node_was_visited = make_map_for_visited_nodes()
    tree_level = 0

    while bfs_queue:
        node = bfs_queue.popleft()
        if node_marks_last_in_level(node): 
            tree_level += 1
            bfs_queue.append(node)
        elif node == target_id:
            return (node, tree_level)
        elif node_was_visited[node] or node_was_genesis(node):
            continue
        else:
            bfs_queue.append(*get_parents(node))
            node_was_visited[node] = 1
    raise Exception("No such genotype ID")

def make_map_for_visited_nodes():
    visited_nodes_map = {}
    for k in pedigree.keys():
        visited_nodes_map[k] = False
    return visited_nodes_map

def node_marks_last_in_level(node):
    return not node

def get_parents(genotype_id):
    listing = pedigree[genotype_id]
    return (listing[1], listing[2])

def node_was_genesis(node):
    genesis_id = '1'
    return node == genesis_id

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python pedigree detail_dump_file_name")
        exit()
    file_name = sys.argv[1]
    create_pedigree_from_detail_file(file_name)
