data{
    int<lower=0> N;                // number of data points
    int Y[N];                     // number of sunspots at each data point
}
parameters{
    real alpha;                    // additive constant
    real varphi;                   // linear predictor coefficient
    real<lower=0> theta;           // noise parameter
}
transformed parameters{
    vector[N] mu;
    
    mu[1] = Y[1];                     // set initial value

    for (t in 2:N) mu[t] = exp(alpha + varphi * Y[t - 1]);
}
model{
    // priors
    theta ~ gamma(0.001, 0.001);
    alpha ~ normal(0, 100);
    varphi ~ normal(0, 100);

    // likelihood
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

