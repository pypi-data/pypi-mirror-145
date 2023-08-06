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
from anakatabatic_metaopt_par import computecec, metagoaleval, metagoal
import time
from scipy.interpolate import interp1d


# cec funs optimization parameters
cecD = 50
cecswarmsize = 3 * cecD
cecmaxit = int(1000 * cecD / cecswarmsize)
cecruns = 100 # should be 100+
CEC = CEC2014(cecD)

# parallel execution
NP = 5 # number of parallel processes (30 % NP == 0!)


#method = 'anakatabatic regression #1'
#w_start = [2.52027188, 1.95742872, 0.02398083, -0.20552353, 1.13543913]
#w_stop = [0.97532703, -0.10531391, 0.46338951, -0.03076367, 1.24613742]
## metascore [oom]: 0.246; 0.447; 0.528

#method = 'anakatabatic regression #2'
#w_start = [-0.3062106, -1.94511926, -0.91208767, 0.57248703, 0.59066022]
#w_stop = [-1.8205138, -1.04268421, 1.78988003, -1.10709181, -0.12374271]
## metascore [oom]: 0.256; 0.538; 0.616

#method = 'anakatabatic regression #3'
#w_start = [-1.34234829, 0.3855831, 1.89174111, -0.83194934, -0.99358996]
#w_stop = [-1.21179385, -0.71343247, -1.44039934, 1.20375851, 0.91364921]
## metascore [oom]: 0.155; 0.515; 0.556

#method = 'anakatabatic regression #4'
#w_start = [0.1485288, -0.86580328, -1.10192784, 0.90069412, -0.58975593]
#w_stop = [0.35188463, 0.86716563, 0.60135122, 0.45269879, -0.51015828]
## metascore [oom]: 0.214; 0.550; 0.639

method = 'anakatabatic regression #5'
w_start = [1.38115425, 0.35091185, 0.8589894, 0.58996527, -1.52940275]
w_stop = [-0.76440057, 0.62747048, -0.32576422, 0.1763448, 1.71590755]
# metascore [oom]: 0.245; 0.792; 0.679


# shared code for above w-defined akb regression funs
try:
    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    f_start = np.poly1d(np.polyfit(Th, w_start, 3))
    f_stop = np.poly1d(np.polyfit(Th, w_stop, 3))
except:
    pass

#method = 'left-flat regression #2'
#w_start = [-0.3062106, -1.94511926, -0.91208767, 0.57248703, 0.59066022]
#w_stop = [-1.8205138, -1.04268421, 1.78988003, -1.10709181, -0.12374271]
#th_cutoff = 7*np.pi/8
#omega_left = -0.8
#Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
#def f_start(theta):
#    OMEGA = []
#    for t in theta:
#        if t < th_cutoff: omega = omega_left
#        else: omega = np.poly1d(np.polyfit(Th, w_start, 3))(t)
#        #else: omega = interp1d(Th, w_start, kind='linear')(t)
#        OMEGA.append(omega)
#    return np.array(OMEGA)
#def f_stop(theta):
#    OMEGA = []
#    for t in theta:
#        if t < th_cutoff: omega = omega_left
#        else: omega = np.poly1d(np.polyfit(Th, w_stop, 3))(t)
#        #else: omega = interp1d(Th, w_stop, kind='linear')(t)
#        OMEGA.append(omega)
#    return np.array(OMEGA)
## metascore [oom]: 0.218(0.256); 0.570(0.538); ???(0.616) # omega_left=-0.8
    
#method = 'LPSO'
#def f_start(theta):
#    OMEGA = []
#    for t in theta:
#        if t < np.pi: omega = 0
#        else: omega = 0.85
#        OMEGA.append(omega)
#    return np.array(OMEGA)
#f_stop = f_start
## metascore [oom]: -0.378; -0.096; -0.222


if __name__ == '__main__': # multiprocessing needs this maybe

    print(f'method: {method}')
    print(f'D = {cecD}; cecruns = {cecruns}')
    pool = Pool(NP)
    pso = PSO()
    setup = [cecD, cecswarmsize, cecmaxit, cecruns, CEC, pso]
    startt = time.time()
    score = metagoaleval(f_start, f_stop, pool, setup, computecec=computecec)
    pool.close()
    stopt = time.time()
    print(f'metascore [oom]: {-score:.3f}')
    print(f'elapsed time [hr]: {(stopt-startt)/3600:.3f}') 
    
    # plot
    THplot = np.linspace(np.pi/4, 5*np.pi/4)
    plt.plot(THplot, f_start(THplot), 'g', label='akb_fun_start')
    plt.plot(THplot, f_stop(THplot), 'r', label='akb_fun_stop')
    #plt.plot(np.linspace(np.pi/4, 5*np.pi/4, 5), w_start, 'go')
    #plt.plot(np.linspace(np.pi/4, 5*np.pi/4, 5), w_stop, 'ro')
    plt.axhline(color='magenta', ls=':')
    plt.axvline(2*np.pi/4, color='magenta', ls=':')
    plt.axvline(4*np.pi/4, color='magenta', ls=':')
    plt.axis([np.pi/4, 5*np.pi/4, -2, 3])
    plt.xlabel(r'$\theta_i$')
    plt.ylabel('$w_i$')
    plt.legend()
    plt.title(method)
    plt.show()
