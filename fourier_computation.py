import numpy as np



def generate_function(raw_points):
    return lambda t: raw_points[int(t * (len(raw_points) - 1))]


def integrate(a, b, f, dx):
    # return np.sum(f(np.arange(a, b, dx)) * dx)
    total = 0
    for x in np.arange(a, b, dx):
        total += f(x) * dx

    return total


def compute_constant(n, f):
    n_t = lambda t: f(t) * np.exp(n * 2j * np.pi * t)
    return integrate(0, 1, n_t, 0.0001)


def compute_fourier_series(n_total, f):
    constants = {}

    for n in range(int(-n_total / 2), int(n_total / 2) + 1):
        constants[n] = compute_constant(n, f)

    return lambda t: [c * np.exp(n * 2j * np.pi * t) for n, c in constants.items()]