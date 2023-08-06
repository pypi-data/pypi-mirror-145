#!/usr/bin/env python
# coding: utf-8

# ## Using non-linear inequality constraints in Ax
# This notebook comes with the following caveats:
# 1. The search space has to be [0, 1]^d
# 2. We need to pass in explicit `batch_initial_conditions` that satisfy the non-linear inequality constraints as starting points for optimizing the acquisition function.
# 3. BATCH_SIZE must be equal to 1.

# In[1]:


import random

import torch
from ax import Data, Experiment, ParameterType, RangeParameter, SearchSpace
from ax.modelbridge.registry import Models
from ax.runners.synthetic import SyntheticRunner
from torch.quasirandom import SobolEngine


# In[2]:


from ax.core.objective import Objective
from ax.core.optimization_config import OptimizationConfig
from ax.metrics.hartmann6 import Hartmann6Metric


search_space = SearchSpace(
    parameters=[
        RangeParameter(name=f"x{i}", parameter_type=ParameterType.FLOAT, lower=0.0, upper=1.0) for i in range(6)
    ]
)

optimization_config = OptimizationConfig(
    objective=Objective(
        metric=Hartmann6Metric(
            name="objective",
            param_names=[f"x{i}" for i in range(6)],
            noise_sd=0.0,
        ),
        minimize=True,
    )
)


# We want to optimize $f_{\text{hartmann6}}(x)$ subject to an additional constraint $|| x ||_0 <= 3$. 
# 
# This constraint isn't differentiable, but it can be approximated by a differentiable relaxation using a sum of narrow Gaussian basis functions. 
# Given a univariate Gaussian basis function $g_{\ell}(x)$ centered at zero with $\ell > 0$ small, 
# we can approximate the constraint by: $|| x ||_0 \approx 6 - \sum_{i=1}^6 g_{\ell}(x_i) \leq 3$, which reduces to $\sum_{i=1}^6 g_{\ell}(x_i) \geq 3$.

# In[3]:


def narrow_gaussian(x, ell):
    return torch.exp(-0.5 * (x / ell) ** 2)


def ineq_constraint(x, ell=1e-3):
    # Approximation of || x ||_0 <= 3. The constraint is >= 0 to conform with SLSQP
    return narrow_gaussian(x, ell).sum(dim=-1) - 3


# ## BO-loop

# In[4]:


from botorch.acquisition import ExpectedImprovement
from botorch.fit import fit_gpytorch_model
from botorch.models import SingleTaskGP
from botorch.models.transforms import Standardize
from gpytorch.mlls import ExactMarginalLogLikelihood
from torch.nn.functional import normalize


def get_batch_initial_conditions(n, X, Y, raw_samples):
    """Generate starting points for the acquisition function optimization."""
    # 1. Draw `raw_samples` Sobol points and randomly set three parameters to zero to satisfy the constraint
    X_cand = SobolEngine(dimension=6, scramble=True).draw(raw_samples).to(torch.double)
    inds = torch.argsort(torch.rand(raw_samples, 6), dim=-1)[:, :3]
    X_cand[torch.arange(X_cand.shape[0]).unsqueeze(-1), inds] = 0
    X_cand = normalize(X_cand, p=1.0, dim = 0)

    # 2. Fit a GP to the observed data, the right thing to do is to use the Ax model here
    gp = SingleTaskGP(X, Y, outcome_transform=Standardize(m=1))
    mll = ExactMarginalLogLikelihood(gp.likelihood, gp)
    fit_gpytorch_model(mll)

    # 3. Use EI to select the best points. Ideally, we should use the Ax acquisition function here as well
    EI = ExpectedImprovement(model=gp, best_f=Y.min(), maximize=False)
    X_cand = X_cand.unsqueeze(1)
    acq_vals = EI(X_cand)
    return X_cand[acq_vals.topk(n).indices]


# In[5]:


N_INIT = 10
BATCH_SIZE = 1
N_BATCHES = 20
print(f"Doing {N_INIT + N_BATCHES * BATCH_SIZE} evaluations")


# In[6]:


import warnings


# Experiment
experiment = Experiment(
    name="saasbo_experiment",
    search_space=search_space,
    optimization_config=optimization_config,
    runner=SyntheticRunner(),
)

# Initial Sobol points (set three random parameters to zero)
sobol = Models.SOBOL(search_space=experiment.search_space)
for _ in range(N_INIT):
    trial = sobol.gen(1)
    keys = [f"x{i}" for i in range(6)]
    random.shuffle(keys)
    for k in keys[:3]:
        trial.arms[0]._parameters[k] = 0.0
    experiment.new_trial(trial).run()

# Run SAASBO
data = experiment.fetch_data()
for i in range(N_BATCHES):
    model = Models.FULLYBAYESIAN(
        experiment=experiment,
        data=data,
        num_samples=256,  # Increasing this may result in better model fits
        warmup_steps=512,  # Increasing this may result in better model fits
        gp_kernel="matern",  # "rbf" is the default in the paper, but we also support "matern"
        torch_dtype=torch.double,
        verbose=False,  # Set to True to print stats from MCMC
        disable_progbar=True,  # Set to False to print a progress bar from MCMC
    )
    batch_initial_conditions = get_batch_initial_conditions(
        n=20, X=model.model.Xs[0], Y=model.model.Ys[0], raw_samples=1024
    )
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # Filter SLSQP warnings
        generator_run = model.gen(
            BATCH_SIZE,
            model_gen_options={
                "optimizer_kwargs": {
                    "nonlinear_inequality_constraints": [ineq_constraint],
                    "batch_initial_conditions": batch_initial_conditions,
                }
            },
        )
        
    trial = experiment.new_batch_trial(generator_run=generator_run)
    for arm in trial.arms:
        arm._parameters = {k: 0.0 if v < 1e-3 else v for k, v in arm.parameters.items()}
        assert sum([v > 1e-3 for v in arm.parameters.values()]) <= 3
    trial.run()
    data = Data.from_multiple_data([data, trial.fetch_data()])

    new_value = trial.fetch_data().df["mean"].min()
    print(
        f"Iteration: {i}, Best in iteration {new_value:.3f}, Best so far: {data.df['mean'].min():.3f}"
    )


# In[ ]:


experiment.arms_by_name

