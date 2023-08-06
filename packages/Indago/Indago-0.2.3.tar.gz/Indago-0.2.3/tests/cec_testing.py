# -*- coding: utf-8 -*-
"""
test Indago CEC implementation

@author: Sinisa
"""

import sys
sys.path.append('..')
from indago.benchmarks import CEC2014
import numpy as np

fname_prefix = 'cec2014_benchmark_data'
N_SAMPLES = 10

funs_not_good = []

for d in [10, 20, 50, 100]:
    print("\nDimension: %d\n" % d)

    # Generating samples
    # np.savetxt('%s/samples_%dd.txt' % (fname_prefix, d),
    #           np.random.uniform(-100, 100, [N_SAMPLES, d]),
    #           fmt='%.5f')
    # continue

    X = np.loadtxt('%s/samples_%dd.txt' % (fname_prefix, d))
    F = np.loadtxt('%s/results_%dd.txt' % (fname_prefix, d)).T
    # X = np.loadtxt(fname_prefix + str(d) + 'd_x.txt')[:N_SAMPLES,:]
    # F = np.loadtxt(fname_prefix + str(d) + 'd_f.txt')[:N_SAMPLES]

    cec = CEC2014(d)
    test_functions = [cec.F1, cec.F2, cec.F3, cec.F4, cec.F5, cec.F6, cec.F7,
                      cec.F8, cec.F9, cec.F10, cec.F11, cec.F12, cec.F13,
                      cec.F14, cec.F15, cec.F16, cec.F17, cec.F18, cec.F19,
                      cec.F20, cec.F21, cec.F22, cec.F23, cec.F24, cec.F25,
                      cec.F26, cec.F27, cec.F28, cec.F29, cec.F30]

    for i, x in enumerate(X):
        for j, fun in enumerate(test_functions):
            f = fun(x)
            f = float('%.10e' % f)
            err = np.abs(f - F[i, j]) / F[i, j]

            # print("%3s: %.10e %.10e %.18e" % (fun.__name__, f, F[i,j], err)

            if err > 1e-8:
                fun_str = '%dD%s' % (d, fun.__name__)
                if fun_str not in funs_not_good:
                    funs_not_good.append(fun_str)
                    print('{}, {}d -> this: {:.10e}, C++: {:.10e}, rel_err: {:.3e}'.format(
                        fun.__name__, d, fun(x), F[i, j], err))

if funs_not_good:
    print('\nfunctions not in agreement with CEC C++ code:')
    print(*sorted(funs_not_good), sep=', ')
else:
    print('all functions OK')
