import unittest
from pedigree.evaluator import *
from pedigree.genotype import *

class Test_EvaluateDeleterious(unittest.TestCase):

    def setUp(self):
        testGenotype = Genotype('31','1','1','Mc20f','','Swp0-25', 'wzcagcccccccccccccccfcccccccccccccccccccczvfcaxgab')
        testMutation = testGenotype.mutations[0]
        evaluator = MutationEvaluator()
        self.fitnessEffect = evaluator.evaluate_effect_of_mutation(testGenotype, testMutation)

    def test_mutation_is_deleterious(self):
        self.assertLess(self.fitnessEffect, 0)

class Test_EvaluateBeneficial(unittest.TestCase):

    def setUp(self):
        testGenotype = Genotype('9','1','1','Mc30o','','Swp0-25', 'wzcagcccccccccccccccccccccccccocccccccccczvfcaxgab')
        testMutation = testGenotype.mutations[0]
        evaluator = MutationEvaluator()
        self.fitnessEffect = evaluator.evaluate_effect_of_mutation(testGenotype, testMutation)

    def test_mutation_is_beneficial(self):
        self.assertGreater(self.fitnessEffect, 0)

