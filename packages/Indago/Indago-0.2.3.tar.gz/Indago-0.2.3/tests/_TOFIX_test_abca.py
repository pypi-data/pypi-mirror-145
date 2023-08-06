# -*- coding: utf-8 -*-

import sys
sys.path.append('..')
import time
import numpy as np
import matplotlib.pyplot as plt
from indago.benchmarks import ShortestPath
from indago import ABC

nd = 30
sp = ShortestPath('case_3.1')

abca = ABC()
abca.objective = sp.penalty
abca.dimensions = nd
abca.lb = np.ones(nd) * -20
abca.ub = np.ones(nd) * 20
abca.iterations = 500
abca.population_size = 50
abca.max_trials = 25

runs = 5
start = time.time()
F, X = np.zeros(runs), np.zeros([runs, nd])
for r in range(runs):
    F[r] = abca.run()
    print('Run %3d f: %10.3f' % (r + 1, F[r]))
end = time.time()

print()
print('Elapsed time: %.2f s' % (end - start))
print('Indago best   fitness:  %.3e' % np.min(F))
print('Indago median fitness:  %.3e' % np.median(F))
print()
