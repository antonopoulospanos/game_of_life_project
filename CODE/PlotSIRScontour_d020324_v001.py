#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 10:31:48 2024

@author: panosantonopoulos
"""

import matplotlib

#matplotlib.use('TKAgg')

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.ticker import MaxNLocator
import pandas as pd
import time



df = pd.read_csv('MapValues.csv')

print(df)

array = df.to_numpy()
print(array)



avgIdivN = np.reshape(array, (21, 21))


levels1 = MaxNLocator(nbins='auto').tick_values(avgIdivN.min(), avgIdivN.max())
levels2 = MaxNLocator(nbins='70').tick_values(avgIdivN.min(), avgIdivN.max())
cmap = plt.colormaps['gnuplot']

fig, ax = plt.subplots(1,1)
cf=ax.contourf(avgIdivN, levels=levels1, cmap=cmap, extent=(0,1,0,1))
#cf=ax.contourf(X,Y,avgIdivN, levels=levels, cmap=cmap)
fig.colorbar(cf, ax=ax)
fig.tight_layout()
ax.set_title("Contour Plot With Auto Setting Bins")

plt.show()
fig1, ax1 = plt.subplots(1,1)

cf1=ax1.contourf(avgIdivN, levels=levels2, cmap=cmap, extent=(0,1,0,1))
fig1.colorbar(cf1, ax=ax1)
fig1.tight_layout()
ax1.set_title("Contour Pot With 70 Bins")

plt.show()

fig2, ax2 = plt.subplots(1,1)
pos = ax2.imshow(np.flipud(avgIdivN), cmap='gnuplot', interpolation='none', vmin=np.min(avgIdivN), vmax=np.max(avgIdivN), extent=[0,1,0,1])
fig2.colorbar(pos, ax=ax2)
ax2.set_title("Colour Map Using imshow")
plt.show()

fig3, ax3 = plt.subplots(1,1)
cf2=ax3.contourf(avgIdivN, extent=(0,1,0,1))
ax3.set_title("Contour Plot")
fig3.colorbar(cf2, ax=ax3)
fig3.tight_layout()
plt.show()