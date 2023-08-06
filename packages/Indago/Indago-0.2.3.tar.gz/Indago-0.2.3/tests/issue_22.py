#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  2 14:56:11 2021

@author: stefan
"""

import sys
sys.path.append('..')
from indago import CandidateState, Optimizer
import numpy as np

optimizer = Optimizer()
optimizer.dimensions = 10
optimizer.objectives = 1
optimizer.constraints = 3
optimizer.evaluation_function = lambda X: np.array([np.sum(X**2), 
                                                    np.sum(X), 
                                                    np.min(X), 
                                                    np.max(X)])
optimizer._init_optimizer()

old = CandidateState(optimizer)
old.X = np.random.uniform(-1, 1, 10)
old.evaluate()
print(old)

new1 = CandidateState(optimizer)
new1.X = np.copy(old.X)
new1.f = old.f
new1.O = np.copy(old.O)
new1.C = np.copy(old.C)
print(new1)

new2 = old.copy()
print(new2)

print(new1 == old)
print(new2 == old)
print(new1 == new2)