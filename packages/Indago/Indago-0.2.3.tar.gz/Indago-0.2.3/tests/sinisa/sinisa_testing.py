# -*- coding: utf-8 -*-
"""
Created on Sat Mar 31 09:57:19 2018

@author: Sinisa
"""

import sys
sys.path.append('../indago/')
sys.path.append('../benchmarks/')
import time
import numpy as np
from cec import CEC2014
from pso import PSO

if __name__ == '__main__':
    
    d = 10

    cec2014 = CEC2014(d)

    pso = PSO()
    pso.objective = cec2014.F7
    pso.dimensions = d
    pso.swarm_size = 30
    pso.lb = np.ones(d) * -100
    pso.ub = np.ones(d) * 100

    pso.iterations = int(1000 * d / pso.swarm_size)

    # pso.method = 'Vanilla'
    # pso.params['inertia'] = 0.65
    # pso.params['cognitive_rate']  = 1.0
    # pso.params['social_rate']  = 1.0

    pso.method = 'TVAC'
    pso.params['inertia'] = 'LDIW'

    pso.params['inertia'] = 'anakatabatic'
    # pso.params['akb_fun_start'] = np.poly1d([0, 0, 0, 0.65])
    # pso.params['akb_fun_start'] = np.poly1d([-0.10400605, 1.28310465,
    #                                             -4.54559204, 5.22110412])
    # pso.params['akb_fun_start'] = lambda theta: 0.38 * theta - 0.85
    pso.params['akb_fun_start'] = np.poly1d([0.07410173, -0.80076351,
                                                3.21656237, -4.14711059])
    pso.params['akb_fun_stop'] = np.poly1d([0.07410173, -0.80076351,
                                                3.21656237, -4.14711059])
    
#    if pso.params['inertia'] == 'anakatabatic': # plot akb_fun_start
#        import matplotlib.pyplot as plt
#        ax = plt.subplot(111, projection='polar')
#        theta = np.linspace(np.pi / 4, 5 * np.pi / 4)
#        ax.plot(theta, pso.params['akb_fun_start'](theta), label='w')
#        ax.set_theta_offset(-np.pi/4)        
#        ax.set_xticks(np.linspace(np.pi / 4, 5 * np.pi / 4, 5))
#        if np.max(pso.params['akb_fun_start'](theta)) > 1:
#            ax.fill_between(theta, 
#                            ax.get_rmax(), 1,
#                            color='magenta', alpha=0.3,
#                            label = 'diverging')
#        if np.min(pso.params['akb_fun_start'](theta)) < 0:
#            ax.fill_between(theta, 
#                            0, ax.get_rmin(),
#                            color='orange', alpha=0.3,
#                            label = 'retreating')
#        ax.set_thetamin(45)
#        ax.set_thetamax(225)
#        ax.set_rlabel_position(180) # not working
#        plt.title(r'anakatabatic $w(\theta)$')
#        plt.legend()
#        plt.show()

    pso.verbose = True

    start = time.time()
    runs = 1000
    FIT = np.zeros(runs)
    if pso.params['inertia'] == 'anakatabatic' and pso.verbose:
        THETA = np.empty([pso.swarm_size, pso.iterations, runs])
    for r in range(runs):
        if pso.verbose:
            FIT[r], _, report = pso.run()
            if pso.params['inertia'] == 'anakatabatic':
                THETA[:, :, r] = report['theta']
        else:
            FIT[r], _ = pso.run()
    end = time.time()

    print('Elapsed time: %.2f s' % (end - start))
    print('Average fitness: %.3e' % np.mean(FIT))

    if pso.params['inertia'] == 'anakatabatic':

        import matplotlib.pyplot as plt
        plt.figure()
        skip_iterations, skip_runs = 5, 10

        for r in range(0, runs, skip_runs):
            for i in range(1, pso.iterations, skip_iterations):
                plt.plot(THETA[:, i, r], i * np.ones(pso.swarm_size),
                         'b.', alpha=max(0.01, 1 / runs))
                # this would possibly be better/faster with plt.hexbin()

        plt.title('theta distribution over iterations\n' +
                  pso.method + ' PSO, anakatabatic inertia')
        plt.axvline(2 * np.pi / 4, color='magenta', ls=':')
        plt.axvline(4 * np.pi / 4, color='magenta', ls=':')
        plt.axis([np.pi / 4, 5 * np.pi / 4, 0, pso.iterations])
        plt.xlabel(r'$\theta_i$')
        plt.ylabel('iterations')
        plt.show()
