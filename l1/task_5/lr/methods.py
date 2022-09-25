"""Method used in lr_thread and lr_proc."""


def clc_ss(X, y, mean_x, mean_y):
    """Method to calculate variance and covariance."""
    covar = 0.0
    var = 0.0
    for i in range(len(X)):
        covar += (X[i] - mean_x) * (y[i] - mean_y)
        var += (X[i] - mean_x) ** 2
    return covar, var


def mean(tab):
    """Method to calculate mean."""
    return sum(tab) / float(len(tab))


def split_data(num_thread, tab):
    """Method to split data."""
    splitted = []
    size = len(tab) / num_thread
    for i in range(num_thread):
        splitted.append(tab[int(i * size): int((i + 1) * size)])
    return splitted
