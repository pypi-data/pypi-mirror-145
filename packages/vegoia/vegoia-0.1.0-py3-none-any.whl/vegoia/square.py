from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Sequence, Union

from .grid import Grid
from .lip import Lip
from .types import *

if TYPE_CHECKING:
    from . import Implicit


@dataclass(frozen=True)
class WalkResult:
    path: Sequence[Lip]
    ends_on_target: bool


@dataclass(frozen=True)
class Square:
    """
    Describes a marching square with a distinguished side

    The marching square is described by a :class:`.Lip` and a delta displacement.
    """

    #: Supporting side of the marching square
    lip: Lip

    #: Delta x shifting the lip to make a square
    dx: int

    #: Delta y shifting the lip to make a square
    dy: int

    def split(self, implicit: Implicit) -> Square:
        """
        Returns a marching square with side size halved

        Args:
            implicit: Function to plot
        """
        return Square(self.lip.split(implicit), self.dx // 2, self.dy // 2)

    def __post_init__(self) -> None:
        delta = self.lip.delta()
        if self.lip.is_horizontal():
            assert self.dx == 0
            assert abs(self.dy) == delta
        else:
            assert self.lip.is_vertical()
            assert abs(self.dx) == delta
            assert self.dy == 0
        ix1, iy1, _, ix2, iy2, _ = self.lip.unpack()
        assert self.lip.grid.is_valid_integer_coordinates(ix1 + self.dx, iy1 + self.dy)
        assert self.lip.grid.is_valid_integer_coordinates(ix2 + self.dx, iy2 + self.dy)

    def reverse(self) -> Optional[Square]:
        """
        Returns, if it exists, the marching square mirrored across the distinguished side

        Text drawing::

            5    1    3

            6    2    4

        The points 1-2 represent the lip. Here, we have ``dx > 0``, and thus the marching square is
        1-2-3-4. The reversed marching square is then 1-2-6-5, keeping the same distinguished side
        (i.e. :class:`.Lip`) and reversing ``(dx,dy)``.
        """
        ix1, iy1, _, ix2, iy2, _ = self.lip.unpack()
        if not self.lip.grid.is_valid_integer_coordinates(ix1 - self.dx, iy1 - self.dy):
            return None
        if not self.lip.grid.is_valid_integer_coordinates(ix2 - self.dx, iy2 - self.dy):
            return None
        return Square(self.lip, -self.dx, -self.dy)

    def walk(self, target: Lip, implicit: Implicit) -> WalkResult:
        """
        Performs a marching square walk from the current square and returns the lips

        The walk stops when:

        - The path attained the target, either by being equal to it, or by being included in it.
          The returned path includes the lip from the initial marching square, but does not include
          the target at the end.

        - The path attained the border of the grid. The returned path includes the lip from the
          original marching square up to the border lip, included.

        Raises:
            Exception: if no progress could be made at any step size delta >= 1.

        Args:
            target: Lip to stop on
            implicit: Function to plot

        Returns:
            A dataclass containing the path and the stopping criterion, or `None`

        """
        step = self
        first = True
        lips: List[Lip] = []
        while first or (not target.contains(step.lip)):
            res: Union[Square, Lip, None] = None
            while res is None:
                res = step.step(implicit)
                if res is None:
                    logging.info("Ambiguous marching square, halving delta")
                    if step.lip.delta() == 1:
                        raise Exception("Could not progress")
                    step = step.split(implicit)
            lips.append(step.lip)
            if isinstance(res, Lip):
                lips.append(res)
                return WalkResult(lips, False)
            assert isinstance(res, Square)
            if implicit.line_callback is not None:
                x1, y1 = step.lip.real_coordinates()
                x2, y2 = res.lip.real_coordinates()
                implicit.line_callback(x1, y1, x2, y2)
            step = res
            first = False
        return WalkResult(lips, True)

    def step(self, implicit: Implicit) -> Union[Square, Lip, None]:
        """
        Returns the result of stepping around this marching square

        There are three situations depending on the result type:

        - if the type is :class:`.Square`, a new marching square was found
        - if the type is :class:`.Lip`, the lip that should support the new marching square is on
          the border and the marching square would extend outside the grid
        - if the type is `None`, the step is ambiguous and the delta should be halved

        Args:
            implicit: Function to plot
        """
        grid = implicit.grid
        altitude = implicit.altitude
        ix1, iy1, v1, ix2, iy2, v2 = self.lip.unpack()
        ix3 = ix1 + self.dx
        iy3 = iy1 + self.dy
        ix4 = ix2 + self.dx
        iy4 = iy2 + self.dy
        # we find the other corners of the marching square, the sides of the square are
        # the segments:
        # 1-3 3-4 2-4, with 1-2 being the current side
        # we want a lip with opposite below/above
        #
        # Example in a given orientation:
        #
        # 1   3
        #
        # 2   4

        valid = 0
        v3 = implicit.eval(ix3, iy3)
        v4 = implicit.eval(ix4, iy4)
        c1 = v1 >= altitude
        c2 = v2 >= altitude
        c3 = v3 >= altitude
        c4 = v4 >= altitude
        # side 1-3
        if c1 != c3:
            valid += 1
            lip = Lip(grid, altitude, ix1, iy1, v1, ix3, iy3, v3)
            dx = ix1 - ix2
            dy = iy1 - iy2
            #   #   #
            #
            #   1 ^ 3
            #
            #   2   4

        if (not c3) and c4:
            # c3 is below, c4 is above
            valid += 1
            lip = Lip(grid, altitude, ix3, iy3, v3, ix4, iy4, v4)
            dx, dy = self.dx, self.dy  # continue in the same direction
            # 1    3     #
            #      >
            # 2    4     #

        if c3 and (not c4):
            # c4 is below, c3 is above
            valid += 1
            lip = Lip(grid, altitude, ix4, iy4, v4, ix3, iy3, v3)
            dx, dy = self.dx, self.dy  # continue in the same direction
            # 1    3     #
            #      >
            # 2    4     #

        if c2 != c4:
            valid = valid + 1
            lip = Lip(grid, altitude, ix4, iy4, v4, ix2, iy2, v2)
            dx = ix2 - ix1
            dy = iy2 - iy1
            #   1   3
            #
            #   2 v 4
            #
            #   #   #
        if valid > 1:
            return None  # ambiguous result
        if not (
            grid.is_valid_integer_coordinates(lip.ix1 + dx, lip.iy1 + dy)
            and grid.is_valid_integer_coordinates(lip.ix2 + dx, lip.iy2 + dy)
        ):
            return lip
        else:
            return Square(lip, dx, dy)

    @staticmethod
    def make(lip: Lip) -> Square:
        """
        Returns a marching square created from a lip

        Args:
            lip: Lip forming the supporting side of the future marching square
        """
        delta = lip.delta()
        if lip.is_horizontal():
            if lip.iy1 + delta <= lip.grid.y_divs:
                return Square(lip, 0, delta)
            else:
                assert lip.iy1 - delta >= 0
                return Square(lip, 0, -delta)
        elif lip.is_vertical():
            if lip.ix1 + delta <= lip.grid.x_divs:
                return Square(lip, delta, 0)
            else:
                assert lip.ix1 - delta >= 0
                return Square(lip, -delta, 0)
        else:
            raise ValueError("Invalid lip")

    @staticmethod
    def from_support_and_target_lip(support: Lip, target: Lip) -> Square:
        """
        Returns a marching square supported by a lip, moving towards another lip

        Both lips must have the same :meth:`.Lip.delta` value.

        Args:
            support: Lip supporting the future marching square
            target: Target direction of the marching square
        """
        delta = support.delta()
        assert delta == target.delta()
        if support.is_horizontal():
            iy = support.iy1
            plus = target.iy1 > iy or target.iy2 > iy
            minus = target.iy1 < iy or target.iy2 < iy
            assert plus != minus
            dx = 0
            if plus:
                dy = delta
            else:
                dy = -delta
        else:
            assert support.is_vertical()
            ix = support.ix1
            plus = target.ix1 > ix or target.ix2 > ix
            minus = target.ix1 < ix or target.ix2 < ix
            assert plus != minus
            dy = 0
            if plus:
                dx = delta
            else:
                dx = -delta
        return Square(support, dx, dy)
