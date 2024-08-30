from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from threejs_stubs import BufferAttribute, IcosahedronGeometry, Vector3
else:
    # Use Any to indicate flexibility at runtime
    BufferAttribute = Any
    IcosahedronGeometry = Any
    Vector3 = Any


# Three.js specific types
__all__ = [
    'BufferAttribute',
    'IcosahedronGeometry',
    'Vector3',
]


# Type alias for LEDMAP and FACEMAP to ensure that they are tuples of exactly 80 integers
Map = tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
PointValue = int | float
GeometryPoint = list[PointValue, PointValue, PointValue]
GeometryData = list[GeometryPoint]
Color = tuple[PointValue, PointValue, PointValue] | list[PointValue]
Colors = list[Color]
# type: ignore