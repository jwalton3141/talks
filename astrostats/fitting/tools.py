from hashlib import md5
import numpy as np
import os.path as path
import pandas as pd
import pickle
import pystan

def load_pkl(pkl_path):
    """ Load and return the pickle file located at path. """
    with open(pkl_path, 'rb') as f:
        x = pickle.load(f)
    return x

def save_pkl(obj, pkl_path):
    """ Save object to pkl_path. """
    with open(pkl_path, "wb") as f:
         pickle.dump(obj, f, protocol=-1)

def StanModel_cache(model_name, proj_dir, **kwargs):
    """ Automatically save and re-use compiled models where possible. """

    model_path = path.join(proj_dir, 'stan_models', '{}.stan'.format(model_name))

    # Load model as string
    try:
        with open(model_path, 'r') as f:
            model_code = f.read()
    except:
            print("{} not a valid model".format(model_name))    

    # Compute hash of model code
    code_hash = md5(model_code.encode('ascii')).hexdigest()
    # Get name of cached model
    cache_path = path.join(proj_dir, 
                           'stan_models',
                           'cached', 
                           'compiled-{}-{}.pkl'.format(model_name, code_hash))

    try:
        # Try load model
        sm = pickle.load(open(cache_path, 'rb'))
    except:
        # Model cache_fn couldn't be found so compile and save
        sm = pystan.StanModel(file=model_path, model_name=model_name, **kwargs)
        save_pkl(sm, cache_path)
    else:
        print("Using cached StanModel")

    return sm

def extract_chains(fit, param_names):
    """ Extract the chains specified by param_names from fit and return a dictionary of chains """
    params = [0] * len(param_names)

    for i, param in enumerate(param_names):
        params[i] = np.array(list(fit.extract(param, permuted=False).values()))[0]
    
    chains = {name : param for name, param in zip(param_names, params)}
    return chains

def load_data(proj_dir):
    """ Load sunspot data and prepare it for inference. """
    path_to_data = path.join(proj_dir, 'data.csv')

    # read data
    data_frame = pd.read_csv(path_to_data)

    # prepare data for Stan
    data = {}
    data['Y'] = [int(round(item)) for item in data_frame['nspots']]
    data['N'] = len(data['Y'])

    return data, data_frame

def get_params(model_name):
    """ Return the names of the parameters for the given model """

    if model_name == 'norm':
        plot_labels = [r'$\alpha$', r'$\varphi$', r'$\sigma$']
        param_names = ['alpha', 'varphi', 'sigma']
    elif model_name == 'neg_bin':
        plot_labels = [r'$\alpha$', r'$\varphi$', r'$\theta$']
        param_names = ['alpha', 'varphi', 'theta']

    return param_names, plot_labels

def load_model_fit(model_name, proj_dir):
    """ Load the pickled model and fit. """

    model = load_pkl(path.join(proj_dir,
                               'out',
                               '{}_model.pkl'.format(model_name)))
    fit = load_pkl(path.join(proj_dir,
                             'out',
                             '{}_fit.pkl'.format(model_name)))

    return model, fit
