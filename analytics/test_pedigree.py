import unittest
import pedigree


class TestParsing(unittest.TestCase):

    def test_correctly_parses_detail_line(self):
        detail_line = ("4775600 org:divide (none) 4765250,4772979 1 2 50 96 336 "+
                "0.285714 2244 9956 -1 291 0 heads_sex " +
                "wrjagcjzptoyvvvbbaynuycduccuqvryptvnbrytylbfcaxgab 9956 159 0")
        result = pedigree.parse_detail_line(detail_line)
        
        expected_result = ('4775600', 'wrjagcjzptoyvvvbbaynuycduccuqvryptvnbrytylbfcaxgab', 
                        '4765250', '4772979')
        self.assertTupleEqual(result, expected_result)

    def test_returns_nothing_for_incorrect_detail(self):
        detail_line = "123123 2312321 123123"
        result = pedigree.parse_detail_line(detail_line)
        self.assertFalse(result)

class TestPedigree(unittest.TestCase):

    simple_genotypes = [('5', 'a', '4', '3'),
                        ('4', 'b', '3', '2'),
                        ('3', 'c', '2', '1'),
                        ('2', 'd', '1', '1')]
    for node in simple_genotypes:
        pedigree.add_genotype_to_pedigree(node)

    def test_simple_pedigree_construction(self):
        expected_pedigree = { '5': ('a', '4', '3'),
                            '4': ('b', '3', '2'),
                            '3': ('c', '2', '1'),
                            '2': ('d', '1', '1') }
        self.assertDictEqual(expected_pedigree, pedigree.pedigree)

    def test_get_parents_returns_correct_parents(self):
        self.assertTupleEqual(pedigree.get_parents('5'), ('4', '3'))
        self.assertTupleEqual(pedigree.get_parents('2'), ('1', '1'))

    def test_search_for_ID_not_in_pedigree_raises_exception(self):
        number_not_in_pedigree = 10
        self.assertRaises(Exception, pedigree.pedigree_breadth_first_search,
                number_not_in_pedigree)

    def test_bfs(self):
        result = pedigree.pedigree_breadth_first_search('5', '2')
        self.assertTupleEqual(result, ('2', 2))

class TestSampleData(unittest.TestCase):

    def test_find_levels(self):
        pedigree.create_pedigree_from_detail_file('detail-250000.spop')
        print(pedigree.pedigree_breadth_first_search('79003567', '1'))
        self.assertTrue(True)



if __name__ == '__main__':
    unittest.main()
