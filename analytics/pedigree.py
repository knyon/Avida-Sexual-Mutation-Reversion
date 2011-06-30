#! /Library/Frameworks/Python.framework/Versions/3.1/bin/python3

import re
import sys

pedigree = {}

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

def create_pedigree_from_detail_file(file_name):
    for line in open(file_name):
        entry = parse_detail_line(line) 
        if entry:
            add_genotype_to_pedigree(entry)

def add_genotype_to_pedigree(entry):
    key = entry[0]
    value = (entry[1], entry[2], entry[3])
    pedigree[key] = value

def find_ancestor( 

def get_lineage_of_genotype(genotype_id, lineage=[]):
    if genotype_id == '1':
        lineage.append("Origin Genotype")
    elif genotype_id not in pedigree:
        raise Exception("No such ID: {}".format(genotype_id))
    else:
        parent_a_id, parent_b_id = get_parents(genotype_id)
        get_lineage_of_genotype(parent_a_id, lineage)
        get_lineage_of_genotype(parent_b_id, lineage)
        lineage.append(genotype_id)
        lineage.append(genotype_id)
    return lineage

def get_parents(genotype_id):
    listing = pedigree[genotype_id]
    return (listing[1], listing[2])

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python pedigree detail_dump_file_name")
        exit()
    file_name = sys.argv[1]
    create_pedigree_from_detail_file(file_name)
