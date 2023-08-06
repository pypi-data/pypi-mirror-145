# %% [markdown]
# <a href="https://colab.research.google.com/github/sparks-baird/AxForChemistry/blob/main/tutorials/multi_objective_example.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Generate Sobol and multi-objective SAASBO Bayesian candidates for wetlab experiments
#
# The first step is to generate a list of Sobol candidates, to be synthesized in a wetlab
# environment or calculated if a simulation, etc. Once these candidates have been added
# as a new .csv file (default is "post-sobol.csv") following the same format as the
# training data, the second step will call `form.bayes_opt()`. At this point, it will suggest a batch of next best
# experiments based on Pareto front-aware multi-objective optimization (MOO) to run for
# a single adaptive design iteration. Note that the CSV file that gets loaded should be
# stripped of any extra columns, otherwise these will be treated as search parameters. For
# example, if you give it a CSV with multiple objectives and run a single-objective
# optimization, the additional objectives will be erroneously considered as part of the
# parameter search space.
#
# For more information, see https://ax.dev/tutorials/saasbo_nehvi.html
#
# Additional batches can then be generated. The setup of this tutorial assumes that there is some time between
# when the experiments are suggested and when they are completed, and that experiments are
# carried out "offline" (meaning this is not a closed-loop optimization process).

# %%
# %pip install axforchemistry

# %% [markdown]
# ## Imports

# %%
from os import path
import pandas as pd
from axforchemistry.axforchemistry_ import FormulationOptimization
from ax.service.utils.instantiation import ObjectiveProperties
from axforchemistry.utils.data import make_compositional_regression
from axforchemistry.utils.plotting import cv_plot

# %% [markdown]
# ## Setup

# To perform multi-objective optimization (MOO), specify the names of the objectives based
# on the columns in the CSV file(s) of interest and whether the objective should be
# minimized or maximized. `threshold == None` means to infer a threshold that the model
# uses to help focus the search to a more useful range for the objective values. This
# threshold acts as a soft constraint, and is set as a scalar value. For example, by
# specifying `threshold=200` for the `"Compressive Strength (MPa)"` objective, where
# greater is better (`minimize=False`), candidates that are likely to perform worse than this threshold are
# less likely to be suggested as next experiments. In other words, this is a place where
# you can bake-in domain knowledge to help the model decide what is useful or not.

# %%
compressive_key = "Compressive Strength (MPa)"
flexural_key = "Flexural Strength (MPa)"
vickers_key = "Vickers Hardness"
shrinkage_key = "Shrinkage (%)"
moo_objectives = {
    compressive_key: ObjectiveProperties(minimize=False, threshold=None),
    flexural_key: ObjectiveProperties(minimize=False, threshold=None),
    vickers_key: ObjectiveProperties(minimize=False, threshold=None),
    shrinkage_key: ObjectiveProperties(minimize=True, threshold=None),
}

data_dir = "data"
train_fname = "train-moo-fake.csv"
post_sobol_fname = "post-sobol-moo-fake.csv"

figdir = path.join("figures", "moo")

# trim the data down to the first 10 datapoints so it runs very fast (dummy run)
trim = False
if trim:
    df = pd.read_csv(path.join(data_dir, post_sobol_fname))
    df = df.head(10)
    post_sobol_fname = "post-sobol-moo-fake-dummy.csv"
    df.to_csv(path.join(data_dir, post_sobol_fname), index=False)

# %% [markdown]
# ### Generate dummy data
#
# The following is generated from a linear model and then the inputs are reworked to conform to our compositional constraint, such that each component is positive and `component_0 + component_1 + ... + component_n == 1.0`. We reparameterize this to `component_0 + component_1 + ... + component_{n-1} <= 1.0` to remove a degenerate dimension of the search and thereby increase the search efficiency.

# %%
n_samples = 100
n_features = 10
n_targets = len(moo_objectives)
targ_columns = [compressive_key, flexural_key, vickers_key, shrinkage_key]

df = make_compositional_regression(
    data_dir, train_fname, targ_columns, n_samples, n_features, n_targets
)
df

# %% [markdown]
# ## Optimization

# The optimization takes place with the FormulationOptimization class, which refers to
# optimization of a formulation of components (i.e. `component_1 + component_2 +
# component_3 + ... + component_n`) such that the sum of the fractional contributions of
# all the components is equal to one.

# %%
# TODO: allow passing DataFrames directly
form = FormulationOptimization(
    train_max_val=1.0,  # i.e. i.e. x_1 + x_2 + x_3 + ... + x_{n-1} <= train_max_val
    sobol_max_val=0.25,  # i.e. x_1 + x_2 + x_3 + ... + x_{n-1} <= sobol_max_val
    sobol_min_val=0.15,  # i.e. x_1 + x_2 + x_3 + ... + x_{n-1} >= sobol_min_val
    bayes_max_val=None,  # default to Sobol equivalent
    bayes_min_val=None,  # default to Sobol equivalent
    seed=12345,
    n_bayes_batch=5,
    n_sobol=10,  # None --> 2*num_parameters
    num_samples=256,  # set to 256+ for real run (lower if OOM, e.g. 64), 16 for dummy run
    warmup_steps=512,  # set to 512+ for real run (lower if OOM, e.g. 128), 32 for dummy run
    exp_name="moo-example",
    moo_objectives=moo_objectives,
    exp_dir=path.join("experiments", "moo"),
    save_dir=path.join("results", "moo"),
    data_dir=data_dir,
    train_fname=train_fname,
    post_sobol_fname=post_sobol_fname,  # same format as `train_fname` + train data
)

# %% [markdown]
# ## Sobol candidates

# First, we generate the suggested (pseudo-random) Sobol experiments to provide an initial
# scaffolding for the initial model fit.

# %%
print("generating Sobol candidates and saving to .csv")
sobol_df, ax_sobol = form.train_and_sobol()
model = form.pre_sobol_model
sobol_df

# %% [markdown]
# ### Plotting

# Now, we take a look at the cross-validation (CV) results for the SAASBO model using
# the existing training data that was supplied to the model.

# %%
figdir2 = path.join(figdir, "pre-sobol")
cv_results, fig, tile_fig = cv_plot(
    model,
    figdir=figdir2,
    fname="moo-cv",
    matplotlibify_kwargs=dict(height_inches=7.0, width_inches=7.0),
)

# %% [markdown]
# ## Bayesian candidates

# ### First iteration
# After completing the Sobol experiments (e.g. via wetlab synthesis and characterization)
# and recording the measured objectives along with all of the available training data
# within the `post_sobol_fname` file (e.g. `post-sobol-moo-fake.csv`), run the following cell
# to generate the first batch of SAASBO Bayesian optimization candidates. The process is
# then repeated: perform the suggested (real-world) experiments and run the script again
# to get another batch of suggested candidates. This is meant to be an offline, manual
# process geared towards manual experimental wetlab synthesis and characterization, though
# more automated options exist.

# %%
print("generating Bayes candidates and saving to .csv")
bayes_df, ax_bayes = form.bayes_opt()
model = ax_bayes.generation_strategy.model
bayes_df

# %% [markdown]
# At this point, you will run the SAASBO suggested experiments. Note that you are free
# to run all of them, downselect, or modify the values of individual experiments, but if
# you add or remove any parameters, these need to be represented for all variables. In the
# case of a formulation where you decide to include a new component (e.g. a chemical that
# you haven't used before), this is easy; simply add a column with `0.0` everywhere except
# where you used the new chemical.

# ### Plotting

# We can take a look at the cross-validation (CV) results for the SAASBO model using
# whatever fully recorded data was made available to the model (i.e. existing training
# data and Sobol data).

# %%
figdir2 = path.join(figdir, "post-sobol")
cv_results, fig, tile_fig = cv_plot(
    model,
    figdir=figdir,
    fname="moo-cv",
    matplotlibify_kwargs=dict(height_inches=7.0, width_inches=7.0),
)

# %% [markdown]
# ### Second iteration
# Once you have finished running the experiments and have
# updated the `post_sobol_fname` file (e.g. `post-sobol-moo-fake.csv`), then you can run
# the second iteration of SAASBO suggested experiments.

# %%
# ensure that `post_sobol_fname` file was updated with the new information.
print("generating Bayes candidates and saving to .csv")
bayes_df, ax_bayes = form.bayes_opt()
model = ax_bayes.generation_strategy.model
bayes_df

# %% [markdown]
# ### Plotting

# We can take a look at the cross-validation (CV) results for the SAASBO model after
# the first iteration using whatever fully recorded data was made available to the model
# (i.e. existing training data, Sobol data, and the first Bayesian batch).

# %%
figdir2 = path.join(figdir, "bayes-0")
cv_results, fig, tile_fig = cv_plot(
    model,
    figdir=figdir,
    fname="moo-cv",
    matplotlibify_kwargs=dict(height_inches=7.0, width_inches=7.0),
)

