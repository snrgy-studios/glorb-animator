def to_rgb(color) -> int | list[int | float] | tuple[float | int]:
    """Normalise a color to RGB values between 0 and 1."""
    if isinstance(color, int):
        # Assume color is hexadcimal
        return  [(color >> 16) / 255, ((color >> 8) & 0xFF) / 255, (color & 0xFF) / 255]
    if all(isinstance(c, int) for c in color) and all(0 <= c <= 255 for c in color):
        # Assume only ints means an RGB color with values between 0 and 255
        return [c / 255 for c in color]
    return color
