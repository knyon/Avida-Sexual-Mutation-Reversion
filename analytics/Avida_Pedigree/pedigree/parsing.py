import re

class DetailParser():

    def __init__(self):
        self.regex = re.compile(r'''
        ^(\d*)                    # The string of digits is the genotype ID
        .+?                       # Skip the intervening sequence
        (\d*),(\d*)               # Here are the two parent IDs
        .+?                       # More junk
        (M\w\d+\w)?,?(M\w\d+\w)?  # One, two, or no mutation codes
        ,?(Swp\d+-\d+)            # The swap area
        .+heads_sex\s             # Junk, but marks before the next part
        ([a-z]+)                  # The genome sequence''',
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

    ## AWC -- 11/16/2011
    ## Hack to try and speed things up
    ## Construct a tulple with the releveant genotype info
    def parse_detail_line(self, line):
        details = re.split(" ", line)
        parents = re.split(",",details[3])
        mutations = re.split(",",details[14])
        mutA = None
        mutB = None
        swp = None  ## for now, assuming 1 swp area

        for mut in mutations:
            if mut[0] == "S":
                swp = mut
            elif mut[0] == "M":
                if (mutA != None):
                    mutB = mut
                else:
                    mutA = mut

        sequence = details[17]
        fitness =  details[9]
        return (details[0],parents[0],parents[1],mutA,mutB,swp,sequence, fitness)

    def parse_genesis_detail_line(self, line):
        matchedDetails = self.genesisRegex.search(line)
        sequence = matchedDetails.group(1)
        return ('1', None, None, None, None, None, sequence)
