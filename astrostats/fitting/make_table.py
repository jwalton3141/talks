#!/usr/bin/env python3

from io import StringIO
import os.path as path
import pandas as pd
from pystan.misc import _summary, _array_to_table
import sys
import re

proj_dir =  path.dirname(path.realpath(__file__))
sys.path.insert(0, proj_dir)
import tools

def rename_cols(df):
    newcols = list(df.columns.values)

    # Rename n_eff to ESS
    newcols[3] = "ESS"

    # Percentage symbol must be escaped in tex
    newcols = [col.replace('%', '\%') for col in newcols]

    # colnames must be wrapped in curly bois to stop siuntix trying to parse them
    newcols = [r'{{{}}}'.format(col) for col in newcols]

    # Rename columns
    df = df.rename(index=str,
                   columns={old : new for old, new in zip(df.columns.values, newcols)})
    return df

def rename_rows(df):
    newrows = df.index.values

    # Typeset rownames in math mode
    newrows = '$' + newrows + '$'
    newrows = '\n'.join(newrows)

    # Elements of paramater object should be subscripted
    newrows = re.sub('\[(.*)\]', '_{\\1}', newrows, flags=re.MULTILINE)
    newrows = re.sub('$\\$', r'\$\\', newrows, flags=re.MULTILINE)

    for letter in ['varphi', 'sigma', 'theta']:
        newrows = re.sub(letter, '\\\\' + letter, newrows, flags=re.MULTILINE)

    newrows = newrows.split('\n')
    df = df.rename({old : new for old, new in zip(df.index.values, newrows)})

    return df

def format_cols(df):
    for col in ['mean', "2.5%", "97.5%"]:
        df[col] = df[col].astype(float).apply('{:05.2f}'.format).astype(str)
    return df

def fit2latex(fit, model_name, params, proj_dir):
    s = _summary(fit, params, [0.025, 0.975])
    body = _array_to_table(s['summary'], s['summary_rownames'], s['summary_colnames'], 2)

    # Convert string to dataframe
    df = pd.read_fwf(StringIO(body), dtype=str, index_col=0)
    # Drop columns we don't care about
    df = df.drop(["se_mean", "sd", "Rhat"], axis=1)
    df = format_cols(df)

    # Round the ESS to the nearest 10
    df["n_eff"] = df["n_eff"].astype(int) // 100 * 100

    # Tidy up column and row names for tex
    df = rename_cols(df)
    df = rename_rows(df)

    df = df.rename_axis('{Parameter}', axis=1)

    # Column formatting. The S column type is provided by siunitx
    col_format = "@{}cS[table-format=2.2]S[table-format=2.2]S[table-format=2.2]r@{}"
    # Print dataframe to latex
    tex = df.to_latex(escape=False,
                      column_format=col_format)

    save_path = path.join(proj_dir, 'out', '{}'.format(model_name))

    with open(save_path + '.tab', "w") as file:
        file.write(tex)

if __name__ == "__main__":

    model_name = input("Name of model to fit (neg_bin or norm): ")
    param_names, plot_labels = tools.get_params(model_name)
    
    model, fit = tools.load_model_fit(model_name, proj_dir)

    fit2latex(fit, model_name, param_names, proj_dir)
