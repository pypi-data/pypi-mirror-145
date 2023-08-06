# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:58:25 2019
Anakatabatic metaopt3
@author: Sinisa
"""

import sys
sys.path.append('..')
import numpy as np
import matplotlib.pyplot as plt
from indago import PSO
from indago.benchmarks import CEC2014
from multiprocessing import Pool
from scipy.interpolate import interp1d


# metaoptimization parameters
metaD = 10 # len(w_start) + len(w_stop)
w_min = -2.0
w_max = 2.0
metaswarmsize = 2 * metaD
metamaxit = int(100 * metaD / metaswarmsize) # should be 1000*... :(

# cec funs optimization parameters
cecD = 10
cecswarmsize = 3 * cecD
cecmaxit = int(1000 * cecD / cecswarmsize)
cecruns = 500 # should be 100+
CEC = CEC2014(cecD)

# parallel execution
NP = 5 # number of parallel processes 
assert cecruns % NP == 0


def computecec(cec, pso, runs):
    np.random.seed()
    FITavgbyf = []
    for f in cec.functions:
        pso.evaluation_function = f
        FITraw = np.zeros(runs) * np.nan
        for r in range(runs):
            FITraw[r] = pso.run().f
        FITavgbyf.append(np.mean(FITraw))
    return np.array(FITavgbyf)

    
def metagoaleval(f_start, f_stop, pool, setup, computecec=computecec):
        
    D, swarmsize, maxit, runs, cec, pso = setup
           
    if pso.method == 'Vanilla':
        pso.params['cognitive_rate'] = 1.0
        pso.params['social_rate'] = 1.0
        
    pso.dimensions = D
    pso.swarm_size = swarmsize
    pso.iterations = maxit
    pso.lb = np.ones(D) * -100
    pso.ub = np.ones(D) * 100
    
    # do all funs with anakatabatic w
    pso.params['inertia'] = 'anakatabatic'
    pso.params['akb_fun_start'] = f_start
    pso.params['akb_fun_stop'] = f_stop
    FITavgbyf_akb = np.mean(pool.starmap(computecec,
                [(cec, pso, cecruns//NP) for _ in range(NP)]), axis=0)
    
    #score = np.mean(np.log10(FITavgbyf_akb))
    #score = np.median(np.log10(FITavgbyf_akb))
    #score = np.mean(np.log10(np.sort(FITavgbyf_akb)[6:])) # mean of bottom 80%
    score = np.mean(np.log10(np.sort(FITavgbyf_akb)[3:-3])) # mean of middle 80%

    print(f'metagoal evaluation (average oom of f): {score:6.3f}', flush=True)
    return score


def metagoal(W, pool, setup, computecec=computecec):
    
    w_start = W[:5] # start = at first iteration
    w_stop = W[5:] # stop = at final iteration
    th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    f_start = interp1d(th, w_start, kind='linear')
    f_stop = interp1d(th, w_stop, kind='linear')
    
    return metagoaleval(f_start, f_stop, pool, setup, computecec=computecec)


if __name__ == '__main__':
          
    pool = Pool(NP)
    pso = PSO()
    
    #pso.method = 'TVAC'
    pso.method = 'Vanilla'
    
    setup = [cecD, cecswarmsize, cecmaxit, cecruns, CEC, pso]
    metaopt = PSO()
    metaopt.evaluation_function = lambda W: metagoal(W, pool, setup)
    
#    metaopt.method = 'TVAC'
#    metaopt.params['inertia'] = 'anakatabatic'
#    metaopt.params['akb_model'] = 'languid'
    
    metaopt.method = 'Vanilla'
    metaopt.params['inertia'] = 0.72
    metaopt.params['cognitive_rate'] = 1.0
    metaopt.params['social_rate'] = 1.0
    
    metaopt.dimensions = metaD
    metaopt.swarm_size = metaswarmsize
    metaopt.lb = np.ones(metaD) * w_min
    metaopt.ub = np.ones(metaD) * w_max
    metaopt.iterations = metamaxit
    
    print('starting metaoptimization...')
    print(f'metaoptimizing {pso.method}...')
    print(f'...by {metaopt.method}', flush=True)

    RESULT = metaopt.run()
    metascore, W = RESULT.f, RESULT.X
    print('ended metaoptimization.')
    pool.close()
    
    w_start = W[:5] # start = at first iteration
    w_stop = W[5:] # stop = at final iteration
    print(f'w_start: {w_start}')
    print(f'w_stop: {w_stop}')
    print(f'metascore [oom]: {-metascore}')
    
    # plot
    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    f_start = interp1d(Th, w_start, kind='linear')
    f_stop = interp1d(Th, w_stop, kind='linear')
    THplot = np.linspace(np.pi/4, 5*np.pi/4)
    plt.plot(THplot, f_start(THplot), 'g', label='akb_fun_start')
    plt.plot(THplot, f_stop(THplot), 'r', label='akb_fun_stop')
    plt.plot(np.linspace(np.pi/4, 5*np.pi/4, 5), w_start, 'go')
    plt.plot(np.linspace(np.pi/4, 5*np.pi/4, 5), w_stop, 'ro')
    plt.axhline(color='magenta', ls=':')
    plt.axvline(2*np.pi/4, color='magenta', ls=':')
    plt.axvline(4*np.pi/4, color='magenta', ls=':')
    plt.axis([np.pi/4, 5*np.pi/4, -2, 3])
    plt.xlabel(r'$\theta_i$')
    plt.ylabel('$w_i$')
    plt.legend()
    #plt.show()
    