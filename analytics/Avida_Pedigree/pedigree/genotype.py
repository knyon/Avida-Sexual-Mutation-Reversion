from pedigree.mutation import *
import re


class Genotype():
    '''Genotype object. Stores all information relating to a genotype.
    Used in tree transversal'''

    def __init__(self, ID, parentA_ID, parentB_ID,
            mutationCodeA, mutationCodeB, swapCode, sequence):

        self.ID = ID
        self.parents = [parentA_ID, parentB_ID]
        self.mutations = []
        self.mutations.append(SubstitutionMutation(mutationCodeA) if mutationCodeA else None)
        self.mutations.append(SubstitutionMutation(mutationCodeB) if mutationCodeB else None)
        self.swapArea = SwapArea(swapCode)
        self.sequence = sequence
        self.children = []

    def replace_parent_ids_with_objects(self, parentObjects):
        self.parents = parentObjects

    def add_child(self, childID):
        if childID not in self.children:
            self.children.append(childID)

    def has_child(self, childID):
        return childID in self.children

    def num_sub_mutations(self):
        mutationCount = 0
        for mutation in self.mutations:
            if mutation:
                mutationCount += 1
        return mutationCount
    
    def sequence_contains_mutation(self, subMut):
        if subMut.mutationAt > len(self.sequence): return False
        return self.sequence[subMut.mutationAt] == subMut.mutationTo

    def get_sequence_with_mutation_reverted(self, subMut):
        revertedSequence = list(self.sequence)
        revertedSequence[subMut.mutationAt] = subMut.mutationFrom
        return ''.join(revertedSequence)
