import numpy as np


# Returns a function such that input t (0 ≤ t ≤ 1) maps to the position 100t% the way through the function
def generate_function(raw_points):
    return lambda t: raw_points[int(t * (len(raw_points) - 1))]

# Numerical integration by splitting the function into rectangles of width dx and summing them
def integrate(a, b, f, dx):
    # return np.sum(f(np.arange(a, b, dx)) * dx)
    total = 0
    for x in np.arange(a, b, dx):
        total += f(x) * dx

    return total

# Calculates the coefficient for the nth term in the Fourier series (determines its magnitude and starting angle)
def compute_constant(n, f):
    n_t = lambda t: f(t) * np.exp(n * 2j * np.pi * t)
    return integrate(0, 1, n_t, 0.0001)

# Returns a function of the series of n complex numbers
def compute_fourier_series(n_total, f):
    constants = {}

    # iterate n from -n/2 to n/2
    for n in range(int(-n_total / 2), int(n_total / 2) + n_total % 2):
        constants[n] = compute_constant(n, f)

    return lambda t: [c * np.exp(n * 2j * np.pi * t) for n, c in constants.items()]