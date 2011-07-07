import re


class Mutation():

    def __init__(self, mutationCode):
        self.mutationCode = mutationCode
        if mutationCode != '  ':
            self.parse_mutation_code(mutationCode)

    def parse_mutation_code(self, mutationCode):
        regex = re.compile(r'M(\w)(\d+)(\w)')
        code = regex.match(mutationCode)
        self.mutationFrom = code.group(1)
        self.mutationLocation = int(code.group(2))
        self.mutationTo = code.group(3)


class MutationVerifier():
    pass
