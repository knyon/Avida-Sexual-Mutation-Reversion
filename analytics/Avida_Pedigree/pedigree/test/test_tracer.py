import unittest
from pedigree.genealogy import *
from pedigree.tracer import *

detailForSubMutTracing = '''\
5 4,3 Mb0c,Swp0-0 heads_sex c
4 3,2 Swp0-0 heads_sex b
3 2,1 Swp0-0 heads_sex b
2 1,1 Ma0b,Swp0-0 heads_sex b
1 (none)  heads_sex a'''

class Test_SubMutTracer(unittest.TestCase):

    def setUp(self):
        genealogyMaker = GenealogyMaker()
        genealogy = genealogyMaker.make_genealogy_from_string(\
                detailForSubMutTracing)
        tracer = SubMutTracer(genealogy)
        startGenotypeID = "2"
        self.trace = tracer.make_trace(startGenotypeID)

    def test_trace_contains_appropriate_relations(self):
        self.assertIn(('2','3'), self.trace)
        self.assertIn(('2','4'), self.trace)
        self.assertIn(('3','4'), self.trace)

    def test_trace_does_not_contain_genotypes_without_mutation(self):
        self.assertNotIn(('4','5'), self.trace)
        self.assertNotIn(('3','5'), self.trace)
