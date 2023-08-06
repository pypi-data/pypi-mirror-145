from itertools import permutations
from os.path import join

import numpy as np
import pandas as pd
from axforchemistry.utils.fractional import fractional_decode, fractional_encode


def load_data(
    data_dir=".",
    fname="train.csv",
    dummy=False,
    is_percent=False,  # False means fraction
    target_names=["target"],
    verbose=True,
):
    if dummy:
        unique_components = ["filler_A", "filler_B", "resin_A", "resin_B", "resin_C"]
        components = np.array(
            [
                ["filler_A", "filler_B", "resin_C"],
                ["filler_A", "resin_B"],
                ["filler_A", "filler_B", "resin_B"],
                ["filler_A", "resin_B", "resin_C"],
                ["filler_B", "resin_A", "resin_B"],
                ["filler_A", "resin_A"],
                ["filler_B", "resin_A", "resin_B"],
            ],
            dtype=object,
        )

        compositions = np.array(
            [
                [0.4, 0.4, 0.2],
                [0.5, 0.5],
                [0.5, 0.3, 0.2],
                [0.5, 0.5, 0.0],
                [0.6, 0.4, 0.0],
                [0.6, 0.4],
                [0.6, 0.2, 0.2],
            ],
            dtype=object,
        )

        X_train = fractional_encode(components, compositions)

        np.random.seed(10)
        y_train = 100 * np.random.rand(X_train.shape[0])

    else:
        fpath = join(data_dir, fname)
        X_train = pd.read_csv(fpath)
        y_train = X_train[target_names]
        X_train.drop(columns=target_names, inplace=True)
        if is_percent:
            # convert percent to fraction
            X_train = X_train / 100

        # last_component = pd.DataFrame(
        #     1 - X_train.sum(axis=1), columns=["last_component"]
        # )
        # X_train = pd.concat((X_train, last_component), axis=1)
        unique_components = list(X_train.columns)
        components, compositions = fractional_decode(X_train)

    if verbose:
        print("loaded unique_components (ensure no extras): ", unique_components)

    return unique_components, X_train, y_train


def fill_missing_keys(
    component_dict,
    composition_dict,
    component_slot_names,
    composition_slot_names,
    unique_components,
):
    # fill the data
    data = {**component_dict, **composition_dict}
    for slot_name in component_slot_names + composition_slot_names:
        if slot_name not in data.keys():
            if slot_name in component_slot_names:
                setdiff = set(unique_components) - set(list(component_dict.values()))
                data[slot_name] = list(setdiff)[0]
            elif slot_name in composition_slot_names:
                data[slot_name] = 0.0
    # sort the data
    sorted_component_dict = {key: data[key] for key in component_slot_names}
    sorted_composition_dict = {key: data[key] for key in composition_slot_names}
    sorted_data = {**sorted_component_dict, **sorted_composition_dict}
    return sorted_data


def gen_symmetric_trials(data, component_slot_names, composition_slot_names):
    nslots = len(data) // 2

    vals = list(data.values())
    pairs = list(zip(vals[:nslots], vals[nslots:]))
    combs = list(permutations(pairs, 5))

    comb_data = []
    for comb in combs:
        subcomponents, subcompositions = zip(*comb)
        component_dict = {
            component_slot_name: component
            for (component_slot_name, component) in zip(
                component_slot_names, subcomponents
            )
        }
        composition_dict = {
            composition_slot_name: component
            for (composition_slot_name, component) in zip(
                composition_slot_names, subcompositions
            )
        }
        comb_data.append({**component_dict, **composition_dict})

    return comb_data


def composition_data(dummy=False, fname="1d-hist-monomers.csv"):
    if dummy:
        unique_components = ["filler_A", "filler_B", "resin_A", "resin_B", "resin_C"]

        components = np.array(
            [
                ["filler_A", "filler_B", "resin_C"],
                ["filler_A", "resin_B"],
                ["filler_A", "filler_B", "resin_B"],
                ["filler_A", "resin_B", "resin_C"],
                ["filler_B", "resin_A", "resin_B"],
                ["filler_A", "resin_A"],
                ["filler_B", "resin_A", "resin_B"],
            ],
            dtype=object,
        )

        compositions = np.array(
            [
                [0.4, 0.4, 0.2],
                [0.5, 0.5],
                [0.5, 0.3, 0.2],
                [0.5, 0.5, 0.0],
                [0.6, 0.4, 0.0],
                [0.6, 0.4],
                [0.6, 0.2, 0.2],
            ],
            dtype=object,
        )

        X_train = fractional_encode(components, compositions)

        np.random.seed(10)
        y_train = 100 * np.random.rand(X_train.shape[0])

        exp_name = "dummy_experiment"
        target_name = "dummy"

        n_slots = 5
        # 2**m candidates will be generated per unique nchoosek combination
        comb_m = 6

    else:
        X_train = pd.read_csv(fname)
        target_name = "Compressive Strength (MPa)"
        y_train = X_train[target_name]
        X_train.drop(columns=target_name, inplace=True)
        # convert percent to fraction
        X_train = X_train / 100
        unique_components = list(X_train.columns)
        components, compositions = fractional_decode(X_train)
        exp_name = "composite_compressive_strength"

        n_slots = 5
        # 2**m candidates will be generated per unique nchoosek combination
        comb_m = 10

    extra_info = dict(
        exp_name=exp_name, target_name=target_name, n_slots=n_slots, comb_m=comb_m
    )
    return X_train, y_train, unique_components, extra_info
