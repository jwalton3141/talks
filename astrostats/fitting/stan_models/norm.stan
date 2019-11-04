data{
    int<lower=0> N;                // number of data points
    int<lower=0> K;                // number of coefficients
    real Y[N];                     // number of sunspots
}
parameters{
    vector[K] varphi;                    // linear predictor coefficients
    real<lower=0> sigma;              // noise parameter
}
model{
    vector[N] mu;

    mu[1] = Y[1];                     // set initial value

    for (t in 2:N) mu[t] = varphi[1] + varphi[2] * Y[t - 1];
    // priors and likelihood
    sigma ~ gamma(0.001, 0.001);
    for (i in 1:K) varphi[i] ~ normal(0, 100);

    Y ~ normal(mu, sigma);
}
generated quantities{   
    vector[N-1] y_pred;

    // posterior predictions
    for (n in 1:(N-1))
        y_pred[n] = normal_rng(varphi[1] + varphi[2] * Y[n], sigma);
}

