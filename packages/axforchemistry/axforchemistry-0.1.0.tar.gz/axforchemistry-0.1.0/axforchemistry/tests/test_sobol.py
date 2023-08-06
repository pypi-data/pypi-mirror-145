import numpy as np
from numpy.testing import assert_allclose
import axforchemistry.utils.sobol as sc


def test_nchoosek_sobol():
    unique_components = ["a", "b", "c"]
    X_train = sc.nchoosek_sobol(
        unique_components,
        n_slots=2,
        comb_m=3,
        scale=1.0,
        use_sobol=True,
        fixed_compositions=True,
        verbose=True,
        seed=10,
    )
    X_check = np.array(
        [
            [0.09002793, 0.90997207, 0.0],
            [0.84595743, 0.15404257, 0.0],
            [0.85923469, 0.14076531, 0.0],
            [0.18800008, 0.81199992, 0.0],
            [0.61794105, 0.0, 0.38205895],
            [0.47698318, 0.0, 0.52301682],
            [0.0, 0.09002793, 0.90997207],
            [0.09002793, 0.0, 0.90997207],
            [0.25658499, 0.0, 0.74341501],
            [0.61794105, 0.38205895, 0.0],
            [0.0, 0.25658499, 0.74341501],
            [0.25658499, 0.74341501, 0.0],
            [0.0, 0.18800008, 0.81199992],
            [0.18800008, 0.0, 0.81199992],
            [0.0, 0.47698318, 0.52301682],
            [0.0, 0.85923469, 0.14076531],
            [0.55160877, 0.0, 0.44839123],
            [0.0, 0.61794105, 0.38205895],
            [0.0, 0.55160877, 0.44839123],
            [0.0, 0.84595743, 0.15404257],
            [0.55160877, 0.44839123, 0.0],
            [0.85923469, 0.0, 0.14076531],
            [0.47698318, 0.52301682, 0.0],
            [0.84595743, 0.0, 0.15404257],
        ]
    )
    assert_allclose(
        X_train,
        X_check,
        atol=1e-4,
        err_msg="combinations of (3 choose 2) with 2**3 unique compositions did not match hard coded values.",
    )


if __name__ == "__main__":
    test_nchoosek_sobol()
