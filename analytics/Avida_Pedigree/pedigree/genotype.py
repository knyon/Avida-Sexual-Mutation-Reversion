from pedigree.mutation import *
import re


class Genotype():
    ##'''Genotype object. Stores all information relating to a genotype.
    ##Used in tree transversal'''

    def __init__(self, ID, parentA_ID, parentB_ID,
            mutationCodeA, mutationCodeB, swapCode, sequence, fit=0.0):

        self.ID = ID
        self.parents = (parentA_ID, parentB_ID)
        self.mutations = (\
                self.parse_mutation_code(mutationCodeA) if mutationCodeA else None,\
                self.parse_mutation_code(mutationCodeB) if mutationCodeB else None)
        self.swapArea = self.parse_swap_code(swapCode) if swapCode else None
        self.sequence = sequence
        self.fitness = float(fit)
        self.children = []
        self.marked = False


    def isMarked(self):
        return self.marked

    def mark(self):
        self.marked = True

    def unmark(self):
        self.marked = False

    def replace_parent_ids_with_objects(self, parentObjects):
        self.parents = parentObjects

    def add_child(self, childID):
        if childID not in self.children:
            self.children.append(childID)

    def has_child(self, childID):
        return childID in self.children

    ## why not use len??
    def num_sub_mutations(self):
        mutationCount = 0
        for mutation in self.mutations:
            if mutation:
                mutationCount += 1
        return mutationCount
    
    def sequence_contains_mutation(self, subMut):
        if subMut[1] > len(self.sequence): return False
        return self.sequence[subMut[1]] == subMut[2]

    def get_sequence_with_mutation_reverted(self, subMut):
        revertedSequence = list(self.sequence)
        revertedSequence[subMut[1]] = subMut[0]
        return ''.join(revertedSequence)

    def parse_swap_code(self, swapCode):
        regex= re.compile(r'Swp(\d+)-(\d+)')
        code = regex.match(swapCode)
        start = int(code.group(1))
        end = int(code.group(2))
        return (start, end)

    def parse_mutation_code(self, mutCode):
        regex= re.compile(r'M(\w)(\d+)(\w)')
        code = regex.match(mutCode)
        mutFrom = code.group(1)
        mutAt = int(code.group(2))
        mutTo = code.group(3)
        return (mutFrom, mutAt, mutTo)
