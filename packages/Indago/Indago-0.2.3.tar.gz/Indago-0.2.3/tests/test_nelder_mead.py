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
from indago import NelderMead

# FWA instance
nm = NelderMead()
nm.iterations = 1000

# Define optimization problem
nm.evaluation_function = lambda x: np.sum((x - np.arange(np.size(x))) ** 2)
nm.dimensions = 10
nm.lb = np.ones(nm.dimensions) * -100
nm.ub = np.ones(nm.dimensions) *  100
nm.objectives = 1
nm.objective_labels = ['Length']


opt = nm.run()
print(opt)

