#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 10:46:32 2024

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

df = pd.read_csv('ImmunityData.csv')

print(df)

f = df['Fraction of Immunity'].tolist()

avgIfrac = df['Average Infected Fraction'].tolist()


plt.scatter(f, avgIfrac, s=7, c='k', marker='s')
plt.xlim(0,1.0)
plt.ylim(0,0.3)

plt.xlabel("f")
plt.ylabel("Average Infected Fraction")
plt.show()
