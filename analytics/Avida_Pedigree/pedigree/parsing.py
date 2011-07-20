import re
from pedigree.genotype import Genotype

class PedigreeParser():

    def __init__(self, fileName = ''):
        self.pedigree = {}
        if fileName:
            self.create_pedigree_from_detail_file(fileName)

    def create_pedigree_from_detail_file(self, fileName):
        for line in open(fileName):
            self.process_line(line)
    
    def create_pedigree_from_string(self, inputString):
        for line in inputString.split('\n'):
            self.process_line(line)

    def process_line(self, line):
        if line[:2] == '1 ':
            details = self.parse_genesis_detail_line(line)
        else:
            details = self.parse_detail_line(line) 
        if details:
            self.add_genotype_to_pedigree(details)


    def add_genotype_to_pedigree(self, details):
        print(details)
        newGenotype = Genotype(*details)
        key = newGenotype.genotypeID
        self.pedigree[key] = newGenotype

    @staticmethod
    def parse_detail_line(line):
        regex = re.compile(r'''
        ^(\d*)                         # The string of digits is the genotype ID
        [\s\)\(:a-z]*                  # Skip the intervening sequence
        (\d*),(\d*)                    # Here are the two parent IDs
        [-\s\d]*                       # More junk
        (M\w\d+\w)?(?:,(M\w\d+\w))?    # One, two, or no mutation codes
        .*heads_sex\s                  # Junk, but marks before the next part
        ([a-z]+)                       # The genome sequence''',
        re.VERBOSE)

        matchedDetails = regex.match(line)
        if matchedDetails:
            return matchedDetails.groups()
        else:
            return None

    @staticmethod
    def parse_genesis_detail_line(line):
        regex = re.compile(r'''
        .*heads_sex\s      # Junk, but marks before the next part
        ([a-z]+)           # The genome sequence''', re.VERBOSE)

        matchedDetails = regex.search(line)
        sequence = matchedDetails.group(1)
        return ('1', None, None, None, None, sequence)
