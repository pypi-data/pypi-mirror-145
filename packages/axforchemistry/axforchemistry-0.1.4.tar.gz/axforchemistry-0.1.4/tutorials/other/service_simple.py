# modified from source: https://ax.dev/docs/api.html
import pandas as pd
from ax.service.ax_client import AxClient

# from ax.utils.measurement.synthetic_functions import branin

ax_client = AxClient()
ax_client.create_experiment(
    name="dummy_test_experiment",
    parameters=[
        {
            "name": "x1",
            "type": "range",
            "bounds": [-5.0, 10.0],
            "value_type": "float",
        },
        {
            "name": "x2",
            "type": "range",
            "bounds": [0.0, 10.0],
        },
    ],
    objective_name="dummy",
    minimize=True,
)

x1 = [-2.0, 0.0, 3.0]
x2 = [8.0, 2.0, 5.0]
y_train = [1.0, 2.0, 3.0]
parameters_df = pd.DataFrame(data=list(zip(x1, x2)), columns=["x1", "x2"])

for i in range(3):
    # parameters, trial_index = ax_client.get_next_trial()
    ax_client.attach_trial(parameters_df.iloc[i].to_dict())
    ax_client.complete_trial(trial_index=i, raw_data=y_train[i])

next_suggested_experiment, trial_index = ax_client.get_next_trial()
print("next suggested experiment: ", next_suggested_experiment)

best_parameters, metrics = ax_client.get_best_parameters()

1 + 1
