#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  2 15:01:48 2024

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

p1 = np.arange(0.2, 0.51, 0.01)
p2 = 0.5
p3 = 0.5

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


def calcVariance(infectedarr, N):
    
    IsqAvg = np.average(infectedarr**2)
    avgIsq = np.average(infectedarr)**2
    
    variance = (IsqAvg-avgIsq)/N
    
    return variance


def bootstrap(func, array, N):
    
    k=1000
    results = [] # List to hold calculated heat capacity/ susceptibility values
    
    for i in range(k):
        
        indices = np.random.randint(0, len(array), size=len(array)) # Array of randomly generated indices
        samples = np.take(array, indices) # Sample the array (E or M) with the random indices
        func_output = func(samples, N) # Find the output of function (susceptibility, heat cap)
        results.append(func_output)
    
    samplesize = len(results)
    #error = np.std(np.asarray(results)) / np.sqrt(samplesize) # Calc standard error on mean for the error
    error = np.std(np.asarray(results)) # Calc standard error on mean for the error
    
    return error


var = []
varerror = []

for a in range(len(p1)):
    startp1 = time.time()
     
    lattice = np.random.choice([1, 0, -1], size=(lx,ly), p=[1/3, 1/3, 1/3])
    I = []
    #print("this one: ,", p1[a], p3[b])
    for n in range(nstep):
            
        for i in range(lx):
            for j in range(ly):
                            
                xselection = random.randint(0, lx-1)
                yselection = random.randint(0, ly-1)
                
                updated_site = updateSite(lattice, xselection, yselection, lx, ly, p1[a], p2, p3)
                    
                lattice[xselection, yselection] = updated_site
                    
        if n > 100:
                
            I.append(np.count_nonzero(lattice == 0))   
                
    
    Iarr = np.asarray(I)
    
    var.append(calcVariance(Iarr, N))
    varerror.append(bootstrap(calcVariance, Iarr, N))
    
    endp1 = time.time()
    print("This value of p1 took: ", endp1-startp1, " seconds")
    
    

plt.scatter(p1, var, s=7, c='k', marker='s')
plt.errorbar(p1, var, yerr=varerror, xerr=None, ls = "None", elinewidth = 1, ecolor = "black", capsize=3)
plt.xlabel("p1")
plt.ylabel("Variance")
plt.show()


data = {'p1': p1, 'Variance': var, 'Error on Variance': varerror}
col = ['p1', 'Variance', 'Error on Variance']
df = pd.DataFrame(data, columns = col) # Create pandas dataframe

print(df)

df.to_csv('DATAvarWerror.csv', index=False) # Save data 

END = time.time()

print("Whole run took: ", END-START," seconds")