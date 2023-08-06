from copy import deepcopy
from ax import Models
from ax.core.observation import ObservationFeatures
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm


def attach_training_data(
    X_train, y_train, n_train, train_search_space, ax_client, drop_last=True
):
    # include pre-existing data with large search
    existing_search_space = deepcopy(ax_client.experiment.search_space)
    ax_client.experiment.search_space = train_search_space
    ct = 0
    for i in range(n_train):
        if drop_last:
            x = X_train.iloc[i, :-1]
        else:
            x = X_train.iloc[i]
        ax_client.attach_trial(x.to_dict())

        # e.g. DataFrame row --> {0: {'Compressive Strength (MPa)': (310.16, None)}}
        raw_data = y_train.iloc[i].to_frame().applymap(lambda x: (x, None)).to_dict()
        # e.g. {'Compressive Strength (MPa)': (310.16, None)}
        raw_data = list(raw_data.values())[0]
        ax_client.complete_trial(trial_index=ct, raw_data=raw_data)
        ct = ct + 1
    ax_client.experiment.search_space = existing_search_space
    return ct


def generate_sobol_experiments(
    target_name, n_sobol, ax_sobol, tkwargs=None, num_samples=256, warmup_steps=512
):
    # corrected Sobol sampling (without compositional constraint reparameterization bias)
    if tkwargs is None:
        tkwargs = {
            "dtype": torch.float32,
            "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        }

    # Only used for getting predictions, not used to affect Sobol points in any way
    model = Models.FULLYBAYESIAN(
        experiment=ax_sobol.experiment,
        data=ax_sobol.experiment.lookup_data(),
        num_samples=num_samples,  # Increasing this may result in better model fits
        warmup_steps=warmup_steps,  # Increasing this may result in better model fits
        gp_kernel="rbf",  # "rbf" is the default in the paper, but we also support "matern"
        torch_device=tkwargs["device"],
        torch_dtype=tkwargs["dtype"],
        verbose=False,  # Set to True to print stats from MCMC
        disable_progbar=False,  # Set to False to print a progress bar from MCMC
    )

    y_preds = []
    y_stds = []
    next_experiments = []
    trial_indices = []
    for _ in tqdm(range(n_sobol)):
        next_experiment, trial_index = ax_sobol.get_next_trial()

        y_pred, y_var = model.predict([ObservationFeatures(next_experiment)])
        y_pred = y_pred[target_name][0]
        y_var = y_var[target_name][target_name][0]
        y_std = np.sqrt(y_var)

        y_preds.append(y_pred)
        y_stds.append(y_std)
        next_experiments.append(next_experiment)
        trial_indices.append(trial_index)
    return y_preds, y_stds, next_experiments, trial_indices, model


def generate_bayes_experiments(
    n_bayes_batch, ax_bayes, target_name=None, moo_objectives=None
):
    bayes_batch_experiments = []
    trial_indices = []
    y_preds = []
    y_stds = []
    for _ in tqdm(range(n_bayes_batch)):
        next_experiment, trial_index = ax_bayes.get_next_trial()
        print("next suggested experiments: ", next_experiment)

        model = ax_bayes.generation_strategy.model
        y_pred, y_var = model.predict([ObservationFeatures(next_experiment)])

        # https://stackoverflow.com/questions/13063691/applying-a-function-to-values-in-dict
        # i.e. extract scalar from list
        y_pred = {k: v[0] for k, v in y_pred.items()}

        if moo_objectives is None:
            y_pred = y_pred[target_name]
            y_var = y_var[target_name][target_name]
            y_std = np.sqrt(y_var)  # REVIEW: incorporate or not? Look back at gh issue
        else:
            # convert to DataFrame, list-->scalar, var-->stdDev
            y_std = pd.DataFrame(y_var).applymap(lambda x: np.sqrt(x[0])).to_dict()

        ax_bayes.complete_trial(trial_index=trial_index, raw_data=y_pred)
        # best_parameters, metrics = ax_bayes.get_best_parameters()

        y_preds.append(y_pred)
        y_stds.append(y_std)
        bayes_batch_experiments.append(next_experiment)
        trial_indices.append(trial_index)
    return y_preds, y_stds, bayes_batch_experiments, trial_indices
