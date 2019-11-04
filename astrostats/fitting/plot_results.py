#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np
import os.path as path
from scipy.stats import gaussian_kde, norm, gamma
import sys

proj_dir =  path.dirname(path.realpath(__file__))
sys.path.insert(0, proj_dir)
import tools

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

def trace_plot(chains, iters, labels, save_path):
    fig, ax = plt.subplots(1, 3, figsize=set_size(vfrac=0.45))

    for i, param in enumerate(chains.keys()):
        ax[i].plot(np.r_[:iters], chains[param], alpha=0.5)
        ax[i].set_xlim(0, iters)
        ax[i].set_xlabel('iteration')
        ax[i].set_ylabel(labels[i])

    fig.tight_layout()
    fig.savefig(save_path + '_trace', bbox_inches='tight')

def hist_plot(chains, labels, save_path):
    fig, ax = plt.subplots(1, 3, figsize=set_size(vfrac=0.45))

    for i, param in enumerate(chains.keys()):
        for col in range(chains[param].shape[1]):
            ax[i].hist(chains[param][:, col], alpha=0.5, density=True)
        ax[i].set_xlabel(labels[i])
        ax[i].set_ylabel('density')

    fig.tight_layout()
    fig.savefig(save_path + '_hist', bbox_inches='tight')

def kde_plot(chains, labels, save_path):
    fig, ax = plt.subplots(1, 3, figsize=set_size(vfrac=0.8))

    for i, param in enumerate(chains.keys()):
        x = np.linspace(chains[param].min(), chains[param].max(), num=200)
    
        # Plot prior beliefs
        if param.startswith('varphi'):
            ax[i].plot(x, norm.pdf(x, 0, 100), c='C1', label='prior beliefs' if i == 0 else "")
        else:
            ax[i].plot(x, gamma.pdf(x, 0.001, 1/0.001), c='C1',
              label='prior beliefs' if i == 0 else "")

        # Plot kde of posterior beliefs
        kernel = gaussian_kde(chains[param].flatten())
        ax[i].plot(x, kernel(x), c='C0', label='posterior beliefs' if i == 0 else "")
        ax[i].set_xlabel(labels[i])

    ax[0].set_ylabel('density')

    fig.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05), prop={'size': 8}, ncol=2)
    fig.tight_layout()
    fig.savefig(save_path + '_kde', bbox_inches='tight')

def data_plot(fit, df, save_path):
    fig, ax = plt.subplots(1, 1, figsize=set_size(hfrac=0.95))

    ax.set_ylabel('Sunspots')
    ax.set_xlabel('Year')

    y_pred = np.array(list(fit.extract('y_pred').values()))[0]
    y_pred[y_pred == -1] = np.nan
    # Plot 50% credible interval
    ax.fill_between(df.year[1:], np.percentile(y_pred, 25, axis=0),
                                 np.percentile(y_pred, 75, axis=0), color='C2', alpha=0.75,
                                 label = 'pred (50\% CI)')
    # Plot 95% credible interval
    ax.fill_between(df.year[1:], np.percentile(y_pred, 2.5, axis=0),
                                 np.percentile(y_pred, 97.5, axis=0), color='C2', alpha=0.3,
                                 label = 'pred (95\% CI)')

    # Plot posterior predictive mean
    ax.plot(df.year[1:], y_pred.mean(0), c='C1', label = 'pred (mean)', alpha=0.7,
            lw=0.75)
    # Plot data
    ax.scatter(df['year'], df['nspots'], c='C0', label = 'data', s=5, alpha=0.75)
    # Put a legend below current axis
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), prop={'size': 8}, ncol=4)

    ax.set_xlim(df['year'].min(), df['year'].max())

    fig.tight_layout()
    fig.savefig(save_path + '_post_fit', bbox_inches='tight')

def plot_all(fit, df, chains, model_name, plot_labels, proj_dir):
    iters = fit.stan_args[0]['iter'] - fit.stan_args[0]['warmup']

    save_path = path.join(proj_dir, 'out', '{}'.format(model_name))

    trace_plot(chains, iters, plot_labels, save_path)
    hist_plot(chains, plot_labels, save_path)
    kde_plot(chains, plot_labels, save_path)
    data_plot(fit, df, save_path)
    
if __name__ == "__main__":

    data, data_frame = tools.load_data(proj_dir)

    model_name = input("Name of model to fit (neg_bin or norm): ")
    param_names, plot_labels = tools.get_params(model_name)

    model, fit = tools.load_model_fit(model_name, proj_dir)
 
    chains = tools.extract_chains(fit, param_names)
    plot_all(fit, data_frame, chains, model_name, plot_labels, proj_dir)
