import re
from pedigree.genotype import Genotype
from pedigree.genealogy import Genealogy

class DetailParser():

    @staticmethod
    def process_line(line):
        if line[:2] == '1 ':
            details = _parse_genesis_detail_line(line)
        else:
            details = _parse_detail_line(line) 
        return details

def _parse_detail_line(line):
    regex = re.compile(r'''
    ^(\d*)                         # The string of digits is the genotype ID
    [\s\)\(:a-z]*                  # Skip the intervening sequence
    (\d*),(\d*)                    # Here are the two parent IDs
    [-\s\d]*                       # More junk
    (M\w\d+\w)?(?:,(M\w\d+\w))?    # One, two, or no mutation codes
    .*(Swp\d+-\d+)
    .*heads_sex\s                  # Junk, but marks before the next part
    ([a-z]+)                       # The genome sequence''',
    re.VERBOSE)

    matchedDetails = regex.match(line)
    if matchedDetails:
        return matchedDetails.groups()
    else:
        return None

def _parse_genesis_detail_line(line):
    regex = re.compile(r'''
    .*heads_sex\s      # Junk, but marks before the next part
    ([a-z]+)           # The genome sequence''', re.VERBOSE)

    matchedDetails = regex.search(line)
    sequence = matchedDetails.group(1)
    return ('1', None, None, None, None, None, sequence)
