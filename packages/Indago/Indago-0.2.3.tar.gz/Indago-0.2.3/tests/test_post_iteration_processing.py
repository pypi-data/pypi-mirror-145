#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:47:13 2020

@author: stefan
"""

import sys
sys.path.append('..')
from indago import PSO, FWA, SSA, DE, BA, EFO, MRFO, NelderMead
import numpy as np
import time
import os
import shutil

test_dir = 'test_post_iteration_processing_directory'
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
os.mkdir(test_dir)

def evaluation(X, unique_str):

    # Create directory for calculation
    os.mkdir(f'{test_dir}/{unique_str}')
    time.sleep(0.02)

    o, c1, c2 = np.sum(X**2), X[0] - X[1] + 35, np.sum(np.cos(X) + 0.2)

    # Save stuff to the directory
    np.savetxt(f'{test_dir}/{unique_str}/in_out.txt', np.hstack((X, [o, c1, c2])))

    return o, c1, c2


def post_iteration_processing(it, candidates, best):
    if candidates[0] <= best:
        # Keeping only overall best solution
        if os.path.exists(f'{test_dir}/best'):
            shutil.rmtree(f'{test_dir}/best')
        os.rename(f'{test_dir}/{candidates[0].unique_str}', f'{test_dir}/best')

        # Keeping best solution of each iteration (if it is the best overall)
        # os.rename(f'{test_dir}/{candidates[0].unique_str}', f'{test_dir}/best_it{it}')

        # Log keeps track of new best solutions in each iteration
        with open(f'{test_dir}/log.txt', 'a') as log:
            X = ', '.join(f'{x:13.6e}' for x in candidates[0].X)
            O = ', '.join(f'{o:13.6e}' for o in candidates[0].O)
            C = ', '.join(f'{c:13.6e}' for c in candidates[0].C)
            log.write(f'{it:6d} X:[{X}], O:[{O}], C:[{C}], fitness:{candidates[0].f:13.6e}\n')

        candidates = np.delete(candidates, 0)  # Remove the bes from candidates (since its directory is already renamed)

    # Remove candidates' directories
    for c in candidates:
        shutil.rmtree(f'{test_dir}/{c.unique_str}')
    return


for optimizer in [PSO(),
                  FWA(),
                  SSA(),
                  # DE(),  # Does not support constraints
                  BA(),
                  # EFO(),  # Doe not support parallel evaluation
                  MRFO(),
                  NelderMead()
                  ]:

    optimizer.objectives = 1
    optimizer.constraints = 2
    optimizer.evaluation_function = evaluation
    optimizer.forward_unique_str = True
    optimizer.post_iteration_processing = post_iteration_processing
    optimizer.number_of_processes = 'maximum'

    optimizer.dimensions = 10
    optimizer.lb = np.ones(optimizer.dimensions) * -20
    optimizer.ub = np.ones(optimizer.dimensions) * 20

    optimizer.iterations = 10
    optimizer.maximum_evaluations = 500
    optimizer.target_fitness = 1.3e-3
    optimizer.maximum_stalled_iterations = 100
    optimizer.maximum_stalled_evaluations = 1000

    optimizer.monitoring = 'dashboard'
    optimizer.optimize()
