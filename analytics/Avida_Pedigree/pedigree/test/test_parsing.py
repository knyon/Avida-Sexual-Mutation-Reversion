import unittest
from pedigree.parsing import *

class Test_Parsing_Detail_Line(unittest.TestCase):

    def test_correctly_parses_detail_line(self):
        detail_line = ("4775600 org:divide (none) 4765250,4772979 1 2 50 96 336 "+
                "0.285714 2244 9956 -1 291 0 heads_sex " +
                "wrjagcjzptoyvvvbbaynuycduccuqvryptvnbrytylbfcaxgab 9956 159 0")
        result = parse_detail_line(detail_line)
        
        expected_result = ('4775600', 'wrjagcjzptoyvvvbbaynuycduccuqvryptvnbrytylbfcaxgab', 
                        '4765250', '4772979')
        self.assertTupleEqual(result, expected_result)

    def test_returns_nothing_for_incorrect_detail(self):
        detail_line = "123123 2312321 123123"
        result = parse_detail_line(detail_line)
        self.assertFalse(result)

class Test_Creating_Pedigree(unittest.TestCase):

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
