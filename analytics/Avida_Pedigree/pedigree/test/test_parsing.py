import unittest
import os, os.path
from pedigree.parsing import PedigreeParser


class Test_Parsing_Detail_Line(unittest.TestCase):

    def test_correctly_parses_detail_line_with_mutation(self):
        sampleDetail = self.__get_sample_detail("sample_detail_mutation.txt")
        result = PedigreeParser.parse_detail_line(sampleDetail)
        expected_result = ('6164236','6152360', '6155638', 'Mv42k',
                'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)

    def test_correctly_parses_detail_line_without_mutation(self):
        sampleDetail = self.__get_sample_detail("sample_detail_no_mutation.txt")
        result = PedigreeParser.parse_detail_line(sampleDetail)
        expected_result = ('6164236','6152360', '6155638', '  ',
                'wuujagcycucbvyyusjvvvmvvjyyuyuuyctcyycvuyzkfcaxgab')

        self.assertTupleEqual(result, expected_result)

    def test_returns_nothing_for_incorrect_detail(self):
        detail_line = "123123 2312321 123123"
        result = PedigreeParser.parse_detail_line(detail_line)
        self.assertFalse(result)

    def __get_sample_detail(self, sampleDetailFileName):
        sampleDetailPath = sampleDetailFileName
        for root, dirs, names in os.walk(os.getcwd()):
            if sampleDetailFileName in names:
                sampleDetailPath = os.path.join(root, sampleDetailFileName)
                
        with open(sampleDetailPath) as f:
            sampleDetail = f.readline()
        return sampleDetail

class Test_Creating_Pedigree_from_file(unittest.TestCase):

    def test_pedigree_loaded_correctly(self):
        somePParser = PedigreeParser("test/simple_detail_dump.spop")
        self.assertEquals(somePParser.pedigree['5'].parentA_ID, '4')
        self.assertEquals(somePParser.pedigree['2'].parentB_ID, '1')
