#! /usr/bin/python
#/home/ac43497/local/bin/python2.7

import sys
from pedigree.output import *
from pedigree.genealogy import *
from pedigree.tracer import *
from pedigree.evaluator import *
from collections import deque

class SearchMarker:

    def __init__(self):
        self.markerMap = {}

    def mark(self, genotypeID):
        self.markerMap[genotypeID] = True

    def unmark(self, genotypeID):
        self.markerMap[genotypeID] = False

    def unmark_all(self):
        del self.MarkerMap
        self.markerMap = {}

    def is_marked(self, genotypeID):
        if genotypeID in self.markerMap:
            return self.markerMap[genotypeID]
        else:
            self.markerMap[genotypeID] = False
            return False

evaluator = MutationEvaluator()
detailedOutput = open("analysis.txt", 'w')
summaryOutput = open("summary.txt", 'w')
detailedOutput.write("Analysis file:")
dominantGenotypeID = '1'
averageFitnessIncreaseBin = 0

def analyze_lineage(genealogy):
    statusCount = 0
    signEpistasisCount = 0
    delMutationCount = 0
    queue = deque()
    queue.append(genealogy['1'])
    while queue:
        parent = queue.popleft()
        statusCount += 1
        for offspring in [genealogy[ID] for ID in parent.children]:
            if not offspring.isMarked():
                if parent.fitness > offspring.fitness and offspring.num_sub_mutations() > 0 and parent.fitness - offspring.fitness > parent.fitness*0.01:
                    for mutation in [m for m in offspring.mutations if m]:
                        if evaluator.evaluate_effect_of_mutation(offspring, mutation) < 0:
                            delMutationCount += 1
                            if analyze_deleterious_mutation(genealogy, offspring, mutation):
                                signEpistasisCount += 1
                                break
                            if queue[-1].ID != offspring.ID:
                                queue.append(offspring)
                else:
                    queue.append(offspring)
                offspring.mark()
        if statusCount % 100 == 0:                                                                                                                                                
            print("On item {} through the queue".format(statusCount))
    summaryOutput.write("\nTotal Deleterious Mutations: {}\nTotal Sign Epistatic Mutations: {}\nAverage increase in fitness with SE event: {}".format(delMutationCount, signEpistasisCount, averageFitnessIncreaseBin/signEpistasisCount))

def analyze_deleterious_mutation(genealogy, origin, delMutation):
    marker = SearchMarker()
    queue = deque()
    queue.append(origin)
    while queue:
        parent = queue.popleft()
        if not marker.is_marked(parent.ID):
            for offspring in [genealogy[ID] for ID in parent.children]:
                if offspring.sequence_contains_mutation(delMutation):
                    if offspring.fitness > parent.fitness and offspring.num_sub_mutations() > 0 and offspring.fitness - parent.fitness > parent.fitness*0.01 and evaluator.evaluate_effect_of_mutation(offspring, delMutation) > 0:
                        detailedOutput.write("\nSign epistatic occurance found:\n")
                        detailedOutput.write("\tOrigin ID  : {}\n".format(origin.ID))
                        detailedOutput.write("\tParent ID  : {}\n".format(parent.ID))
                        detailedOutput.write("\tRecovery ID: {}\n".format(offspring.ID))
                        detailedOutput.write("\tOrigin sequence  : {}\n".format(origin.sequence))
                        detailedOutput.write("\tParent sequence  : {}\n".format(parent.sequence))
                        detailedOutput.write("\tRecovery sequence: {}\n".format(offspring.sequence))
                        detailedOutput.write("\tDeleterious mutation: {0} to {2} at {1}\n".format(*delMutation))
                        for mutation in [m for m in offspring.mutations if m]:
                            detailedOutput.write("\tRecovery mutation  : {0} to {2} at {1}\n".format(*mutation))
                            check_if_mutation_in_final_dominant(mutation, offspring.ID, genealogy)
                        detailedOutput.write("\tOrigin fitness   : {}\n".format(origin.fitness))
                        detailedOutput.write("\tParent fitness   : {}\n".format(parent.fitness))
                        detailedOutput.write("\tRecovery fitness: {}\n".format(offspring.fitness))
                        del marker
                        averageFitnessIncreaseBin += offspring.fitness - parent.fitness
                        return True
                    else: 
                        queue.append(offspring)
            marker.mark(parent.ID)
    return False

def check_if_mutation_in_final_dominant(mutation, genotypeID, genealogy):
    finalDominant = genealogy[dominantGenotypeID]
    if finalDominat.sequence_contains_mutation(mutation):
        summaryOutput.write("Final dominant contains sign epistatic mutation {} that arose in genotype #{}\n".format(mutation, genotypeID))

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Nope")
        exit()
    fileName = sys.argv[1]
    dominantGenotypeID = sys.argv[2]
    genealogy = GenealogyMaker().make_genealogy_from_file(fileName, dominantGenotypeID)
    genealogy.prune_all_non_lineage_genotypes()
    print "Genologized!"
    analyze_lineage(genealogy)
    print("Finished!")
    detailedOutput.close()
    summaryOutput.close()
