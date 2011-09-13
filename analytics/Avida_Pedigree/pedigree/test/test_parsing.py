import unittest
import os, os.path
from pedigree.parsing import DetailParser
from pedigree.genealogy import Genealogy

genesisDetailLine = '''\
1 org:file_load (none) (none) 0 3438 50 47 189 0.248677 0 -1 531 0  0 \
heads_sex wzcagcccccccccccccccccccccccccccccccccccczvfcaxgab'''

detailLineWithOneMutation = '''\
6164236 org:divide (none) 6152360,6155638 1 1 50 0 0 0 \
2503 9997 -1 434 Mv42k Swp10-30 0 heads_sex \
wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab 9952 132 0'''

detailLineWithNoMutations = '''\
6164236 org:divide (none) 6152360,6155638 1 1 50 0 0 0 \
2503 9997 -1 434  Swp10-30 0 heads_sex \
wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab 9952 132 0'''

detailLineWithTwoMutations = '''\
6164236 org:divide (none) 6152360,6155638 1 1 50 0 0 0 \
2503 9997 -1 434 Mv42k,Ma1w Swp10-30 0 heads_sex \
wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab 9952 132 0'''

detailLineWithNoSwapArea = '''\
6164236 org:divide (none) 6152360,6155638 1 1 50 0 0 0 \
2503 9997 -1 434 Mv42k,Ma1w 0 heads_sex \
wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab 9952 132 0'''

class Test_Parsing_Detail_Line(unittest.TestCase):

    def setUp(self):
        self.parser = DetailParser()

    def test_correctly_parses_genesis_detail_line(self):
        result = self.parser.process_line(genesisDetailLine)
        expected_result = ('1', None, None, None, None,
                None, 'wzcagcccccccccccccccccccccccccccccccccccczvfcaxgab')
        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_one_mutation(self):
        result = self.parser.process_line(detailLineWithOneMutation)
        expected_result = ('6164236','6152360', '6155638', 'Mv42k', None,
                'Swp10-30', 'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_no_mutations(self):
        result = self.parser.process_line(detailLineWithNoMutations)
        expected_result = ('6164236','6152360', '6155638', None, None,
                'Swp10-30', 'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_two_mutations(self):
        result = self.parser.process_line(detailLineWithTwoMutations)
        expected_result = ('6164236','6152360', '6155638', 'Mv42k', 'Ma1w',
                'Swp10-30', 'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_no_swap_rea(self):
        result = self.parser.process_line(detailLineWithNoSwapArea)
        expected_result = ('6164236','6152360', '6155638', 'Mv42k', 'Ma1w',
                None, 'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)
    def test_returns_nothing_for_incorrect_detail(self):
        detail_line = "123123 2312321 123123"
        result = self.parser.process_line(detail_line)
        self.assertIsNone(result)
