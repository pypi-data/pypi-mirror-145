from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Any, Tuple, overload

import numpy as np
import numpy.typing as npt

from .types import *


@dataclass(frozen=True)
class Grid:
    x_min: float
    x_max: float
    y_min: float
    y_max: float
    x_divs: int
    y_divs: int

    def __post_init__(self) -> None:
        assert round(math.log2(self.x_divs)) == math.log2(self.x_divs)
        assert round(math.log2(self.y_divs)) == math.log2(self.y_divs)

    def power_of_two_deltas(self, x_size: float, y_size: float) -> Tuple[int, int]:
        dx = x_size / (self.x_max - self.x_min) * self.x_divs
        dy = y_size / (self.y_max - self.y_min) * self.y_divs
        return int(2 ** math.floor(math.log2(dx))), int(2 ** math.floor(math.log2(dy)))

    def power_of_two_delta(self, size: float) -> int:
        dx, dy = self.power_of_two_deltas(size, size)
        return min(dx, dy)

    @staticmethod
    def make(
        x_min: Float, x_max: Float, y_min: Float, y_max: Float, x_divs: int, y_divs: int
    ) -> Grid:
        """
        Returns a coordinate system with a discrete grid

        Args:
            x_min: Minimum x coordinate
            x_max: Maximum x coordinate
            y_min: Minimum y coordinate
            y_max: Maximum y coordinate
            x_divs: Number of divisions of the range ``(x_min,x_max)``, must be a power-of-two
            y_divs: Number of divisions of the range ``(x_min,x_max)``, must be a power-of-two
        """
        return Grid(float(x_min), float(x_max), float(y_min), float(y_max), x_divs, y_divs)

    @overload
    def unrounded_integer_coordinates(self, x: Float, y: Float) -> Tuple[Float, Float]:
        pass

    @overload
    def unrounded_integer_coordinates(self, x: Vec[f8], y: Vec[f8]) -> Tuple[Vec[f8], Vec[f8]]:
        pass

    def unrounded_integer_coordinates(self, x: Any, y: Any) -> Tuple[Any, Any]:
        ix = (x - self.x_min) / (self.x_max - self.x_min) * self.x_divs
        iy = (y - self.y_min) / (self.y_max - self.y_min) * self.y_divs
        return ix, iy

    @overload
    def integer_coordinates(self, x: Float, y: Float) -> Tuple[int, int]:
        pass

    @overload
    def integer_coordinates(self, x: Vec[f8], y: Vec[f8]) -> Tuple[Vec[i8], Vec[i8]]:
        pass

    def integer_coordinates(self, x: Any, y: Any) -> Tuple[Any, Any]:
        ix = (x - self.x_min) / (self.x_max - self.x_min) * self.x_divs
        iy = (y - self.y_min) / (self.y_max - self.y_min) * self.y_divs
        if np.isscalar(ix):
            ix = round(ix)  # type: ignore
            iy = round(iy)  # type: ignore
        else:
            ix = np.round(ix).astype(i8)
            iy = np.round(iy).astype(i8)
        return ix, iy

    def is_valid_integer_coordinates(self, x: int, y: int) -> bool:
        return (0 <= x <= self.x_divs) and (0 <= y <= self.y_divs)

    @overload
    def real_coordinates(self, ix: int, iy: int) -> Tuple[float, float]:
        pass

    @overload
    def real_coordinates(self, ix: Vec[u4], iy: Vec[u4]) -> Tuple[Vec[f8], Vec[f8]]:
        pass

    def real_coordinates(self, ix: Any, iy: Any) -> Tuple[Any, Any]:
        x = self.x_min + (self.x_max - self.x_min) * ix / self.x_divs
        y = self.y_min + (self.y_max - self.y_min) * iy / self.y_divs
        if np.isscalar(x) and np.isscalar(y):
            x = float(x)  # type: ignore
            y = float(y)  # type: ignore
            if ix == self.x_divs:
                x = self.x_max
            if iy == self.y_divs:
                y = self.y_max
        else:
            assert (not np.isscalar(x)) and (not np.isscalar(y))
            x[ix == self.x_divs] == self.x_max
            y[iy == self.y_divs] == self.y_max
        return x, y
