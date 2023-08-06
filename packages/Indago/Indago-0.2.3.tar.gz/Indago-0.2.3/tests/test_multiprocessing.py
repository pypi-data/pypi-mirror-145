#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 15:47:13 2020

@author: stefan
"""

import sys
sys.path.append('..')
import indago
from indago import PSO
from indago import Optimizer
from indago.benchmarks import CEC2014, ShortestPath
import numpy as np

if __name__ == '__main__':
    print(f'Indago version: {indago.__version__}')

    seed = 1
    dim = 200
    # use cpus = 'maximum' for employing all available processors/cores
    cpus = 6
    #cpus = 'maximum'
    neval = 1000

    # cec = CEC2014(100)
    # def cec_sum(X):
    #     return np.sum([fun(X) for fun in cec.functions])
    sp = ShortestPath('case_6.1')

    optimizer1 = Optimizer()
    optimizer2 = Optimizer()
    optimizer2.number_of_processes = cpus

    for optimizer in [optimizer1, optimizer2]:
        #optimizer.evaluation_function = cec.F27
        #optimizer.evaluation_function = cec_sum
        optimizer.evaluation_function = sp.penalty
        optimizer.dimensions = dim
        optimizer.lb = np.ones(optimizer.dimensions) * -100
        optimizer.ub = np.ones(optimizer.dimensions) *  100

    optimizer1.tic()
    sol1 = optimizer1.multiprocess_evaluate_test(number_of_candidates=neval, seed=seed)
    optimizer1.toc(msg='Singleprocess Optimizer elapsed time:')
    print(f'Candidate 0 fitness: {sol1[0].f}')

    optimizer2.tic()
    sol2 = optimizer2.multiprocess_evaluate_test(number_of_candidates=neval, seed=seed)
    optimizer2.toc(msg='Multiprocess Optimizer elapsed time:')
    print(f'Candidate 0 fitness: {sol2[0].f}')




    pso1 = PSO()
    pso2 = PSO()
    pso2.number_of_processes = cpus

    for pso in [pso1, pso2]:
        #pso.evaluation_function = cec.F27
        #pso.evaluation_function = cec_sum
        #pso.evaluation_function = sp.penalty
        pso.evaluation_function = sp.obj_cnstr
        pso.constraints = 1

        pso.dimensions = dim
        pso.lb = np.ones(optimizer.dimensions) * -100
        pso.ub = np.ones(optimizer.dimensions) *  100
        pso.params['swarm_size'] = 400
        pso.iterations = 20
        pso.method = 'Vanilla'
        pso.params['inertia'] = 0.65
        pso.params['cognitive_rate'] = 1.0
        pso.params['social_rate'] = 1.0

    pso1.tic()
    sol1 = pso1.optimize(seed=seed)
    pso1.toc(msg='Singleprocess PSO elapsed time:')
    print(f'Candidate 0 fitness: {sol1.f}')

    pso2.tic()
    sol2 = pso2.optimize(seed=seed)
    pso2.toc(msg='Multiprocess PSO elapsed time:')
    print(f'Candidate 0 fitness: {sol2.f}')