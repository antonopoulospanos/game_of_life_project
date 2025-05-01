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
import scipy
import pandas as pd

condition = str(input("Random (r), oscillator (o), glider (g) or beehive (b) initial condition?: ")) 
lx = 50
ly = lx

init_arr = np.zeros((lx, ly), dtype=float)

fig = plt.figure()
im = plt.imshow(init_arr, animated=True)

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

def beehiveCondition(array, lx, ly):
    
    centrey = int(ly/2)
    centrex = int(lx/2)
    
    array[(centrey-1), centrex] = 1
    array[(centrey+2), centrex] = 1
    array[centrey, (centrex-1)] = 1
    array[centrey, (centrex+1)] = 1
    array[(centrey+1), (centrex-1)] = 1
    array[(centrey+1), (centrex+1)] = 1
    
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
            
def CoM(current_state):
    
    blah = []
    xcm = np.sum(np.where(current_state==1)[0])/5
    ycm = np.sum(np.where(current_state==1)[1])/5
    #print(xcm,ycm)
    #cm = scipy.ndimage.center_of_mass(current_state)
    #print(cm)
    for i in range(len(np.where(current_state==1)[0])):
        blah.append(np.where(current_state==1)[0][i])
        #print(np.where(lattice==1)[0][i])
        
    for j in range(len(np.where(current_state==1)[1])):
        blah.append(np.where(current_state==1)[1][j])
    
  
    
    if 0 not in blah:
        if (lx-1) not in blah:
    
    
            return xcm, ycm

    
    

if condition == "r":
    
    lattice = randomCondition(init_arr, lx, ly)
    
elif condition == "o":
    
    lattice = oscillatorCondition(init_arr, lx, ly)
    
elif condition == "g":
    
    lattice = gliderCondition(init_arr, lx, ly)

elif condition == "b":
    
    lattice = beehiveCondition(init_arr, lx, ly)
    
t = []
num_alive = []
com = []
xcom = []
ycom = []
time_sweep = []

for n in range(180):
    
    t.append(n)
    
    #num_alive.append(numAlive(lattice))
    
    lattice = updateState(lattice, lx, ly)    
    
    
    
    if (n%4) == 0:
        
        output = CoM(lattice)
        
        if output is not None:
            
            #print(type(CoM(lattice)))
            xcom.append(output[0])
            ycom.append(output[1])
            time_sweep.append(n)
            #print(output[0], output[1])

      
        #       show animation
    plt.cla()
    im = plt.imshow(lattice, animated=True, vmin=0, vmax=1) # should i make different lattice names?
    plt.draw()
    plt.pause(0.001)

"""
deltay = ycom[-1]-ycom[0]
deltax = xcom[-1]-xcom[0]


velocity_every_four = deltay/deltax

velocity_every_sweep = velocity_every_four/4
"""
if condition == 'g':
    
    maxy = np.max(ycom)
    starty = ycom[0]
    maxx = np.max(xcom)
    startx = xcom[0]
    deltay = maxy-starty
    deltax = maxx-startx
    
    
    maxtime = time_sweep[np.argmax(ycom)]
    #print(maxtime)
    #print(time_sweep)
    mintime = time_sweep[0]
    
    deltat = maxtime-mintime
    
    velocity_x = deltax/deltat
    
    print("The glider velocity is :", velocity_x, " sites per sweep in the x direction")
    
    velocity_y = deltay/deltat
    
    print("The glider velocity is :", velocity_y, " sites per sweep in the y direction")
    
    speed = np.sqrt(velocity_x**2 + velocity_y**2)
    
    print("The glider speed is :", speed, " sites per sweep")
    
    #print(np.where(np.asarray(time_sweep)==maxtime))
    
    time = time_sweep[:np.where(np.asarray(time_sweep)==maxtime)[0][0]]
    x = xcom[:np.where(np.asarray(xcom)==maxx)[0][0]]
    
    gradient = np.polyfit(time,x, deg=1)[0]
    print(gradient)
    print("The glider velocity as calculated using polyfit is: ", gradient, " sites in x per sweep")
    
    #fig, ax = plt.subplots(1,1)
    
    #ax.scatter(xcom, ycom, s=2)
    
    #ax.set_xlabel("x")
    
    #ax.set_ylabel("y")
    
    
    #plt.show()
    
    fig1, ax1 = plt.subplots(1,1)
    
    ax1.scatter(time_sweep, xcom, s=2)
    
    ax1.set_xlabel("time")
    
    ax1.set_ylabel("xcom")
    
    
    plt.show()
    
    fig2, ax2 = plt.subplots(1,1)
    
    ax2.scatter(time_sweep, ycom, s=2)
    
    ax2.set_xlabel("time")
    
    ax2.set_ylabel("ycom")
    
    
    plt.show()
    
    data = {'Sweep': time_sweep,'X Centre of Mass': xcom, 
                'Y Centre of Mass': ycom} 
    
    col = ['Sweep', 'X Centre of Mass', 'Y Centre of Mass'] # Pandas dataframe parameters 
    
    df = pd.DataFrame(data, columns = col) # Create pandas dataframe
    
    df.to_csv('CoM.csv', index=False) # Save data 