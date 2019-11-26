#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

try:
    plt.style.use('metropolis')
except:
    plt.style.use('seaborn')

def sim_AR1(y, T, alpha, phi, sigma):
    y[0] = alpha
    noise = np.random.normal(0, sigma, size=T-1)
    for t in range(1, T):
        y[t] = alpha + phi * y[t - 1] + noise[t - 1]
    return y

# Number of timesteps
T = 1000
# Array to store data in
x = np.zeros((3, T))

# Parmaters
phi = np.array([0, 0.8, 0.95])
sigma = 1
alpha = 0

# Text for plots
phi_txt = [r"$\varphi_1={}$".format(val) for val in phi]

# Generate time series
for i in range(3):
    x[i] = sim_AR1(x[i], T, alpha, phi[i], sigma)

fig, ax = plt.subplots(3, 1, figsize=(6, 3))
ax = ax.reshape(3)

colours = ('C0', 'C1', 'C2', 'C3')
for i in range(3):
    ax[i].plot(np.r_[:T], x[i], color=colours[i])
    ax[i].set_xlim(0, T)
    ax[i].set_ylabel('$x$')
    ax[i].text(1.02, 0.5, phi_txt[i], transform=ax[i].transAxes, verticalalignment='center')

# Only need the xticks on the bottom plot
for i in range(2):
    ax[i].set_xticks([])
ax[2].set_xlabel('$t$')

fig.subplots_adjust(top=0.98, bottom=0.14, hspace=0.15, left=0.09, right=0.83)

fig.savefig('AR.pdf')
