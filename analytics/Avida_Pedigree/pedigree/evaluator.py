import os
import re


class MutationEvaluator:

    def __init__(self, pathToAvida):
        self.pathToAvida = pathToAvida

    def evaluate_effect_of_mutation(self, genotype, mutation):
        genotypeFitness = get_fitness_of_sequence(genotype.sequence)
        revertedSequence = genotype.get_sequence_with_mutation_reverted(mutation)
        revertedFitness = get_fitness_of_sequence(revertedSequence)
        if revertedFitness > genotypeFitness:
            return 1
        else:
            return -1

    def evaluate_if_mutation_is(self, genotype, mutation):
        genotypeFitness = get_fitness_of_sequence(genotype.sequence)
        revertedSequence = genotype.get_sequence_with_mutation_reverted(mutation)
        revertedFitness = get_fitness_of_sequence(revertedSequence)
        if revertedFitness > genotypeFitness:
            return False
        else:
            return True

    def get_fitness_of_sequence(self, sequence)
        write_sequence_to_avida_analyze_file(sequence)
        run_avida_in_analyze_mode()
        return get_fitness_from_analyze_output_file()

    def write_sequence_to_avida_analyze_file(self):
        analyzeFilePath = self.pathToAvida + "analyze.cfg"
        output = 'LOAD_SEQUENCE {0}\nRECALCULATE\nDETAIL fitness detail.txt'.format(sequence)
        if(os.path.exists(analyzeFilePath)):
            os.remove(analyzeFilePath)
        fp = open(analyzeFilePath, 'w')
        fp.write(output)
        fp.close()

    def run_avida_in_analyze_mode(self):
        command = self.pathToAvida + "avida -a"
        os.system(command)

    def get_fitness_from_analyze_output_file(self):
        outputFilePath = self.pathToAvida + os.path.sep + 'detail.txt'
        fp = open(outputFilePath)
        analyzeOutputFile = fp.read()
        fp.close()
        fitnessRegex = re.search(analyzeOutputFile, "(?=<Fitness:)\d+.?\d*")
        return float(fitnessRegex.group(0))
        

