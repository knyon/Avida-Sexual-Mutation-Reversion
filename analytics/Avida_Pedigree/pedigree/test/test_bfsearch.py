import unittest
from pedigree.parsing import *
from pedigree.bfsearch import *

class Test_Breadth_First_Search(unittest.TestCase):

    def setUp(self):
        simple_genotypes = [('5', 'a', '4', '3'),
                            ('4', 'b', '3', '2'),
                            ('3', 'c', '2', '1'),
                            ('2', 'd', '1', '1')]
        for node in simple_genotypes:
            add_genotype_to_pedigree(node)
        pedigree = get_pedigree()
        self.someBFSearcher = BFSearcher(pedigree)
    

    def test_get_parents_returns_correct_parents(self):
        self.assertTupleEqual(self.someBFSearcher.get_parents('5'), ('4', '3'))
        self.assertTupleEqual(self.someBFSearcher.get_parents('2'), ('1', '1'))

    def test_search_for_ID_not_in_pedigree_raises_exception(self):
        self.assertRaises(Exception, 
                self.someBFSearcher.pedigree_breadth_first_search, '5', '10')

    def test_correctly_finds_parent_in_pedigree(self):
        result = self.someBFSearcher.pedigree_breadth_first_search('5', '2')
        self.assertTupleEqual(result, ('2', 2))
