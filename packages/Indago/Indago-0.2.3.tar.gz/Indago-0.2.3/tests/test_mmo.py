# -*- coding: utf-8 -*-
"""
Tutorial code given in the readme.md
"""

# need this for local (non-pip) install only
import sys
sys.path.append('..')

import numpy as np

from indago.benchmarks import CEC2014


if __name__ == '__main__': 

    ### Particle Swarm Algorithm
    
    from indago import PSO
    pso = PSO()
    pso.method = 'Vanilla' # we will use standard PSO, the other available option is 'TVAC' [1]
    pso.dimensions = 10 # number of variables in the design vector (x)
    pso.params['swarm_size'] = pso.dimensions # default
    pso.iterations = 10000 * pso.dimensions # a big number, so maximum evaluations would be hit first
    pso.maximum_evaluations = 1000 * pso.dimensions
        
    ### Fireworks Algorithm
    
    from indago import FWA
    fwa = FWA()
    fwa.method = 'Vanilla'
    fwa.dimensions = pso.dimensions
    fwa.iterations = pso.iterations
    fwa.maximum_evaluations = pso.maximum_evaluations
    
    ### Differential Evolution
    
    from indago import DE
    de = DE()
    de.method = 'SHADE'
    de.dimensions = pso.dimensions
    de.iterations = pso.iterations
    de.maximum_evaluations = pso.maximum_evaluations
       
    ### Mutualistic Multi-Optimization
    
    from indago import MMO
    mmo1 = MMO() 
    mmo1.method = {'PSO': 'Vanilla', 
                   'FWA': 'Vanilla'}
    mmo1.dimensions = pso.dimensions
    mmo1.params['swarm_size'] = pso.params['swarm_size']
    mmo1.iterations = pso.iterations
    mmo1.maximum_evaluations = pso.maximum_evaluations
    
    mmo2 = MMO() 
    mmo2.method = {'PSO': 'Vanilla', 
                   'DE': 'SHADE'}
    mmo2.dimensions = pso.dimensions
    mmo2.params['swarm_size'] = pso.params['swarm_size']
    mmo2.params['initial_population_size'] = 100
    mmo2.iterations = pso.iterations
    mmo2.maximum_evaluations = pso.maximum_evaluations
    
    mmo3 = MMO() 
    mmo3.method = {'FWA': 'Vanilla', 
                   'DE': 'SHADE'}
    mmo3.dimensions = pso.dimensions
    mmo3.params['initial_population_size'] = 100
    mmo3.iterations = pso.iterations
    mmo3.maximum_evaluations = pso.maximum_evaluations
    
    mmo4 = MMO() 
    mmo4.method = {'PSO': 'Vanilla', 
                   'DE': 'SHADE',
                   'FWA': 'Vanilla'}
    mmo4.dimensions = pso.dimensions
    mmo4.params['swarm_size'] = pso.params['swarm_size'] // 2 # half-swarm
    mmo4.params['initial_population_size'] = 50
    mmo4.iterations = pso.iterations
    mmo4.maximum_evaluations = pso.maximum_evaluations
       
    ### TEST
    
    for optimizer in [de, mmo1, mmo2, mmo3, mmo4]:
    
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
            #print(f'run #{r}: {np.mean(np.log10(np.array(test_results)))}')
            test_results_all.append(np.mean(np.log10(np.array(test_results))))
        
        print(f'median score on {runs} runs: {np.median(np.array(test_results_all))}')


"""
SCORES:
PSO 2.02
FWA 2.33
DE 2.01
MMO PSO+FWA 1.96
MMO PSO+DE 1.53
MMO FWA+DE 1.54
MMO PSO+FWA+DE 1.33
"""
