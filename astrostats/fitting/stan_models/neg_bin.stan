data{
    int<lower=0> N;                // number of data points
    int<lower=0> K;                // number of coefficients
    int Y[N];                      // nuber of sunspots
}
parameters{
    vector[K] varphi;                    // linear predictor coefficients
    real<lower=0> theta;              // noise parameter
}
transformed parameters{
    vector[N] mu;
    
    mu[1] = Y[1];                     // set initial value

    for (t in 2:N) mu[t] = exp(varphi[1] + varphi[2] * Y[t - 1]);
}
model{
    // priors and likelihood
    theta ~ gamma(0.001, 0.001);
    for (i in 1:K) varphi[i] ~ normal(0, 100);

    Y ~ neg_binomial_2(mu, theta);
}
generated quantities{   
    vector[N-1] y_pred;

    // posterior predictions
    for (n in 1:(N-1)) {

        if (mu[n] > 3269017) {
            y_pred[n] = -1; 
        } else { 
            y_pred[n] = neg_binomial_2_rng(mu[n], theta);
        } 

    }
}

