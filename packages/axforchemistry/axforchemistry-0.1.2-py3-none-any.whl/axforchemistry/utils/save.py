from os import path
import pandas as pd


def save_output_dataframe(
    y_preds, y_stds, full_bayes_experiments, unique_components, save_dir, fname
):
    tmp_df = pd.DataFrame(full_bayes_experiments)
    tmp_df[tmp_df < 1e-5] = 0
    pred_df = pd.DataFrame(
        {"predicted (MPa)": y_preds, "uncertainty stdDev (MPa)": y_stds}
    )
    out_df = tmp_df.join(pred_df)
    last_component = unique_components[-1]
    out_df[last_component] = 1 - out_df[unique_components[:-1]].sum(axis=1)
    out_df.to_csv(path.join(save_dir, fname), index=False)
    return out_df
