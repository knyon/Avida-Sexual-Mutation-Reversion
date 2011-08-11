import unittest
from pedigree.genealogy import *
from pedigree.genotype import Genotype

simpleDetailLine = "5 4,3 Md1e Swp0-0 heads_sex e"

simpleDetailDump = '''\
5 4,3 Md1e Swp0-0 heads_sex e
4 3,2 Mc1d Swp0-0 heads_sex d
3 2,1 Mb1c Swp0-0 heads_sex c
2 1,1 Ma1b Swp0-0 heads_sex b
1 (none)  heads_sex a'''

simpleDetailChild = ('2', '1', '1', None, None, 'Swp0-0', 'a')
simpleDetailParent = ('1', None, None, None, None, None, 'a')

class Test_Genealogy(unittest.TestCase):

    def setUp(self):
        self.genealogy = Genealogy()
        self.childGenotype = Genotype(*simpleDetailChild)
        self.parentGenotype = Genotype(*simpleDetailParent)
        self.genealogy.add_genotype(self.childGenotype)
        self.genealogy.add_genotype(self.parentGenotype)


    def test_correctly_added_genotype(self):
        self.assertTrue(self.genealogy.has_genotype_id('2'))
        self.assertTrue(self.genealogy.has_genotype_id('1'))

    def test_add_children_to_all_genotypes(self):
        self.genealogy.add_children_to_all_genotypes()
        children = self.parentGenotype.children
        self.assertListEqual(children, [self.childGenotype])

class Test_GenealogyMaker(unittest.TestCase):

    def test_returns_new_genotype_from_line(self):
        geno = GenealogyMaker.new_genotype_from_detail_line(simpleDetailLine)
        self.assertIsInstance(geno, Genotype)

    def test_should_make_new_genealogy_from_string(self):
        genealogy = GenealogyMaker.make_genealogy_from_string(simpleDetailDump)
        self.assertTrue(genealogy.has_genotype_id('5'))
        self.assertTrue(genealogy.has_genotype_id('4'))
        self.assertTrue(genealogy.has_genotype_id('3'))
        self.assertTrue(genealogy.has_genotype_id('2'))
        self.assertTrue(genealogy.has_genotype_id('1'))
