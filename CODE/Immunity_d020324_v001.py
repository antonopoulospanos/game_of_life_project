#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 16:04:23 2024

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

nstep = 10000

# input

lx = int(input("Array size: "))

START = time.time()

p1 = 0.5
p2 = 0.5
p3 = 0.5

f = np.arange(0, 1.025, 0.025)

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


avgIfrac = []

for a in range(len(f)):
    startf = time.time()
     
    lattice = np.random.choice([1, 0, -1], size=(lx,ly), p=[1/3, 1/3, 1/3])
    
    for x in range(lx):
        for y in range(ly):

            r1 = random.random()
            if r1<=f[a]:
                lattice[x][y] = -2
    
    I = []
    #print("this one: ,", p1[a], p3[b])
    for n in range(nstep):
            
        for i in range(lx):
            for j in range(ly):
                            
                xselection = random.randint(0, lx-1)
                yselection = random.randint(0, ly-1)
                
                updated_site = updateSite(lattice, xselection, yselection, lx, ly, p1, p2, p3)
                    
                lattice[xselection, yselection] = updated_site
                    
        if n > 100:
                
            I.append(np.count_nonzero(lattice == 0))   
                
    avgIfrac.append(np.average(np.asarray(I))/N)

    endf = time.time()
    print("This value of f took: ", endf-startf, " seconds")
    
    

plt.scatter(f, avgIfrac, s=7, c='k', marker='s')

plt.xlabel("f")
plt.ylabel("Average Infected Fraction")
plt.show()


data = {'Fraction of Immunity': f, 'Average Infected Fraction': avgIfrac}
col = ['Fraction of Immunity', 'Average Infected Fraction']
df = pd.DataFrame(data, columns = col) # Create pandas dataframe

print(df)

df.to_csv('ImmunityData.csv', index=False) # Save data 

END = time.time()

print("Whole run took: ", END-START," seconds")