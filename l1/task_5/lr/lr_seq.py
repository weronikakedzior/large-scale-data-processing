"""Linear regression sequential."""

from typing import List
from lr import base


class LinearRegressionSequential(base.LinearRegression):
    """Linear regression sequential class."""

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        """Fit method."""
        n = len(X)
        mean_x = sum(X) / float(n)
        mean_y = sum(y) / float(n)
        covar = 0.0
        var = 0.0
        for i in range(n):
            covar += (X[i] - mean_x) * (y[i] - mean_y)
            var += (X[i] - mean_x)**2
        b_1 = covar / var
        b_0 = mean_y - b_1 * mean_x
        self._coef = [b_0, b_1]
        return self
