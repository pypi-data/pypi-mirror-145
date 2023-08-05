from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

import numpy as np
import scipy.sparse
from typing_extensions import Protocol, runtime_checkable

from .grid import Grid
from .isoline import Isoline
from .lip import Lip
from .square import Square, WalkResult
from .types import *

__all__ = [
    "Implicit",
    "Lip",
    "Data",
    "Grid",
    "Square",
    "Isoline",
]


@runtime_checkable
class Fun(Protocol):
    def __call__(self, x: float, y: float) -> float:
        pass


@dataclass(frozen=True)
class Implicit:
    f: Fun
    grid: Grid
    data: Data
    altitude: float
    eval_callback: Optional[Callable[[float, float, float], None]]
    line_callback: Optional[Callable[[float, float, float, float], None]]

    @staticmethod
    def make(
        f: Callable[[float, float], float],
        grid: Grid,
        data: Data,
        altitude: float,
        eval_callback: Optional[Callable[[float, float, float], None]] = None,
        line_callback: Optional[Callable[[float, float, float, float], None]] = None,
    ) -> Implicit:
        assert isinstance(f, Fun)
        return Implicit(
            f, grid, data, altitude, eval_callback=eval_callback, line_callback=line_callback
        )

    def is_above(self, ix: int, iy: int) -> bool:
        return self.eval(ix, iy) >= self.altitude

    def is_below(self, ix: int, iy: int) -> bool:
        return self.eval(ix, iy) < self.altitude

    def eval(self, ix: int, iy: int) -> float:
        assert 0 <= ix <= self.grid.x_divs
        assert 0 <= iy <= self.grid.y_divs
        v = float(self.data.cache[ix, iy])
        if v == 0:
            x, y = self.grid.real_coordinates(ix, iy)
            f = self.f
            v = f(float(x), float(y))
            cb = self.eval_callback
            if cb:
                cb(x, y, v)
            if v == 0:
                v = sys.float_info.min
            self.data.cache[ix, iy] = v
        if v == sys.float_info.min:
            v = 0
        return v

    def find_integer_coordinates(
        self, x: float, y: float, above: bool, delta: int
    ) -> Tuple[int, int, int]:
        f = self.f
        ix0, iy0 = self.grid.integer_coordinates(x, y)
        c = self.eval(ix0, iy0) >= self.altitude
        if c == above:
            return ix0, iy0, delta
        while delta >= 1:
            for dx, dy in [(0, 1), (1, 0), (1, 1)]:
                ix = round(ix0 / delta + dx) * delta
                iy = round(iy0 / delta + dy) * delta
                c = self.eval(ix, iy) >= self.altitude
                if c == above:
                    return ix, iy, delta
            delta = delta // 2
        raise Exception("COuld not find starting point")


@dataclass(frozen=True)
class Data:
    """
    Class holding evaluted function points
    """

    #: Data array, type of elements is :data:`numpy.float64`
    #:
    #: The size of this matrix is ``x_divs+1`` times ``y_divs+1``.
    cache: scipy.sparse.dok_matrix

    x_divs: int
    y_divs: int

    @staticmethod
    def empty(x_divs: int, y_divs: int) -> Data:
        """
        Returns fresh empty storage for evaluated function points

        Args:
            x_divs: Number of x divisions, must be a power-of-two
            y_divs: Number of y divisions, must be a power-of-two
        """
        cache = scipy.sparse.dok_matrix((x_divs + 1, y_divs + 1), dtype=np.float64)
        return Data(cache, x_divs, y_divs)
