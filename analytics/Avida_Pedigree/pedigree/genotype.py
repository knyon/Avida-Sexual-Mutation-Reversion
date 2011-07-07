from pedigree.mutation import Mutation

class Genotype():
    '''Genotype object. Stores all information relating to a genotype.
    Used in tree transversal'''

    def __init__(self, genotypeID, parentA_ID, parentB_ID, sequence, mutationCode):
        self.genotypeID = genotypeID
        self.parentA_ID = parentA_ID
        self.parentB_ID  = parentB_ID
        self.sequence = sequence
        self.mutation = Mutation(mutationCode)
        self.children = []

    def get_parents_as_tuple(self):
        return (self.parentA_ID, self.parenta_ID)

    def has_child(self, child_id):
        return child_id in self.children
