import arviz as az
import matplotlib.pyplot as plt
import numpy as np
import pymc3 as pm
import theano.tensor as tt
import numpy as np
from pymc3.gp.util import plot_gp_dist

from ..data import Aubry

def GP_example():

    Aubry.set_vars(xvar='H', yvar='Q')

    x = Aubry.x
    y = Aubry.y

    with pm.Model() as model:
        rho = pm.HalfCauchy('rho', 0.5)
        eta = pm.HalfCauchy('eta', 3)
        b0 = pm.Normal('b0', 10)
        b1_0 = pm.Normal('b1_0', 1)
        b1 = pm.Deterministic('b1', b1_0+4)
        M = pm.gp.mean.Linear(coeffs=b1, intercept=b0)
        K = eta*pm.gp.cov.Matern52(1, rho)
        gp = pm.gp.Marginal(mean_func=M, cov_func=K)
        s = pm.HalfNormal('s', 50)
        gp = pm.gp.Marginal(mean_func=M, cov_func=K)
        gp.marginal_likelihood('y', X=x[:,None], y=y, noise=s)

        trace = pm.sample(2000, tune=2000, cores=2, random_seed=42, return_inferencedata=True)

    with model:
        az.plot_trace(trace)
        plt.show()


    xp = np.linspace(x.min(), x.max(), 100).reshape(-1,1)
    with model:
        y_pred = gp.conditional('y_pred', xp)
        y_pred_noise = gp.conditional('y_pred_noise', xp, pred_noise=True)
        y_s = pm.sample_posterior_predictive(trace, var_names=['y_pred', 'y_pred_noise'], samples=5000, random_seed=42)


    fig1, ax1 = plt.subplots()
    plot_gp_dist(ax1, y_s['y_pred'], np.power(10,xp))
    ax1.scatter(np.power(10,x),y,c='k',s=50)

    fig2, ax2 = plt.subplots()
    plot_gp_dist(ax2, y_s['y_pred_noise'], np.power(10,xp), palette='Blues')
    ax2.scatter(np.power(10,x),y,c='k',s=50)

    plt.show()