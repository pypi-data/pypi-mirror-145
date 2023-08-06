"""Ax Service API.

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
from tqdm import tqdm

import numpy as np
import pandas as pd

from ax.modelbridge.generation_strategy import GenerationStrategy, GenerationStep
from ax.modelbridge.registry import Models

# from ax.service.managed_loop import optimize
from ax.service.ax_client import AxClient

from axforchemistry.utils.fractional import (
    fractional_encode,
    fractional_decode,
    count_nonzero_components,
)

from axforchemistry.utils.data import fill_missing_keys, gen_symmetric_trials

filler_names = ["filler_A", "filler_B"]
resin_names = ["resin_A", "resin_B", "resin_C"]
unique_components = filler_names + resin_names

dummy = True

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

    unique_components = list(X_train.columns)
    components, compositions = fractional_decode(X_train, sort=True)

    last_component = pd.DataFrame(1 - X_train.sum(axis=1), columns=["last_component"])
    X_train = pd.concat((X_train, last_component), axis=1)

np.random.seed(10)
y_train = 100 * np.random.rand(len(components))

n_train = X_train.shape[0]

n_components = count_nonzero_components(X_train).astype("float")

if not np.allclose(np.sum(X_train, axis=1), 1):
    raise ValueError(
        "rows of X_train do not sum to 1 within tolerance (i.e. composition is not close to unity for at least one row)."
    )

# Ax-specific
nslots = 5
component_slot_names = ["component_slot_" + str(i) for i in range(nslots)]
component_slots = []
for (i, component_slot_name) in enumerate(component_slot_names):
    # if i == 0:
    #     values = filler_names
    # elif i == 1:
    #     values = resin_names
    # else:
    values = unique_components

    component_slots.append(
        {
            "name": component_slot_name,
            "type": "choice",
            "values": values,
        }
    )
composition_slot_names = ["composition_slot_" + str(i) for i in range(nslots)]
composition_slots = [
    {"name": composition_slot_name, "type": "range", "bounds": [0.0, 1.0]}
    for composition_slot_name in composition_slot_names
]
parameters = component_slots + composition_slots

separator = " + "
unity_constraint = separator.join(composition_slot_names[:-1]) + " <= 1.0"

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
ax_client = AxClient(generation_strategy=gs, verbose_logging=False)
ax_client.create_experiment(
    name="ultradent",
    parameters=parameters,
    parameter_constraints=[unity_constraint],
    minimize=True,
)

j = 0
for i in tqdm(range(n_train)):
    # TODO: augment data (ABC, ACB, BCA, ..., AAB, ABA, ACA, CAA, ..., AAA, ...)
    component_dict = {
        component_slot_name: component
        for (component_slot_name, component) in zip(component_slot_names, components[i])
    }
    composition_dict = {
        composition_slot_name: component
        for (composition_slot_name, component) in zip(
            composition_slot_names, compositions[i]
        )
    }

    data = fill_missing_keys(
        component_dict,
        composition_dict,
        component_slot_names,
        composition_slot_names,
        unique_components,
    )

    # TODO: filter out trials that put resin in slot 1 or filler in slot 2
    comb_data = gen_symmetric_trials(data, component_slot_names, composition_slot_names)

    for subdata in comb_data:
        ax_client.attach_trial(subdata)
        ax_client.complete_trial(trial_index=j, raw_data=y_train[i])
        j += 1

next_experiment, trial_index = ax_client.get_next_trial()
print("[Next Suggested Experiment]")
print(pd.DataFrame(next_experiment, index=[0]).transpose())

# best_parameters, metrics = ax_client.get_best_parameters()

1 + 1

# %% Code Graveyard
# from sklearn.preprocessing import OneHotEncoder
# from sklearn.preprocessing import normalize
# from sklearn.ensemble import RandomForestRegressor

# from ax.service.utils.instantiation import ObjectiveProperties
# from ax import ChoiceParameter, RangeParameter, ParameterType

# component_slots = [
#     ChoiceParameter(
#         name=component_slot_name,
#         parameter_type=ParameterType.STRING,
#         values=unique_components,
#         sort_values=False,
#     )
#     for component_slot_name in component_slot_names
# ]
# composition_slots = [
#     RangeParameter(
#         name=composition_slot_name,
#         parameter_type=ParameterType.FLOAT,
#         lower=0.0,
#         upper=1.0,
#     )
#     for composition_slot_name in composition_slot_names
# ]

# https://stackoverflow.com/a/57445425/13697228
# res = [[]]
# for pair in pairs:
#     res += [(*r, x) for r in res for x in pair]

# data = {**component_dict, **composition_dict}
# for slot_name in component_slot_names + composition_slot_names:
#     if slot_name not in data.keys():
#         if slot_name in component_slot_names:
#             setdiff = set(unique_components) - set(components[i])
#             data[slot_name] = list(setdiff)[0]
#         elif slot_name in composition_slot_names:
#             data[slot_name] = 0.0


# symmetry_constraints = [
#     lhs + " >= " + rhs
#     for (lhs, rhs) in list(zip(composition_slot_names[:-1], composition_slot_names[1:]))
# ]

# symmetry_constraints = [
#     lhs + " >= " + rhs
#     for (lhs, rhs) in list(zip(composition_slot_names[:-1], composition_slot_names[1:]))
# ]
