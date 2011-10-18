from pedigree.genotype import Genotype
from pedigree.parsing import DetailParser

class GenealogyMaker:
    '''Class with only static methods used in creating a genealogy from a
    detail dump. A detail dump may be either a detail dump file created by
    Avida or a string, which is useful in testing.'''

    def make_genealogy_from_file(self, fileName):
        detailDump = open(fileName)
        return self.build_genealogy(detailDump)

    def make_genealogy_from_string(self, inputString):
        detailDump = inputString.split('\n')
        return self.build_genealogy(detailDump)

    def build_genealogy(self, detailDump):
        '''Build and return a Genealogy object by adding Genotypes parsed from
        a detail dump'''
        parser = DetailParser()
        genealogy = Genealogy()
        for line in detailDump:
            details = parser.process_line(line)
            if details:
                genealogy.add_genotype(Genotype(*details))
        genealogy.create_relations_between_genotypes()
        return genealogy


class Genealogy():
    '''Class to contain all of the Genotype objects.'''

    def __init__(self):
        self.genotypes = {}

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
        for idx,parentID in enumerate(genotype.parents):
            if parentID and self.has_genotype_id(parentID):
                genotype.parents[idx] = self.genotypes[parentID]
            else:
                genotype.parents[idx] = None

    def add_child_to_parent_genotype(self, genotype):
        '''Add the genotype to it's parent'''
        for parent in genotype.parents:
            if parent:
                parent.add_child(genotype)

