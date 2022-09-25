"""Numpy linear regression."""

from typing import List
from lr import base
import numpy as np


class LinearRegressionNumpy(base.LinearRegression):
    """Numpy linear regression class."""

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        """Fit method for linear regression."""
        X = np.array(X)
        y = np.array(y)
        n = np.size(X)
        m_x, m_y = np.mean(X), np.mean(y)
        SS_xy = np.sum(y * X) - n * m_y * m_x
        SS_xx = np.sum(X * X) - n * m_x * m_x
        b_1 = SS_xy / SS_xx
        b_0 = m_y - b_1 * m_x

        self._coef = [b_0, b_1]
        return self
