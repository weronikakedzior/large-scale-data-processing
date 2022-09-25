"""Base."""

from __future__ import annotations

import abc
from typing import List

import numpy as np


class ScikitPredictor(abc.ABC):
    """ScikitPredictor."""

    @abc.abstractmethod
    def fit(self, X, y):
        """Abstract fit."""
        pass

    @abc.abstractmethod
    def predict(self, X):
        """Abstract predict."""
        pass


class LinearRegression(ScikitPredictor):
    """Base Linear Regression."""

    def __init__(self):
        """Linear Regression init."""
        self._coef = None

    @abc.abstractmethod
    def fit(self, X: List[float], y: List[float]) -> LinearRegression:
        """Abstract fit method."""
        pass

    def predict(self, X: List[float]) -> np.ndarray:
        """Predict method."""
        if self._coef is None:
            raise RuntimeError('Please fit model before prediction')

        return self._coef[0] + self._coef[1] * np.array(X)
