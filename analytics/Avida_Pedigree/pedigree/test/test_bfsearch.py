import unittest
from pedigree.parsing import *
from pedigree.bfsearch import *


simpleDetailDump = '''\
5 4,3 Md1e heads_sex e
4 3,2 Mc1d heads_sex d
3 2,1 Mb1c heads_sex c
2 1,1 Ma1b heads_sex b
1 (none)  heads_sex a'''

class Test_BFSearcher(unittest.TestCase):

    def setUp(self):
        somePParser = PedigreeParser()
        somePParser.create_pedigree_from_string(simpleDetailDump)
        self.someBFSearcher = BFSearcher(somePParser.pedigree)
    

    def test_get_parents_returns_correct_parents(self):
        self.assertTupleEqual(self.someBFSearcher.get_parents('5'), ('4', '3'))
        self.assertTupleEqual(self.someBFSearcher.get_parents('2'), ('1', '1'))

    def test_search_for_ID_not_in_pedigree_raises_exception(self):
        self.assertRaises(Exception, 
                self.someBFSearcher.search_pedigree, '5', '10')

    def test_correctly_finds_parent_in_pedigree(self):
        result = self.someBFSearcher.search_pedigree('5', '2')
        self.assertTupleEqual(result, ('2', 2))

class Test_BFTraverser(unittest.TestCase):

    def setUp(self):
        somePParser = PedigreeParser()
        somePParser.create_pedigree_from_string(simpleDetailDump)
        self.someTranverser = BFTraverser(somePParser.pedigree)
        self.someTranverser.add_children_to_genotypes('5')
    
    def test_children_are_correct(self):
        pedigree = self.someTranverser.pedigree
        children = pedigree['2'].children
        self.assertIn('3', children)
        self.assertIn('4', children)
