"""Bayesian optimization using sequential search spaces."""
# %% imports
import numpy as np
import pandas as pd
from ax.modelbridge.generation_strategy import GenerationStep, GenerationStrategy
from ax.modelbridge.registry import Models
from ax.models.torch.botorch_modular.surrogate import Surrogate
from ax.service.ax_client import AxClient

from botorch.acquisition.monte_carlo import qNoisyExpectedImprovement
from botorch.models.gp_regression import SingleTaskGP

batch_size = 1

unique_components = ["Al", "Co", "Cr", "Cu", "Fe", "Ni"]

compositions = np.array(
    [
        [18.2, 9.1, 18.2, 18.2, 18.2, 18.2],
        [18.2, 18.2, 9.1, 18.2, 18.2, 18.2],
        [18.2, 18.2, 18.2, 18.2, 9.1, 18.2],
        [18.2, 18.2, 18.2, 18.2, 18.2, 9.1],
        [5.3, 21.1, 21.1, 0, 26.3, 26.3],
        [12.5, 12.5, 12.5, 0, 12.5, 50],
    ],
)

X_train = pd.DataFrame(compositions, columns=unique_components)
# normalize https://stackoverflow.com/a/35679163/13697228
X_train = X_train.div(X_train.sum(axis=1), axis=0)
X_train = X_train.iloc[:, :-1]  # drop "Ni"
unique_components = unique_components[:-1]
np.random.seed(10)
y_train = 100 * np.random.rand(X_train.shape[0])

exp_name = "dummy_experiment"
target_name = "dummy"

n_components = X_train.shape[1]
n_train = X_train.shape[0]

orig_max_val = 1.0
max_val = 0.196

orig_parameters = [
    {"name": component, "type": "range", "bounds": [0.0, orig_max_val]}
    for component in unique_components[:-1]
]
parameters = [
    {"name": component, "type": "range", "bounds": [0.0, max_val]}
    for component in unique_components[:-1]
]

separator = " + "
orig_comp_constraint = separator.join(unique_components[:-1]) + f" <= {orig_max_val}"
composition_constraint = separator.join(unique_components[:-1]) + f" <= {max_val}"

# %% optimize
gs = GenerationStrategy(
    steps=[
        GenerationStep(
            model=Models.BOTORCH_MODULAR,
            num_trials=-1,  # No limitation on how many trials should be produced from this step
            max_parallelism=batch_size,  # Parallelism limit for this step, often lower than for Sobol
            # More on parallelism vs. required samples in BayesOpt:
            # https://ax.dev/docs/bayesopt.html#tradeoff-between-parallelism-and-total-number-of-trials
            model_kwargs={
                # https://github.com/facebook/Ax/issues/768#issuecomment-1009007526
                "fit_out_of_design": True,
                "surrogate": Surrogate(SingleTaskGP),
                "botorch_acqf_class": qNoisyExpectedImprovement,
            },
        ),
    ]
)

ax_client = AxClient(generation_strategy=gs)
ax_client.create_experiment(
    name=exp_name,
    parameters=orig_parameters,
    parameter_constraints=[orig_comp_constraint],
    objective_name=target_name,
    minimize=True,
    immutable_search_space_and_opt_config=False,
)

ax_client_tmp = AxClient(generation_strategy=gs)
ax_client_tmp.create_experiment(
    name=exp_name,
    parameters=parameters,
    parameter_constraints=[composition_constraint],
    objective_name=target_name,
    minimize=True,
    immutable_search_space_and_opt_config=False,
)

ct = 0
for i in range(n_train):
    ax_client.attach_trial(X_train.iloc[i, :-1].to_dict())
    ax_client.complete_trial(trial_index=ct, raw_data=y_train[i])
    ct = ct + 1

# narrow the search space
ax_client.experiment.search_space = ax_client_tmp.experiment.search_space

for _ in range(15):
    parameters, trial_index = ax_client.get_next_trial()
    ax_client.complete_trial(trial_index=trial_index, raw_data=np.random.rand()

best_parameters, metrics = ax_client.get_best_parameters()
