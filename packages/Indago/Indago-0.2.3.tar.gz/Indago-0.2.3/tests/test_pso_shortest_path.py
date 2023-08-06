# -*- coding: utf-8 -*-
"""
Created on Fri Mar 30 21:52:32 2018

@author: Stefan
"""
import sys
sys.path.append('..')
from indago import PSO
from indago.benchmarks import CEC2014
from indago.benchmarks import ShortestPath
import numpy as np
import time
import matplotlib.pyplot as plt



# NewPSO instance
pso = PSO()
runs = 5 # Number of runs

# Define optimization problem
sp = ShortestPath('case_2.5')
pso.evaluation_function = sp.obj_cnstr
pso.number_of_processes = 4
pso.dimensions = 100
pso.lb = np.ones(pso.dimensions) * -10
pso.ub = np.ones(pso.dimensions) *  10
pso.objectives = 1
pso.objective_labels = ['Length']
pso.constraints = 1
pso.constraint_labels = ['Obstacles intersection length']

# Define PSO parameters
pso.swarm_size = 50
pso.iterations = 100
pso.method = 'Vanilla'
pso.params['inertia'] = 0.65
pso.params['cognitive_rate'] = 1.0
pso.params['social_rate'] = 1.0
# pso.params['anakatabatic_inertia'] = None

print(pso)

OPT = []
start = time.time()
for run in range(runs):
    opt = pso.optimize()
    OPT.append(opt)
    print(f'Run {run +1} fitness: {opt.f}')
end = time.time()
print(f'Average fitness: {np.average([opt.f for opt in OPT])}')

best = np.min(OPT)

print()
print('Total elapsed time: %.2f s' % (end - start))
print('Run average time: %.2f s' % ((end - start) / runs))
print('Best result:')
print(best)
print()
pso.results.plot_convergence()

plt.figure()
plt.title('PSO')
ax = plt.gca()
sp.draw_obstacles(ax)
for run, opt in enumerate(OPT):
    sp.draw_path(opt.X, ax, f'Run {run + 1}, f:{opt.f:.2f}')
plt.legend()
