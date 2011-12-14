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
analysisOutput = open("analysis.txt", 'w')
analysisOutputHeader = '''# Analysis of all sign epsistatic events that occurred in the lineage of the final dominant genotype
# Values separated by spaces, in order:
# 0. Phylogenetic Depth between origin and recovery
# 1. Total Phylogenetic Depth
# 2. Is the deleterious mutation in the final dominant sequence?
# 3. Distance from recovery to final dominant if mutation is in sequence; else -1
# 4. Deleterious mutation
# 5. Genotype ID of origin of deleterious mutation
# 6. Origin fitness
# 7. Origin sequence
# 8. Parent 1 of origin ID
# 9. Parent 1 of origin fitness
# 10. Parent 1 of origin sequence
# 11. Parent 2 of origin ID
# 12. Parent 2 of origin fitness
# 13. Parent 2 of origin sequence
# 14. Genotype ID of recovery genotype
# 15. Recovery fitness
# 16. Recovery sequence
# 17. Mutation 1 in recovery genotype
# 18. Mutation 2 in recovery genotype OR 'None'
# 19. Parent 1 of recovery ID
# 20. Parent 1 of recovery fitness
# 21. Parent 1 of recovery sequence
# 22. Parent 2 of recovery ID
# 23. Parent 2 of recovery fitness
# 24. Parent 2 of recovery sequence\n\n\n'''
analysisOutput.write(analysisOutputHeader)
summaryOutput = open("summary.txt", 'w')

def analyze_lineage(genealogy):
    totalPhylogeneticDepth = 0
    statusCount = 0
    signEpistasisCount = 0
    delMutationCount = 0
    queue = deque()
    queue.append(genealogy['1'])
    queue.append(None)
    while queue:
        parent = queue.popleft()
        if parent is None:
            if queue:
                queue.append(None)
                totalPhylogeneticDepth += 1
        else:
            statusCount += 1
            for offspring in [genealogy[ID] for ID in parent.children]:
                if not offspring.isMarked():
                    if parent.fitness > offspring.fitness and offspring.num_sub_mutations() > 0 and parent.fitness - offspring.fitness > parent.fitness*0.01:
                        for mutation in [m for m in offspring.mutations if m]:
                            if mutation[0] != mutation[2] and evaluator.evaluate_effect_of_mutation(offspring, mutation) < 0:
                                delMutationCount += 1
                                if analyze_deleterious_mutation(genealogy, offspring, mutation, totalPhylogeneticDepth):
                                    signEpistasisCount += 1
                                    break
                                if queue[-1] is not None and queue[-1].ID != offspring.ID:
                                    queue.append(offspring)
                    else:
                        queue.append(offspring)
                    offspring.mark()
            if statusCount % 100 == 0:                                                                                                                                                
                print("On item {} through the queue".format(statusCount))
    summaryOutput.write("Total Deleterious Mutations: {}\nTotal Sign Epistatic Mutations: {}".format(delMutationCount, signEpistasisCount))

def deleterious_mutation_in_final_dominant(genealogy, recoveryGenotype, delMutation):
    global dominantGenotypeID
    marker = SearchMarker()
    queue = deque()
    queue.append(recoveryGenotype)
    queue.append(None)
    distanceFromFinalDominant = 0
    while queue:
        parent = queue.popleft()
        if parent is None:
            if queue:
                queue.append(None)
                distanceFromFinalDominant += 1
        elif not marker.is_marked(parent.ID):
            if parent.sequence_contains_mutation(delMutation):
                if parent.ID == dominantGenotypeID:
                    del marker, queue
                    return 1, distanceFromFinalDominant
                else:
                    for offspring in [genealogy[ID] for ID in parent.children]:
                        queue.append(offspring)
            elif parent.ID == dominantGenotypeID:
                del marker, queue
                return 0, distanceFromFinalDominant
            marker.mark(parent.ID)
    return 0, -1

def analyze_deleterious_mutation(genealogy, origin, delMutation, totalPhylogeneticDepth):
    marker = SearchMarker()
    queue = deque()
    queue.append(origin)
    queue.append(None)
    phylogeneticDepth = 0
    while queue:
        parent = queue.popleft()
        if parent is None:
            if queue:
                queue.append(None)
                phylogeneticDepth += 1
        elif not marker.is_marked(parent.ID):
            for offspring in [genealogy[ID] for ID in parent.children]:
                if offspring.sequence_contains_mutation(delMutation):
                    if offspring.fitness > parent.fitness and offspring.num_sub_mutations() > 0 and offspring.fitness - parent.fitness > parent.fitness*0.01 and evaluator.evaluate_effect_of_mutation(offspring, delMutation) > 0:
                        inFinalDominant, distanceFromFinalDominant= deleterious_mutation_in_final_dominant(genealogy, offspring, delMutation)
                        analysisLine = "{phylogeneticDepth} {totalPhylogeneticDepth} {inFinalDominant} {distanceFromFinalDominant} "\
                                       "{deleteriousMutation} {originID} {originFitness} {originSequence} "\
                                       "{originParent1ID} {originParent1Fitness} {originParent1Sequence} "\
                                       "{originParent2ID} {originParent2Fitness} {originParent2Sequence} "\
                                       "{recoveryID} {recoveryFitness} {recoverySequence} {recoveryMutation1} {recoveryMutation2} "\
                                       "{recoveryParent1ID} {recoveryParent1Fitness} {recoveryParent1Sequence} "\
                                       "{recoveryParent2ID} {recoveryParent2Fitness} {recoveryParent2Sequence}\n"\
                        .format(phylogeneticDepth=phylogeneticDepth,totalPhylogeneticDepth=totalPhylogeneticDepth,inFinalDominant=inFinalDominant,distanceFromFinalDominant=distanceFromFinalDominant,
                                deleteriousMutation=delMutation, originID=origin.ID, originFitness=origin.fitness, originSequence=origin.sequence,
                                originParent1ID=genealogy[origin.parents[0]].ID, originParent1Fitness=genealogy[origin.parents[0]].fitness, originParent1Sequence=genealogy[origin.parents[0]].sequence,
                                originParent2ID=genealogy[origin.parents[1]].ID, originParent2Fitness=genealogy[origin.parents[1]].fitness, originParent2Sequence=genealogy[origin.parents[1]].sequence,
                                recoveryID=offspring.ID, recoveryFitness=offspring.fitness, recoverySequence=offspring.sequence, recoveryMutation1=offspring.mutations[0], recoveryMutation2.mutations[1],
                                recoveryParent1ID=genealogy[offspring.parents[0]].ID, recoveryParent1Fitness=genealogy[offspring.parents[0]].fitness, recoveryParent1Sequence=genealogy[offspring.parents[0]].sequence,
                                recoveryParent2ID=genealogy[offspring.parents[1]].ID, recoveryParent2Fitness=genealogy[offspring.parents[1]].fitness, recoveryParent2Sequence=genealogy[offspring.parents[1]].sequence
                                )
                        analysisOutput.write(analysisLine)
                        del marker, queue
                        return offspring.fitness - parent.fitness
                    else: 
                        queue.append(offspring)
            marker.mark(parent.ID)
    return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Nope")
        exit()
    fileName = sys.argv[1]
    global dominantGenotypeID
    dominantGenotypeID = sys.argv[2]
    genealogy = GenealogyMaker().make_genealogy_from_file(fileName, dominantGenotypeID)
    genealogy.prune_all_non_lineage_genotypes()
    print "Genologized!"
    analyze_lineage(genealogy)
    print("Finished!")
    analysisOutput.close()
    summaryOutput.close()
