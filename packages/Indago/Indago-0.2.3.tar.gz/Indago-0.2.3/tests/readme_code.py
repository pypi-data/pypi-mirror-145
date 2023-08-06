# -*- coding: utf-8 -*-
"""
Tutorial code given in the readme.md
"""

# need this for local (non-pip) install only
import sys
sys.path.append('..')


### Particle Swarm Algorithm

import numpy as np
from indago import PSO
pso = PSO()

def goalfun(x):	# must take 1d np.array
    return np.sum(x**2) # must return scalar number
pso.evaluation_function = goalfun

pso.method = 'Vanilla' # we will use Standard PSO, the other available option is 'TVAC' [1]; default method='Vanilla'
pso.dimensions = 20 # number of variables in the design vector (x)
pso.params['swarm_size'] = 15 # number of PSO particles; default swarm_size=dimensions
pso.iterations = 1000 # default iterations=100*dimensions
# pso.maximum_evaluations = 5000 # optional maximum allowed number of function evaluations; when surpassed, optimization is stopped (if reached before pso.iterations are exhausted)
# pso.target_fitness = 10**-3 # optional fitness threshold; when reached, optimization is stopped (if it didn't already stop due to exhausted pso.iterations or pso.maximum_evaluations)
pso.lb = np.ones(pso.dimensions) * -1 # 1d np.array of lower bound values
pso.ub = np.ones(pso.dimensions) * 1 # 1d np.array of upper bound values

pso.params['cognitive_rate'] = 1.0 # PSO parameter also known as c1 (should range from 0.0 to 2.0); default cognitive_rate=1.0
pso.params['social_rate'] = 1.0 # PSO parameter also known as c2 (should range from 0.0 to 2.0); default social_rate=1.0
pso.params['inertia'] = 0.8 # PSO parameter known as inertia weight w (should range from 0.5 to 1.0), the other available options are 'LDIW' (w linearly decreasing from 1.0 to 0.4) and 'anakatabatic'; default inertia=0.72

"""
# anakatabatic option
pso.params['inertia'] = 'anakatabatic'
pso.params['akb_model'] = 'Languid' # other options are 'FlyingStork', 'MessyTie', 'RightwardPeaks', 'OrigamiSnake'
"""

pso.number_of_processes = 4 # optional number of processes for parallel swarm evaluation (scales well only on slow goal functions), use 'maximum' for employing all available processors/cores
pso.monitoring = 'dashboard' # the available options are None, 'basic', 'dashboard'; default monitoring=None

if __name__ == '__main__': # needed for multiprocessing
    result = pso.optimize()
    min_f = result.f # fitness at minimum, np.array scalar number
    x_min = result.X # design vector at minimum, 1d np.array
    print('PSO', min_f)


### Fireworks Algorithm

from indago import FWA
fwa = FWA()

fwa.evaluation_function = pso.evaluation_function
fwa.dimensions = pso.dimensions
fwa.iterations = pso.iterations
# fwa.target_fitness = pso.target_fitness
fwa.number_of_processes = pso.number_of_processes
fwa.monitoring = pso.monitoring
fwa.lb = pso.lb
fwa.ub = pso.ub

fwa.method = 'Vanilla'

fwa.params['n'] = 20
fwa.params['m1'] = 10
fwa.params['m2'] = 10

if __name__ == '__main__': # needed for multiprocessing
    result = fwa.optimize()
    min_f = result.f # fitness at minimum, np.array scalar number
    x_min = result.X # design vector at minimum, 1d np.array
    print('FWA', min_f)


### Squirrel Search Algorithm

from indago import SSA
ssa = SSA()

ssa.evaluation_function = pso.evaluation_function
ssa.dimensions = pso.dimensions
ssa.params['swarm_size'] = pso.params['swarm_size']
ssa.iterations = pso.iterations
# ssa.target_fitness = pso.target_fitness
ssa.number_of_processes = pso.number_of_processes
ssa.monitoring = pso.monitoring
ssa.lb = pso.lb
ssa.ub = pso.ub

ssa.params['acorn_tree_attraction'] = 0.6 # ranges from 0.0 to 1.0; default acorn_tree_attraction=0.5

## optional parameters
# ssa.params['predator_presence_probability'] = 0.1
# ssa.params['gliding_constant'] = 1.9 
# ssa.params['gliding_distance_limits'] = [0.5, 1.11] 

if __name__ == '__main__': # needed for multiprocessing
    result = ssa.optimize()
    min_f = result.f # fitness at minimum, np.array scalar number
    x_min = result.X # design vector at minimum, 1d np.array
    print('SSA', min_f)


### Differential Evolution

from indago import DE
de = DE()

de.evaluation_function = pso.evaluation_function
de.dimensions = pso.dimensions
de.iterations = pso.iterations
# de.target_fitness = pso.target_fitness
de.number_of_processes = pso.number_of_processes
de.monitoring = pso.monitoring
de.lb = pso.lb
de.ub = pso.ub

de.method = 'LSHADE'

## optional parameters
# de.params['initial_population_size'] = 200 # default initial_population_size=dimensions*18
# de.params['external_archive_size_factor'] = 2.6 # default
# de.params['historical_memory_size'] = 4 # default historical_memory_size=6
# de.params['p_mutation'] = 0.2 # default p_mutation=0.11

if __name__ == '__main__': # needed for multiprocessing
    result = de.optimize()
    min_f = result.f # fitness at minimum, np.array scalar number
    x_min = result.X # design vector at minimum, 1d np.array
    print('DE', min_f)

"""
### CEC2014

from indago.benchmarks import CEC2014
test = CEC2014(20) # initialization od 20-dimension functions, you can also use 10, 50 and 100

optimizer = ssa # we'll take SSA on the CEC-ride
test_results = []
for f in test.functions[:3]:
    optimizer.evaluation_function = f
    test_results.append(optimizer.optimize().f)
    print(f'{f.__name__:3s} ({f.__doc__:50s}), best fitness: {test_results[-1]}')
print(test_results)
"""