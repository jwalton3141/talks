#!/usr/bin/env python3

import os.path as path
import matplotlib.pyplot as plt
import pandas as pd

try:
    plt.style.use('metropolis')
except:
    plt.style.use('seaborn')

def set_size(width_pt=398.3386, hfrac=1, vfrac=1):

    # Width of figure
    fig_width_pt = width_pt * hfrac

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * vfrac

    return [fig_width_in, fig_height_in]

def plot_raw_data(df, save_path):
    fig, ax = plt.subplots(1, 1, figsize=set_size(hfrac=0.95, vfrac=0.95))

    ax.set_ylabel('Sunspots')
    ax.set_xlabel('Year')

    ax.scatter(df['year'], df['nspots'], c='C0', s=9)
    ax.plot(df['year'], df['nspots'], c='C0')

    ax.set_xlim(df['year'].min(), df['year'].max())

    fig.tight_layout()
    fig.savefig(save_path, bbox_inches='tight')

if __name__ == "__main__":
    path_to_data = path.join('../', 'fitting', 'data.csv')
    data_frame = pd.read_csv(path_to_data)

    filename = 'data.pdf'
    plot_raw_data(data_frame, filename)
