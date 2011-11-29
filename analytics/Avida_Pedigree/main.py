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
output = open("analysis.txt", 'w')
output.write("Analysis file:")

def analyze_lineage(genealogy):
    genealogyLength = len(genealogy)
    print("Total length of genealogy to be analyzed: {}".format(genealogyLength))
    statusCount = 0
    queue = deque()
    queue.append(genealogy['1'])
    while queue:
        parent = queue.popleft()
        statusCount += 1
        for offspring in [genealogy[ID] for ID in parent.children]:
            if not offspring.isMarked():
                if parent.fitness > offspring.fitness and offspring.num_sub_mutations() > 0:
                    for mutation in [m for m in offspring.mutations if m]:
                        if evaluator.evaluate_effect_of_mutation(offspring, mutation) < 0:
                            if not analyze_deleterious_mutation(genealogy, offspring, mutation) and queue[-1].ID != offspring.ID:
                                queue.append(offspring)
                else:
                    queue.append(offspring)
                offspring.mark()
        if statusCount % 100 == 0:                                                                                                                                                
            print("On genotype {}".format(statusCount))

def analyze_deleterious_mutation(genealogy, origin, mutation):
    marker = SearchMarker()
    queue = deque()
    queue.append(origin)
    while queue:
        parent = queue.popleft()
        if not marker.is_marked(parent.ID):
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
                        del marker
                        return True
                    else: 
                        queue.append(offspring)
    return False


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
    output.close()


