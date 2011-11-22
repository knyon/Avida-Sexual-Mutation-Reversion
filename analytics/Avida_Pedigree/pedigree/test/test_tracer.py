import unittest
from pedigree.genealogy import *
from pedigree.tracer import *

detailForSubMutTracing = '''\
5 4,3 Mb0c,Swp0-0 heads_sex c
4 3,2 Swp0-0 heads_sex b
3 2,1 Ma0b,Swp0-0 heads_sex b
2 1,1 Swp0-0 heads_sex b
1 (none)  heads_sex a'''

class Test_TopDownTrace(unittest.TestCase):

    def setUp(self):
        genealogyMaker = GenealogyMaker()
        genealogy = genealogyMaker.make_genealogy_from_string(\
                detailForSubMutTracing)
        tracer = Tracer(genealogy, TopDownTracePattern())
        startGenotype = genealogy['3']
        self.trace = tracer.make_trace(startGenotype)

    def test_trace_contains_descendants(self):
        self.assertIn(('3','4'), self.trace)
        self.assertIn(('3','5'), self.trace)
        self.assertIn(('4','5'), self.trace)

    def test_trace_does_not_contain_non_descendants(self):
        self.assertNotIn(('1','2'), self.trace)
        self.assertNotIn(('2','3'), self.trace)

class Test_BottomUpTrace(unittest.TestCase):

    def setUp(self):
        genealogyMaker = GenealogyMaker()
        genealogy = genealogyMaker.make_genealogy_from_string(\
                detailForSubMutTracing)
        tracer = Tracer(genealogy, BottomUpTracePattern())
        startGenotype = genealogy['3']
        self.trace = tracer.make_trace(startGenotype)

    def test_trace_contains_ancestors(self):
        self.assertIn(('3','2'), self.trace)
        self.assertIn(('3','1'), self.trace)
        self.assertIn(('2','1'), self.trace)

    def test_trace_does_not_contain_non_ancestors(self):
        self.assertNotIn(('1','2'), self.trace)
        self.assertNotIn(('2','3'), self.trace)

class Test_SubMutTDTrace(unittest.TestCase):

    def setUp(self):
        genealogyMaker = GenealogyMaker()
        genealogy = genealogyMaker.make_genealogy_from_string(\
                detailForSubMutTracing)
        startGenotype = genealogy['3']
        trackedMutation = startGenotype.mutations[0]
        pattern = SubMutTDTracePattern(trackedMutation)
        tracer = Tracer(genealogy, pattern)
        self.trace = tracer.make_trace(startGenotype)

    def test_trace_contains_descendants_with_mutations(self):
        self.assertIn(('3','4'), self.trace)

    def test_trace_does_not_contain_descendants_without_mutations(self):
        self.assertNotIn(('3','5'), self.trace)

class Test_SubMutBUTrace(unittest.TestCase):

    def setUp(self):
        genealogyMaker = GenealogyMaker()
        genealogy = genealogyMaker.make_genealogy_from_string(\
                detailForSubMutTracing)
        startGenotype = genealogy['4']
        trackedMutation = genealogy['3'].mutations[0]
        pattern = SubMutBUTracePattern(trackedMutation)
        tracer = Tracer(genealogy, pattern)
        self.trace = tracer.make_trace(startGenotype)

    def test_trace_contains_ancestors_with_mutations(self):
        self.assertIn(('4','3'), self.trace)
        self.assertIn(('3','2'), self.trace)

    def test_trace_does_not_contain_ancestors_without_mutations(self):
        self.assertNotIn(('2','1'), self.trace)

