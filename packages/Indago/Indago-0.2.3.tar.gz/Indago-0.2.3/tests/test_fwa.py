# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 14:53:52 2018

@author: Stefan
"""


import sys
sys.path.append('..')
import time
import numpy as np
import matplotlib.pyplot as plt
from indago.benchmarks import ShortestPath
from indago import FWA

if __name__ == '__main__':
        
    # FWA instance
    fw = FWA()
    runs = 10  # Number of runs
    
    # Define optimization problem
    sp = ShortestPath('case_3.1')
    fw.evaluation_function = sp.obj_cnstr
    fw.number_of_processes = 4
    fw.dimensions = 50
    fw.lb = np.ones(fw.dimensions) * -20
    fw.ub = np.ones(fw.dimensions) *  20
    fw.objectives = 1
    fw.objective_labels = ['Length']
    fw.constraints = 1
    fw.constraint_labels = ['Obstacles intersection length']
    
    fw.iterations = 500
    fw.params['n'] = 20
    fw.params['m1'] = 10
    fw.params['m2'] = 10
    
    print('\nRANK')
    OPT1 = []
    fw.method = 'Rank'
    for run in range(runs):
        fw.tic()
        opt = fw.optimize()
        OPT1.append(opt)
        fw.toc(f'Run {run + 1} fitness: {opt.f}')
    print(f'Average fitness: {np.average([opt.f for opt in OPT1])}')
    print(f'Median fitness: {np.median([opt.f for opt in OPT1])}')
    
    print('\nVANILLA')
    OPT2 = []
    fw.method = 'Vanilla'
    fw.evaluation_function = sp.penalty
    fw.constraints = 0
    fw.constraint_labels = None
    start = time.time()
    for run in range(runs):
        fw.tic()
        opt = fw.optimize()
        OPT2.append(opt)
        fw.toc(f'Run {run + 1} fitness: {opt.f}')
    end = time.time()
    print(f'Average fitness: {np.average([opt.f for opt in OPT2])}')
    print(f'Median fitness: {np.median([opt.f for opt in OPT2])}')
    best = np.min(OPT1 + OPT2)
    
    print()
    print('Total elapsed time: %.2f s' % (end - start))
    print('Run average time: %.2f s' % ((end - start) / runs))
    #print('Best result:')
    #print(best)
    print()
    #fw.results.plot_convergence()
    
    plt.figure()
    plt.title('FWA')
    ax = plt.gca()
    sp.draw_obstacles(ax)
    for run, opt in enumerate(OPT1):
        sp.draw_path(opt.X, ax, f'(Rank) Run {run + 1}, f:{opt.f:.2f}', c='b', a=0.1)
    for run, opt in enumerate(OPT2):
        sp.draw_path(opt.X, ax, f'(Vanilla) Run {run + 1}, f:{opt.f:.2f}', c='r', a=0.1)
    sp.draw_path(best.X, ax, f'Best, f:{opt.f:.2f}', c='k', a=1)
    #plt.legend()
    print(f'RANK vs VANILLA: {np.average([opt.f for opt in OPT1])} vs {np.average([opt.f for opt in OPT2])}')
    plt.show()
