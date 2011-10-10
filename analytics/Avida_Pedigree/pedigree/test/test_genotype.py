from pedigree.genotype import Genotype
from pedigree.genotype import *
import unittest


class Test_Genotype(unittest.TestCase):

    def test_retrieve_details_from_genotype(self):
        someGenotype = Genotype('3', '1', '2', 'Ma3q', None, 'Swp0-0', 'asdf',)

        self.assertEquals(someGenotype.ID, '3')
        self.assertEquals(someGenotype.parents[0], '1')
        self.assertEquals(someGenotype.parents[1], '2')
        self.assertEquals(someGenotype.sequence, 'asdf')

    def test_genotype_with_no_mutations(self):
        someGenotype = Genotype('3', '1', '2', None, None, 'Swp0-0', 'asdf')
        self.assertEquals(someGenotype.num_sub_mutations(), 0)

    def test_genotype_with_one_mutation(self):
        someGenotype = Genotype('3', '1', '2', 'Ma3q', None, 'Swp0-0', 'asdf')
        self.assertEquals(someGenotype.num_sub_mutations(), 1)

    def test_genotype_with_two_mutations(self):
        someGenotype = Genotype('3', '1', '2', 'Ma3q', 'Mb2s', 'Swp0-0', 'asdf')
        self.assertEquals(someGenotype.num_sub_mutations(), 2)

    def test_genotype_should_have_sub_mutation_that_matches(self):
        someGenotype = Genotype('3', '1', '2', None, None, 'Swp0-0', 'asdf')
        previousMutation = SubstitutionMutation("Mz1s")
        self.assertTrue(someGenotype.sequence_contains_mutation(previousMutation))

    def test_sub_mutation_outside_sequence_should_not_be_true(self):
        someGenotype = Genotype('3', '1', '2', None, None, 'Swp0-0', 'asdf')
        previousMutation = SubstitutionMutation("Mz5f")
        self.assertFalse(someGenotype.sequence_contains_mutation(previousMutation))

    def test_genotype_should_not_have_sub_mutation_that_doesnt_match(self):
        someGenotype = Genotype('3', '1', '2', None, None, 'Swp0-0', 'asdf')
        previousMutation = SubstitutionMutation("Mz0z")
        self.assertFalse(someGenotype.sequence_contains_mutation(previousMutation))
