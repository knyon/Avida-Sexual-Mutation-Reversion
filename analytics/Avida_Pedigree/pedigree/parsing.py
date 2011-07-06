import re


pedigree = {}

def create_pedigree_from_detail_file(file_name):
    for line in open(file_name):
        entry = parse_detail_line(line) 
        if entry:
            add_genotype_to_pedigree(entry)
    return pedigree

def parse_detail_line(detail):
    regex = re.compile(r"^(\d*)[\s\)\(:a-z]*(\d*),(\d*).*heads_sex\s([a-z]*)")
    matched_genotype_ids = regex.match(detail)

    if matched_genotype_ids:
        genotype_id = matched_genotype_ids.group(1)
        parent_a_id = matched_genotype_ids.group(2)
        parent_b_id = matched_genotype_ids.group(3)
        sequence = matched_genotype_ids.group(4)
        return (genotype_id, sequence, parent_a_id, parent_b_id)
    else:
        return ''

def add_genotype_to_pedigree(entry):
    key = entry[0]
    value = (entry[1], entry[2], entry[3])
    pedigree[key] = value

def get_pedigree():
    return pedigree
