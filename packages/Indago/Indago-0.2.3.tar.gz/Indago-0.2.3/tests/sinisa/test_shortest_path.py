# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 14:53:52 2018

@author: Stefan
"""


import sys, os
#sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append('..')
import pyswarms as ps
import time
import numpy as np
import matplotlib.pyplot as plt
from indago.benchmarks import ShortestPath
from indago.legacy_pso import LegacyPSO
from scipy.interpolate import interp1d


nd = 100
sp = ShortestPath('case_3.1')
pso = LegacyPSO()
pso.objective = sp.penalty
pso.dimensions = nd
pso.swarm_size = nd
pso.lb = np.ones(nd) * -20
pso.ub = np.ones(nd) * 20
pso.iterations = 100 * nd

# Vanilla
pso.method = 'Vanilla'
pso.params['inertia'] = 0.72
pso.params['cognitive_rate'] = 1.0
pso.params['social_rate'] = 1.0

## TVAC
#pso.method = 'TVAC'
#pso.params['inertia'] = 'LDIW'

# Anakatabatic
method = 'anakatabatic interpolation #1'
w_start = [-1.02261132, -2.00000000, 1.57508999, 0.26801405, 0.30031952]
w_stop = [0.7123562, -1.20676283, -0.46124989, 0.33481816, -0.18299209]
#splinetype = 'cubic'
splinetype = 'linear'
#method = 'anakatabatic interpolated regression #5' # "fish"
#w_start = [1.36340883, 0.42189353, 0.75251688, 0.66094695, -1.54714817]
#w_stop = [-0.70413858, 0.38642251, 0.03580773, -0.06470317, 1.77616954]
#splinetype = 'cubic'
Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
f_start = interp1d(Th, w_start, kind=splinetype)
f_stop = interp1d(Th, w_stop, kind=splinetype)
pso.params['inertia'] = 'anakatabatic'
pso.params['akb_fun_start'] = f_start
pso.params['akb_fun_stop'] = f_stop

fig = plt.figure()
ax = fig.gca()

print()
print(pso.method)
try: print(method, splinetype)
except: pass

runs = 20
start = time.time()
F, X = np.zeros(runs), np.zeros([runs, nd])
for r in range(runs):
    F[r], X[r, :] = pso.run()
    print('Run %3d f: %10.3f' % (r + 1, F[r]))
    pso.results.plot_convergence(ax)
end = time.time()

print('Elapsed time: %.2f s' % (end - start))
print('Indago best fitness: %.3e' % np.min(F))
print('Indago median fitness: %.3e' % np.median(F))
print()

plt.figure()
ax = plt.gca()
sp.draw_obstacles(ax)
for r in range(runs):
    sp.draw_path(X[r, :], ax, 'Run %d' % (r + 1))

plt.figure()
plt.title('Best path')
ax = plt.gca()
best = np.argmin(F)
sp.draw_path(X[best, :], ax)
sp.draw_obstacles(ax)

# Pyswarms
# pso.params['inertia'] = 0.72
# options = {'c1': pso.params['cognitive_rate'],
#            'c2': pso.params['social_rate'],
#            'w': pso.params['inertia']}

# PS = np.zeros(runs)
# for r in range(runs):
#     # Call instance of PSO with bounds argument
#     optimizer = ps.single.GlobalBestPSO(n_particles=pso.swarm_size,
#                                         dimensions=nd,
#                                         options=options,
#                                         bounds=(pso.lb, pso.ub))
#     def fun(x):
#         n_particles = x.shape[0]
#         j = [sp.penalty(x[i]) for i in range(n_particles)]
#         return np.array(j)

#     # Perform optimization
#     cost, pos = optimizer.optimize(fun, print_step=100,
#                                    iters=pso.iterations, verbose=3)
#     cost, pos = optimizer.optimize(fun, print_step=100,
#                                    iters=pso.iterations, verbose=0)
#     PS[r] = cost


# print()
# print('Pyswarms best   fitness:  %.3e' % np.min(PS))
# print('Pyswarms median fitness:  %.3e' % np.median(PS))
# print()


"""
*************************
shortest_path test results: 20d, 20 runs
*************************

Vanilla 
Indago median fitness: 1.922e+02

Vanilla akb int_reg_5_cubic
Indago median fitness: 1.922e+02

Vanilla akb int_1_cubic
Indago median fitness: 1.923e+02

Vanila akb int_1_linear
Indago median fitness: 1.924e+02

TVAC *** WINNER ***
Indago median fitness: 1.917e+02

TVAC akb int_reg_5_cubic
Indago median fitness: 1.918e+02

TVAC akb int_1_cubic
Indago median fitness: 1.922e+02

TVAC akb int_1_linear
Indago median fitness: 1.920e+02

FWA vanilla
Indago median fitness: 1.924

FWA rank
Indago median fitness: 1.920


*************************
shortest_path test results: 100d, 20 runs
*************************

Vanilla *** WINNER ***
Indago median fitness: 1.885e+02

Vanilla akb int_reg_5_cubic
Indago median fitness: 1.900e+02

Vanilla akb int_1_cubic
Indago median fitness: 1.917e+02

Vanilla akb int_1_linear
Indago median fitness: 1.917e+02

Vanila akb int_1_linear
Indago median fitness: 1.918e+02

TVAC
Indago median fitness: 1.928e+02

TVAC akb int_reg_5_cubic
Indago median fitness: 1.893e+02

TVAC akb int_1_cubic
Indago median fitness: 1.897e+02

TVAC akb int_1_linear
Indago median fitness: 1.888e+02
"""
