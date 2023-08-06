#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 09:24:11 2019

@author: stefan
"""

import sys
sys.path.append('..')

import indago
import indago.legacy_pso as pso
#import indago.pso.PSO # No module named 'indago.pso.PSO'; 'indago.pso' is not a package
from indago import legacy_pso
from indago.legacy_pso import LegacyPSO
from indago import PSO

import indago.fwa as fwa
from indago import ABC

# Old - FAILS
#from benchmarks import cec
#from benchmarks.cec import CEC2014
#from benchmarks.shortest_path import ShortestPath

from indago.benchmarks import CEC2014
from indago.benchmarks import ShortestPath
import indago.benchmarks as b