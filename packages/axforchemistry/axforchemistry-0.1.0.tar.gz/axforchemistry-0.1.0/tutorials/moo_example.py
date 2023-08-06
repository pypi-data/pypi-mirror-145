"""Multi-step script to generate Sobol and multi-objective Bayesian candidates.

The first step is to generate a list of Sobol candidates, to be synthesized in a wetlab
environment or calculated if a simulation, etc. Once these candidates have been added
as a new .csv file (default is "post-sobol.csv") following the same format as the
training data, the second step is to flip the `sobol_complete` flag to True and run,
which will call `mo.bayes_opt()`. At this point, it will suggest a batch of next best
experiments based on Pareto front-aware multi-objective optimization (MOO) to run for
a single adaptive design iteration. Note that the CSV file that gets loaded should be
stripped of any extra columns, otherwise these will be treated as search parameters. For
example, if you give it a CSV with multiple objectives and run a single-objective
optimization, the additional objectives will be erroneously considered as part of the
parameter search space.

For more information, see https://ax.dev/tutorials/saasbo_nehvi.html

At this point, once the new data has been recorded, then the script can be run again to
generate another batch. The setup of this script assumes that there is some time between
when the experiments are suggested and when they are completed, and that experiments are
carried out "offline" (meaning this is not a closed-loop optimization process).
"""
from os import path

import pandas as pd
from axforchemistry.axforchemistry_ import FormulationOptimization
from ax.service.utils.instantiation import ObjectiveProperties

from axforchemistry.utils.plotting import cv_plot

# change to True once all Sobol wetlab experiments recorded
sobol_complete = False

# threshold == None means infer, otherwise can set a scalar value as soft constraint
# (i.e. if you have domain knowledge you can use for what's considered not useful)
moo_objectives = {
    "Compressive Strength (MPa)": ObjectiveProperties(minimize=False, threshold=None),
    "Flexural Strength (MPa)": ObjectiveProperties(minimize=False, threshold=None),
    "Vickers Hardness": ObjectiveProperties(minimize=False, threshold=None),
    "Shrinkage (%)": ObjectiveProperties(minimize=True, threshold=None),
}


data_dir = "data"
train_fname = "train-moo-fake.csv"
post_sobol_fname = "post-sobol-moo-fake.csv"

trim = False
if trim:
    df = pd.read_csv(path.join(data_dir, post_sobol_fname))
    df = df.head(10)
    post_sobol_fname = "post-sobol-moo-fake-dummy.csv"
    df.to_csv(path.join(data_dir, post_sobol_fname), index=False)

# ignore the fake Sobol data
post_sobol_fname = train_fname

# TODO: allow passing DataFrames directly
form = FormulationOptimization(
    dummy=False,  # whether to use fictitious compositional data or not
    dummy_max_val=1.0,
    train_max_val=0.4,
    sobol_max_val=0.25,
    sobol_min_val=0.15,
    bayes_max_val=None,  # default to Sobol equivalent
    bayes_min_val=None,  # default to Sobol equivalent
    seed=12345,
    n_bayes_batch=5,
    n_sobol=10,  # None --> 2*num_parameters
    num_samples=64,  # set to 256+ for real run (lower if OOM), 16 for dummy run
    warmup_steps=128,  # set to 512+ for real run (lower if OOM), 32 for dummy run
    exp_name="monomers-moo",
    moo_objectives=moo_objectives,
    exp_dir=path.join("experiments", "moo"),
    save_dir=path.join("results", "moo"),
    data_dir=data_dir,
    train_fname=train_fname,
    post_sobol_fname=post_sobol_fname,  # same format as `train_fname` + train data
)

if not sobol_complete:
    print("generating Sobol candidates and saving to .csv")
    sobol_df, ax_sobol = form.train_and_sobol()
    model = form.pre_sobol_model
else:
    print("generating Bayes candidates and saving to .csv")
    bayes_df, ax_bayes = form.bayes_opt()
    model = ax_bayes.generation_strategy.model

figdir = path.join("figures", "moo")

if sobol_complete:
    figdir = path.join(figdir, "sobol")

cv_results, fig, tile_fig = cv_plot(model, figdir=figdir, fname="moo-cv")

1 + 1
