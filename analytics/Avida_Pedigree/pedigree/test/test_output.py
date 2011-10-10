import unittest
import os
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *

simpleDetailDump = '''\
5 4,3 Md1e Swp0-0 heads_sex e
4 3,2 Mc1d Swp0-0 heads_sex d
3 2,1 Mb1c Swp0-0 heads_sex c
2 1,1 Ma1b Swp0-0 heads_sex b
1 (none)  heads_sex a'''

class Test_output(unittest.TestCase):

    def setUp(self):
        genealogyMaker = GenealogyMaker()
        genealogy = genealogyMaker.make_genealogy_from_string(simpleDetailDump)
        tracer = Tracer(genealogy)
        trace = tracer.make_trace()
        graphWriter = GraphvizWriter()
        graphWriter.write_trace_to_graphviz(trace, "genealogy.dot")

    def test_print_genealogy(self):
        self.assertTrue(os.path.exists('genealogy.dot'))

    def tearDown(self):
        if os.path.exists('genealogy.dot'):
            os.remove('genealogy.dot')
