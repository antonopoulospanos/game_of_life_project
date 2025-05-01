#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 14:14:06 2024

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

nstep = 1000

# input

lx = int(input("Array size: "))

START = time.time()

p1 = np.arange(0, 1.05, 0.05)
p2 = 0.5
p3 = np.arange(0, 1.05, 0.05)

ly = lx
N=lx*ly
"""
fig = plt.figure()
im = plt.imshow(lattice, animated=True)
"""
def updateSite(lattice, xselection, yselection, lx, ly, prob1, prob2, prob3):
    
    site = lattice[xselection, yselection]
    
    if site == 1:
        
        upperneighbour = lattice[(xselection-1)%lx, yselection]
        lowerneighbour = lattice[(xselection+1)%lx, yselection]
        rightneighbour = lattice[xselection, (yselection+1)%ly]
        leftneighbour = lattice[xselection, (yselection-1)%ly]
        
        if 0 in (upperneighbour, lowerneighbour, rightneighbour, leftneighbour):
            
            r = random.random()
            if r <= prob1:
                
                lattice[xselection, yselection] = 0
    
    if site == 0:
        
        r = random.random()
        if r <= prob2:
            
            lattice[xselection, yselection] = -1
            
    if site == -1:
        
        r = random.random()
        if r <= prob3:
            
            lattice[xselection, yselection] = 1    

    return lattice[xselection, yselection]


avgIdivN = np.zeros((len(p1),len(p3)))
datap1 = []
datap3 = []
dataz = []
for a in range(len(p3)):
    startp1 = time.time()
    
    for b in range(len(p1)):
        
        lattice = np.random.choice([1, 0, -1], size=(lx,ly), p=[1/3, 1/3, 1/3])
        I = []
        #print("this one: ,", p1[a], p3[b])
        for n in range(nstep):
            
            for i in range(lx):
                for j in range(ly):
                            
                    xselection = random.randint(0, lx-1)
                    yselection = random.randint(0, ly-1)
                    
                    updated_site = updateSite(lattice, xselection, yselection, lx, ly, p1[b], p2, p3[a])
                    
                    lattice[xselection, yselection] = updated_site
                    
            if n > 100:
                
                I.append(np.count_nonzero(lattice == 0))   
                
        #print(np.average(I))      
        avgIdivN[a][b]= np.average(I) / N
        
        datap1.append(p1[b])
        datap3.append(p3[a])
        dataz.append(np.average(I) / N)
        
    endp1 = time.time()
    print("This value of p3 took: ", endp1-startp1, " seconds")
    

#X, Y = np.meshgrid(p1, p3)      
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
cf2=ax3.contourf(avgIdivN)
ax3.set_title("Contour Plot")
fig3.colorbar(cf2, ax=ax3)
fig3.tight_layout()
plt.show()


data = {'p1': datap1, 'p3': datap3, 'Average number of infected sites': dataz}
col = ['p1', 'p3', 'Average number of infected sites']
df = pd.DataFrame(data, columns = col) # Create pandas dataframe

#print(df)

df.to_csv('DATA.csv', index=False) # Save data 

data1 = {'Map Values': avgIdivN.flatten()}
col1 = ['Map Values']
df1 = pd.DataFrame(data1, columns = col1) # Create pandas dataframe

#print(df1)

df1.to_csv('MapValues.csv', index=False) # Save data 

END = time.time()

print("Whole run took: ", END-START," seconds")
