import unittest
from pedigree.genealogy import *
from pedigree.genotype import Genotype


simpleDetailChild = ('2', '1', '1', None, None, 'Swp0-0', 'a')
simpleDetailParent = ('1', None, None, None, None, 'Swp0-0', 'a')

class Test_Genealogy_adds_genotype(unittest.TestCase):

    def setUp(self):
        self.someGenotype = Genotype(*simpleDetailParent)
        self.genealogy = Genealogy()
        self.genealogy.add_genotype(self.someGenotype)

    def test_genealogy_should_have_genotype_id(self):
        self.assertTrue(self.genealogy.has_genotype_id(
            self.someGenotype.ID))
            
simpleDetailDump = '''\
5 4,3 Md1e,Swp0-0 heads_sex e
4 3,2 Mc1d,Swp0-0 heads_sex d
3 2,1 Mb1c,Swp0-0 heads_sex c
2 1,1 Ma1b,Swp0-0 heads_sex b
1 (none)  heads_sex a'''

class Test_GenealogyMaker_makes_genealogy_from_detail_dump(unittest.TestCase):

    def setUp(self):
        self.genealogy = GenealogyMaker().make_genealogy_from_string(simpleDetailDump)

    def test_should_make_new_genealogy_from_string(self):
        self.assertTrue(self.genealogy.has_genotype_id('5'))
        self.assertTrue(self.genealogy.has_genotype_id('4'))
        self.assertTrue(self.genealogy.has_genotype_id('3'))
        self.assertTrue(self.genealogy.has_genotype_id('2'))
        self.assertTrue(self.genealogy.has_genotype_id('1'))


class Test_GenotypeRelationshipTool_creates_relations_between_genotypes(unittest.TestCase):

    def setUp(self):
        self.parentGenotype = Genotype(*simpleDetailParent)
        self.childGenotype = Genotype(*simpleDetailChild)
        genealogy = Genealogy()
        genealogy.add_genotype(self.parentGenotype)
        genealogy.add_genotype(self.childGenotype)
        GenotypeRelationshipTool()\
            .create_relationships_between_genotypes_in_genealogy(genealogy)
    
    def test_parent_should_have_child_genotype(self):
        children = self.parentGenotype.children
        self.assertListEqual(children, [self.childGenotype])

    def test_parent_id_swapped_with_object(self):
        self.assertIsInstance(self.childGenotype.parents[0], Genotype)


detailDumpWithMissingGenotypesEntry = '''4 3,2 Mc1d,Swp0-0 heads_sex d'''
        
class Test_GenotypeRelationTool_handles_missing_parent_genotypes(unittest.TestCase):

    def setUp(self):
        genealogy = GenealogyMaker()\
            .make_genealogy_from_string(detailDumpWithMissingGenotypesEntry)
        GenotypeRelationshipTool()\
            .create_relationships_between_genotypes_in_genealogy(genealogy)
        self.orphanGenotype = genealogy.genotypes['4']

    def test_missing_parents_are_none(self):
        for parent in self.orphanGenotype.parents:
            self.assertIsNone(parent)
