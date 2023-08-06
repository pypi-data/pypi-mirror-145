from copy import deepcopy
from ax.service.ax_client import AxClient
from ax.modelbridge.generation_strategy import GenerationStrategy, GenerationStep
from ax.modelbridge.registry import Models
import torch


def get_parameters(
    unique_components, max_val, min_val=0.0, upper_lim=1.0, drop_last=True,
):
    sub_components = unique_components[:-1]
    last_component = unique_components[-1]
    parameters = [
        {"name": component, "type": "range", "bounds": [0.0, max_val]}
        for component in sub_components
    ]
    if not drop_last:
        last_parameter = {
            "name": last_component,
            "type": "range",
            "bounds": [upper_lim - max_val, upper_lim - min_val],
        }
        parameters.append(last_parameter)

    return parameters


def get_constraint(unique_components, max_val, upper=True):
    separator = " + "
    if upper:
        c = "<="
    else:
        c = ">="
    constraint = separator.join(unique_components[:-1]) + f" {c} {max_val}"
    return constraint


def get_sobol_gen_strategy(n_components, n_sobol=None):
    if n_sobol is None:
        n_sobol = n_components - 1
    gs_sobol = GenerationStrategy(
        steps=[
            # 1. Initialization step (does not require pre-existing data and is well-suited
            #    for initial sampling of the search space)
            GenerationStep(
                model=Models.SOBOL,
                # How many trials should be produced from this generation step
                num_trials=n_sobol,
                # min_trials_observed=3,  # How many trials need to be completed to move to next model
                # max_parallelism=5,  # Max parallelism for this step
                min_trials_observed=n_sobol,
                model_kwargs={
                    # "seed": random_seed, # not working for some reason..
                    "fit_out_of_design": True,
                    "fallback_to_sample_polytope": True,
                },  # Any kwargs you want passed into the model
                model_gen_kwargs={
                    "optimizer_kwargs": {
                        "equality_constraints": [
                            (torch.arange(n_components), torch.ones(n_components), 1)
                        ]
                    }
                },  # sum(x) == 1},  # Any kwargs you want passed to `modelbridge.gen`
            )
        ]
    )

    return gs_sobol


def get_bayes_gen_strategy(
    batch_size,
    use_moo=False,
    num_samples=256,
    warmup_steps=512,
    tkwargs={"device": "cuda", "dtype": torch.double},
):
    if use_moo:
        model = Models.FULLYBAYESIANMOO
    else:
        model = Models.FULLYBAYESIAN

    gs_bayes = GenerationStrategy(
        steps=[
            # 2. Bayesian optimization step (requires data obtained from previous phase and learns
            # from all data available at the time of each new candidate generation call)
            GenerationStep(
                model=model,
                num_trials=-1,  # No limitation on how many trials should be produced from this step
                max_parallelism=batch_size,  # Parallelism limit for this step, often lower than for Sobol
                # More on parallelism vs. required samples in BayesOpt:
                # https://ax.dev/docs/bayesopt.html#tradeoff-between-parallelism-and-total-number-of-trials
                model_kwargs={
                    "fit_out_of_design": True,
                    "torch_device": tkwargs["device"],
                    "torch_dtype": tkwargs["dtype"],
                    "num_samples": num_samples,  # Increasing this may result in better model fits
                    "warmup_steps": warmup_steps,  # Increasing this may result in better model fits
                    "gp_kernel": "rbf",  # "rbf" is the default in the paper, but we also support "matern"
                    # "acquisition_options": {
                    #     "optimizer_options": {"options": {"batch_limit": 1}}
                    # }, # not the place to use `batch_limit` for SAASBO
                },  # https://github.com/facebook/Ax/issues/768#issuecomment-1009007526
            ),
        ]
    )

    return gs_bayes


def get_train_search_space(
    exp_name,
    train_parameters,
    train_comp_constraints,
    gs_sobol,
    target_name=None,
    soo_minimize=False,
    moo_objectives=None,
    random_seed=None,
    extra_kwargs={},
):
    if (moo_objectives is None and target_name is None) or (
        moo_objectives is not None and target_name is not None
    ):
        raise ValueError("only one of `objectives` or `target_name` may be specified")

    if moo_objectives is not None:
        kwargs = dict(objectives=moo_objectives)
    else:
        kwargs = dict(objective_name=target_name, minimize=soo_minimize)

    # uses Sobol generation strategy just to have something in there
    ax_train = AxClient(
        generation_strategy=gs_sobol, verbose_logging=False, random_seed=random_seed
    )
    ax_train.create_experiment(
        name=exp_name,
        parameters=train_parameters,
        parameter_constraints=train_comp_constraints,
        immutable_search_space_and_opt_config=False,
        **kwargs,
        **extra_kwargs,
    )

    train_search_space = ax_train.experiment.search_space
    return train_search_space


def get_ax_sobol_and_sobol_search(
    exp_name,
    target_name,
    full_parameters,
    gs_sobol,
    sobol_constraints,
    random_seed=None,
):
    # deal with the bias introduced through x1+x2+x3==1 --> x1+x2<=1 reparameterization
    ax_sobol = AxClient(
        generation_strategy=gs_sobol, verbose_logging=False, random_seed=random_seed
    )
    ax_sobol.create_experiment(
        name=exp_name,
        parameters=full_parameters,
        parameter_constraints=sobol_constraints,
        objective_name=target_name,
        minimize=False,
        immutable_search_space_and_opt_config=False,
    )
    # copy before modifying
    sobol_search = deepcopy(ax_sobol.experiment.search_space)
    return ax_sobol, sobol_search


def get_ax_bayes_and_bayes_search(
    exp_name,
    parameters,
    bayes_constraints,
    gs_bayes,
    tkwargs,
    target_name=None,
    soo_minimize=False,
    moo_objectives=None,
    extra_kwargs={},
):
    if (moo_objectives is None and target_name is None) or (
        moo_objectives is not None and target_name is not None
    ):
        raise ValueError("only one of `objectives` or `target_name` may be specified")
    if moo_objectives is not None:
        kwargs = dict(objectives=moo_objectives)
    else:
        kwargs = dict(objective_name=target_name, minimize=soo_minimize)
    ax_bayes = AxClient(generation_strategy=gs_bayes, torch_device=tkwargs["device"])
    ax_bayes.create_experiment(
        name=exp_name,
        parameters=parameters,
        parameter_constraints=bayes_constraints,
        objective_name=target_name,
        immutable_search_space_and_opt_config=False,
        **kwargs,
        **extra_kwargs,
    )

    # needs to appear before changing ax_client search space
    bayes_search = deepcopy(ax_bayes.experiment.search_space)
    return ax_bayes, bayes_search
