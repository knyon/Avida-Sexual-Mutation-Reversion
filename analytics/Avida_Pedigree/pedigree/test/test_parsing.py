import unittest
import os, os.path
from pedigree.parsing import DetailParser
from pedigree.genealogy import Genealogy

genesisDetailLine = '''\
1 org:file_load (none) (none) 0 3438 50 47 189 0.248677 0 -1 531 0  0 \
heads_sex wzcagcccccccccccccccccccccccccccccccccccczvfcaxgab'''

detailLineWithNoMutations = '''\
72 org:divide (none) 3,18 0 17 50 47 188 0.25 13 82 176 2 Swp14-26 0 heads_sex \
wzcagcccccccccccccccccccbccccccmccccccccczvfcaxgab '''

detailLineWithOneMutation = '''\
1055 org:divide (none) 781,781 0 1 50 47 187 0.251337 26 163 176 4 \
Mc13y,Swp25-38 0 heads_sex \
wzcagccccccccyccccccccwcccccccccccrcccccczvfcaxgab'''

detailLineWithTwoMutations = '''\
79496 org:divide (none) 30490,57433 0 5 50 46 184 0.25 82 513 570 14 \
Mc15y,Mc40z,Swp9-16 0 heads_sex \
wzcagccccccccccycpcccehccccckccccckpcccczzvfcaxgab'''

class Test_Parsing_Detail_Line(unittest.TestCase):

    def setUp(self):
        self.parser = DetailParser()

    def test_correctly_parses_genesis_detail_line(self):
        result = self.parser.process_line(genesisDetailLine)
        expected_result = ('1', None, None, None, None,
                None, 'wzcagcccccccccccccccccccccccccccccccccccczvfcaxgab')
        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_two_mutations(self):
        result = self.parser.process_line(detailLineWithNoMutations)
        expected_result = ('6164236','6152360', '6155638', None, None,
                'Swp10-30', 'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')
        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_one_mutation(self):
        result = self.parser.process_line(detailLineWithOneMutation)
        expected_result = ('6164236','6152360', '6155638', 'Mv42k', None,
                'Swp10-30', 'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')
        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_two_mutations(self):
        result = self.parser.process_line(detailLineWithTwoMutations)
        expected_result = ('6164236','6152360', '6155638', 'Mv42k', 'Ma1w',
                'Swp10-30', 'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')
        self.assertTupleEqual(result, expected_result)

    def test_returns_nothing_for_incorrect_detail(self):
        detail_line = "123123 2312321 123123"
        result = self.parser.process_line(detail_line)
        self.assertIsNone(result)
