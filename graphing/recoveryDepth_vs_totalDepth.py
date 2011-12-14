from data_extractor import *
from analysis_files import analysis_files
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

data = aggregate_data_lists(analysis_files)
totalDepths = []
recoveryDepths = []
for entry in data:
    recoveryDepths.append(entry[0])
    totalDepths.append(entry[1])

matplotlib.rcParams['axes.unicode_minus'] = False
fig = plt.figure()
plt.xlabel("Total Phylogenetic Depth", fontsize=10)
plt.ylabel("Relative Phylogenetic Depth to Recovery", fontsize=10)
ax = fig.add_subplot(111)
ax.plot(totalDepths, recoveryDepths, 'o', alpha=0.7, markersize=8)
ax.set_title("Total Phylogenetic Depth\nvs.\nRelative Phylogenetic Depth to Fitness Recovery", fontsize=10)
#plt.show()
plt.savefig("totalDepth_vs_recoverDepth.png", format="png")
