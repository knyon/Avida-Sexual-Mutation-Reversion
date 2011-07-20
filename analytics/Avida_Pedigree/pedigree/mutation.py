import re


class Mutation():

    def __init__(self, mutationCode):
        if mutationCode:
            self.mutationCode = mutationCode
            self.parse_mutation_code(mutationCode)
        else:
            self.mutationCode = None

    def parse_mutation_code(self, mutationCode):
        regex = re.compile(r'M(\w)(\d+)(\w)')
        code = regex.match(mutationCode)
        self.mutationFrom = code.group(1)
        self.mutationLocation = int(code.group(2))
        self.mutationTo = code.group(3)

    def is_defined(self):
        if self.mutationCode:
            return True
        else:
            return False


class MutationVerifier():
     
    @staticmethod
    def verify_mutation(genotype, parentA_genotype, parentB_genotype):
        pass

