# -*- coding: utf-8 -*-
"""
Tutorial code given in the readme.md
"""

# need this for local (non-pip) install only
import sys
sys.path.append('..')

import time
import numpy as np

from indago.benchmarks import CEC2014


if __name__ == '__main__': 

    ### Particle Swarm Algorithm
    
    from indago import PSO
    pso = PSO()
    pso.method = 'Vanilla' # we will use standard PSO, the other available option is 'TVAC' [1]
    pso.dimensions = 10 # number of variables in the design vector (x)
    pso.iterations = 10000 * pso.dimensions # a big number, so maximum evaluations would be hit first
    pso.maximum_evaluations = 1000 * pso.dimensions
    pso.monitoring = 'none'
        
    ### Fireworks Algorithm
    
    from indago import FWA
    fwa = FWA()
    fwa.method = 'Vanilla'
    fwa.dimensions = pso.dimensions
    fwa.iterations = pso.iterations
    fwa.maximum_evaluations = pso.maximum_evaluations
    fwa.monitoring = pso.monitoring
       
    ### Differential Evolution
    
    from indago import DE
    shade = DE() 
    shade.method = 'SHADE'
    shade.dimensions = pso.dimensions
    shade.iterations = pso.iterations
    shade.maximum_evaluations = pso.maximum_evaluations
    shade.monitoring = pso.monitoring
    lshade = DE() 
    lshade.method = 'LSHADE'
    lshade.dimensions = pso.dimensions
    lshade.iterations = pso.iterations
    lshade.maximum_evaluations = pso.maximum_evaluations
    lshade.monitoring = pso.monitoring
       
    ### TEST
    
    for optimizer in [shade, lshade]:
    
        test = CEC2014(optimizer.dimensions)
        optimizer.lb = np.ones(optimizer.dimensions) * -100
        optimizer.ub = np.ones(optimizer.dimensions) * 100
        runs = 100
        optimizer.number_of_processes = 'maximum'
        
        test_results_all = []
        for r in range(runs):
            test_results = []
            for f in test.functions:
                optimizer.evaluation_function = f
                test_results.append(optimizer.optimize().f)
            print(f'run #{r}: {np.mean(np.log10(np.array(test_results)))}')
            test_results_all.append(np.mean(np.log10(np.array(test_results))))
        
        print(f'median score on {runs} runs: {np.median(np.array(test_results_all))}')


"""
SCORES:
PSO 2.02
FWA 2.33
SHADE 1.85
LSHADE 0.95
"""
