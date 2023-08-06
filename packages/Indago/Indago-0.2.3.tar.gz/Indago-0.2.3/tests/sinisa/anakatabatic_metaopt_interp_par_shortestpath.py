# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:58:25 2019
Anakatabatic metaopt
@author: Sinisa
"""

import sys
sys.path.append('..')
import numpy as np
import matplotlib.pyplot as plt
from indago import PSO
from indago.benchmarks import ShortestPath
from multiprocessing import Pool
from scipy.interpolate import interp1d


# metaoptimization parameters
metaD = 10 # len(w_start) + len(w_stop)
w_min = -2.0
w_max = 2.0
metaswarmsize = 2 * metaD
metamaxit = int(100 * metaD / metaswarmsize) # should be 1000*... :(

# shortest path optimization parameters
CASE = 'case_3.1'
SP = ShortestPath(CASE)
spD = 20
spswarmsize = 3 * spD
spmaxit = int(1000 * spD / spswarmsize)
spruns = 100 # should be 100+

# parallel execution
NP = 5 # number of parallel processes
assert spruns % NP == 0
runsperproc = spruns//NP


def computesp(pso, runs):
    FITavg = []
    FITraw = np.zeros(runs) * np.nan
    for r in range(runs):
        FITraw[r] = pso.run().f
    FITavg.append(np.mean(FITraw))
    return np.array(FITavg)

    
def metagoaleval(f_start, f_stop, pool, pso, computesp=computesp):
        
    #maxit, runs, pso = setup
    
    if pso.method == 'Vanilla':
        pso.params['cognitive_rate'] = 1.0
        pso.params['social_rate'] = 1.0
    
#    # do all runs with default w
#    if pso.method == 'TVAC':
#        pso.params['inertia'] = 'LDIW'
#    else:
#        pso.params['inertia'] = 0.72
#    FITavg_all_base = np.array(pool.starmap(computesp,
#                        [(pso, runsperproc) for i in range(NP)])).ravel()
    
    # do all runs with anakatabatic w
    pso.params['inertia'] = 'anakatabatic'
    pso.params['akb_fun_start'] = f_start
    pso.params['akb_fun_stop'] = f_stop
    FITavg_all_akb = np.array(pool.starmap(computesp,
                        [(pso, runsperproc) for i in range(NP)])).ravel()
    
    score = np.mean(FITavg_all_akb)# - np.mean(FITavg_all_base)

#    print(f'metagoal evaluation (more is better): {-score:6.3f}')
    print(f'metagoal evaluation (less is better): {score:6.3f}')
    return score


def metagoal(W, pool, setup, computesp=computesp):
    
    w_start = W[:5] # start = at first iteration
    w_stop = W[5:] # stop = at final iteration
    th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    f_start = interp1d(th, w_start, kind='linear')
    f_stop = interp1d(th, w_stop, kind='linear')
    
    return metagoaleval(f_start, f_stop, pool, pso, computesp=computesp)


if __name__ == '__main__':
          
    pso = PSO()
    
    #pso.method = 'TVAC'
    pso.method = 'Vanilla'
    
    pso.dimensions = spD
    pso.swarm_size = spswarmsize
    pso.iterations = spmaxit
    pso.lb = np.ones(spD) * -20
    pso.ub = np.ones(spD) * 20
    pso.objectives = 1
    pso.objective_labels = ['Length']
    pso.constraints = 1
    pso.constraint_labels = ['Obstacles intersection length']
    pso.evaluation_function = SP.obj_cnstr
    #setup = [spmaxit, spruns, pso]
    
    pool = Pool(NP)
    
    metaopt = PSO()
    metaopt.evaluation_function = lambda W: metagoal(W, pool, pso)
    
    metaopt.method = 'TVAC'
    metaopt.params['inertia'] = 'LDIW'
    
    metaopt.dimensions = metaD
    metaopt.swarm_size = metaswarmsize
    metaopt.lb = np.ones(metaD) * w_min
    metaopt.ub = np.ones(metaD) * w_max
    metaopt.iterations = metamaxit
    
    print('starting metaoptimization...')
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
    