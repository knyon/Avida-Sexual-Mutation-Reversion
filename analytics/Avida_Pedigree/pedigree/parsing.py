import re

class DetailParser():

    def __init__(self):
        self.regex = re.compile(r'''
        ^(\d*)                         # The string of digits is the genotype ID
        [\s\)\(:a-z]*                  # Skip the intervening sequence
        (\d*),(\d*)                    # Here are the two parent IDs
        [-\s\d]*                       # More junk
        (M\w\d+\w)?(?:,(M\w\d+\w))?    # One, two, or no mutation codes
        \,?(Swp\d+-\d+)?                 # The swap area
        .*heads_sex\s                  # Junk, but marks before the next part
        ([a-z]+)                       # The genome sequence''',
        re.VERBOSE)

        self.genesisRegex = re.compile(r'''
        .*heads_sex\s      # Junk, but marks before the next part
        ([a-z]+)           # The genome sequence''', re.VERBOSE)

    def process_line(self, line):
        if line[:2] == '1 ':
            details = self.parse_genesis_detail_line(line)
        else:
            details = self.parse_detail_line(line) 
        return details

    def parse_detail_line(self, line):
        matchedDetails = self.regex.match(line)
        if matchedDetails:
            print(matchedDetails.groups())
            return matchedDetails.groups()
        else:
            return None

    def parse_genesis_detail_line(self, line):
        matchedDetails = self.genesisRegex.search(line)
        sequence = matchedDetails.group(1)
        return ('1', None, None, None, None, None, sequence)
