# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:58:25 2019
Anakatabatic metaopt
@author: Sinisa
"""

import sys
sys.path.append('..')

from indago import PSO
from indago.benchmarks import CEC2014

import numpy as np
import matplotlib.pyplot as plt


# metaoptimization parameters
metaD = 10 # len(w_start) + len(w_stop)
w_min = -2.0
w_max = 3.0
metaswarmsize = 3 * metaD
metamaxit = int(10 * metaD / metaswarmsize) # should be 1000 :(

# cec funs optimization parameters
cecD = 10
cecswarmsize = 3 * cecD
cecmaxit = int(1000 * cecD / cecswarmsize)
cecruns = 10 # should be 100
cec = CEC2014(cecD)


def metagoal(W):
    
    w_start = W[:5] # start = at first iteration
    w_stop = W[5:] # stop = at final iteration
    th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    
    pso = PSO()
    pso.method = 'TVAC'
        
    pso.dimensions = cecD
    pso.swarm_size = cecswarmsize
    pso.iterations = cecmaxit
    pso.lb = np.ones(cecD) * -100
    pso.ub = np.ones(cecD) * 100
    
    # do all funs with LDIW w
    pso.params['inertia'] = 'LDIW'
    FITavgbyf_tvac = []
    for f in cec.functions: # try skipping some, i.e. cec.functions[::2]
        #print('LDIW', f.__name__)
        pso.objective = f
        FITraw_tvac = np.zeros(cecruns) * np.nan
        for r in range(cecruns):
            FITraw_tvac[r], _ = pso.run()
        FITavgbyf_tvac.append(np.mean(FITraw_tvac))
    FITavgbyf_tvac = np.array(FITavgbyf_tvac)
    
    # do all funs with anakatabatic w
    pso.params['inertia'] = 'anakatabatic'
    pso.params['akb_fun_start'] = np.poly1d(np.polyfit(th, w_start, 3))
    pso.params['akb_fun_stop'] = np.poly1d(np.polyfit(th, w_stop, 3))    
    FITavgbyf_akb = []
    for f in cec.functions: # try skipping some, i.e. cec.functions[::2]
        #print('anakatabatic', f.__name__)
        pso.objective = f
        FITraw_akb = np.zeros(cecruns) * np.nan
        for r in range(cecruns):
            FITraw_akb[r], _ = pso.run()
        FITavgbyf_akb.append(np.mean(FITraw_akb))
    FITavgbyf_akb = np.array(FITavgbyf_akb)
    
    score = np.average(np.log10(FITavgbyf_akb/FITavgbyf_tvac))
    print(f'metagoal evaluation (score) [oom]: {-score:6.3f}')
    return score


if __name__ == '__main__':
    
    metaopt = PSO()
    metaopt.evaluation_function = metagoal
    metaopt.method = 'TVAC'
    metaopt.params['inertia'] = 'LDIW'
    
    # pso.method = 'Vanilla'
    # pso.params['inertia'] = 0.65
    # pso.params['cognitive_rate']  = 1.0
    # pso.params['social_rate']  = 1.0
    
    metaopt.dimensions = metaD
    metaopt.swarm_size = metaswarmsize
    metaopt.lb = np.ones(metaD) * w_min
    metaopt.ub = np.ones(metaD) * w_max
    metaopt.iterations = metamaxit
    
    print('starting metaoptimization...')
    metascore, W = metaopt.run()
    print('ended metaoptimization.')
    
    w_start = W[:5] # start = at first iteration
    w_stop = W[5:] # stop = at final iteration
    print(f'w_start: {w_start}')
    print(f'w_stop: {w_stop}')
    print(f'metascore [oom]: {-metascore}')
    
    # plot
    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    a_start = np.polyfit(Th, w_start, 3)
    a_stop = np.polyfit(Th, w_stop, 3)
    THplot = np.linspace(np.pi/4, 5*np.pi/4)
    plt.plot(THplot, np.poly1d(a_start)(THplot), 'g', label='akb_fun_start')
    plt.plot(THplot, np.poly1d(a_stop)(THplot), 'r', label='akb_fun_stop')
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
    