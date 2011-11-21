#! /usr/bin/python
import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *
from pedigree.evaluator import *

evaluator = MutationEvaluator()
output = open("analysis.txt", 'w')
output.write("Analysis file:")

def analyze_lineage(genealogy, dominantLineage):
    edgeTotal = len(dominantLineage)
    edgeCount = 0
    for parentID, offspringID in dominantLineage:
        edgeCount += 1
        if edgeCount % 50 == 0:
            print("On edge {} of {}".format(edgeCount, edgeTotal))
        parent = genealogy.genotypes[parentID]
        offspring = genealogy.genotypes[offspringID]
        if parent.fitness > offspring.fitness and offspring.num_sub_mutations() > 0:
            for mutation in [m for m in offspring.mutations if m]:
                if evaluator.evaluate_effect_of_mutation(offspring, mutation) < 0:
                    analyze_deleterious_mutation(genealogy, offspring, mutation)

def analyze_deleterious_mutation(genealogy, origin, mutation):
    pattern = SubMutTDTracePattern(mutation)
    mutationTrace = Tracer(genealogy, pattern).make_trace(origin)
    if mutationTrace:
        for parentID, offspringID in mutationTrace:
            parent = genealogy.genotypes[parentID]
            offspring = genealogy.genotypes[offspringID]
            if offspring.fitness > parent.fitness and offspring.num_sub_mutations() > 0 and evaluator.evaluate_effect_of_mutation(offspring, mutation) > 0:
                output.write("\nSign epistatic occurance found:\n")
                output.write("\tOrigin ID  : {}\n".format(origin.ID))
                output.write("\tParent ID  : {}\n".format(parent.ID))
                output.write("\tRecovery ID: {}\n".format(offspring.ID))
                output.write("\tOrigin sequence  : {}\n".format(origin.sequence))
                output.write("\tParent sequence  : {}\n".format(origin.sequence))
                output.write("\tRecovery sequence: {}\n".format(offspring.sequence))
                output.write("\tDeleterious mutation: {0} to {2} at {1}\n".format(*mutation))
                for mutation in [m for m in offspring.mutations if m]:
                    output.write("\tRecovery mutation  : {0} to {2} at {1}\n".format(*mutation))
                output.write("\tParent fitness   : {}\n".format(parent.fitness))
                output.write("\tRecovery fitness: {}\n".format(offspring.fitness))
                return


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Nope")
        exit()
    fileName = sys.argv[1]
    dominantGenotypeID = sys.argv[2]
    genealogy = GenealogyMaker().make_genealogy_from_file(fileName, dominantGenotypeID)
    dominantGenotype = genealogy.genotypes[dominantGenotypeID]
    genesisGenotype = genealogy.genotypes['1']
    print "Genologized!"
    genealogy.unmark_all_genotypes()
    dominantLineage = Tracer(genealogy, TopDownTracePattern()).make_trace(genesisGenotype)
    print "Traced!"
    analyze_lineage(genealogy, dominantLineage)
    print("Finished!")
    output.close()
