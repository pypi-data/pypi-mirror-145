#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: stefan
"""

import sys
sys.path.append('..')
from indago import PSO
import numpy as np


if __name__ == '__main__':


    def f_strarg(X, s=None):
        if s is not None:
            pass
            #print(s)
        return np.sum(X**2)

    CPUS = [1, 1, 6, 6]
    UNIQ = [True, False, True, False]

    for conf in range(4):
        pso = PSO()
        pso.number_of_processes = CPUS[conf]
        pso.evaluation_function = f_strarg

        # Passing unique string to evaluation function as additional argument
        # It slows down the optimization
        pso.forward_unique_str = UNIQ[conf]

        pso.dimensions = 2000
        pso.lb = np.ones(pso.dimensions) * -100
        pso.ub = np.ones(pso.dimensions) *  100
        pso.swarm_size = 1000
        pso.iterations = 20
        pso.method = 'Vanilla'
        pso.params['inertia'] = 0.65
        pso.params['cognitive_rate'] = 1.0
        pso.params['social_rate'] = 1.0

        pso.tic()
        pso.title(f'PSO (cpus={CPUS[conf]}, fw_uniqe_str:{UNIQ[conf]})')
        opt = pso.optimize(seed=10)
        pso.toc(msg='PSO elapsed time:')
        pso.log(f'Candidate 0 fitness: {opt.f}')