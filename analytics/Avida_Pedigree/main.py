#! /usr/local/bin/python3
import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Nope")
        exit()
    file_name = sys.argv[1]
    genealogy = GenealogyMaker().make_genealogy_from_file(file_name)
    trace = Tracer(genealogy).make_trace()
    GraphvizWriter().write_trace_to_graphviz(trace)
