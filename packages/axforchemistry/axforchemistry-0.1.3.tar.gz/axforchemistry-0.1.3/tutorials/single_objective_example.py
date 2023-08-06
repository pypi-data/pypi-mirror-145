"""Multi-step script to generate Sobol candidates and Bayesian suggestions.

The first step is to generate a list of Sobol candidates, to be synthesized in a wetlab
environment or calculated if a simulation, etc. Once these candidates have been added
as a new .csv file (default is "post-sobol.csv") following the same format as the
training data, the second step is to flip the `sobol_complete` flag to True and run,
which will call `mo.bayes_opt()`. At this point, it will suggest a batch of next best
experiments to run for a single adaptive design iteration.

At this point, once the new data has been recorded, then the script can be run again to
generate another batch. The setup of this script assumes that there is some time between
when the experiments are suggested and when they are completed, and that experiments are
carried out "offline" (meaning this is not a closed-loop optimization process).
"""
from axforchemistry.axforchemistry_ import FormulationOptimization

sobol_complete = False  # change to True once all Sobol wetlab experiments recorded

mo = FormulationOptimization(
    dummy=False,  # whether to use fictitious compositional data or not
    dummy_max_val=1.0,
    train_max_val=0.4,
    sobol_max_val=0.25,
    sobol_min_val=0.15,
    bayes_max_val=None,  # default to Sobol equivalent
    bayes_min_val=None,  # default to Sobol equivalent
    seed=12345,
    n_bayes_batch=5,
    n_sobol=10,  # None --> 2*num_parameters, 10/90 Sobol/Bayes, total=100 iterations is convention for SAASBO
    num_samples=256,  # set to 256 for real run, 16 for dummy run
    warmup_steps=512,  # set to 512 for real run, 32 for dummy run
    exp_name="dummy",
    target_name="target",
    exp_dir="experiments",
    data_dir="data",
    train_fname="train.csv",
    post_sobol_fname="post-sobol-fake.csv",  # same format as `train_fname` + train data
)

if not sobol_complete:
    print("generating Sobol candidates and saving to .csv")
    sobol_df, ax_sobol = mo.train_and_sobol()
else:
    print("generating Bayes candidates and saving to .csv")
    bayes_df, ax_bayes = mo.bayes_opt()

1 + 1
