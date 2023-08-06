# -*- coding: utf-8 -*-
"""
test stall criterion
"""

# need this for local (non-pip) install only
import sys
sys.path.append('..')

import numpy as np

def F(X):
    return 1


if __name__ == '__main__': 

    ### Particle Swarm Algorithm
    
    from indago import PSO, EFO, DE, BA, FWA, MRFO, SSA, MMO
    opt = MRFO()
    opt.dimensions = 10
    opt.iterations = 100000
    opt.maximum_evaluations = 1000 * opt.dimensions 
    opt.lb = np.ones(opt.dimensions) * -5
    opt.ub = np.ones(opt.dimensions) * 5    
    opt.evaluation_function = F
    opt.monitoring = 'basic'   
    opt.number_of_processes = 1
    
    opt.maximum_stalled_iterations = 10
    opt.maximum_stalled_evaluations = 40
    
    opt.optimize()
