#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:47:13 2020

@author: stefan
"""

import sys
sys.path.append('..')
from indago import PSO
from indago.benchmarks import CEC2014, ShortestPath
import numpy as np
import matplotlib.pyplot as plt

dim = 20
n_discrete = 5
seed = 3
runs = 10

#fun = CEC2014(dim).F2
#sp = ShortestPath('case_2.1')
#fun = sp.obj_cnstr
def fun(X):
    return np.sum((X - np.arange(X.size) - 0.123)**2)
def round_fun(X):
    return fun(np.hstack([np.round(X[:n_discrete]), X[n_discrete:]]))
def quantum_fun(X):
    Xq = np.copy(X)
    R = np.remainder(X[:n_discrete], 1)
    for i in range(n_discrete): # Number of discrete variables
        if np.random.uniform(0, 1) > R[i]:
            Xq[i] = np.floor(X[i])
        else:
            Xq[i] = np.ceil(X[i])
    return fun(Xq)



pso1 = PSO()
pso2 = PSO()
pso3 = PSO()
pso1.evaluation_function = fun
pso2.evaluation_function = round_fun
pso3.evaluation_function = quantum_fun
LABELS = 'real round quantum'.split()

RESULTS = np.zeros([runs, 3])
for run in range(runs):
    print(f'Run {run + 1}')
    for imethod, (pso, label) in enumerate(zip([pso1, pso2, pso3], LABELS)):    
        
        pso.dimensions = dim
        pso.lb = np.ones(pso.dimensions) * -100
        pso.ub = np.ones(pso.dimensions) * 100
        # For shortest path:
        #pso.objectives = 1
        #pso.objective_labels = ['Length']
        #pso.constraints = 1
        #pso.constraint_labels = ['Obstacles intersection length']
        
        pso.swarm_size = 40
        pso.iterations = 500
        pso.method = 'Vanilla'
        pso.params['inertia'] = 0.65
        pso.params['cognitive_rate'] = 1.0
        pso.params['social_rate'] = 1.0
            
        #np.random.seed(seed)
        #pso.init()
        opt = pso.run()
        print(f'PSO_{label}: {opt.f}')
        #pso.results.plot_convergence()
        #plt.title(title)
        RESULTS[run, imethod] = opt.f


for i, label in enumerate(LABELS):
    print()
    print(f'PSO_{label}')
    print(f'f_avg: {np.average(RESULTS[:, i])}')
    print(f'f_median: {np.median(RESULTS[:, i])}')
    print(f'f_min: {np.min(RESULTS[:, i])}')
    


