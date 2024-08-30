from pyodide.ffi import to_js # type: ignore
from js import console # type: ignore
from js.THREE import Color, IcosahedronGeometry # type: ignore
import js.THREE as THREE # type: ignore

# _Color = tuple[int | float, int | float, int | float] | list[int | float]
# Colors = list[_Color] | tuple[_Color, ...]


# # Type alias for LEDMAP and FACEMAP to ensure that they are tuples of exactly 80 integers
# Map = tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
# PointValue = int | float
# GeometryPoint = list[PointValue, PointValue, PointValue]
# GeometryData = list[GeometryPoint]
# _Color = tuple[PointValue, PointValue, PointValue] | list[PointValue]
# Colors = list[_Color]

Map = tuple[int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int, int]
PointValue = int | float
GeometryPoint = list[PointValue, PointValue, PointValue]
GeometryData = list[GeometryPoint]
RGBColor = tuple[PointValue, PointValue, PointValue] | list[PointValue]
Colors = list[RGBColor]


from threejs import GLORBThreeJS as GLORB


def to_rgb(color) -> int | list[int | float] | tuple[float | int]:
    """Normalise a color to RGB values between 0 and 1."""
    if isinstance(color, int):
        # Assume color is hexadcimal
        return  [(color >> 16) / 255, ((color >> 8) & 0xFF) / 255, (color & 0xFF) / 255]
    if all(isinstance(c, int) for c in color) and all(0 <= c <= 255 for c in color):
        # Assume only ints means an RGB color with values between 0 and 255
        return [c / 255 for c in color]
    return color


def _set_colors(colors: Colors, geometry: 'IcosahedronGeometry') -> None:
    color = THREE.Color.new()
    colors1 = geometry.attributes.color
    for index, new_color in enumerate(colors):
        color.setRGB(*to_rgb(new_color))
        for j in range(3):
            colors1.setXYZ(index * 3 + j, color.r, color.g, color.b)
    colors1.needsUpdate = True


def set_colors(glorb: GLORB) -> None:
    color = THREE.Color.new()
    colors1 = glorb.geometry.attributes.color
    # for index, new_color in zip(FACE_MAP, colors):  # If colors are unmapped
    for index, new_color in enumerate(glorb.colors):
        color.setRGB(*to_rgb(new_color))
        for j in range(3):
            colors1.setXYZ(index * 3 + j, color.r, color.g, color.b)
    colors1.needsUpdate = True
