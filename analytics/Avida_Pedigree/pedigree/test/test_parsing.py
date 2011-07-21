import unittest
import os, os.path
from pedigree.parsing import PedigreeParser
from pedigree.genealogy import Genealogy


detailLineWithOneMutation = '''\
6164236 org:divide (none) 6152360,6155638 1 1 50 0 0 0 \
2503 9997 -1 434 Mv42k 0 heads_sex \
wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab 9952 132 0'''

detailLineWithNoMutations = '''\
6164236 org:divide (none) 6152360,6155638 1 1 50 0 0 0 \
2503 9997 -1 434  0 heads_sex \
wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab 9952 132 0'''

detailLineWithTwoMutations = '''\
6164236 org:divide (none) 6152360,6155638 1 1 50 0 0 0 \
2503 9997 -1 434 Mv42k,Ma1w 0 heads_sex \
wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab 9952 132 0'''

simpleDetailDump = '''\
5 4,3 Md1e heads_sex e
4 3,2 Mc1d heads_sex d
3 2,1 Mb1c heads_sex c
2 1,1 Ma1b heads_sex b
1 (none)  heads_sex a'''

class Test_Parsing_Detail_Line(unittest.TestCase):

    def test_correctly_parses_detail_line_with_one_mutation(self):
        result = PedigreeParser.parse_detail_line(detailLineWithOneMutation)
        expected_result = ('6164236','6152360', '6155638', 'Mv42k', None,
                'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_no_mutations(self):
        result = PedigreeParser.parse_detail_line(detailLineWithNoMutations)
        expected_result = ('6164236','6152360', '6155638', None, None,
                'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_with_two_mutations(self):
        result = PedigreeParser.parse_detail_line(detailLineWithTwoMutations)
        expected_result = ('6164236','6152360', '6155638', 'Mv42k', 'Ma1w',
                'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)

    def test_returns_nothing_for_incorrect_detail(self):
        detail_line = "123123 2312321 123123"
        result = PedigreeParser.parse_detail_line(detail_line)
        self.assertIsNone(result)

class Test_Creating_Pedigree_from_String(unittest.TestCase):

    def test_pedigree_parsed_from_string(self):
        someGenealogy = Genealogy()
        somePParser = PedigreeParser(someGenealogy)
        somePParser.create_pedigree_from_string(simpleDetailDump)
        self.assertTrue(someGenealogy.has_genotype_id('5'))
        self.assertTrue(someGenealogy.has_genotype_id('1'))
