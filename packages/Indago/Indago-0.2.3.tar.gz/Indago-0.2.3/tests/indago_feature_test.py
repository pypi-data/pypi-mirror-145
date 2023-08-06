# -*- coding: utf-8 -*-
"""
indago feature test
(mostly) comprehensive test of indago features
SHOULD BE RUN AT EVERY INDAGO UPGRADE
A TEST FOR EVERY NEW FEATURE SHOULD BE ADDED HERE
"""

# need this for local (non-pip) install only
import sys
sys.path.append('..')

import io
from contextlib import redirect_stdout

import numpy as np
from indago.benchmarks import CEC2014
from indago import PSO, FWA, SSA, MMO, DE, BA, EFO, MRFO


DIM = 10
F = CEC2014(DIM).F3
MAXEVAL = 1000
TOL = 1e-10


def check(optimizer, description=None, 
          expected_result=None, tolerance=TOL,
          expected_printout=''):
    
    # print(f'* Testing: {description}')
    
    optimizer.evaluation_function = F
    optimizer.dimensions = DIM
    optimizer.lb = np.ones(optimizer.dimensions) * -100
    optimizer.ub = np.ones(optimizer.dimensions) * 100
    optimizer.iterations = 1000
    optimizer.maximum_evaluations = MAXEVAL
    
    IOout = io.StringIO()
    with redirect_stdout(IOout):
        result = np.log10(optimizer.optimize(seed=0).f)
    printout = IOout.getvalue().rstrip()

    if not expected_result:
        print(f'*** RESULT -> {result}')
        return
    
    assert expected_result - tolerance < result < expected_result + tolerance \
            and printout == expected_printout, \
        f'{description} FAILED, result={result}'


if __name__ == '__main__': 
    
    test = 'PSO defaults'    
    optimizer = PSO()
    check(optimizer, test, 4.4687271330225835)
    del optimizer
    
    test = 'PSO Vanilla custom parameters'
    optimizer = PSO()
    optimizer.method = 'Vanilla'
    optimizer.params['swarm_size'] = 10
    optimizer.params['inertia'] = 0.6
    optimizer.params['cognitive_rate'] = 2.0
    optimizer.params['social_rate'] = 2.0
    check(optimizer, test, 4.935545710009518)
    del optimizer
    
    test = 'PSO TVAC defaults'
    optimizer = PSO()
    optimizer.method = 'TVAC'
    check(optimizer, test, 5.1531023920522445)
    del optimizer
    
    test = 'PSO TVAC too many parameters'
    msg = 'Warning: Excessive parameter cognitive_rate'
    optimizer = PSO()
    optimizer.method = 'TVAC'
    optimizer.params['cognitive_rate'] = 2.0
    check(optimizer, test, 5.1531023920522445, expected_printout=msg)
    del optimizer
    
    test = 'PSO Vanilla LDIW'
    optimizer = PSO()
    optimizer.params['inertia'] = 'LDIW'
    check(optimizer, test, 4.772117204754762)
    del optimizer
    
    test = 'PSO Vanilla anakatabatic FlyingStork'
    optimizer = PSO()
    optimizer.method = 'Vanilla'
    optimizer.params['inertia'] = 'anakatabatic'
    optimizer.params['akb_model'] = 'FlyingStork'
    check(optimizer, test, 4.316089584721751, tolerance=1e-3)
    del optimizer
    
    test = 'PSO Vanilla anakatabatic TipsySpider'
    optimizer = PSO()
    optimizer.method = 'Vanilla'
    optimizer.params['inertia'] = 'anakatabatic'
    optimizer.params['akb_model'] = 'TipsySpider'
    check(optimizer, test, 3.8943071168580605, tolerance=1e-3)
    del optimizer
    
    test = 'PSO TVAC anakatabatic OrigamiSnake'
    optimizer = PSO()
    optimizer.method = 'TVAC'
    optimizer.params['inertia'] = 'anakatabatic'
    optimizer.params['akb_model'] = 'OrigamiSnake'
    check(optimizer, test, 4.637440531990269, tolerance=1e-1)
    del optimizer
    
    test = 'PSO TVAC anakatabatic Languid'
    optimizer = PSO()
    optimizer.method = 'TVAC'
    optimizer.params['inertia'] = 'anakatabatic'
    optimizer.params['akb_model'] = 'Languid'
    check(optimizer, test, 4.7196754302755135)
    del optimizer
    
    test = 'PSO defaults, multiprocessing on 4 processors'
    # Note: multiprocessing is slower due to pool start/stop each run
    optimizer = PSO()
    optimizer.number_of_processes = 4
    check(optimizer, test, 4.4687271330225835)
    del optimizer
    
    test = 'PSO defaults, multiprocessing on maximum processors'
    # Note: multiprocessing is slower due to pool start/stop each run
    optimizer = PSO()
    optimizer.number_of_processes = 'maximum'
    check(optimizer, test, 4.4687271330225835)
    del optimizer
    
    test = 'FWA defaults'
    optimizer = FWA()
    check(optimizer, test, 3.8417077823060226, tolerance=1e-3)
    del optimizer
    
    test = 'FWA custom parameters'
    optimizer = FWA()
    optimizer.params['n'] = 12
    optimizer.params['m1'] = 8
    optimizer.params['m2'] = 6
    check(optimizer, test, 4.250784072558093, tolerance=1e-3)
    del optimizer
    
    test = 'SSA defaults'
    optimizer = SSA()
    check(optimizer, test, 5.2006580754454745)    
    del optimizer
    
    test = 'SSA custom parameters'
    optimizer = SSA()
    optimizer.params['swarm_size'] = 12
    optimizer.params['acorn_tree_attraction'] = 0.8
    check(optimizer, test, 4.217644352979585)
    del optimizer
    
    test = 'SSA custom additional parameters'
    optimizer = SSA()
    optimizer.params['swarm_size'] = 12
    optimizer.params['predator_presence_probability'] = 0.2
    optimizer.params['gliding_constant'] = 1.5
    check(optimizer, test, 4.852974034102223)
    del optimizer

    test = 'DE defaults'
    optimizer = DE()
    check(optimizer, test, 4.819958736743474)
    del optimizer
    
    test = 'DE LSHADE defaults'
    optimizer = DE()
    optimizer.method = 'LSHADE'
    check(optimizer, test, 4.567308970943115)
    del optimizer
    
    test = 'DE LSHADE custom parameters'
    optimizer = DE()
    optimizer.method = 'LSHADE'
    optimizer.params['initial_population_size'] = 20
    optimizer.params['external_archive_size_factor'] = 2
    check(optimizer, test, 3.927040138589889)
    del optimizer
    
    test = 'BA defaults'
    optimizer = BA()
    check(optimizer, test, 4.849803061666929)
    del optimizer
    
    test = 'EFO defaults'
    optimizer = EFO()
    check(optimizer, test, 4.728563872454055)
    del optimizer
    
    test = 'MRFO defaults'
    optimizer = MRFO()
    check(optimizer, test, 4.375633159276136)
    del optimizer
    
    test = 'MMO defaults'
    optimizer = MMO()
    check(optimizer, test, 4.088557003106588)
    del optimizer
    
    test = 'MMO FWA+PSO custom parameters'
    optimizer = MMO()
    optimizer.method = {'FWA': 'Vanilla', 
                        'PSO': 'TVAC'}
    optimizer.params['n'] = 6 # FWA
    optimizer.params['swarm_size'] = 8 # PSO
    optimizer.params['inertia'] = 'anakatabatic' # PSO
    optimizer.params['akb_model'] = 'OrigamiSnake' # PSO    
    check(optimizer, test, 4.3203553000854145, tolerance=1e-6)
    del optimizer
    
    test = 'MMO DE+FWA+PSO custom parameters'
    optimizer = MMO()
    optimizer.method = {'DE': 'LSHADE', 
                        'FWA': 'Vanilla',
                        'PSO': 'TVAC'}
    optimizer.params['initial_population_size'] = 20
    optimizer.params['external_archive_size_factor'] = 2
    optimizer.params['n'] = 12
    optimizer.params['m1'] = 8
    optimizer.params['m2'] = 6
    optimizer.params['swarm_size'] = 10 # PSO
    optimizer.params['inertia'] = 'anakatabatic'
    optimizer.params['akb_model'] = 'Languid'
    check(optimizer, test, 3.7691442219622555, tolerance=1e-8)
    del optimizer
    