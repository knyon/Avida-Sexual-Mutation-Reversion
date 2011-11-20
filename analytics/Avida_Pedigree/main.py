#! /usr/bin/python
import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *
from pedigree.evaluator import *

evaluator = MutationEvaluator()

def analyze_lineage(genealogy, dominantLineage):
    #evaluator = MutationEvaluator()
    count = 0
    for parentID, offspringID in dominantLineage:
        parent = genealogy.genotypes[parentID]
        offspring = genealogy.genotypes[offspringID]
        if parent.fitness > offspring.fitness and offspring.num_sub_mutations() > 0:
            for mutation in [m for m in offspring.mutations if m]:
                analyze_deleterious_mutation(genealogy, offspring, mutation)

def analyze_deleterious_mutation(genealogy, genotype, mutation):
    pattern = SubMutTDTracePattern(mutation)
    mutationTrace = Tracer(genealogy, pattern).make_trace(genotype)
    if mutationTrace:
        for parentID, offspringID in mutationTrace:
            parent = genealogy.genotypes[parentID]
            offspring = genealogy.genotypes[offspringID]
            if evaluator.evaluate_effect_of_mutation(offspring, mutation) > 0:
                print("Sign epistatic occurance found:\n")
                print("\tGenotype ID: {}".format(offspring.ID))
                print("\tParent ID: {}".format(parent.ID))
                print("\tGenotype sequence: {}".format(offspring.sequence))
                print("\tParent sequence: {}".format(parent.sequence))
                print("\tMutation: {} to {} at {}".format(*mutation))
                print("\tOffspring fitness: {}".format(offspring.fitness))
                print("\tParent fitness: {}".format(parent.fitness))
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
