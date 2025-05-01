#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 11 14:53:26 2024

@author: panosantonopoulos
"""

import matplotlib

#matplotlib.use('TKAgg')

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import pandas as pd

#condition = str(input("Random (r), oscillator (o) or glider (g) initial condition?: ")) 
lx = 50
ly = lx

#init_arr = np.zeros((lx, ly), dtype=float)
"""
fig = plt.figure()
im = plt.imshow(init_arr, animated=True)
"""
def randomCondition(array, lx, ly):
    
    for i in range(lx):
        for j in range(ly):
            r = random.random()
            #if (r < 0.5): array[i, j] = 0
            if (r >= 0.5): 
                
                array[i, j] = 1
            
    return array
    
     
def oscillatorCondition(array, lx, ly):
    
    midy = int(ly/2)
    x = int(lx/2)
    
    array[(midy-1), x] = 1
    array[midy, x] = 1
    array[(midy+1), x] = 1
    
    return array
     
    
def gliderCondition(array, lx, ly):
    
    basey = int(ly/2)
    bottom_midx = int(lx/2)
    
    array[basey, (bottom_midx-1)] = 1
    array[basey, bottom_midx] = 1
    array[basey, (bottom_midx+1)] = 1
    array[(basey-1), (bottom_midx+1)] = 1
    array[(basey-2), bottom_midx] = 1
    
    return array

def updateState(current_state, lx, ly):
    
    new_state = current_state.copy()
    
    for i in range(lx):
        
        for j in range(ly):
            
            num_alive_nn = ( current_state[(i-1)%lx, j] + current_state[i, (j-1)%ly]
                            + current_state[(i+1)%lx, j] + current_state[i, (j+1)%ly]
                            + current_state[(i+1)%lx, (j+1)%ly] + current_state[(i+1)%lx, (j-1)%ly]
                            + current_state[(i-1)%lx, (j+1)%ly] + current_state[(i-1)%lx, (j-1)%ly] )
            
            if current_state[i,j] == 1:
                
                if num_alive_nn == 2 or num_alive_nn == 3:
                    
                    new_state[i,j] = 1
                
                elif num_alive_nn < 2 or num_alive_nn > 3:
                    
                    new_state[i,j] = 0

            elif current_state[i,j] == 0:
                
                if num_alive_nn == 3:
                    
                    new_state[i,j] = 1
                    
    return new_state

def numAlive(current_state):
    
    num = 0
    
    for i in range(lx):
        
        for j in range(ly):
            
            num = num + current_state[i,j]
            
    return num
            




num_steps = []
sim = []

for k in range(1000):
    
    start = time.time()
    init_arr = np.zeros((lx, ly), dtype=float)
    lattice = randomCondition(init_arr, lx, ly)
        
    duration = 0

    for steps in range(5000):
        
        num_previous = numAlive(lattice)
        
        lattice = updateState(lattice, lx, ly)   
        
        num_current = numAlive(lattice)
        
        if num_previous == num_current:
            
            duration = duration + 1
            
        else:
            
            duration = 0
        
        if duration >= 10:
            
            num_steps.append(steps)
            sim.append(k)
            break
        

            

    end = time.time()
    
    #print(num_steps)
    
    print("Sim ", k, " needed ", steps, "steps to equilibrate, which took ", end-start, " seconds")
    
    #sim.append(k)
    
binedges = np.arange(0, 5000, step=200)

fig1 = plt.figure()
counts, bins, plot = plt.hist(num_steps, bins=binedges)
plt.xlabel("Time to steady state/absorption (sweeps)")
plt.ylabel("Counts")

plt.show()
fig2 = plt.figure()
plt.stairs(counts/10, bins)
plt.xlabel("Time to steady state/absorption (sweeps)")
plt.ylabel("Probability (%)")
plt.show()

data = {'Simulation run': sim, 
            'Number of steps to equilibrate': num_steps} 

col = ['Simulation run', 'Number of steps to equilibrate'] # Pandas dataframe parameters 
print(len(sim))
print(len(num_steps))

df = pd.DataFrame(data, columns = col) # Create pandas dataframe

df.to_csv('DATA.csv', index=False) # Save data 

        
      
        
        


