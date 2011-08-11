from pedigree.genotype import Genotype
from pedigree.genotype import Mutation
import unittest


class Test_Genotype(unittest.TestCase):

    def test_retrieve_details_from_genotype(self):
        someGenotype = Genotype('3', '1', '2', 'Ma3q', None, 'Swp0-0', 'asdf',)

        self.assertEquals(someGenotype.ID, '3')
        self.assertEquals(someGenotype.parents[0], '1')
        self.assertEquals(someGenotype.parents[1], '2')
        self.assertEquals(someGenotype.sequence, 'asdf')

    def test_genotype_with_no_mutations(self):
        someGenotype = Genotype('3', '1', '2', None, None, 'Swp0-0', 'asdf',)
        self.assertEquals(someGenotype.mutationA.mutationCode, None)
        self.assertEquals(someGenotype.mutationB.mutationCode, None)
        self.assertEquals(someGenotype.number_of_mutations(), 0)

    def test_genotype_with_one_mutation(self):
        someGenotype = Genotype('3', '1', '2', 'Ma3q', None, 'Swp0-0', 'asdf',)
        self.assertEquals(someGenotype.mutationA.mutationCode, 'Ma3q')
        self.assertEquals(someGenotype.mutationB.mutationCode, None)
        self.assertEquals(someGenotype.number_of_mutations(), 1)

    def test_genotype_with_two_mutations(self):
        someGenotype = Genotype('3', '1', '2', 'Ma3q', 'Mb2s', 'Swp0-0', 'asdf',)
        self.assertEquals(someGenotype.mutationA.mutationCode, 'Ma3q')
        self.assertEquals(someGenotype.mutationB.mutationCode, 'Mb2s')
        self.assertEquals(someGenotype.number_of_mutations(), 2)
