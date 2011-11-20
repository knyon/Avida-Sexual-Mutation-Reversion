#! /usr/bin/python
import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *
from pedigree.evaluator import *

evaluator = MutationEvaluator()

def analyze_lineage(genealogy, dominantLineage):
    for parentID, offspringID in dominantLineage:
        parent = genealogy.genotypes[parentID]
        offspring = genealogy.genotypes[offspringID]
        if parent.fitness > offspring.fitness and offspring.num_sub_mutations() > 0:
            for mutation in [m for m in offspring.mutations if m]:
                #if evaluator.evaluate_effect_of_mutation(offspring, mutation) < 0:
                analyze_deleterious_mutation(genealogy, offspring, mutation)

def analyze_deleterious_mutation(genealogy, origin, mutation):
    pattern = SubMutTDTracePattern(mutation)
    mutationTrace = Tracer(genealogy, pattern).make_trace(origin)
    if mutationTrace:
        for parentID, offspringID in mutationTrace:
            parent = genealogy.genotypes[parentID]
            offspring = genealogy.genotypes[offspringID]
            if offspring.num_sub_mutations() > 0 and evaluator.evaluate_effect_of_mutation(offspring, mutation) > 0:
                print("\nSign epistatic occurance found:\n")
                print("Recovery = Genotype where fitness reversal occured, Origin = Genotype that deleterious mutation originated")
                print("\tRecovery ID: {}".format(offspring.ID))
                print("\tOrigin ID  : {}".format(origin.ID))
                print("\tRecovery sequence: {}".format(offspring.sequence))
                print("\tOrigin sequence  : {}".format(origin.sequence))
                print("\tDeleterious mutation: {0} to {2} at {1}".format(*mutation))
                for mutation in [m for m in offspring.mutations if m]:
                    print("\tRecovery mutation  : {0} to {2} at {1}".format(*mutation))
                print("\tRecovery fitness: {}".format(offspring.fitness))
                print("\tParent fitness   : {}".format(parent.fitness))
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
    dominantLineage = Tracer(genealogy, TopDownTracePattern()).make_trace(genesisGenotype)
    print "Traced!"
    analyze_lineage(genealogy, dominantLineage)
