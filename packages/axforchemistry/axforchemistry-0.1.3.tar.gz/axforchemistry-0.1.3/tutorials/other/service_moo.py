"""Bayesian optimization of dental composite compositions.

Initial Testing and Functionality
TODO: create appropriate directory structure (tests, utils, etc.)
TODO: write test functions (for fractional_encode, fractional_decode, etc.)
TODO: incorporate tests into GitHub actions
TODO: convert to class structure
TODO: split code into two repos: general code and Ultradent-specific code
TODO: use multi-objective optimization to limit number of components (or
single-objective with an objective that gets smaller with higher complexity)
TODO: compare with "choices" version (hard-coded to e.g. no more than 5 components)

Code Deployment
TODO: update README.md
TODO: code documentation
TODO: make general repo public
TODO: package on PyPI and Anaconda
TODO: incorporate packaging into GitHub actions
TODO: connect documentation with readthedocs
TODO: add badges to README

Future Work
TODO: incorporate domain knowledge (i.e. user-specified feature vectors)
"""

# %% imports
import numpy as np
import pandas as pd

# from sklearn.preprocessing import OneHotEncoder
# from sklearn.preprocessing import normalize
# from sklearn.ensemble import RandomForestRegressor

from ax.modelbridge.generation_strategy import GenerationStrategy, GenerationStep
from ax.modelbridge.registry import Models

# from ax.service.managed_loop import optimize
from ax.service.ax_client import AxClient

# from ax.service.utils.instantiation import ObjectiveProperties

from axforchemistry.utils.fractional import (
    fractional_encode,
    fractional_decode,
    append_last_component,
    count_nonzero_components,
)

unique_components = ["filler_A", "filler_B", "resin_A", "resin_B", "resin_C"]

dummy = False

if dummy:

    components = np.array(
        [
            ["filler_A", "filler_B", "resin_C"],
            ["filler_A", "resin_B"],
            ["filler_A", "filler_B", "resin_B"],
            ["filler_A", "resin_B", "resin_C"],
            ["filler_B", "resin_A", "resin_B"],
            ["filler_A", "resin_A"],
            ["filler_B", "resin_A", "resin_B"],
        ],
        dtype=object,
    )

    compositions = np.array(
        [
            [0.4, 0.4, 0.2],
            [0.5, 0.5],
            [0.5, 0.3, 0.2],
            [0.5, 0.5, 0.0],
            [0.6, 0.4, 0.0],
            [0.6, 0.4],
            [0.6, 0.2, 0.2],
        ],
        dtype=object,
    )

    X_train = fractional_encode(components, compositions)

else:
    X_train = pd.read_csv("train.csv")
    # convert percent to fraction
    X_train = X_train / 100
    # X_train = X_train.iloc[:, 0:10]
    last_component = pd.DataFrame(1 - X_train.sum(axis=1), columns=["last_component"])
    X_train = pd.concat((X_train, last_component), axis=1)
    unique_components = list(X_train.columns)
    components, compositions = fractional_decode(X_train)

np.random.seed(10)
y_train = 100 * np.random.rand(len(components))

n_train = X_train.shape[0]

n_components = count_nonzero_components(X_train).astype("float")

if not np.allclose(np.sum(X_train, axis=1), 1):
    raise ValueError(
        "rows of X_train do not sum to 1 within tolerance (i.e. composition is not close to unity for at least one row)."
    )

# Ax-specific
parameters = [
    {"name": component, "type": "range", "bounds": [0.0, 1.0]}
    for component in unique_components[:-1]
]

separator = " + "
composition_constraint = separator.join(unique_components[:-1]) + " <= 0.5"

# %% optimize
gs = GenerationStrategy(
    steps=[
        # 2. Bayesian optimization step (requires data obtained from previous phase and learns
        # from all data available at the time of each new candidate generation call)
        GenerationStep(
            model=Models.GPEI,
            num_trials=-1,  # No limitation on how many trials should be produced from this step
            max_parallelism=3,  # Parallelism limit for this step, often lower than for Sobol
            # More on parallelism vs. required samples in BayesOpt:
            # https://ax.dev/docs/bayesopt.html#tradeoff-between-parallelism-and-total-number-of-trials
        ),
    ]
)
ax_client = AxClient(generation_strategy=gs)
ax_client.create_experiment(
    name="ultradent",
    parameters=parameters,
    parameter_constraints=[
        composition_constraint,
    ],
    objective_name="y_train",
    outcome_constraints=["n_components <= 18.0"],
    # objectives={
    #     "strength": ObjectiveProperties(minimize=False),
    #     "n_components": ObjectiveProperties(minimize=True, threshold=(1, 7)),
    # },
    minimize=True,
)

for i in range(n_train):
    ax_client.attach_trial(X_train.iloc[i, :-1].to_dict())
    ax_client.complete_trial(
        trial_index=i, raw_data={"y_train": y_train[i], "n_components": n_components[i]}
    )

next_experiment, trial_index = ax_client.get_next_trial()
print("next suggested experiment: ", next_experiment)

# best_parameters, metrics = ax_client.get_best_parameters()

next_experiment = append_last_component(next_experiment, unique_components)
print(next_experiment)

1 + 1

# %% Code Graveyard
