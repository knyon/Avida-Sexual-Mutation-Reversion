pedigree = {}


def pedigree_breadth_first_search(start_genotype_id, target_id):
    bfs_queue = pedigree_queue(start_genotype_id, None)
    node_was_visited = make_map_for_visited_nodes()
    tree_level = 0

    while bfs_queue:
        node = bfs_queue.popleft()
        if node_marks_last_in_level(node): 
            if len(bfs_queue) == 0:
                break
            tree_level += 1
            bfs_queue.append(node)
        elif node == target_id:
            return (node, tree_level)
        elif node_was_genesis(node) or node_was_visited[node]:
            continue
        else:
            bfs_queue.append(*get_parents(node))
            node_was_visited[node] = True
    raise Exception("No such genotype ID")

def make_map_for_visited_nodes():
    visited_nodes_map = {}
    for k in pedigree.keys():
        visited_nodes_map[k] = False
    return visited_nodes_map

def node_marks_last_in_level(node):
    return node is None

def get_parents(genotype_id):
    listing = pedigree[genotype_id]
    return (listing[1], listing[2])

def node_was_genesis(node):
    genesis_id = '1'
    return node == genesis_id
