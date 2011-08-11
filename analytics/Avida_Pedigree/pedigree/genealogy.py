from collections import deque
from pedigree.genotype import Genotype
from pedigree.parsing import DetailParser

GENESIS = '1'

def node_marks_last_in_level(node):
    return isinstance(node, EndOfLevelMarker)

def node_is_genesis(node):
    return node == GENESIS


class ExtndDeque(deque):
    '''Extension of the deque collection that allows for appending multiple
    items at once'''
    def __init__(self, *items):
        super(ExtndDeque, self).__init__(self)
        self.append(*items)
    def append(self, *items):
        for i in items:
            super(ExtndDeque, self).append(i)


class EndOfLevelMarker():
    '''EndOfLevelMarker is just a hollow class to detect the end of a queue
    in a breadth-first search. This is more clear than just using 'None' or
    some other indicator.'''
    pass


class GenealogyMaker:

    @staticmethod
    def make_genealogy_from_file(fileName):
        detailDump = open(fileName)
        return GenealogyMaker.build_genealogy(detailDump)

    @staticmethod
    def make_genealogy_from_string(inputString):
        detailDump = inputString.split('\n')
        return GenealogyMaker.build_genealogy(detailDump)

    @staticmethod
    def build_genealogy(detailDump):
        genealogy = Genealogy()
        for line in detailDump:
            newGenotype = GenealogyMaker.new_genotype_from_detail_line(line)
            if newGenotype:
                genealogy.add_genotype(newGenotype)
        genealogy.add_children_to_all_genotypes()
        return genealogy
    
    @staticmethod
    def new_genotype_from_detail_line(line):
            details = DetailParser.process_line(line)
            if details:
                return Genotype(*details)
            else:
                return None

    #def add_children_to_lineage_of_genotype(self, genealogy, start_genotype_id):
        #queue = ExtndDeque(start_genotype_id, EndOfLevelMarker())
        #node_was_visited = self._make_map_for_visited_nodes(genealogy)

        #while queue:
            #node = queue.popleft()
            #if node_marks_last_in_level(node): 
                #if len(queue) == 0:
                    #break
                #tree_level += 1
                #queue.append(node)
            #elif node_is_genesis(node) or node_was_visited[node]:
                #continue
            #else:
                #parentIDs = self.genealogy.genotypes[node].get_parents_as_tuple()
                #self._add_child_to_parents(node, parentIDs)
                #queue.append(*parentIDs)
                #node_was_visited[node] = True

    #def _make_map_for_visited_nodes(self, genealogy):
        #visited_nodes_map = {}
        #for k in genealogy.keys():
            #visited_nodes_map[k] = False
        #return visited_nodes_map

    #def _add_child_to_parents(self, node, parentIDs):
        #for parentID in parentIDs:
            #parentGenotype = self.genealogy[parentID]
            #if not parentGenotype.has_child(node):
                #parentGenotype.add_child(node)

class Genealogy():

    def __init__(self):
        self.genotypes = {}
        self.children_mapping = {}

    def has_genotype_id(self, genotypeID):
        return genotypeID in self.genotypes.keys()

    def add_genotype(self, newGenotype):
        key = newGenotype.ID
        self.genotypes[key] = newGenotype

    def add_children_to_all_genotypes(self):
        for genotype in self.genotypes.values():
            for parent in genotype.parents:
                self.genotypes[parent].add_child(genotype)
