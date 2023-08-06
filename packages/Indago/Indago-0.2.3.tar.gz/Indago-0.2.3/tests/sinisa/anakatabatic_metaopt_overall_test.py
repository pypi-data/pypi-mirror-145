# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:58:25 2019
Anakatabatic overall test
@author: Sinisa
"""

import sys
sys.path.append('..\..')
from indago.benchmarks import CEC2014
from indago import PSO
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Pool
import time
from scipy.interpolate import interp1d


# cec funs optimization parameters
cecD = 20
cecmaxit = 100 * cecD
cecruns = 960 #960 # 1000+ would be safe
CEC = CEC2014(cecD)

# parallel execution
NP = 12 # number of parallel processes
assert cecruns % NP == 0

# testing variant
VARIANT = 'Vanilla'
#VARIANT = 'TVAC'

##############################################################################

# load base results
FITmedbyf_base = np.loadtxt('anakatabatic_metaopt_overall_test_base_' + VARIANT + '.txt')
FITmedbyf_base = FITmedbyf_base[[10, 20, 50].index(cecD), :]
FITmedbyf_base[FITmedbyf_base == 0.0] = np.nan # avoiding divison by zero

def computecec(cec, pso, runs):
    np.random.seed()
    FITmedbyf = []
    for f in cec.functions:
        pso.evaluation_function = f
        FITraw = np.zeros(runs) * np.nan
        for r in range(runs):
            FITraw[r] = pso.optimize().f
        FITmedbyf.append(np.median(FITraw))
    return np.array(FITmedbyf)
    
def metagoaleval(akb_model, f_start, f_stop, pool, setup, computecec=computecec):
        
    D, maxit, runs, cec, pso = setup
        
    pso.dimensions = D
    pso.iterations = maxit
    pso.lb = -100
    pso.ub = 100
    pso.eval_fail_behavior = 'ignore'
    
    # do all funs with anakatabatic w
    pso.params['inertia'] = 'anakatabatic'
    if akb_model:
        pso.params['akb_model'] = akb_model
    else:
        pso.params['akb_fun_start'] = f_start
        pso.params['akb_fun_stop'] = f_stop
    FITmedbyf_akb = np.median(pool.starmap(computecec,
                        [(cec, pso, cecruns//NP) for _ in range(NP)]), axis=0)
        
    return FITmedbyf_akb

##############################################################################

### Anakatabatic Vanilla

# akb_model = 'Languid'
# # omega [oom]: 0.042, 0.139, 0.047
# # alpha: 0.092, 0.197, 0.106
# # FITmedbyf_akb = [1.00943987e+06, 2.87048798e+03, 8.14126739e+03, 8.72839091e+01, 2.06138085e+01, 2.04122224e+01, 8.62666247e-03, 8.25814807e+01, 9.12873599e+01, 5.84201980e+03, 7.72668835e+03, 1.39435127e+00, 3.85042470e-01, 2.98329988e-01, 2.52376613e+01, 1.93799971e+01, 9.54806276e+04, 7.35108939e+02, 1.59851482e+01, 6.21110722e+03, 1.03878498e+05, 4.27363740e+02, 3.44004501e+02, 2.78232382e+02, 2.27493413e+02, 2.00097677e+02, 9.23025441e+02, 1.45004473e+03, 3.82266051e+07, 1.22382033e+04]
# # FITmedbyf_akb = np.array(FITmedbyf_akb) 
    
# akb_model = 'FlyingStork'
# # omega [oom]: 0.043, 0.118, ???
# # alpha: 0.098, 0.188, ???

# akb_model = 'MessyTie'
# # omega [oom]: -0.173, ???, ???
# # alpha: -0.338, ???, ???

akb_model = 'TipsySpider'
# omega [oom]: 0.100, 0.041, ???
# alpha: 0.223, 0.098, ???

# # 'med'
# w_start = [-0.32, -0.06, -0.16, -0.63, 0.31]
# w_stop = [0.16, 0.21, 0.42, -0.55, 0.03]
# # omega [oom]: -0.690, ???, ???
# # alpha: -0.727, ???, ???

# # '2med'
# w_start = np.array([-0.32, -0.06, -0.16, -0.63, 0.31]) * 2
# w_stop = np.array([0.16, 0.21, 0.42, -0.55, 0.03]) * 2
# # omega [oom]: 0.035, ???, ???
# # alpha: 0.085, ???, ???

# # '3med'
# w_start = np.array([-0.32, -0.06, -0.16, -0.63, 0.31]) * 3
# w_stop = np.array([0.16, 0.21, 0.42, -0.55, 0.03]) * 3
# # omega [oom]: -0.519, ???, ???
# # alpha: -0.681, ???, ???

# # 'minmax'
# w_start = [-1.36, 0.85, -0.90, 1.44, -1.44]
# w_stop = [0.88, -0.78, 1.12, -1.49, 1.12]
# # omega [oom]: -0.125, ???, ???
# # alpha: -0.139, ???, ???

# # 'maxmin'
# w_start = [1.18, -0.97, 1.35, -1.49, 0.76]
# w_stop = [-0.84, 0.97, -0.54, 0.79, -0.95]
# # omega [oom]: -0.002, ???, ???
# # alpha: 0.068, ???, ???

# # 'maxmin/2'
# w_start = np.array([1.18, -0.97, 1.35, -1.49, 0.76]) / 2
# w_stop = np.array([-0.84, 0.97, -0.54, 0.79, -0.95]) / 2
# # omega [oom]: -0.667, ???, ???
# # alpha: -0.744, ???, ???

# # 'minmax/2'
# w_start = np.array([-1.36, 0.85, -0.90, 1.44, -1.44]) / 2
# w_stop = np.array([0.88, -0.78, 1.12, -1.49, 1.12]) / 2
# # omega [oom]: -0.728, ???, ???
# # alpha: -0.819, ???, ???

# # '1.6med'
# w_start = np.array([-0.32, -0.06, -0.16, -0.63, 0.31]) * 1.6
# w_stop = np.array([0.16, 0.21, 0.42, -0.55, 0.03]) * 1.6
# # omega [oom]: 0.059, ???, ???
# # alpha: 0.133, ???, ???

# # '1.7med'
# w_start = np.array([-0.32, -0.06, -0.16, -0.63, 0.31]) * 1.7
# w_stop = np.array([0.16, 0.21, 0.42, -0.55, 0.03]) * 1.7
# # omega [oom]: 0.084, -0.013, ???
# # alpha: 0.187, -0.135, ???

# # '2.2med'
# w_start = np.array([-0.32, -0.06, -0.16, -0.63, 0.31]) * 2.2
# w_stop = np.array([0.16, 0.21, 0.42, -0.55, 0.03]) * 2.2
# # omega [oom]: -0.065, ???, ???
# # alpha: -0.126, ???, ???

# # 'languid+med'
# w_start = np.array([-0.32, -0.06, -0.16, 0.77, 0.77])
# w_stop = np.array([0.16, 0.21, 0.42, 0.77, 0.77])
# # omega [oom]: 0.034, ???, ???
# # alpha: 0.079, ???, ???

# # '1.8med-based'
# w_start = [0, 0, 0, -1, 0.7]
# w_stop = [0, 0, 0, -1, 0]
# # omega [oom]: 0.055, -0.215, ???
# # alpha: 0.123, -0.436, ???

# # '1.8med-based-plus'
# w_start = [0, 0, 0, 1, 0.7]
# w_stop = [0, 0, 0, 1, 0]
# # omega [oom]: 0.067, -0.002, ???
# # alpha: 0.149, -0.003, ???

# # 'clustering4_0'
# w_start = [0.64, -0.53333333, -0.4, -1.09, 0.45333333]
# w_stop = [-0.15666667, 0.27, 0.37333333, -0.64666667, 0.05333333]
# # omega [oom]:  0.123, 0.041, -0.390
# # alpha: 0.268, 0.002, -0.482
# # FITmedbyf_akb = [1.29581273e+07, 6.98334217e+06, 6.56184612e+04, 1.67411280e+02, 2.06584658e+01, 1.23186664e+01, 1.09029533e+00, 4.78243193e+01, 1.74420984e+02, 7.17152485e+03, 8.56207769e+03, 2.06445344e+00, 3.63073759e-01, 3.57806925e-01, 8.35828150e+01, 2.06153598e+01, 2.54725029e+06, 6.39085471e+02, 5.75617475e+01, 1.90694608e+04, 2.53550337e+06, 1.83840802e+03, 3.44699275e+02, 2.70734604e+02, 2.23961369e+02, 1.00449764e+02, 8.97894419e+02, 1.28274665e+03, 3.61217332e+07, 4.67215474e+04]
# # FITmedbyf_akb = np.array(FITmedbyf_akb) 

# # 'clustering4_1'
# w_start = [-0.174, 0.002, 0.734, -0.834, -0.746]
# w_stop = [0.2, 0.364, 0.4, -0.83, -0.224]
# # omega [oom]:  0.044, -0.041, ???
# # alpha: 0.098, -0.196, ???

# # 'clustering4_2' aka 'TipsySpider'
# w_start = [-0.32333333, 0.09666667, -0.80666667, 1.19333333, 0.55]
# w_stop = [0.33666667, 0.36, 0.28, 0.75, 0.08333333]
# # omega [oom]: 0.100, 0.033, 0.263
# # alpha: 0.224, 0.084, 0.011
# # FITmedbyf_akb = [2.59632129e+06, 2.72780040e+03, 1.15791066e+04, 9.81031243e+01, 2.06659414e+01, 6.23716082e+00, 9.36020705e-12, 4.52326463e+01, 1.25572674e+02, 6.97363094e+03, 8.21205407e+03, 1.50346931e+00, 2.33448257e-01, 2.88431669e-01, 2.24243133e+01, 2.04503635e+01, 1.26723389e+06, 1.14529267e+03, 2.40318842e+01, 3.14017291e+03, 1.04385628e+06, 8.88136388e+02, 3.44004501e+02, 2.69761188e+02, 2.11466161e+02, 1.00331717e+02, 7.78087181e+02, 1.50912255e+03, 3.97647219e+07, 4.01204410e+04]
# # FITmedbyf_akb = np.array(FITmedbyf_akb) 

# # 'clustering4_3'
# w_start = [-0.9, -0.2075, -0.0425, -0.6125, 0.4675]
# w_stop = [0.2725, -0.29, 0.225, -0.68, 0.71]
# # omega [oom]:  -0.592, ???, ???
# # alpha: -0.637, ???, ???

# # 'clustering4_2-based'
# w_start = [0, 0, -0.80666667, 1.19333333, 0.55]
# w_stop = [0, 0, 0.28, 0.75, 0.08333333]
# # omega [oom]: 0.103, 0.037, ???
# # alpha: 0.229, 0.092, ???

# # 'clustering4_2-based2'
# w_start = [0, 0, 0, 1.19333333, 0.55]
# w_stop = [0, 0, 0, 0.75, 0.08333333]
# # omega [oom]: 0.062, -0.052, ???
# # alpha: 0.139, -0.079, ???
	

""" MAIN STUFF """

# akb_model, f_start, f_stop = None, None, None
try:            # if akb_model exists, akb functions are not needed
    akb_model  
    f_start, f_stop = None, None
except:         # if akb_model does not exist, create akb functions
    akb_model = None
    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    f_start = interp1d(Th, w_start, kind='linear')
    f_stop = interp1d(Th, w_stop, kind='linear')


if __name__ == '__main__': # multiprocessing needs this maybe

    # print('sleeping...\n')
    # time.sleep(3600*0)

    print(f'variant: {VARIANT}')
    print(f'model: {akb_model}') 
    print(f'D = {cecD}; cecruns = {cecruns}')
    
    pool = Pool(NP)
    pso = PSO()
    pso.method = VARIANT
    setup = [cecD, cecmaxit, cecruns, CEC, pso]
    
    startt = time.time()
    FITmedbyf_akb = metagoaleval(akb_model, f_start, f_stop, pool, setup, computecec=computecec)
    pool.close()
    stopt = time.time()
    print(f'elapsed time [hr]: {(stopt-startt)/3600:.3f}')

    # COMPUTE LOG-SCORE
    omega = np.nanmean(np.log10(FITmedbyf_akb/FITmedbyf_base))
    print(f'omega [oom]: {-omega:6.3f}')
    
    # COMPUTE ALPHA-SCORE
    alpha = np.nanmean(2 * (FITmedbyf_base - FITmedbyf_akb)/(FITmedbyf_base + FITmedbyf_akb))
    print(f'alpha [-]: {alpha:6.3f}')     
    
    """
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
    plt.title(f'{akb_model}')
    plt.legend()
    plt.show()
    """

