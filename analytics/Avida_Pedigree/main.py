#! /usr/local/bin/python3
import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Nope")
        exit()
    fileName = sys.argv[1]
    dominantGenotype = sys.argv[2]
    genealogy = GenealogyMaker().make_genealogy_from_file(fileName)
    print_output()
