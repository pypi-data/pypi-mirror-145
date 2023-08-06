# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 10:58:25 2019
Anakatabatic plot model
@author: Sinisa
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from scipy.interpolate import interp1d

## Anakatabatic models

#model = 'akb vanilla #3a'
#modelaka = 'FlyingStork'
## obtained by Vanilla, languid, metaopt eval = 80D, cecit = 500
## metaopt score = ???
#w_start = [-0.86, 0.24, -1.10, 0.75, 0.72]
#w_stop = [-0.81, -0.35, -0.26, 0.64, 0.60]
#splinetype = 'linear'
## alpha: 0.130, 0.190, 0.085
## omega [oom]: 0.058, 0.086, 0.038

#model = 'akb vanilla #4a' # desno isto kao FlyingStork
#modelaka = 'PoorFlyingStork'
#w_start = [-1.35, -0.82, 0.75, 0.75, 0.72]
#w_stop = [0.33, -0.96, -0.81, 0.64, 0.60]
#splinetype = 'linear'
## alfa: 0.086, 0.119, 0.079
## omega: 0.034, 0.117, 0.034

#model = 'akb vanilla #5'
#modelaka = 'MessyTie'
## obtained by Vanilla, languid, D = 20, metaopt eval = 60D, cecit = 500, omegascore = 2.09
## metaopt score = -2.0865682041224605
#w_start = [-0.62, 0.18, 0.65, 0.32, 0.77]
#w_stop = [0.36, 0.73, -0.62, 0.40, 1.09]
#splinetype = 'linear'
## alfa: -0.09, 0.11, 0.09
## omega: -0.05, 0.05, 0.08


#model = 'akb tvac #1'
#modelaka = 'RightwardPeaks'
## obtained by Vanilla, metaopt eval = 100D, cecit = 500
## metaopt score = 1.93
##w_start = [-1.79457153, -0.33409362, 2., -0.67365566, 1.29661024]
##w_stop = [-0.9120458, -0.87835946, -0.83647823, 0.67106473, -0.36185384]
#w_start = [-1.79, -0.33, 2.00, -0.67, 1.30]
#w_stop = [-0.91, -0.88, -0.84, 0.67, -0.36]
#splinetype = 'linear'
## alpha: 0.516, 0.701, 0.739
## omega [oom]: 0.280, 0.503, 0.589

model = 'akb tvac #2'
modelaka = 'OrigamiSnake'
# obtained by TVAC, metaopt eval = 80D, cecit = 500
# metaopt score = 1.93
# w_start: [-1.35775837  2.          0.99517856 -0.59799006  1.22378286]
# w_stop: [ 0.30163937  1.02731527 -0.20840698  0.39628794  0.05674581]
w_start = [-1.36, 2.00, 1.00, -0.60, 1.22]
w_stop = [0.30, 1.03, -0.21, 0.40, 0.06]
splinetype = 'linear'
# alpha: 0.524, 0.705, 0.718
# omega [oom]: 0.292, 0.541, 0.547


## LPSO +0.05
#model = 'LPSO'
#modelaka = 'languid'
#def f_start(Th):
#    w = (0.72 + 0.05) * np.ones_like(Th)
#    for i, th in enumerate(Th):
#        if th < 4*np.pi/4: 
#            w[i] = 0
#    return w
#f_stop = f_start
#splinetype = None



""" MAIN STUFF """

try: f_start    # if akb funs do not exist...
except:         # ...create w-defined akb interpolation funs
    Th = np.linspace(np.pi/4, 5*np.pi/4, 5)
    f_start = interp1d(Th, w_start, kind=splinetype)
    f_stop = interp1d(Th, w_stop, kind=splinetype)


THplot = np.linspace(np.pi/4, 5*np.pi/4, 5)
plt.fill_between(THplot, f_start(THplot), f_stop(THplot), 
                 color='lightgrey', alpha=0.5)
plt.plot(THplot, f_start(THplot), color='seagreen', marker='o',
         label=r'starting $w$-function $W_s(\theta)$')
plt.plot(THplot, f_stop(THplot), color='orangered', marker='o', 
         label=r'final $w$-function $W_f(\theta)$')
plt.axhline(color='grey', ls='-', lw=1)
plt.axvline(2*np.pi/4, color='grey', ls=':', lw=1)
plt.axvline(4*np.pi/4, color='grey', ls=':', lw=1)
plt.axis([np.pi/4, 5*np.pi/4, -2.5, 3.0])
plt.xlabel(r'$\theta_k$', fontsize='x-large')
plt.ylabel('$w_k$', fontsize='x-large')
plt.text(np.pi/4 + 0.03, 2.7, r'$\frac{\pi}{4}$', fontsize='x-large')
plt.text(2*np.pi/4 + 0.03, 2.7, r'$\frac{\pi}{2}$', fontsize='x-large')
plt.text(4*np.pi/4 + 0.03, 2.7, r'$\pi$', fontsize='x-large')
plt.text(5*np.pi/4 - 0.1, 2.7, r'$\frac{5\pi}{4}$', fontsize='x-large')
#plt.title(f'{model}, {splinetype}')
plt.legend(bbox_to_anchor=(0.5, 1.1), loc='upper center', 
           ncol=2, frameon=False, fontsize='x-large')
plt.tight_layout(pad=0.0)
plt.savefig(f'akb_int_{modelaka}.pdf')


"""
# plot quadrants
plt.figure(figsize=(5,5))
plt.axhline(color='grey', ls='-', lw=1)
plt.axvline(color='grey', ls='-', lw=1)
plt.plot([-1, 1], [-1, 1], ls='-', lw=3)

plt.plot(-0.66, 0.5*2/3, 'ro', label='particle-vs-swarm state')
plt.plot([-1, 0], [0.5, 0], color='grey', ls=':', lw=1)

plt.xticks([], []), plt.yticks([], [])
plt.xlabel(r'best-advancing particle fitness change $\min \Delta f\left( \mathbf{x}_k^{(t)}\right)$ $\longrightarrow$')
plt.ylabel(r'$k$-th particle fitness change $\Delta f\left( \mathbf{x}_k^{(t)}\right)$ $\longrightarrow$')
plt.text(0.03, -0.1, r'$(0,0)$')
plt.text(0.2, 0.5, r'$\theta_k$')

plt.text(0.05, 0.75, r'$\frac{\pi}{4} \leq \theta_k \leq \frac{\pi}{2}$' + '\nall particles \nascending')
plt.text(-0.96, 0.67, r'$\frac{\pi}{2} \leq \theta_k \leq \pi$' + '\n' + r'$k$-th particle ascending,' + '\nbest-advancing \nparticle descending')
plt.text(-0.96, -0.39, r'$\pi \leq \theta_k \leq \frac{5\pi}{4}$' + '\n' + r'both $k$-th particle and' + '\nbest-advancing \nparticle \ndescending')

from matplotlib.patches import Arc, RegularPolygon
ax = plt.gca()
def drawCirc(ax,radius,centX,centY,angle_,theta2_,color_='black'): # radius is not in scale
    #========Line
    arc = Arc([centX,centY],radius,radius,angle=angle_,
          theta1=0,theta2=theta2_,capstyle='round',linestyle='-',lw=1,color=color_)
    ax.add_patch(arc)
    #========Create the arrow head
    endX=centX+(radius/2)*np.cos(np.radians(theta2_+angle_)) #Do trig to determine end position
    endY=centY+(radius/2)*np.sin(np.radians(theta2_+angle_))
    ax.add_patch(                    #Create triangle as arrow head
        RegularPolygon(
            (endX, endY),            # (x,y)
            3,                       # number of vertices
            radius/25,                # radius
            np.radians(angle_+theta2_),     # orientation
            color=color_
        )
    )
    ax.set_xlim([centX-radius,centY+radius]) and ax.set_ylim([centY-radius,centY+radius]) 
    # Make sure you keep the axes scaled or else arrow will distort
drawCirc(ax,1,0,0,0,148)

plt.fill_between(plt.xlim(), [-1, 1], [-1, -1], 
                 color='lightblue', alpha=0.5, 
                 label='unfeasible area')
plt.axis([-1, 1, -1, 1]) # ovo kao 
plt.legend(loc='lower right')
plt.tight_layout(pad=0)
plt.savefig(f'akb_scheme.pdf')
"""