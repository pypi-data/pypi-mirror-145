from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from tkinter import N
from typing import TYPE_CHECKING, List, Optional, Sequence, Tuple

import numpy as np
import numpy.typing as npt
from numpy import linalg

from .grid import Grid
from .lip import Lip
from .square import Square, WalkResult
from .types import *

if TYPE_CHECKING:
    from . import Implicit


def triangle_area(x: Vec[f8], y: Vec[f8]) -> float:
    m = np.vstack([[1.0, 1.0, 1.0], x, y])
    return float(linalg.det(m))


def refine2(l1: Lip, l2: Lip, implicit: Implicit) -> Optional[Sequence[Lip]]:
    """
    Refines the path between two lips

    Args:
        l1: Starting lip
        l2: Target lip
        implicit: Function to plot

    Returns:
        A new path between l1 and l2, both included, or None if the path could not be refined
    """
    delta = l1.delta()
    assert delta == l2.delta()
    if l1.shared_point(l2) is not None:
        if delta == 1:
            return None
        else:
            return [l1.split(implicit), l2]
    start: Square = Square.from_support_and_target_lip(l1, l2)
    res = start.walk(l2, implicit)
    if not res.ends_on_target:
        # on border, verify that the path ends on a refinement of the next lip
        assert l2.on_border() and l2.contains(res.path[-1])
        return res.path
    else:
        return [*res.path, l2]


def refine3_12(l1: Lip, l2: Lip, l3: Lip, implicit: Implicit) -> Optional[Sequence[Lip]]:
    res = refine2(l1, l2, implicit)
    if res is None:
        return None
    return [*res, l3]


def refine3_23(l1: Lip, l2: Lip, l3: Lip, implicit: Implicit) -> Optional[Sequence[Lip]]:
    res = refine2(l2, l3, implicit)
    if res is None:
        return None
    return [l1, *res]


def refine3(l1: Lip, l2: Lip, l3: Lip, implicit: Implicit) -> Optional[Sequence[Lip]]:
    d1 = l1.delta()
    d2 = l2.delta()
    d3 = l3.delta()
    d = min(d1, d2, d3)
    if d1 != d:
        l1 = l1.split(implicit)
        return [l1, l2, l3]
    if d2 != d:
        l2 = l2.split(implicit)
        return [l1, l2, l3]
    if d3 != d:
        l3 = l3.split(implicit)
        return [l1, l2, l3]

    if l1.distance_squared(l2) >= l2.distance_squared(l3):
        seq = [refine3_12, refine3_23]
    else:
        seq = [refine3_23, refine3_12]

    for s in seq:
        res = s(l1, l2, l3, implicit)
        if res is not None:
            return res

    return None


@dataclass
class IsolineWIP:
    starting_lip: Lip
    path1: Sequence[Lip]
    path2: Optional[Sequence[Lip]]

    @staticmethod
    def make(starting_lip: Lip) -> IsolineWIP:
        pass


@dataclass
class Isoline:
    #: Matrix of lip coordinates, every row is (ix1, iy1, ix2, iy2)
    lips: Mat[i8]

    #: Vector of interpolated x real coordinates
    x: Vec[f8]

    #: Vector of interpolated y real coordinates
    y: Vec[f8]

    #: Area of the triangle support by the three points supported around a point
    area: Vec[f8]

    #: Whether this isoline is open
    is_closed: bool

    #: Altitude of the isoline
    altitude: float

    def plot_coordinates(self) -> Tuple[Vec[f8], Vec[f8]]:
        """
        Returns the coordinates to plot this isoline

        If the isoline is open, it returns the points of the isoline (:attr:`.x` and :attr:`.y`)

        If the isoline is closed however, it repeats the starting point at the beginning and the
        end so that you can draw a closed shape.

        Returns:
            A tuple (vec_x, vec_y)
        """
        if self.is_closed:
            return np.concatenate([self.x, [self.x[0]]]), np.concatenate([self.y, [self.y[0]]])
        else:
            return self.x, self.y

    def max_error(self) -> float:
        """
        Returns an estimation of the maximal error for the segments in this isoline, in area units
        """
        return float(np.max(self.area))

    def lip(self, i: int, implicit: Implicit) -> Lip:
        """
        Return the i-th lip in this isoline

        Args:
            i: Lip index
            implicit: Function to plot
        """
        n = len(self.x)
        if self.is_closed:
            i = i % n
        else:
            assert 0 <= i <= n
        ix1 = int(self.lips[i, 0])
        iy1 = int(self.lips[i, 1])
        v1 = implicit.eval(ix1, iy1)
        ix2 = int(self.lips[i, 2])
        iy2 = int(self.lips[i, 3])
        v2 = implicit.eval(ix2, iy2)
        return Lip(implicit.grid, self.altitude, ix1, iy1, v1, ix2, iy2, v2)

    # def refine(self, implicit: Implicit) -> bool:
    #     ind = np.where(self.area == np.max(self.area))
    #     i = int(ind[0])
    #     lips = refine3(
    #         self.lip(i - 1, implicit), self.lip(i, implicit), self.lip(i + 1, implicit), implicit
    #     )
    #     if lips is None:
    #         return False
    #     self.subs(i, lips)
    #     return True

    # def refine(self, implicit: Implicit) -> bool:
    #     ind = np.where(self.area == np.max(self.area))
    #     i = int(ind[0])
    #     lips = refine3(
    #         self.lip(i, implicit), self.lip(i + 1, implicit), self.lip(i + 2, implicit), implicit
    #     )
    #     if lips is None:
    #         return False
    #     self.subs(i + 1, lips)
    #     return True

    # def refine(self, implicit: Implicit) -> bool:
    #     """
    #     Performs a refinement step of this isoline

    #     Args:
    #         implicit: Function to plot

    #     Returns:
    #         Whether a refinement could be done
    #     """
    #     raise NotImplementedError

    @staticmethod
    def from_bisection(
        below: Optional[Tuple[float, float]],
        above: Optional[Tuple[float, float]],
        feature_size: float,
        implicit: Implicit,
    ) -> Isoline:
        grid = implicit.grid
        delta = grid.power_of_two_delta(feature_size)
        i_below: Optional[Tuple[int, int]] = None
        i_above: Optional[Tuple[int, int]] = None
        if below is not None:
            ix, iy, delta = implicit.find_integer_coordinates(
                below[0], below[1], above=False, delta=delta
            )
            i_below = (ix, iy)
        if above is not None:
            ix, iy, delta = implicit.find_integer_coordinates(
                above[0], above[1], above=True, delta=delta
            )
            i_above = (ix, iy)
        lip, _ = Lip.from_bisection(i_below, i_above, delta, implicit)
        return Isoline.from_starting_lip(lip, implicit)

    @staticmethod
    def from_grid(cell_size: float, feature_size: float, implicit: Implicit) -> Sequence[Isoline]:
        assert feature_size <= cell_size
        grid = implicit.grid
        gdx, gdy = grid.power_of_two_deltas(cell_size, cell_size)
        delta = grid.power_of_two_delta(feature_size)
        starting_lips = Lip.from_grid(gdx, gdy, delta, implicit)
        return [Isoline.from_starting_lip(lip, implicit) for lip in starting_lips]

    @staticmethod
    def from_starting_lip(lip: Lip, implicit: Implicit) -> Isoline:
        start = Square.make(lip)
        res = start.walk(lip, implicit)
        lips = res.path
        if res.ends_on_target:
            is_closed = True
        else:
            is_closed = False
            step_rev = start.reverse()
            if step_rev is not None:
                res_rev = step_rev.walk(lip, implicit)
                if res_rev is None:
                    return None
                assert not res_rev.ends_on_target
                lips_rev = res_rev.path
                # drop the first step, which is present in both, then reverse the one that
                # went in the other direction and prepend it
                lips = [*reversed(lips), *lips_rev[1:]]
        n = len(lips)
        x_coords = np.zeros((n,), dtype=f8)
        y_coords = np.zeros((n,), dtype=f8)
        lips_coords = np.zeros((n, 4), dtype=i8)
        area = np.zeros((n,), dtype=f8)
        for i in range(n):
            l = lips[i]
            x, y = l.real_coordinates()
            x_coords[i] = x
            y_coords[i] = y
            lips_coords[i, :] = [l.ix1, l.iy1, l.ix2, l.iy2]
        if is_closed:
            r = range(0, n)  # 0 to n-1
        else:
            r = range(1, n - 1)  # 1 to n-2
        for i in r:  # 1 to n-1
            r3 = [i - 1, i, i + 1]
            area[i] = triangle_area(x_coords[r3], y_coords[r3])
        return Isoline(lips_coords, x_coords, y_coords, area, is_closed, implicit.altitude)
