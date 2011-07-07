from pedigree.pqueue import PedigreeQueue

class BreadthFirst():
    def __init__(self, pedigree):
        self.pedigree = pedigree


    def get_parents(self, genotype_id):
        genotype = self.pedigree[genotype_id]
        return genotype.get_parents_as_tuple()

    def get_children(self, genotype_id):
        genotype = self.pedigree[genotype_id]
        return genotype.children

    def _make_map_for_visited_nodes(self):
        visited_nodes_map = {}
        for k in self.pedigree.keys():
            visited_nodes_map[k] = False
        return visited_nodes_map

    @staticmethod
    def _node_marks_last_in_level(node):
        return node is None

    @staticmethod
    def _node_was_genesis(node):
        genesis_id = '1'
        return node == genesis_id


class BFSearcher(BreadthFirst):

    def search_pedigree(self, start_genotype_id, target_id):
        bf_queue = PedigreeQueue(start_genotype_id, None)
        node_was_visited = self._make_map_for_visited_nodes()
        tree_level = 0

        while bf_queue:
            node = bf_queue.popleft()
            if self._node_marks_last_in_level(node): 
                if len(bf_queue) == 0:
                    break
                tree_level += 1
                bf_queue.append(node)
            elif node == target_id:
                return (node, tree_level)
            elif self._node_was_genesis(node) or node_was_visited[node]:
                continue
            else:
                bf_queue.append(*self.get_parents(node))
                node_was_visited[node] = True
        raise Exception("No such genotype ID")


#####ROUGH######
class CHILD_BFSearcher(BreadthFirst):

    def search_pedigree(self, start_genotype_id, target_id):
        bf_queue = PedigreeQueue(start_genotype_id, None)
        node_was_visited = self._make_map_for_visited_nodes()
        tree_level = 0

        while bf_queue:
            node = bf_queue.popleft()
            if self._node_marks_last_in_level(node): 
                if len(bf_queue) == 0:
                    break
                tree_level += 1
                bf_queue.append(node)
            elif node == target_id:
                return (node, tree_level)
            elif self._node_was_genesis(node) or node_was_visited[node]:
                continue
            else:
                bf_queue.append(*self.get_children(node))
                node_was_visited[node] = True
        raise Exception("No such genotype ID")


class BFTraverser(BreadthFirst):

    def add_children_to_genotypes(self, start_genotype_id):
        bf_queue = PedigreeQueue(start_genotype_id, None)
        node_was_visited = self._make_map_for_visited_nodes()
        tree_level = 0

        while bf_queue:
            node = bf_queue.popleft()
            if self._node_marks_last_in_level(node): 
                if len(bf_queue) == 0:
                    break
                tree_level += 1
                bf_queue.append(node)
            elif self._node_was_genesis(node) or node_was_visited[node]:
                continue
            else:
                parentIDs = self.get_parents(node)
                self.add_child_to_parents(node, parentIDs)
                bf_queue.append(*parentIDs)
                node_was_visited[node] = True

    def add_child_to_parents(self, node, parentIDs):
        for parentID in parentIDs:
            parentGenotype = self.pedigree[parentID]
            if not parentGenotype.has_child(node):
                parentGenotype.add_child(node)
