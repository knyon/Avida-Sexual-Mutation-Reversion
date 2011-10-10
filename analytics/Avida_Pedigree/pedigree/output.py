import os
from pedigree.genealogy import *

GENESIS = '1'

class GraphvizWriter:

    def write_trace_to_graphviz(self, trace, filename = "genealogy.dot"):
        fo = open(filename, 'w')
        fo.write(self.build_graphviz(trace))
        fo.close()

    def build_graphviz(self, trace):
        head = "digraph FamilyTree {\n"
        body = ''.join(
                ["\t{0} -> {1};\n".format(parent, child)
                for (parent,child) in trace])
        end = "}"
        return head + body + end
