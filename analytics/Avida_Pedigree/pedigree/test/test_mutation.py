from pedigree.mutation import *
import unittest


class Test_Mutation(unittest.TestCase):
    
    def test_substitution_mutation_code_parsing(self):
        subMut = SubstitutionMutation('Ma3q')
        self.assertEquals(subMut.mutationFrom, 'a')
        self.assertEquals(subMut.mutationAt, 3)
        self.assertEquals(subMut.mutationTo, 'q')

    def test_swap_area_code_parsing(self):
        swap = SwapArea('Swp10-30')
        self.assertEquals(swap.swapStart, 10)
        self.assertEquals(swap.swapEnd, 30)
