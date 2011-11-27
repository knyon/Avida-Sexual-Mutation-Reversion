#! /usr/bin/python
#/home/ac43497/local/bin/python2.7

import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *
from pedigree.evaluator import *
from collections import deque

evaluator = MutationEvaluator()
output = open("analysis.txt", 'w')
output.write("Analysis file:")

def analyze_lineage(genealogy, dominantLineage):
    queue = deque()
    queue.append(genealogy['1'])
    while queue:
        parent = queue.popleft()
        for offspring in [genealogy[ID] for ID in parent.children]:
            if not offspring.isMarked():
                if parent.fitness > offspring.fitness and offspring.num_sub_mutations() > 0:
                    for mutation in [m for m in offspring.mutations if m]:
                        if evaluator.evaluate_effect_of_mutation(offspring, mutation) < 0:
                            analyze_deleterious_mutation(genealogy, offspring, mutation)
                offspring.mark()
                queue.append(offspring)

def analyze_deleterious_mutation(genealogy, origin, mutation):
    queue = deque()
    queue.append(origin)
    while queue:
        parent = queue.popleft()
        for offspring in [genealogy[ID] for ID in parent.children]:
            if offspring.sequence_contains_mutation(mutation):
                if offspring.fitness > parent.fitness and offspring.num_sub_mutations() > 0 and evaluator.evaluate_effect_of_mutation(offspring, mutation) > 0:
                    output.write("\nSign epistatic occurance found:\n")
                    output.write("\tOrigin ID  : {}\n".format(origin.ID))
                    output.write("\tParent ID  : {}\n".format(parent.ID))
                    output.write("\tRecovery ID: {}\n".format(offspring.ID))
                    output.write("\tOrigin sequence  : {}\n".format(origin.sequence))
                    output.write("\tParent sequence  : {}\n".format(parent.sequence))
                    output.write("\tRecovery sequence: {}\n".format(offspring.sequence))
                    output.write("\tDeleterious mutation: {0} to {2} at {1}\n".format(*mutation))
                    for mutation in [m for m in offspring.mutations if m]:
                        output.write("\tRecovery mutation  : {0} to {2} at {1}\n".format(*mutation))
                    output.write("\tOrigin fitness   : {}\n".format(origin.fitness))
                    output.write("\tParent fitness   : {}\n".format(parent.fitness))
                    output.write("\tRecovery fitness: {}\n".format(offspring.fitness))
                    return None
                else: 
                    queue.append(offspring)




if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Nope")
        exit()
    fileName = sys.argv[1]
    dominantGenotypeID = sys.argv[2]
    genealogy = GenealogyMaker().make_genealogy_from_file(fileName, dominantGenotypeID)
    genealogy.prune_all_non_lineage_genotypes()
    print "Genologized!"
    # No need to trace, because the pruned genealogy is the trace
    #dominantLineage = Tracer(genealogy, TopDownTracePattern()).make_trace(genesisGenotype)
    #print "Traced!"
    analyze_lineage(genealogy)
    print("Finished!")
    output.close()
