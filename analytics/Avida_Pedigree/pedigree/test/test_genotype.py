from pedigree.genotype import Genotype
import unittest


class Test_Genotype(unittest.TestCase):

    def test_retrieve_a_detail(self):
        someGenotype = Genotype('3', '1', '2', 'asdf', 'Ma3q')
        self.assertEquals(someGenotype.parent_a_id, '1')
