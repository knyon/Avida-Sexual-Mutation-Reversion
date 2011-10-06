import re

class Mutation():

    def __init__(self, mutationCode):
        self.mutationCode = mutationCode
        self.parse_mutation_code()

    def parse_mutation_code(self):
        pass

class SubstitutionMutation(Mutation):
    regex= re.compile(r'M(\w)(\d+)(\w)')

    def parse_mutation_code(self):
        code = SubstitutionMutation.regex.match(self.mutationCode)
        self.mutationFrom = code.group(1)
        self.mutationAt = int(code.group(2))
        self.mutationTo = code.group(3)

class SwapArea(Mutation):
    regex= re.compile(r'Swp(\d+)-(\d+)')

    def parse_mutation_code(self):
        if self.mutationCode:
            code = SwapArea.regex.match(self.mutationCode)
            self.swapStart = int(code.group(1))
            self.swapEnd = int(code.group(2))
