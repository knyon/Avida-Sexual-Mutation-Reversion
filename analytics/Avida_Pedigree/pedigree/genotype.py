from pedigree.mutation import Mutation

class Genotype():
    '''Genotype object. Stores all information relating to a genotype.
    Used in tree transversal'''

    def __init__(self, genotypeID, parentA_ID, parentB_ID,
            mutationCodeA, mutationCodeB, sequence):

        self.genotypeID = genotypeID
        self.parentA_ID = parentA_ID
        self.parentB_ID  = parentB_ID
        self.mutationA = Mutation(mutationCodeA)
        self.mutationB = Mutation(mutationCodeB)
        self.sequence = sequence
        self.children = []

    def get_parents_as_tuple(self):
        return (self.parentA_ID, self.parentB_ID)

    def add_child(self, child_ID):
        self.children.append(child_ID)

    def has_child(self, child_id):
        return child_id in self.children

    def number_of_mutations(self):
        if self.mutationA.is_defined() and self.mutationB.is_defined():
            return 2
        elif self.mutationA.is_defined():
            return 1
        else:
            return 0
