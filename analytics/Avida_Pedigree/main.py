#! /usr/local/bin/python3
import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Nope")
        exit()
    file_name = sys.argv[1]
    genealogy = GenealogyMaker().make_genealogy_from_file(file_name)
    if sys.argv[2]:
        trace = SubMutTracer(genealogy).make_trace(sys.argv[2])
    else:
        trace = Tracer(genealogy).make_trace()
    if sys.argv[3]:
        GraphvizWriter().write_trace_to_graphviz(trace, sys.argv[3])
    else:
        GraphvizWriter().write_trace_to_graphviz(trace)
