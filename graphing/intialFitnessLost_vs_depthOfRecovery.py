from data_extractor import *
from analysis_files import analysis_files
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


def calc_inital_fitness_loss(entry):
    originFitness = float(entry[6])
    parent1Fitness = float(entry[9])
    parent2Fitness = float(entry[12])
    higherParentFitness = parent1Fitness if parent1Fitness > parent2Fitness else parent2Fitness
    return ((higherParentFitness - originFitness) / higherParentFitness) * 100

data = aggregate_data_lists(analysis_files)
initialFitnessLost = []
recoveryDepths = []
for entry in data:
    initialFitnessLost.append(calc_inital_fitness_loss(entry))
    recoveryDepths.append(int(entry[0]))

matplotlib.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
plt.xlabel("Relative Phylogenetic Depth To Recovery", fontsize=10)
plt.ylabel("% Decrease in Fitness", fontsize=10)
ax = fig.add_subplot(111)
ax.plot(recoveryDepths, initialFitnessLost, 'o', alpha=0.7, markersize=8)
ax.set_title("Relative Phylogenetic Depth to Fitness Recovery\nvs.\nPercentage Decrease in Fitness in Origin of Deleterious Mutation", fontsize=10)
#plt.show()
plt.savefig("initFitLoss_vs_depthRecover.png", format="png")
