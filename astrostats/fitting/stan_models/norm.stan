data{
    int<lower=0> N;                // number of data points
    real Y[N];                     // number of sunspots at each data point
}
parameters{
    real alpha;                    // additive constant
    real varphi;                   // linear predictor coefficient
    real<lower=0> sigma;           // noise parameter
}
transformed parameters{
    vector[N] mu;

    mu[1] = Y[1];                  // set initial value

    for (t in 2:N) mu[t] = alpha + varphi * Y[t - 1];
}
model{
    // priors
    sigma ~ gamma(0.001, 0.001);
    alpha ~ normal(0, 100);
    varphi ~ normal(0, 100);

    // likelihood
    Y ~ normal(mu, sigma);
}
generated quantities{   
    vector[N-1] y_pred;

    // posterior predictions
    for (n in 1:(N-1))
        y_pred[n] = normal_rng(mu[n], sigma);
}

