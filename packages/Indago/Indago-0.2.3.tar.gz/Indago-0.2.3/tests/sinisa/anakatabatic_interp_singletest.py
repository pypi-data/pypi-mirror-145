# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:58:25 2019
Anakatabatic singletest
@author: Sinisa
"""

import sys
sys.path.append('..')
from indago.benchmarks import CEC2014
from indago import PSO
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time
from scipy.interpolate import interp1d


# cec funs optimization parameters
cecD = 10
cecswarmsize = 3 * cecD
cecmaxit = int(1000 * cecD / cecswarmsize)
cecruns = 1000 # should be 100+
CEC = CEC2014(cecD)

# parallel execution
NP = 8 # number of parallel processes
assert cecruns % NP == 0

# testing variant
VARIANT = 'Vanilla'
#VARIANT = 'TVAC'

##############################################################################

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
    
    # do all funs with default w
    if pso.method == 'TVAC':
        pso.params['inertia'] = 'LDIW'
    else:
        pso.params['inertia'] = 0.72
    FITavgbyf_base = np.mean(pool.starmap(computecec,
                [(cec, pso, cecruns//NP) for _ in range(NP)]), axis=0)
    
    # do all funs with anakatabatic w
    pso.params['inertia'] = 'anakatabatic'
    pso.params['akb_fun_start'] = f_start
    pso.params['akb_fun_stop'] = f_stop
    FITavgbyf_akb = np.mean(pool.starmap(computecec,
                [(cec, pso, cecruns//NP) for _ in range(NP)]), axis=0)
    
    # COMPUTE LOG-SCORE
    score = np.mean(np.log10(FITavgbyf_akb/FITavgbyf_base))
    print(f'omega [oom]: {-score:6.3f}')
        
    # COMPUTE ALPHA-SCORE
    score = np.mean(2 * (FITavgbyf_base - FITavgbyf_akb)/(FITavgbyf_base + FITavgbyf_akb))
    print(f'alpha [-]: {score:6.3f}')   

##############################################################################


### Anakatabatic Vanilla
    
#model = 'akb vanilla #3a'
#modelaka = '???'
## obtained by Vanilla, languid, metaopt eval = 80D, cecit = 500
## metaopt score = ???
#w_start = [-0.86, 0.24, -1.10, 0.75, 0.72]
#w_stop = [-0.81, -0.35, -0.26, 0.64, 0.60]
#splinetype = 'linear'
## alpha: 0.130, 0.190, 0.085
## omega [oom]: 0.058, 0.086, 0.038


### Anakatabatic TVAC

#model = 'akb tvac #1'
#modelaka = 'RightwardPeaks'
## obtained by Vanilla, metaopt eval = 100D, cecit = 500
## metaopt score = 1.93
##w_start = [-1.79457153, -0.33409362, 2., -0.67365566, 1.29661024]
##w_stop = [-0.9120458, -0.87835946, -0.83647823, 0.67106473, -0.36185384]
#w_start = [-1.79, -0.33, 2.00, -0.67, 1.30]
#w_stop = [-0.91, -0.88, -0.84, 0.67, -0.36]
#splinetype = 'linear'
## alpha: 0.516, 0.701, 0.739
## omega [oom]: 0.280, 0.503, 0.589


### LPSO
    
#model = 'languid' # the original LPSO
#def f_start(Th):
#    w = 0.72 * np.ones_like(Th)
#    for i, th in enumerate(Th):
#        if th < 4*np.pi/4: 
#            w[i] = 0
#    return w
#f_stop = f_start
#splinetype = None
## Vanilla alpha: 0.174, 0.228, 0.034
## Vanilla omega [oom]: 0.083, 0.105, 0.009
## TVAC alpha: 0.190, 0.553, 0.594
## TVAC omega [oom]: 0.088, 0.330, 0.400

#model = 'languid +0.05'
#def f_start(Th):
#    w = (0.72 + 0.05) * np.ones_like(Th)
#    for i, th in enumerate(Th):
#        if th < 4*np.pi/4: 
#            w[i] = 0
#    return w
#f_stop = f_start
#splinetype = None
## Vanilla alpha: 0.172, 0.221, -0.01
## Vanilla omega [oom]: 0.080, 0.101, -0.03
## TVAC alpha: 0.046, 0.402, 0.247
## TVAC omega [oom]: 0.020, 0.230, 0.421


""" MAIN STUFF """

try: f_start    # if akb funs do not exist...
except:         # ...create w-defined akb interpolation funs
    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    f_start = interp1d(Th, w_start, kind=splinetype)
    f_stop = interp1d(Th, w_stop, kind=splinetype)


if __name__ == '__main__': # multiprocessing needs this maybe

    print(f'variant: {VARIANT}')
    print(f'model: {model}')
    print(f'spline: {splinetype}')  
    print(f'D = {cecD}; cecruns = {cecruns}')
    pool = Pool(NP)
    pso = PSO()
    pso.method = VARIANT
    setup = [cecD, cecswarmsize, cecmaxit, cecruns, CEC, pso]
    startt = time.time()
    score = metagoaleval(f_start, f_stop, pool, setup, computecec=computecec)
    pool.close()
    stopt = time.time()
    print(f'elapsed time [hr]: {(stopt-startt)/3600:.3f}') 
    
    # plot
    THplot = np.linspace(np.pi/4, 5*np.pi/4, 200)
    plt.plot(THplot, f_start(THplot), 'g', label='akb_fun_start')
    plt.plot(THplot, f_stop(THplot), 'r', label='akb_fun_stop')
    plt.axhline(color='magenta', ls=':')
    plt.axvline(2*np.pi/4, color='magenta', ls=':')
    plt.axvline(4*np.pi/4, color='magenta', ls=':')
    plt.axis([np.pi/4, 5*np.pi/4, -2, 3])
    plt.xlabel(r'$\theta_i$')
    plt.ylabel('$w_i$')
    plt.title(f'{model}, {splinetype}')
    plt.legend()
    plt.show()

