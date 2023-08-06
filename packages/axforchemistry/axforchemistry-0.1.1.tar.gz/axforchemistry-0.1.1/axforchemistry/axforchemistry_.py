"""Bayesian optimization of formulations via Adaptive Experimentation (Ax) platform."""
# %% imports
from os import path
from pathlib import Path
import numpy as np
import torch
from axforchemistry.utils.fractional import append_last_components

from axforchemistry.utils.data import load_data
from axforchemistry.utils.experiment import (
    attach_training_data,
    generate_sobol_experiments,
    generate_bayes_experiments,
)
from axforchemistry.utils.save import save_output_dataframe
from axforchemistry.utils.search import (
    get_ax_bayes_and_bayes_search,
    get_ax_sobol_and_sobol_search,
    get_bayes_gen_strategy,
    get_parameters,
    get_train_search_space,
    get_constraint,
    get_sobol_gen_strategy,
)

# %%
class FormulationOptimization:
    def __init__(
        self,
        dummy=False,
        dummy_max_val=1.0,
        train_max_val=0.4,
        sobol_max_val=0.25,
        sobol_min_val=0.15,
        bayes_max_val=None,
        bayes_min_val=None,
        seed=12345,
        n_bayes_batch=5,
        n_sobol=None,
        num_samples=256,
        warmup_steps=512,
        exp_name="test",
        target_name="target",
        soo_minimize=False,
        moo_objectives=None,
        exp_dir="experiments",
        save_dir="results",
        data_dir="data",
        train_fname="train.csv",
        post_sobol_fname="post-sobol.csv",
        verbose=True,
    ):
        # TODO: expose sub-compositional constraints at top-level
        if seed is not None:
            torch.manual_seed(seed)
        # TODO: make sure tkwargs gets passed properly
        self.tkwargs = {
            "dtype": torch.float32,  # TODO: pass to generation strategy
            "device": torch.device("cuda" if torch.cuda.is_available() else "cpu"),
        }

        self.dummy = dummy

        if moo_objectives is None:
            (self.unique_components, self.X_train, self.y_train) = load_data(
                data_dir=data_dir,
                fname=train_fname,
                dummy=dummy,
                target_names=[target_name],
                verbose=verbose,
            )
        else:
            self.target_names = list(moo_objectives.keys())
            (self.unique_components, self.X_train, self.y_train) = load_data(
                data_dir=data_dir,
                fname=train_fname,
                dummy=dummy,
                target_names=self.target_names,
                verbose=verbose,
            )
            target_name = self.target_names[0]  # for compatibility with train and Sobol

        self.data_dir = data_dir
        self.train_fname = train_fname
        self.post_sobol_fname = post_sobol_fname

        self.n_components = self.X_train.shape[1]
        self.n_train = self.X_train.shape[0]
        if n_sobol is None:
            n_sobol = self.n_components - 1
        self.n_sobol = n_sobol

        self.n_bayes_batch = n_bayes_batch

        self.target_name = target_name
        self.exp_name = exp_name

        self.num_samples = num_samples
        self.warmup_steps = warmup_steps
        self.random_seed = seed

        self.soo_minimize = soo_minimize
        self.moo_objectives = moo_objectives

        if dummy:
            if not np.allclose(np.sum(self.X_train, axis=1), 1):
                raise ValueError(
                    "rows of X_train do not sum to 1 within tolerance (i.e. composition is not close to unity for at least one row)."
                )
            self.train_max_val = dummy_max_val
            self.sobol_max_val = dummy_max_val
            self.bayes_max_val = dummy_max_val
            self.sobol_min_val = 0.0
            self.bayes_min_val = 0.0
        else:
            self.train_max_val = train_max_val

            self.sobol_max_val = sobol_max_val
            self.sobol_min_val = sobol_min_val
            if bayes_max_val is None:
                bayes_max_val = sobol_max_val
                bayes_min_val = sobol_min_val
            self.bayes_max_val = bayes_max_val
            self.bayes_min_val = bayes_min_val

        if dummy:
            exp_dir = path.join(exp_dir, "dummy")
            save_dir = path.join(save_dir, "dummy")
        Path(exp_dir).mkdir(exist_ok=True, parents=True)
        Path(save_dir).mkdir(exist_ok=True, parents=True)
        self.exp_dir = exp_dir
        self.save_dir = save_dir

        self.verbose = verbose

    def train_and_sobol(self):
        # %% Training and Sobol search setup
        # constraints, parameterse, generation strategies, search spaces, and Ax clients
        self.train_constraints = [
            get_constraint(self.unique_components, self.train_max_val, upper=True)
        ]
        self.sobol_upp_constraint = get_constraint(
            self.unique_components, self.sobol_max_val, upper=True
        )

        self.sobol_low_constraint = get_constraint(
            self.unique_components, self.sobol_min_val, upper=False
        )

        self.sobol_constraints = [self.sobol_upp_constraint, self.sobol_low_constraint]

        self.train_parameters = get_parameters(
            self.unique_components, self.train_max_val, drop_last=False
        )

        self.gs_dummy = get_sobol_gen_strategy(self.n_components)

        # NOTE: maybe I should be using some of Ax's helper functions here
        self.train_search_space = get_train_search_space(
            self.exp_name,
            self.train_parameters,
            self.train_constraints,
            self.gs_dummy,
            target_name=self.target_name if self.moo_objectives is None else None,
            soo_minimize=self.soo_minimize,
            moo_objectives=self.moo_objectives,
        )

        self.gs_sobol = get_sobol_gen_strategy(self.n_components, n_sobol=self.n_sobol)

        self.sobol_parameters = get_parameters(
            self.unique_components,
            self.sobol_max_val,
            min_val=self.sobol_min_val,
            drop_last=False,
        )

        self.ax_sobol, self.sobol_search = get_ax_sobol_and_sobol_search(
            self.exp_name,
            self.target_name,
            self.sobol_parameters,
            self.gs_sobol,
            self.sobol_constraints,
            random_seed=self.random_seed,
        )

        # existing data, which gets attached to the Sobol AxClient
        attach_training_data(
            self.X_train,
            self.y_train,
            self.n_train,
            self.train_search_space,
            self.ax_sobol,
            drop_last=False,
        )

        # Sobol data accounts for the bias introduced when reparameterizing:
        # x_1 + x_2 + ... + x_n == 1.0 --> x_1 + x_2 + ... + x_{n-1} <= 1.0
        (
            self.sobol_preds,
            self.sobol_stds,
            self.sobol_experiments,
            self.sobol_trial_indices,
            self.pre_sobol_model,
        ) = generate_sobol_experiments(
            self.target_name,
            self.n_sobol,
            self.ax_sobol,
            tkwargs=self.tkwargs,
            num_samples=self.num_samples,
            warmup_steps=self.warmup_steps,
        )

        self.sobol_df = save_output_dataframe(
            self.sobol_preds,
            self.sobol_stds,
            self.sobol_experiments,
            self.unique_components,
            self.save_dir,
            "sobol.csv",
        )

        self.ax_sobol.save_to_json_file(path.join(self.exp_dir, "sobol.json"))

        return self.sobol_df, self.ax_sobol

    def bayes_opt(self):
        self.train_constraints = [
            get_constraint(self.unique_components, self.train_max_val, upper=True)
        ]

        self.train_parameters = get_parameters(
            self.unique_components, self.train_max_val, drop_last=True
        )

        self.gs_dummy = get_sobol_gen_strategy(self.n_components)

        # NOTE: maybe I should be using some of Ax's helper functions here
        self.train_search_space = get_train_search_space(
            self.exp_name,
            self.train_parameters,
            self.train_constraints,
            self.gs_dummy,
            target_name=self.target_name if self.moo_objectives is None else None,
            soo_minimize=self.soo_minimize,
            moo_objectives=self.moo_objectives,
        )

        # %% Bayes search setup
        self.bayes_parameters = get_parameters(
            self.unique_components,
            self.bayes_max_val,
            min_val=self.bayes_min_val,
            drop_last=True,
        )
        use_moo = False if self.moo_objectives is None else True
        self.gs_bayes = get_bayes_gen_strategy(
            self.n_bayes_batch,
            use_moo=use_moo,
            num_samples=self.num_samples,
            warmup_steps=self.warmup_steps,
            tkwargs=self.tkwargs,
        )

        self.bayes_upp_constraint = get_constraint(
            self.unique_components, self.bayes_max_val, upper=True
        )

        self.bayes_low_constraint = get_constraint(
            self.unique_components, self.bayes_min_val, upper=False
        )

        self.bayes_constraints = [self.bayes_upp_constraint, self.bayes_low_constraint]

        self.ax_bayes, self.bayes_search = get_ax_bayes_and_bayes_search(
            self.exp_name,
            self.bayes_parameters,
            self.bayes_constraints,
            self.gs_bayes,
            self.tkwargs,
            target_name=self.target_name if self.moo_objectives is None else None,
            soo_minimize=self.soo_minimize,
            moo_objectives=self.moo_objectives,
        )

        self.unique_components, self.X_train_bayes, self.y_train_bayes = load_data(
            data_dir=self.data_dir,
            fname=self.post_sobol_fname,
            dummy=self.dummy,
            target_names=self.target_names,
        )

        self.n_train_bayes = self.X_train_bayes.shape[0]
        # existing data, which gets attached to the Sobol AxClient
        attach_training_data(
            self.X_train_bayes,
            self.y_train_bayes,
            self.n_train_bayes,
            self.train_search_space,
            self.ax_bayes,
            drop_last=True,
        )

        self.ax_bayes.experiment.search_space = self.bayes_search

        # %% Bayesian batch trials
        # single adaptive design iteration, multiple suggestions
        (
            self.bayes_preds,
            self.bayes_stds,
            self.bayes_experiments,
            self.bayes_trial_indices,
        ) = generate_bayes_experiments(
            self.n_bayes_batch,
            self.ax_bayes,
            target_name=self.target_name if self.moo_objectives is not None else None,
            moo_objectives=self.moo_objectives,
        )

        self.full_bayes_experiments = append_last_components(
            self.unique_components, self.bayes_experiments
        )

        self.bayes_df = save_output_dataframe(
            self.bayes_preds,
            self.bayes_stds,
            self.full_bayes_experiments,
            self.unique_components,
            self.save_dir,
            "bayes.csv",
        )

        self.ax_bayes.save_to_json_file(path.join(self.exp_dir, "bayes.json"))

        return self.bayes_df, self.ax_bayes


# %% Code Graveyard
# tmp_df = tmp_df[tmp_df > 1e-6].dropna()
