#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 11:34:28 2021

@author: stefan
"""

import sys
sys.path.append('..')
from indago import PSO, FWA, SSA, DE
import numpy as np
import matplotlib.pyplot as plt

def f(X):
    return np.array([np.sum(X**2), 
                     12 + np.sum(np.sin(X)),
                     7 - np.average(X),
                     ])

for optimizer in [SSA(),
                  PSO(), 
                  FWA(),
                  # DE()
                  ]:

    optimizer.evaluation_function = f
    optimizer.number_of_processes = 1
    optimizer.dimensions = 20
    optimizer.lb = np.ones(optimizer.dimensions) * -10
    optimizer.ub = np.ones(optimizer.dimensions) *  10
    optimizer.objectives = 1
    optimizer.objective_labels = ['Objective']
    optimizer.constraints = 2
    optimizer.constraint_labels = ['Constraint 1', 'Constraint 2']
    optimizer.monitoring = 'dashboard'
    optimizer.maximum_evaluations = 40000
    
    opt = optimizer.optimize()
    optimizer.results.plot_convergence()
    plt.title(optimizer.__doc__)

plt.show()