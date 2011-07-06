import unittest
from pedigree.parsing import add_genotype_to_pedigree, get_pedigree


class TestPedigree(unittest.TestCase):

    simple_genotypes = [('5', 'a', '4', '3'),
                        ('4', 'b', '3', '2'),
                        ('3', 'c', '2', '1'),
                        ('2', 'd', '1', '1')]
    for node in simple_genotypes:
        add_genotype_to_pedigree(node)

    def test_simple_pedigree_construction(self):
        expected_pedigree = { '5': ('a', '4', '3'),
                            '4': ('b', '3', '2'),
                            '3': ('c', '2', '1'),
                            '2': ('d', '1', '1') }
        print(get_pedigree())
        self.assertDictEqual(expected_pedigree, get_pedigree())
