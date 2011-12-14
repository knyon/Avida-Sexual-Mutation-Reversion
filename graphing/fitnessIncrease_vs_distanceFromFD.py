from data_extractor import *
from analysis_files import analysis_files
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

#def calc_average_distance_from 

def calc_inital_fitness_increase(entry):
    recoveryFitness = float(entry[15])
    parent1Fitness = float(entry[20])
    parent2Fitness = float(entry[23])
    averageParentFitness = (parent1Fitness + parent2Fitness)/2
    return ((recoveryFitness - averageParentFitness) / averageParentFitness) * 100

data = aggregate_data_lists(analysis_files)
recoveryFitnessIncrease = []
totalDepths = []
for entry in data:
    if entry[2] == '1':
        recoveryFitnessIncrease.append(calc_inital_fitness_increase(entry))
        #totalDepths.append(int(entry[1])+int(entry[0]))
        totalDepths.append(int(entry[3]))

matplotlib.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
plt.xlabel("Relative Phylogenetic Depth from Final Dominant", fontsize=10)
plt.ylabel("% Increase in Fitness", fontsize=10)
ax = fig.add_subplot(111)
ax.plot(totalDepths, recoveryFitnessIncrease, 'o', alpha=0.7, markersize=8)
ax.set_title("Phylogenetic Depth from Final Dominant Genotype\nvs.\nPercentage Increase in Fitness in Recovery Genotype", fontsize=10)
#plt.show()
plt.savefig("fitnessInc_vs_FDDepth.png", format="png")
