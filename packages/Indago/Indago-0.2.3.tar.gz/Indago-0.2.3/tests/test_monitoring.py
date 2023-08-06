#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:47:13 2020

@author: stefan
"""

import sys
sys.path.append('..')
from indago import PSO
from indago import NelderMead
import numpy as np
import time

def fun(X):
    time.sleep(0.02)
    return np.sum(X**2), X[0] - X[1] + 35, np.sum(np.cos(X) + 0.2)
seed = None


for optimizer in [PSO(),
                  NelderMead(),
                  ]:

    optimizer.objectives = 1
    optimizer.constraints = 2
    optimizer.evaluation_function = fun

    optimizer.dimensions = 10
    optimizer.lb = np.ones(optimizer.dimensions) * -20
    optimizer.ub = np.ones(optimizer.dimensions) * 20

    optimizer.iterations = 1000
    optimizer.maximum_evaluations = 500
    optimizer.target_fitness = 1.3e3
    optimizer.maximum_stalled_iterations = 100
    optimizer.maximum_stalled_evaluations = 1000

    for v in [#'none',
              #'basic',
              'dashboard',
              ]:
        #print(f'verbose={v}')
        optimizer.monitoring = v
        optimizer.optimize()
        #print('done\n')
