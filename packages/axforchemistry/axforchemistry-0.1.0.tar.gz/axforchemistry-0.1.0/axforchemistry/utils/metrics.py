#!/usr/bin/env python3
# modified from source: ax\metrics\hartmann6.py
# Copyright (c) Meta Platforms, Inc. and affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any, List, Optional, Union
from ax import Data
import numpy as np
from ax.metrics.noisy_function import NoisyFunctionMetric
from ax.utils.common.typeutils import checked_cast
from ax.utils.measurement.synthetic_functions import aug_hartmann6, hartmann6
import pandas as pd
from scipy.interpolate import RegularGridInterpolator
from ax.core.base_trial import BaseTrial
from ax.storage.metric_registry import register_metric


class CompositionalHartmann6Metric(NoisyFunctionMetric):
    def f(self, x: np.ndarray) -> float:
        return checked_cast(float, hartmann6(np.append(x, 1 - sum(x))))


class NoisyCompositionalHartmann6Metric(NoisyFunctionMetric):
    def __init__(
        self,
        name: str,
        param_names: List[str],
        noise_sd: Optional[float] = 0.0,
        lower_is_better: Optional[bool] = None,
        synth_dither: Optional[float] = 0.0,
        sem: Optional[float] = None,
        n: Optional[int] = 10,
        seed: Optional[int] = None,
    ):
        superparams = dict(
            name=name,
            param_names=param_names,
            noise_sd=noise_sd,
            lower_is_better=lower_is_better,
        )
        super().__init__(**superparams)
        self.noise_sd = noise_sd
        self.synth_dither = synth_dither
        self.sem = sem
        self.n = n
        self.seed = seed
        self.interp = self.get_interpolator(synth_dither=synth_dither, n=n, seed=seed)

    def get_interpolator(self, synth_dither=0.0, n=10, seed=None):
        X = tuple([np.linspace(0, 1.001, n) for _ in range(6)])
        shp = [n] * 6
        if seed is not None:
            np.random.seed(seed)
        y = synth_dither * np.random.randn(*shp)
        interp = RegularGridInterpolator(X, y, bounds_error=False, fill_value=0)
        return interp

    def f(self, x: np.ndarray) -> float:
        x_append = np.append(x, 1 - sum(x))
        synth_dither = self.interp(x_append)[0]
        return checked_cast(float, hartmann6(x_append) + synth_dither)

    def f_without_dither(self, x: np.ndarray) -> float:
        x_append = np.append(x, 1 - sum(x))
        return checked_cast(float, hartmann6(x_append))

    # override
    def fetch_trial_data(
        self, trial: BaseTrial, noisy: bool = True, **kwargs: Any
    ) -> Data:
        sem = self.sem if noisy else 0.0
        noise_sd = self.noise_sd if noisy else 0.0
        arm_names = []
        mean = []
        for name, arm in trial.arms_by_name.items():
            arm_names.append(name)
            val_true = self._evaluate(params=arm.parameters)
            if noise_sd:
                # add heteroskedastic noise
                val = val_true + noise_sd * val_true / -1.515 * np.random.randn()
            mean.append(val)
        # indicate unknown noise level in data
        if noise_sd is None:
            noise_sd = float("nan")
        df = pd.DataFrame(
            {
                "arm_name": arm_names,
                "metric_name": self.name,
                "mean": mean,
                "sem": sem,
                "trial_index": trial.index,
                "n": 10000 / len(arm_names),
                "frac_nonnull": mean,
            }
        )
        return Data(df=df)


register_metric(NoisyCompositionalHartmann6Metric)


def extraordinary_probability(
    y_true: Union[list, np.ndarray],
    y_pred: Union[list, np.ndarray],
    mx: float = None,
    mn: float = None,
    thresh: float = 0.10,
    verbose: bool = True,
    minimize: bool = True,
    use_quantile: bool = False,
):
    """Determine the probability of finding an extraordinary candidate.

    Note that the predicted values are used for thresholding, while the true values are
    for determining whether or not an extraordinary candidate was found. In other words,
    this assumes you are on a fixed budget and using this as a screening tool.
    Candidates which had a low predicted value and a high true value wouldn't be
    considered in the pool of extraordinary candidates. This is similar to doing repeats
    to verify extraordinary observations subject to noise.

    Parameters
    ----------
    y_true : Union[list, np.ndarray]
        True property values.
    y_pred : Union[list, np.ndarray]
        Predicted property values.
    mx : float, optional
        Estimate of true maximum. If None, then max(y_true) is used. By default None.
    mn : float, optional
        Estimate of true minimum. If None, then min(y_true) is used. By default None.
    thresh : float, optional
        Threshold to use for defining an extraordinary candidate, by default 0.10
    verbose : bool, optional
        Whether or not to print information about the number of candidates required to
        find and the probability of finding an extraordinary compound, by default True
    minimize : bool, optional
        Whether lower values are considered more optimal, by default True
    use_quantile : bool, optional
        Whether to use quantile methods of thresholding rather than a percentage
        relative to the true optimum, by default False

    Returns
    -------
    p
        probability of finding an extraordinary candidate
    ids
        ids of candidates considered to be extraordinary
    """
    if isinstance(y_true, list):
        y_true = np.array(y_true)
    if isinstance(y_pred, list):
        y_pred = np.array(y_pred)
    if mx is None:
        mx = max(y_true)
    if mn is None:
        mn = min(y_true)
    if minimize:
        if use_quantile:
            cutoff = np.quantile(y_true, 0.02)
        else:
            cutoff = mn + (mx - mn) * thresh
        ids = y_pred < cutoff
        n_ext = sum(y < cutoff for y in y_pred)
        p = n_ext / len(y_true)
    else:
        if use_quantile:
            cutoff = np.quantile(y_true, 0.02)
        else:
            cutoff = mx - (mx - mn) * thresh
        ids = y_pred > cutoff
        n_ext = sum(y > cutoff for y in y_pred)
        p = n_ext / len(y_true)
    if verbose:
        if n_ext > 0:
            print(
                f"probability of finding candidate within {100*thresh:.1f}% of best estimated optimum (f<{cutoff:.4f}): {100*p:.4f}%. In other words, on average {int(np.round(1/p)) if p != 0 else np.inf} candidates required to find one extraordinary candidate."
            )
        else:
            print(
                f"no candidates found within {100*thresh:.1f}% of best estimated optimum (f<{cutoff:.4f}): using {len(y_true)} observations. "
            )
    return p, ids


# %% Code Graveyard
# class NoisyCompositionalHartmann6Metric(NoisyFunctionMetric):
#     def __init__(self, simplex_noise=0.0, pts_per_hull=1000, n_hulls=100, seed=None):
#         self.interps = self.get_interpolators(
#             simplex_noise=simplex_noise,
#             pts_per_hull=pts_per_hull,
#             n_hulls=n_hulls,
#             seed=seed,
#         )
#         super().__init__()

#     def get_interpolators(simplex_noise=0.0, pts_per_hull=1000, n_hulls=100, seed=None):
#         interps: List[LinearNDInterpolator] = []
#         if seed is not None:
#             np.random.seed(seed)
#         Pts = np.random.rand(n_hulls, pts_per_hull, 7)
#         for pts in Pts:
#             interp = LinearNDInterpolator(
#                 pts[:, :6], simplex_noise * pts[:, 6], rescale=True
#             )
#             interps.append(interp)
#         return interps

#     def evaluate_interpolators(self, x: np.ndarray) -> float:
#         y = 0.0
#         d = len(self.interps)
#         for interp in self.interps:
#             y = y + interp(x)
#         y = y / d  # rescale
#         return y

#     def f(self, x: np.ndarray) -> float:
#         x_append = np.append(x, 1 - sum(x))

#         return checked_cast(float, hartmann6(x_append))
