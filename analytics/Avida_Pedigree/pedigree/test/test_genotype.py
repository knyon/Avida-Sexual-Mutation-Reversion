from pedigree.genotype import Genotype
from pedigree.genotype import Mutation
import unittest


class Test_Genotype(unittest.TestCase):

    def test_retrieve_details_from_genotype(self):
        someGenotype = Genotype('3', '1', '2', 'Ma3q','asdf',)

        self.assertEquals(someGenotype.genotypeID, '3')
        self.assertEquals(someGenotype.parentA_ID, '1')
        self.assertEquals(someGenotype.parentB_ID, '2')
        self.assertEquals(someGenotype.mutation.mutationCode, 'Ma3q')
        self.assertEquals(someGenotype.sequence, 'asdf')
