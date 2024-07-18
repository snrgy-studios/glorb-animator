import pytest
from utils import to_rgb


def test_smoketest():
    assert True


@pytest.mark.parametrize("color, expected", [
    pytest.param([0.0, 0.0, 0.0], [0.0, 0.0, 0.0], id="black"),
    pytest.param([1.0, 1.0, 1.0], [1.0, 1.0, 1.0], id="white"),
    pytest.param([1.0, 0.0, 0.0], [1.0, 0.0, 0.0], id="red"),
    pytest.param([1.0, 0.5019607843137255, 0.0], [1.0, 0.5019607843137255, 0.0], id="orange"),
    pytest.param([0.0, 1.0, 0.5019607843137255], [0.0, 1.0, 0.5019607843137255], id="seafoam"),
    pytest.param([255.0, 50.0, 0.5], [255.0, 50.0, 0.5], id="> 1.0"),
])
def test_can_convert_color_to_rgb_percentages_from_floats(color: list[float], expected: list[float]):
    assert to_rgb(color) == expected


@pytest.mark.parametrize("color, expected", [
    pytest.param([0, 0, 0], [0.0, 0.0, 0.0], id="black"),
    pytest.param([255, 255, 255], [1.0, 1.0, 1.0], id="white"),
    pytest.param([255, 0, 0], [1.0, 0.0, 0.0], id="red"),
    pytest.param([256, 0, 0], [256, 0, 0], id="> 255"),
    pytest.param([1, 1, 1], [1/255, 1/255, 1/255], id="ones"),
])
def test_can_convert_color_to_rgb_percentages_from_ints(color: list[int], expected: list[int | float]):
    assert to_rgb(color) == expected


@pytest.mark.parametrize("color, expected", [
    pytest.param([0, 255.0, 0], [0, 255.0, 0], id="green"),
    pytest.param([0.0, 0, 255], [0.0, 0, 255], id="blue"),
])
def test_can_convert_color_to_rgb_percentages_from_ints_and_floats(color: list[int], expected: list[int | float]):
    assert to_rgb(color) == expected


@pytest.mark.parametrize("color, expected", [
    pytest.param(0xffffff, [1.0, 1.0, 1.0], id="white"),
    pytest.param(0x000000, [0.0, 0.0, 0.0], id="black"),
    pytest.param(0x00cc00, [0.0, 0.8, 0.0], id="green"),
])
def test_can_convert_color_to_rgb_percentages_from_hexadecimal_int(color: int, expected: list[float]):
    assert to_rgb(color) == expected
