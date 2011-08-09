from collections import deque
from pedigree.genotype import Genotype

GENESIS = '1'

def node_marks_last_in_level(node):
    return isinstance(node, EndOfLevelMarker)

def node_is_genesis(node):
    return node == GENESIS


class ParamExpandDeque(deque):
    '''Extension of the deque collection that allows for appending multiple
    items at once'''
    def __init__(self, *items):
        super(ParamExpandDeque, self).__init__(self)
        self.append(*items)
    def append(self, *items):
        for i in items:
            super(ParamExpandDeque, self).append(i)


class EndOfLevelMarker():
    '''EndOfLevelMarker is just a skeleton class to detect the end of a queue
    in a breadth-first search. This is more clear than just using 'None' or
    some other indicator.'''
    pass


################################################################################

class GenealogyCreator:

    def create_pedigree_from_detail_file(fileName):
        genealogy = Genealogy()
        for line in open(fileName):
            details = DetailParser.process_line(line)
            genealogy.add_genotype(*details)
    
    def create_pedigree_from_string(inputString):
        genealogy = Genealogy()
        for line in inputString.split('\n'):
            details = DetailParser.process_line(line)
            genealogy.add_genotype(*details)
        add_childr


    @staticmethod
    def add_children_to_lineage_of_genotype(self, start_genotype_id):
        queue = ParamExpandDeque(start_genotype_id, EndOfLevelMarker())
        node_was_visited = self._make_map_for_visited_nodes()
        tree_level = 0

        while queue:
            node = queue.popleft()
            if node_marks_last_in_level(node): 
                if len(queue) == 0:
                    break
                tree_level += 1
                queue.append(node)
            elif node_is_genesis(node) or node_was_visited[node]:
                continue
            else:
                parentIDs = self.get_parents(node)
                self._add_child_to_parents(node, parentIDs)
                queue.append(*parentIDs)
                node_was_visited[node] = True

    @staticmethod
    def _make_map_for_visited_nodes(genealogy):
        visited_nodes_map = {}
        for k in genealogy.keys():
            visited_nodes_map[k] = False
        return visited_nodes_map

    def _add_child_to_parents(self, node, parentIDs):
        for parentID in parentIDs:
            parentGenotype = self.genealogy[parentID]
            if not parentGenotype.has_child(node):
                parentGenotype.add_child(node)

################################################################################


class Genealogy():

    def __init__(self):
        self.genealogy = {}

    def has_genotype_id(self, genotypeID):
        return genotypeID in self.genealogy.keys()

    def add_genotype(self, details):
        newGenotype = Genotype(*details)
        key = newGenotype.genotypeID
        self.genealogy[key] = newGenotype

    def get_parents(self, genotype_id):
        genotype = self.genealogy[genotype_id]
        return genotype.get_parents_as_tuple()

    def get_children(self, genotype_id):
        genotype = self.genealogy[genotype_id]
        return genotype.children


    #def print_out_mutations_from_top_to_bottom(self):
        #queue = ParamExpandDeque(*genealogy[GENESIS].children)
        #queue.append(EndOfLevelMarker())
        #node_was_visited = self._make_map_for_visited_nodes()
        #while queue:
            #node = queue.popleft()
            #if node.children and node.number_of_mutations > 0:
                #childrenStack append(*node.children)
                #for mutation in node.mutations:

