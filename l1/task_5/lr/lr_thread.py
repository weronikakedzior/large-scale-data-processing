"""Linear regression threads."""

from typing import List
from lr import base
from lr.methods import clc_ss, mean, split_data
from concurrent.futures import ThreadPoolExecutor


class LinearRegressionThreads(base.LinearRegression):
    """Linear regression threads class."""

    def fit(self, X: List[float], y: List[float]) -> base.LinearRegression:
        """Fit method."""
        num_thread = 2
        covar = 0
        var = 0
        with ThreadPoolExecutor(max_workers=num_thread) as e:
            m_x, m_y = mean(X), mean(y)
            s_X = split_data(num_thread, X)
            s_y = split_data(num_thread, y)
            for i in range(num_thread):
                result = e.submit(clc_ss, s_X[i], s_y[i], m_x, m_y).result()
                covar += result[0]
                var += result[1]
            b_1 = covar / var
            b_0 = m_y - b_1 * m_x
            self._coef = [b_0, b_1]

        return self
