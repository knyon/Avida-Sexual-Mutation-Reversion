#! /usr/bin/python
import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Nope")
        exit()
    fileName = sys.argv[1]
    dominantGenotype = str(sys.argv[2])
    genealogy = GenealogyMaker().make_genealogy_from_file(fileName, dominantGenotype)
    print "Genologized!"
    dominantLineage = Tracer(genealogy, TopDownTracePattern()).make_trace(dominantGenotype))
    print "Traced!"
    print(dominantLineage)
    #analyze_lineage(genealogy, dominantLineage)


#def analyze_lineage(genealogy, dominantLineage):
    #evaluator = MutationEvaluator()
    #for parent, offspring in dominantLineage:
        #for mutation in parent.mutations:
            #if mutation:
                #pattern = MutRevTracePattern(mutation, evaluator)
                #tracer = Tracer(genealogy, pattern)
                #output(tracer)

#def output(tracer):
    #pass
