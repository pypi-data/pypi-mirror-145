# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:58:25 2019
Anakatabatic metaopt3
@author: Sinisa
"""

import sys
sys.path.append('..\..')
import numpy as np
import matplotlib.pyplot as plt
from indago import PSO, DE
from indago.benchmarks import CEC2014
from multiprocessing import Pool
from scipy.interpolate import interp1d


# metaoptimization parameters
metaD = 10 # len(w_start) + len(w_stop)
w_min = -1.5
w_max = 1.5
metamaxit = 5 * metaD
metastallit = 2 * metaD

# cec funs optimization parameters
cecD = 10
cecmaxit = 100 * cecD
cecruns = 480 # 1000+ would be safe
CEC = CEC2014(cecD)
CECfun = CEC.F10

# parallel execution
NP = 12 # number of parallel processes 
assert cecruns % NP == 0


def computecec(pso, runs):
    np.random.seed()    
    FITrun = np.zeros(runs) * np.nan
    for r in range(runs):
        FITrun[r] = pso.optimize().f
    return FITrun

    
def metagoaleval(f_start, f_stop, pool, setup, computecec=computecec):
        
    D, maxit, runs, pso = setup
        
    pso.dimensions = D
    pso.iterations = maxit
    pso.lb = -100
    pso.ub = 100
    
    pso.eval_fail_behavior = 'ignore'
    
    # do the optimization with anakatabatic w
    pso.params['inertia'] = 'anakatabatic'
    pso.params['akb_fun_start'] = f_start
    pso.params['akb_fun_stop'] = f_stop
    FITall = pool.starmap(computecec,
                [(pso, cecruns//NP) for _ in range(NP)])
    FITall = np.array(FITall).flatten()
    
    score = np.median(np.log10(FITall))
    # print(f'metagoal evaluation (median oom): {score:6.3f}', flush=True)
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
    pso.evaluation_function = CECfun
    
    #pso.method = 'TVAC'
    pso.method = 'Vanilla'
    
    """
    ## strong test
    pso.dimensions = cecD
    pso.iterations = cecmaxit
    pso.lb = -100 #np.ones(cecD) * -100
    pso.ub = 100 # np.ones(cecD) * 100
    
    # ## F1
    # w_start = [-0.64975824, 0.14230817, -0.75271859, 1.05640908, 0.57726151]
    # w_stop = [-0.15503759, 0.28587953, 1.12341945, 0.72290624, 0.68793692]
    
    # th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    # pso.params['inertia'] = 'anakatabatic'
    # pso.params['akb_fun_start'] = interp1d(th, w_start, kind='linear')
    # pso.params['akb_fun_stop'] = interp1d(th, w_stop, kind='linear')
    
    FITall = pool.starmap(computecec,
                [(pso, 960//NP) for _ in range(NP)])
    FITall = np.array(FITall).flatten()
    score = np.median(np.log10(FITall))
    pool.close()
    print(f'strong score (median oom): {score:6.3f}')
    """   
    
    setup = [cecD, cecmaxit, cecruns, pso]
    metaopt = DE()
    metaopt.method = 'LSHADE'
    metaopt.params['initial_population_size'] = 10 * metaD
    metaopt.evaluation_function = lambda W: metagoal(W, pool, setup)
    metaopt.dimensions = metaD
    metaopt.lb = np.ones(metaD) * w_min
    metaopt.ub = np.ones(metaD) * w_max
    metaopt.iterations = metamaxit
    metaopt.maximum_stalled_iterations = metastallit
    metaopt.monitoring = 'dashboard'
    
    print(f'metaoptimizing {pso.method}-PSO...')
    RESULT = metaopt.optimize()
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
    plt.show()
    
    #"""
