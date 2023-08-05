import typing

import numpy
import numpy.typing
from typing_extensions import Annotated

_ScalarType = typing.TypeVar("_ScalarType", bound=numpy.generic, covariant=True)

f8 = numpy.float64
u4 = numpy.uint32
i8 = numpy.int64

Float = typing.Union[numpy.float64, float]
Int = typing.Union[numpy.int64, int]

if typing.TYPE_CHECKING:
    Mat = numpy.typing.NDArray[_ScalarType]
    Vec = numpy.typing.NDArray[_ScalarType]
else:
    try:
        import beartype.vale

        Mat = Annotated[
            numpy.typing.NDArray[_ScalarType],
            beartype.vale.IsAttr["ndim", beartype.vale.IsEqual[2]],
        ]
        Vec = Annotated[
            numpy.typing.NDArray[_ScalarType],
            beartype.vale.IsAttr["ndim", beartype.vale.IsEqual[1]],
        ]
    except ImportError:
        Mat = (numpy.typing.NDArray[_ScalarType],)
        Vec = numpy.typing.NDArray[_ScalarType]
