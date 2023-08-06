from timeit import default_timer as timer
import string
import numpy as np
from constraint import Problem

start = timer()

problem = Problem()

n_vars = 13
n_slots = 5
n_values = 10
vars = list(string.ascii_lowercase)[0:n_vars]
values = list(range(n_values))
[problem.addVariable(var, values) for var in vars]


def count_nonzero_components(*values, tol=1e-3):
    n_components = np.count_nonzero([value if value > tol else 0 for value in values])
    return n_components


def in_component_range(*values, min_components=1, max_components=n_slots):
    n_components = count_nonzero_components(*values)
    in_range = n_components >= min_components and n_components <= max_components
    return in_range


problem.addConstraint(in_component_range, vars)

params = problem.getSolutions()

end = timer()
print(end - start)

1 + 1
