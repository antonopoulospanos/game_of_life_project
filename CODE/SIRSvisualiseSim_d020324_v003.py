#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 11:41:06 2024

@author: panosantonopoulos
"""

import matplotlib

#matplotlib.use('TKAgg')

import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


nstep = 10000

# input

lx = int(input("Array size: "))
p1 = float(input("P1: "))
p2 = float(input("P2: "))
p3 = float(input("P3: "))

ly = lx

lattice = np.random.choice([1, 0, -1], size=(lx,ly), p=[1/3, 1/3, 1/3])

fig = plt.figure()
im = plt.imshow(lattice, animated=True)

def updateSite(lattice, xselection, yselection, lx, ly, p1, p2, p3):
    
    site = lattice[xselection, yselection]
    
    if site == 1: # 1 is susceptible 
        
        upperneighbour = lattice[(xselection-1)%lx, yselection]
        lowerneighbour = lattice[(xselection+1)%lx, yselection]
        rightneighbour = lattice[xselection, (yselection+1)%ly]
        leftneighbour = lattice[xselection, (yselection-1)%ly]
        
        if 0 in (upperneighbour, lowerneighbour, rightneighbour, leftneighbour):
            
            r = random.random()
            if r <= p1:
                
                lattice[xselection, yselection] = 0
    
    elif site == 0: # 0 is infected
        
        r = random.random()
        if r <= p2:
            
            lattice[xselection, yselection] = -1
            
    elif site == -1: # -1 is recovered 
        
        r = random.random()
        if r <= p3:
            
            lattice[xselection, yselection] = 1    

    return lattice[xselection, yselection]


for n in range(nstep):
    for i in range(lx):
        for j in range(ly):
                    
            xselection = random.randint(0, lx-1)
            yselection = random.randint(0, ly-1)
            
            updated_site = updateSite(lattice, xselection, yselection, lx, ly, p1, p2, p3)
            
            lattice[xselection, yselection] = updated_site
            
    if (n % 5 == 0):
                #       update measurements
                #       dump output (e.g., for gnuplot)
                

                #       show animation
        plt.cla()
        im = plt.imshow(lattice, animated=True)
        plt.draw()
        plt.pause(0.00001)
            