import unittest
from pedigree.bfsearch import *
from pedigree.parsing import *

class Test_Breadth_First_Search(unittest.TestCase):
    simple_genotypes = [('5', 'a', '4', '3'),
                        ('4', 'b', '3', '2'),
                        ('3', 'c', '2', '1'),
                        ('2', 'd', '1', '1')]
    for node in simple_genotypes:
        add_genotype_to_pedigree(node)
    pedigree = get_pedigree()

    def test_get_parents_returns_correct_parents(self):
        self.assertTupleEqual(pedigree.get_parents('5'), ('4', '3'))
        self.assertTupleEqual(pedigree.get_parents('2'), ('1', '1'))

    def test_search_for_ID_not_in_pedigree_raises_exception(self):
        self.assertRaises(Exception, pedigree.pedigree_breadth_first_search,
                '5', '10')

    def test_bfs(self):
        result = pedigree.pedigree_breadth_first_search('5', '2')
        self.assertTupleEqual(result, ('2', 2))
