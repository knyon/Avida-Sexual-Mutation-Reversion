from pedigree.mutation import *
import re

GENESIS = '1'

class Genotype():
    '''Genotype object. Stores all information relating to a genotype.
    Used in tree transversal'''

    def __init__(self, ID, parentA_ID, parentB_ID,
            mutationCodeA, mutationCodeB, swapCode, sequence):

        self.ID = ID
        self.parents = [parentA_ID, parentB_ID] if ID != GENESIS else []
        self.subMutA = SubstitutionMutation(mutationCodeA) if mutationCodeA else None
        self.subMutB = SubstitutionMutation(mutationCodeB) if mutationCodeB else None
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
        if self.subMutA and self.subMutB:
            return 2
        elif self.subMutA:
            return 1
        else:
            return 0
    
    def sequence_contains_mutation(self, subMut):
        if subMut.mutationAt > len(self.sequence): return False
        return self.sequence[subMut.mutationAt] == subMut.mutationTo
