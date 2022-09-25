"""Linear regression process."""

from typing import List
from concurrent.futures import ProcessPoolExecutor
from lr import base
from lr.methods import clc_ss, mean, split_data


class LinearRegressionProcess(base.LinearRegression):
    """Linear regression process class."""

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        """Fit method."""
        num = 2
        covar = 0
        var = 0
        with ProcessPoolExecutor(max_workers=num) as e:
            m_x, m_y = mean(X), mean(y)
            s_X = split_data(num, X)
            s_y = split_data(num, y)
            for i in range(num):
                result = e.submit(clc_ss, s_X[i], s_y[i], m_x, m_y).result()
                covar += result[0]
                var += result[1]
            b_1 = covar / var
            b_0 = m_y - b_1 * m_x
            self._coef = [b_0, b_1]

        return self
