from collections import deque
from pedigree.genotype import Genotype

class GenealogyQueue(deque):
    '''Extension of the deque collection that allows for appending multiple
    items at once'''

    def __init__(self, *items):
        super(GenealogyQueue, self).__init__(self)
        self.append(*items)

    def append(self, *items):
        for i in items:
            super(GenealogyQueue, self).append(i)

class EndOfLevelMarker():
    '''EndOfLevelMarker is just a skeleton class to detect the end of a queue
    in a breadth-first search. This is more clearn than just using 'None' or
    some other indicator.'''
    pass


def _node_marks_last_in_level(node):
    return isinstance(node, EndOfLevelMarker)

def _node_was_genesis(node):
    genesis_id = '1'
    return node == genesis_id


class Genealogy():
    def __init__(self, dominantGenotype=''):
        self.dominantGenotype = dominantGenotype
        self.genealogy = {}

    def has_genotype_id(self, genotypeID):
        return genotypeID in self.genealogy.keys()

    def add_genotype(self, details):
        newGenotype = Genotype(*details)
        key = newGenotype.genotypeID
        self.genealogy[key] = newGenotype

    def add_children_to_lineage_of_genotype(self, start_genotype_id):
        queue = GenealogyQueue(start_genotype_id, EndOfLevelMarker())
        node_was_visited = self._make_map_for_visited_nodes()
        tree_level = 0

        while queue:
            node = queue.popleft()
            if _node_marks_last_in_level(node): 
                if len(queue) == 0:
                    break
                tree_level += 1
                queue.append(node)
            elif _node_was_genesis(node) or node_was_visited[node]:
                continue
            else:
                parentIDs = self.get_parents(node)
                self._add_child_to_parents(node, parentIDs)
                queue.append(*parentIDs)
                node_was_visited[node] = True

    def get_parents(self, genotype_id):
        genotype = self.genealogy[genotype_id]
        return genotype.get_parents_as_tuple()

    def get_children(self, genotype_id):
        genotype = self.genealogy[genotype_id]
        return genotype.children

    def _make_map_for_visited_nodes(self):
        visited_nodes_map = {}
        for k in self.genealogy.keys():
            visited_nodes_map[k] = False
        return visited_nodes_map

    def _add_child_to_parents(self, node, parentIDs):
        for parentID in parentIDs:
            parentGenotype = self.genealogy[parentID]
            if not parentGenotype.has_child(node):
                parentGenotype.add_child(node)
