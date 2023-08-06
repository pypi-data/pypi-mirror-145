"""Bayesian optimization of dental composite compositions using list of candidates."""
# %% imports
from typing import List
import numpy as np
import pandas as pd
from timeit import default_timer as timer
from tqdm import tqdm
from os.path import join
from pathlib import Path

from ax.plot.parallel_coordinates import plot_parallel_coordinates_plotly

import torch

from botorch.models.gp_regression import (
    SingleTaskGP,
    FixedNoiseGP,
    HeteroskedasticSingleTaskGP,
)
from botorch.acquisition.monte_carlo import qNoisyExpectedImprovement
from ax.models.torch.botorch_modular.surrogate import Surrogate
from ax.models.torch.fully_bayesian import FullyBayesianBotorchModel
from ax import SearchSpace

from ax.core.observation import ObservationFeatures
from ax.modelbridge.generation_strategy import GenerationStrategy, GenerationStep
from ax.modelbridge.registry import Models
from ax.modelbridge.modelbridge_utils import (
    extract_search_space_digest,
    extract_objective_weights,
)

# from ax.service.managed_loop import optimize
from ax.storage.json_store.save import save_experiment
from ax.service.ax_client import AxClient

from sobol import nchoosek_sobol
from fractional import fractional_encode, fractional_decode, append_last_component

dummy = False
batch_size = 1

torch.manual_seed(12345)  # To always get the same Sobol points
tkwargs = {
    "dtype": torch.double,
    "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
}

if dummy:
    unique_components = ["Al", "Co", "Cr", "Cu", "Fe", "Ni"]

    components = np.array([unique_components * 5], dtype=object)

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

    X_train = fractional_encode(components, compositions)

    np.random.seed(10)
    y_train = 100 * np.random.rand(X_train.shape[0])

    exp_name = "dummy_experiment"
    target_name = "dummy"

    n_slots = 5
    # 2**m candidates will be generated per unique nchoosek combination
    comb_m = 6

else:
    X_train = pd.read_csv("train.csv")
    # NOTE: keep only Ramsey synthesis until dealing with hidden differences
    X_train = X_train.iloc[158:].reset_index(drop=True)
    target_name = "Compressive Strength (MPa)"
    y_train = X_train[target_name]
    X_train.drop(columns=target_name, inplace=True)
    # convert percent to fraction
    X_train = X_train / 100
    # X_train = X_train.iloc[:, 0:10]
    # last_component = pd.DataFrame(1 - X_train.sum(axis=1), columns=["last_component"])
    # X_train = pd.concat((X_train, last_component), axis=1)
    unique_components = list(X_train.columns)
    components, compositions = fractional_decode(X_train)
    exp_name = "composite_compressive_strength"

    n_slots = 5
    # 2**m candidates will be generated per unique nchoosek combination
    comb_m = 10

n_components = X_train.shape[1]
n_train = X_train.shape[0]

# Ax-specific
if dummy:
    orig_max_val = 1.0
    max_val = 1.0
else:
    orig_max_val = 0.4
    max_val = 0.196

X_pred = nchoosek_sobol(
    unique_components,
    n_slots=n_slots,
    comb_m=comb_m,
    scale=max_val,
    verbose=False,
    seed=11,
)
pred_components, pred_compositions = fractional_decode(X_pred)

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
        # 1. Initialization step (does not require pre-existing data and is well-suited for
        # initial sampling of the search space)
        # GenerationStep(
        #     model=Models.SOBOL,
        #     num_trials=n_components,  # How many trials should be produced from this generation step
        #     # min_trials_observed=3,  # How many trials need to be completed to move to next model
        #     # max_parallelism=5,  # Max parallelism for this step
        #     model_kwargs={
        #         "seed": 999,
        #         "fallback_to_sample_polytope": True,
        #     },  # Any kwargs you want passed into the model
        #     model_gen_kwargs={},  # Any kwargs you want passed to `modelbridge.gen`
        # ),
        # 2. Bayesian optimization step (requires data obtained from previous phase and learns
        # from all data available at the time of each new candidate generation call)
        GenerationStep(
            model=Models.BOTORCH_MODULAR,
            num_trials=-1,  # No limitation on how many trials should be produced from this step
            max_parallelism=batch_size,  # Parallelism limit for this step, often lower than for Sobol
            # More on parallelism vs. required samples in BayesOpt:
            # https://ax.dev/docs/bayesopt.html#tradeoff-between-parallelism-and-total-number-of-trials
            model_kwargs={
                # https://github.com/facebook/Ax/issues/768#issuecomment-1009007526
                "fit_out_of_design": True,
                # FullyBayesianBotorchModel not working, see https://github.com/facebook/Ax/issues/771#issuecomment-1013535992
                "surrogate": Surrogate(HeteroskedasticSingleTaskGP),
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
    ax_client.complete_trial(trial_index=ct, raw_data=(y_train[i], 5.0))
    ct = ct + 1

# narrow the search space
ax_client.experiment.search_space = ax_client_tmp.experiment.search_space

# ensure ax_client.generation_strategy.model gets assigned (then discard dummy trial)
_, trial_index = ax_client.get_next_trial()
ct = ct + 1
trial = ax_client.experiment.trials[trial_index]
trial.mark_completed()

# initialize
y_preds = []
y_stds = []
next_experiments = []


observation_features = [
    ObservationFeatures(dict(zip(unique_components[:-1], x_pred)))
    for x_pred in X_pred.iloc[:, :-1].values
]

print("number of candidates: ", len(observation_features))


start = timer()
for i in range(batch_size):
    model_bridge = ax_client.generation_strategy.model
    transformed_gen_args = model_bridge._get_transformed_gen_args(
        search_space=ax_client.experiment.search_space,
    )
    search_space_digest = extract_search_space_digest(
        search_space=transformed_gen_args.search_space,
        param_names=model_bridge.parameters,
    )
    objective_weights = extract_objective_weights(
        objective=ax_client.experiment.optimization_config.objective,
        outcomes=model_bridge.outcomes,
    )

    def chunks(L, n, check_divisible=False):
        """Yield successive n-sized chunks from L.
        
        modified from source: https://stackoverflow.com/q/2130016/13697228
        """
        if check_divisible:
            if len(L) % n != 0:
                raise ValueError("L should be divisible by n")
        for i in range(0, len(L), n):
            yield L[i : i + n]

    n = 1000
    obs_chunks = list(chunks(observation_features, n))

    acqf_values: List[float] = []
    for i, obs_chunk in enumerate(tqdm(obs_chunks, unit="chunk")):
        # `acqf_values` is a list of floats (since we can evaluate acqf for multiple points at once);
        # ordering corresponds to order of points in `observation_features` input
        acqf_values = acqf_values + model_bridge.evaluate_acquisition_function(
            # Each `ObservationFeatures` below represents one point in experiment (untransformed) search space:
            observation_features=obs_chunk,
            search_space_digest=search_space_digest,
            objective_weights=objective_weights,
        )

    max_value = max(acqf_values)
    max_index = acqf_values.index(max_value)
    next_observation = observation_features[max_index]
    next_experiment = next_observation.parameters
    del observation_features[max_index]

    model = ax_client.generation_strategy.model
    y_pred, y_var = model.predict([next_observation])
    y_pred = y_pred[target_name][0]
    y_var = y_var[target_name][target_name][0]
    y_std = np.sqrt(y_var)

    ax_client.attach_trial(next_experiment)
    ax_client.complete_trial(trial_index=ct, raw_data=(y_pred, 5.0))
    best_parameters, metrics = ax_client.get_best_parameters()

    y_preds.append(y_pred)
    y_stds.append(y_std)
    next_experiments.append(next_experiment)
    ct = ct + 1
end = timer()
print("time (s): ", end - start)

experiment_dir = join(
    "experiments", f"{exp_name}", f"n_slots_{n_slots}", f"comb_m_{comb_m}"
)
Path(experiment_dir).mkdir(exist_ok=True, parents=True)
experiment_fpath = join(experiment_dir, "experiment.json")
experiment = ax_client.experiment
save_experiment(experiment, experiment_fpath)

# model.model.surrogate.feature_importances()
# fig = plot_feature_importance_by_feature_plotly(ax_client.generation_strategy.model)
# fig.show()

fig = plot_parallel_coordinates_plotly(experiment)
fig.show()

next_experiments = [
    append_last_component(next_experiment, unique_components, max=max_val)
    for next_experiment in next_experiments
]

tmp_df = pd.DataFrame(next_experiments)
# tmp_df = tmp_df[tmp_df > 1e-6].dropna()
# tmp_df[tmp_df < 1e-6] = 0
pred_df = pd.DataFrame({"predicted (MPa)": y_preds, "uncertainty stdDev (MPa)": y_stds})
out_df = tmp_df.join(pred_df)
print(tmp_df)
# time.sleep(1)
out_df.to_csv("next_experiments.csv", index=False)
# print(next_experiment)

1 + 1

# %% Code Graveyard

