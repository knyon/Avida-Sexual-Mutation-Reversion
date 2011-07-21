import unittest
from pedigree.parsing import *
from pedigree.genealogy import *


simpleDetailDump = '''\
5 4,3 Md1e heads_sex e
4 3,2 Mc1d heads_sex d
3 2,1 Mb1c heads_sex c
2 1,1 Ma1b heads_sex b
1 (none)  heads_sex a'''

class Test_Genealogy(unittest.TestCase):

    def setUp(self):
        self.someGenealogy = Genealogy()
        somePParser = PedigreeParser(self.someGenealogy)
        somePParser.create_pedigree_from_string(simpleDetailDump)
        self.someGenealogy.add_children_to_lineage_of_genotype('5')

    def test_get_parents_returns_correct_parents(self):
        self.assertTupleEqual(self.someGenealogy.get_parents('5'), ('4', '3'))
        self.assertTupleEqual(self.someGenealogy.get_parents('2'), ('1', '1'))

    def test_get_children_returns_correct_children(self):
        children = self.someGenealogy.get_children('2')
        self.assertIn('3', children)
        self.assertIn('4', children)

    def test_children_are_correctly_added_to_genealogy(self):
        genealogy = self.someGenealogy.genealogy
        children = genealogy['2'].children
        self.assertIn('3', children)
        self.assertIn('4', children)

    def test_add_genotype(self):
        self.someGenealogy.add_genotype(('6', '5', '4', None, None, 'e'))
        self.assertIsNotNone(self.someGenealogy.genealogy['6'])
