# About

I originally gave this talk to Newcastle University's applied 
maths department in October 2019. The talk was intended to give 
an introduction to Bayesian statistics to the uninitiated. With 
the aim of showcasing the Bayesian paradigm, an astrophysically 
motivated case study was then given. 

## Using this code

Having cloned this repo, all the code should work as-is. Though 
you'll likely have to `pip install pystan` before getting going (and 
maybe a couple of other packages if you don't use python much).

The script `fitting/run_infer.py` will prompt for the name of the 
model you'd like to fit. The options here are `norm` and `neg_bin`. 
All the plots and tables generated will be saved in the directory 
`fitting/out/`. Once you have run `fitting/run_infer.py` for `norm` 
and `neg_bin` you will have all the output you need to compile 
`astrostats.tex`.

## References

I took much inspiration from the book "Bayesian models for
 astrophysical data: using R, JAGS, Python, and Stan." and in fact
the code in `fitting/stan_models/neg_bin.stan` was taken verbatim
from the book.

