from pedigree.mutation import Mutation
import unittest


class Test_Mutation(unittest.TestCase):
    
    def test_mutation_code_parsing(self):
        someMutation = Mutation('Ma3q')

        self.assertEquals(someMutation.mutationFrom, 'a')
        self.assertEquals(someMutation.mutationLocation, 3)
        self.assertEquals(someMutation.mutationTo, 'q')
