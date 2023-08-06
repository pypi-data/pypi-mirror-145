# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 14:53:52 2018

@author: Stefan
"""


import sys, os
sys.path.append('..')
#import pyswarms as ps
import time
import numpy as np
import matplotlib.pyplot as plt
from indago.benchmarks import ShortestPath
from indago import PSO
from indago import SSA
from scipy.interpolate import interp1d


nd = 100
runs = 20

CASE = 'case_3.1'
sp = ShortestPath(CASE)


"""
ssa = SSA()
ssa.evaluation_function = sp.obj_cnstr

ssa.dimensions = nd
ssa.swarm_size = nd
ssa.lb = np.ones(nd) * -20
ssa.ub = np.ones(nd) * 20
ssa.iterations = 100 * nd
ssa.objectives = 1
ssa.objective_labels = ['Length']
ssa.constraints = 1
ssa.constraint_labels = ['Obstacles intersection length']
ssa.method = 'Vanilla'
ssa.params = {'acorn_tree_attraction': 0.5} # larger ACT is better for this problem

print('SSA')
print(ssa.method)

OPTIMIZER = ssa
"""

 
pso = PSO()
pso.evaluation_function = sp.obj_cnstr # new PSO
#pso.objective = sp.penalty # old PSO
pso.dimensions = nd
pso.params['swarm_size'] = nd
pso.lb = np.ones(nd) * -20
pso.ub = np.ones(nd) * 20
pso.iterations = 100 * nd
pso.objectives = 1
pso.objective_labels = ['Length']
pso.constraints = 1
pso.constraint_labels = ['Obstacles intersection length']


## Vanilla
#pso.method = 'Vanilla'
#pso.params['inertia'] = 0.72
#pso.params['cognitive_rate'] = 1.0
#pso.params['social_rate'] = 1.0

# TVAC
pso.method = 'TVAC'
pso.params['inertia'] = 'LDIW'


## Anakatabatic models

#method = 'akb vanillaSP1 aka 4SquashedXs'
#w_start = [-0.7515819, 0.8609477, -1.49907453, -0.74599866, 0.22661593]
#w_stop = [-0.99890941, 1.49659705, -2., 0.10159583, -0.88263859]
##splinetype = 'cubic'
#splinetype = 'linear'

method = 'akb tvac1 aka RightwardPeaks'
w_start = [-1.79457153, -0.33409362, 2., -0.67365566, 1.29661024]
w_stop = [-0.9120458, -0.87835946, -0.83647823, 0.67106473, -0.36185384]
splinetype = 'linear'

#method = 'LPSO'
#def f_start(Th):
#    w = 0.72 * np.ones_like(Th)
#    for i, th in enumerate(Th):
#        if th < 4*np.pi/4: 
#            w[i] = 0
#    return w
#f_stop = f_start
#splinetype = None


try: f_start    # if akb funs do not exist...
except:         # ...create w-defined akb interpolation funs
    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    f_start = interp1d(Th, w_start, kind=splinetype)
    f_stop = interp1d(Th, w_stop, kind=splinetype)

pso.params['inertia'] = 'anakatabatic'
pso.params['akb_fun_start'] = f_start
pso.params['akb_fun_stop'] = f_stop

print('PSO')
print(pso.method)
print(f'{nd} dims; {runs} runs')
try: print(method, splinetype)
except: pass

OPTIMIZER = pso


#fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

OPT = []
start = time.time()
for run in range(runs):
    opt = OPTIMIZER.optimize()
    OPT.append(opt)
    print(f'Run {run +1} fitness: {opt.f}')
    #OPTIMIZER.results.plot_convergence((ax1, ax2))
end = time.time()

print(f'Elapsed time: {(end - start):.2f}s')
print(f'Average fitness: {np.average([opt.f for opt in OPT])}')
print(f'Median fitness: {np.median([opt.f for opt in OPT])}')

best = np.min(OPT)
print(f'Best fitness: {best.f}')
#print(best)


"""
plt.figure()
ax = plt.gca()
sp.draw_obstacles(ax)
for r in range(runs):
    sp.draw_path(OPT[r].X, ax, 'Run %d' % (r + 1))

plt.figure()
plt.title('Best path')
ax = plt.gca()
sp.draw_path(best.X, ax)
sp.draw_obstacles(ax)
"""


""" 
*************************
shortest_path test results: 20d, 20 runs 
*************************

PSO Vanilla 
Median fitness: 1.922e+02

PSO Vanilla LPSO
Median fitness: 1.924e+02

PSO Vanilla vanillaSP1
Median fitness: 1.893e+02 *** WINNER ***

PSO TVAC 
Median fitness: 1.917e+02

PSO TVAC LPSO
Median fitness: 1.920e+02

PSO TVAC vanillaSP1
Median fitness: 1.893e+02 *** WINNER ***

PSO TVAC tvac1
Median fitness: 1.905e+02

FWA Vanilla
Median fitness: 1.924e+02

SSA Vanilla
Median fitness: 1.906e+02 # avrg of 10 results with varying ACT is 1.914e+02


*************************
shortest_path test results: 100d, 20 runs
*************************

PSO Vanilla 
Median fitness: 1.885e+02

PSO Vanilla vanillaSP1
Median fitness: 1.868e+02 *** WINNER ***

PSO TVAC
Median fitness: 1.928e+02

PSO TVAC vanillaSP1
Median fitness: 1.914e+02

PSO TVAC tvac1
Median fitness: 1.894e+02

SSA Vanilla
Median fitness: 1.907e+02
"""



"""
# Pyswarms
pso.params['inertia'] = 0.72
options = {'c1': pso.params['cognitive_rate'],
           'c2': pso.params['social_rate'],
           'w': pso.params['inertia']}
PS = np.zeros(runs)
for r in range(runs):
    # Call instance of PSO with bounds argument
    optimizer = ps.single.GlobalBestPSO(n_particles=pso.swarm_size,
                                        dimensions=nd,
                                        options=options,
                                        bounds=(pso.lb, pso.ub))
def fun(x):
    n_particles = x.shape[0]
    j = [sp.penalty(x[i]) for i in range(n_particles)]
    return np.array(j)
# Perform optimization
cost, pos = optimizer.optimize(fun, print_step=100,
                               iters=pso.iterations, verbose=3)
cost, pos = optimizer.optimize(fun, print_step=100,
                               iters=pso.iterations, verbose=0)
PS[r] = cost
print()
print('Pyswarms best   fitness:  %.3e' % np.min(PS))
print('Pyswarms median fitness:  %.3e' % np.median(PS))
print()
"""