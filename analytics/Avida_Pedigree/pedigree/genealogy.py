from pedigree.genotype import Genotype
from pedigree.parsing import DetailParser

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
        genealogy.create_relations_between_genotypes()
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

    def create_relations_between_genotypes(self):
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

