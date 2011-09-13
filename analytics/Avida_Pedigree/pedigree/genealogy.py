from collections import deque
from pedigree.genotype import Genotype
from pedigree.parsing import DetailParser

class ExtndDeque(deque):
    '''Extension of the deque collection that allows for appending multiple
    items at once'''
    def __init__(self, *items):
        super(ExtndDeque, self).__init__(self)
        self.append(*items)
    def append(self, *items):
        for i in items:
            super(ExtndDeque, self).append(i)

class GenealogyMaker:
    '''Class with only static methods used in creating a genealogy from a
    detail dump. A detail dump may be either a detail dump file created by
    Avida or a string, which is useful in testing.'''

    def __init__(self):
        self.parser = DetailParser()

    def make_genealogy_from_file(self, fileName):
        detailDump = open(fileName)
        return self.build_genealogy(detailDump)

    def make_genealogy_from_string(self, inputString):
        detailDump = inputString.split('\n')
        return self.build_genealogy(detailDump)

    def build_genealogy(self, detailDump):
        '''Build and return a Genealogy object by adding Genotypes parsed from
        a detail dump'''
        genealogy = Genealogy()
        for line in detailDump:
            newGenotype = self.new_genotype_from_detail_line(line)
            if newGenotype:
                genealogy.add_genotype(newGenotype)
        genealogy.add_related_genotypes_to_all_genotypes()
        return genealogy
    
    def new_genotype_from_detail_line(self, line):
        '''Create a new Genotype object from a parsed line of a detail dump. If
        there's nothing returned from the parser (e.g., the DetailParser parses
        a commented line), return None'''
        details = self.parser.process_line(line)
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
    '''Class to contain all of the Genotype objects.'''

    def __init__(self):
        self.genotypes = {}
        self.children_mapping = {}

    def has_genotype_id(self, genotypeID):
        return genotypeID in self.genotypes.keys()

    def add_genotype(self, newGenotype):
        '''Add new genotype to the genealogy'''
        key = newGenotype.ID
        self.genotypes[key] = newGenotype

    def add_related_genotypes_to_all_genotypes(self):
        '''For all genotypes, add their related Genotype objects (children and
        parents)'''
        for genotype in self.genotypes.values():
            self.add_parent_objects_to_genotype(genotype)
            self.add_child_to_parent_genotype(genotype)

    def add_parent_objects_to_genotype(self, genotype):
        '''Genotype object initially created with just the parents' IDs.
        Replace them with the parents' Genotype objects'''
        parentObjects = self.find_multiple_genotypes_by_id(genotype.parents)
        genotype.replace_parent_ids_with_objects(parentObjects)

    def find_multiple_genotypes_by_id(self, ids):
        foundGenotypes = []
        for i in ids:
            foundGenotypes.append(self.genotypes[i])
        return foundGenotypes

    def add_child_to_parent_genotype(self, genotype):
        '''Add the genotype to it's parent'''
        for parent in genotype.parents:
            parent.add_child(genotype)

