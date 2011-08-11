from pedigree.mutation import Mutation
import re

GENESIS = '1'

class Genotype():
    '''Genotype object. Stores all information relating to a genotype.
    Used in tree transversal'''

    def __init__(self, ID, parentA_ID, parentB_ID,
            mutationCodeA, mutationCodeB, swapCode, sequence):

        self.ID = ID
        self.parents = [parentA_ID, parentB_ID] if ID != GENESIS else []
        self.mutationA = Mutation(mutationCodeA)
        self.mutationB = Mutation(mutationCodeB)
        self.swapCode = SwapArea(swapCode)
        self.sequence = sequence
        self.children = []

    def replace_parent_ids_with_objects(self, parentA, parentB):
        self.parents = [parentA, parentB]

    def add_child(self, childID):
        if childID not in self.children:
            self.children.append(childID)

    def has_child(self, childID):
        return childID in self.children

    def number_of_mutations(self):
        if self.mutationA.is_defined() and self.mutationB.is_defined():
            return 2
        elif self.mutationA.is_defined():
            return 1
        else:
            return 0


class SwapArea():

    def __init__(self, swapCode):
        if swapCode:
            self.parse_swap_code(swapCode)

    def parse_swap_code(self, swapCode):
        regex = re.compile(r'Swp(\d+)-(\d+)')
        code = regex.match(swapCode)
        self.swapStart = int(code.group(1))
        self.swapEnd = int(code.group(2))
