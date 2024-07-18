from js.THREE import Color, IcosahedronGeometry


FACE_MAP = (63, 22, 6, 3, 24, 60, 61, 62, 23, 21, 20, 7, 5, 4, 0, 1, 2, 26, 25, 27, 46, 43, 41, 42, 59, 76, 77, 79, 38, 10, 9, 8, 12, 16, 17, 19, 28, 67, 65, 66, 45, 44, 40, 56, 57, 58, 78, 39, 37, 36, 11, 14, 13, 15, 18, 30, 29, 31, 64, 47, 49, 48, 52, 53, 55, 72, 73, 75, 34, 33, 32, 71, 69, 70, 50, 51, 54, 74, 35, 68)


def to_rgb(color) -> int | list[int | float] | tuple[float | int]:
    """Normalise a color to RGB values between 0 and 1."""
    if isinstance(color, int):
        # Assume color is hexadcimal
        return  [(color >> 16) / 255, ((color >> 8) & 0xFF) / 255, (color & 0xFF) / 255]
    if all(isinstance(c, int) for c in color) and all(0 <= c <= 255 for c in color):
        # Assume only ints means an RGB color with values between 0 and 255
        return [c / 255 for c in color]
    return color


def set_colors(colors: list[list[int]], color: Color, geometry: IcosahedronGeometry):
    colors1 = geometry.attributes.color
    for index, new_color in zip(FACE_MAP, colors):
        color.setRGB(*to_rgb(new_color))
        for j in range(3):
            colors1.setXYZ(index * 3 + j, color.r, color.g, color.b)
    colors1.needsUpdate = True
