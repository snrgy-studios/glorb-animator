from pyodide.ffi import to_js # type: ignore
from js import console # type: ignore
from js.THREE import Color, IcosahedronGeometry # type: ignore
import js.THREE as THREE # type: ignore
from gtypes import Color as RGBColor, Colors, IcosahedronGeometry, Vector3
from __init__ import to_spherical

from threejs import GLORBThreeJS as GLORB
# from icosahedron import geometry


def to_rgb(color) -> int | RGBColor:
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
    for index, new_color in enumerate(GLORB.map_colors(colors)):
        color.setRGB(*to_rgb(new_color))
        for j in range(3):
            colors1.setXYZ(index * 3 + j, color.r, color.g, color.b)
    colors1.needsUpdate = True


def set_colors(glorb: GLORB) -> None:
    color = THREE.Color.new()
    colors1 = glorb.geometry.attributes.color
    for index, new_color in enumerate(glorb.colors_mapped):
        color.setRGB(*to_rgb(new_color))
        for j in range(3):
            colors1.setXYZ(index * 3 + j, color.r, color.g, color.b)
    colors1.needsUpdate = True
