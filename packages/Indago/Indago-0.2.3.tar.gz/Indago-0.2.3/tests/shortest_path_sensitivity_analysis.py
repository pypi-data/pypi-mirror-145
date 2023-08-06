#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:02:47 2018

@author: stefan
"""

import sys
sys.path.append('..')
import indago
import matplotlib.pyplot as plt
import numpy as np
from indago.benchmarks import ShortestPath

sp = ShortestPath('case_3.2')

ph_range = 180
# PH1 = np.linspace(-0, 60, 11)
# PH2 = np.linspace(-60, 0, 15)
PH1 = np.linspace(-ph_range / 2, ph_range / 2, 301)
PH2 = np.linspace(-ph_range / 2, ph_range / 2, 301)
L = np.zeros([np.size(PH1), np.size(PH2)])
P = np.zeros([np.size(PH1), np.size(PH2)])
F = np.zeros([np.size(PH1), np.size(PH2)])

for i1, ph1 in enumerate(PH1):
    for i2, ph2 in enumerate(PH2):

        x, y, l, d = sp.generate_path(np.array([ph1, ph2]))

        F[i1, i2] = l + d * 10

        if d > 1e-6:
            L[i1, i2] = np.nan
            P[i1, i2] = d
        else:
            L[i1, i2] = l
            P[i1, i2] = np.nan

best = np.unravel_index(F.argmin(), F.shape)
global_min = np.array([PH1[best[0]], PH2[best[1]]])

print('Global best:', global_min)
print('F:', F[best[0], best[1]])
print('L:', L[best[0], best[1]])
print('P:', P[best[0], best[1]])

plt.figure(figsize=(7.5, 6))
plt.title('Fitness')
fplt = plt.contourf(PH1, PH2, F.T, 100)
plt.contour(PH2, PH1, F.T, 30, colors='wheat', linewidths=0.1, linestyles='--')
plt.colorbar(fplt, fraction=0.046, pad=0.01)
plt.plot(global_min[0], global_min[1], 'w+', ms=20)
plt.xlabel(r'$\phi_1$ [°]')
plt.ylabel(r'$\phi_2$ [°]')
plt.axis('image')
plt.subplots_adjust(left=0.05, right=0.9,
                    bottom=0.1, top=0.95)

plt.figure(figsize=(9, 6))
plt.title('Path length and obstacle collision length')
lplt = plt.contourf(PH1, PH2, L.T, 100)
dplt = plt.contourf(PH1, PH2, P.T, 100, cmap=plt.cm.Reds)
plt.contour(PH2, PH1, L.T, 30, colors='wheat', linewidths=0.1, linestyles='--')
plt.contour(PH2, PH1, P.T, 30, colors='wheat', linewidths=0.1, linestyles='--')

plt.xlabel(r'$\phi_1$ [°]')
plt.ylabel(r'$\phi_2$ [°]')
plt.axis('image')

plt.subplots_adjust(left=0.05, right=0.9,
                    bottom=0.1, top=0.95)
plt.colorbar(dplt, fraction=0.046, pad=0.12, label='Collision length')
plt.colorbar(fplt, fraction=0.046, pad=0.02, label='Path length')

plt.figure(figsize=(6, 6))
ax = plt.gca()
sp.draw_obstacles(ax)
sp.draw_path(global_min, ax, 'Global best')

plt.xlabel(r'$\phi_1$ [°]')
plt.ylabel(r'$\phi_2$ [°]')
plt.axis('image')

plt.show()
