#! /usr/bin/env python3

import os.path as path
import sys

proj_dir =  path.dirname(path.realpath(__file__))
sys.path.insert(0, proj_dir)

from make_table import fit2latex
from plot_results import plot_all
import tools

def save(model, fit):
    # Save model
    tools.save_pkl(model, path.join(proj_dir,
                                    'out',
                                    '{}_model.pkl'.format(model_name)))
    # Save fit
    tools.save_pkl(fit, path.join(proj_dir,
                                  'out',
                                  '{}_fit.pkl'.format(model_name)))

if __name__ == "__main__":
    data, data_frame = tools.load_data(proj_dir)

    model_name = input("Name of model to fit (neg_bin or norm): ")
    param_names, plot_labels = tools.get_params(model_name)

    # Run mcmc
    model = tools.StanModel_cache(model_name, proj_dir)
    fit = model.sampling(data=data, iter=7500, chains=4, n_jobs=-1, warmup=5000)

    save(model, fit)

    chains = tools.extract_chains(fit, param_names)
    plot_all(fit, data_frame, chains, model_name, plot_labels, proj_dir)
    fit2latex(fit, model_name, param_names, proj_dir)
