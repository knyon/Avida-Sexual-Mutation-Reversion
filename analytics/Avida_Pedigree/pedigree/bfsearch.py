from pedigree.pqueue import PedigreeQueue

class BFSearcher():

    def __init__(self, pedigree):
        self.pedigree = pedigree

    def pedigree_breadth_first_search(self, start_genotype_id, target_id):
        bfs_queue = PedigreeQueue(start_genotype_id, None)
        node_was_visited = self.make_map_for_visited_nodes()
        tree_level = 0

        while bfs_queue:
            node = bfs_queue.popleft()
            if self.node_marks_last_in_level(node): 
                if len(bfs_queue) == 0:
                    break
                tree_level += 1
                bfs_queue.append(node)
            elif node == target_id:
                return (node, tree_level)
            elif self.node_was_genesis(node) or node_was_visited[node]:
                continue
            else:
                bfs_queue.append(*self.get_parents(node))
                node_was_visited[node] = True
        raise Exception("No such genotype ID")

    def make_map_for_visited_nodes(self):
        visited_nodes_map = {}
        for k in self.pedigree.keys():
            visited_nodes_map[k] = False
        return visited_nodes_map

    def get_parents(self, genotype_id):
        genotype = self.pedigree[genotype_id]
        return genotype.get_parents_as_tuple()

    @staticmethod
    def node_marks_last_in_level(node):
        return node is None

    @staticmethod
    def node_was_genesis(node):
        genesis_id = '1'
        return node == genesis_id
