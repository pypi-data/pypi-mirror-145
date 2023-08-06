# -*- coding: utf-8 -*-
"""
test eval_retry
"""

# need this for local (non-pip) install only
import sys
sys.path.append('..')

import numpy as np

def F(X):
    if np.logical_and(X > 1.95, X < 2.05).any():
        return np.nan
    else:
        return np.sum(X**2)


if __name__ == '__main__': 

    ### Particle Swarm Algorithm
    
    from indago import PSO, EFO, DE, BA, FWA, MRFO, SSA, MMO
    opt = PSO()
    # opt.method = 'Rank' # needed for FWA
    opt.dimensions = 10
    opt.iterations = 100000
    opt.maximum_evaluations = 1000 * opt.dimensions 
    opt.lb = np.ones(opt.dimensions) * -5
    opt.ub = np.ones(opt.dimensions) * 5    
    opt.evaluation_function = F
    opt.monitoring = 'basic'   
    opt.number_of_processes = 1
    
    opt.safe_evaluation = True
    opt.eval_fail_behavior = 'ignore'
    opt.eval_retry_attempts = 10
    opt.eval_retry_recede = 0.05
    
    runs = 5
    
    for r in range(runs):
        test_results = []
        test_results.append(opt.optimize().f)
