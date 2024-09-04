from js import THREE  # type: ignore

from glorb_utils.glorb import GLORBBase, to_spherical
from glorb_utils.gtypes import BufferAttribute, Color, Colors, GeometryData, IcosahedronGeometry, PointValue, Vector3
from glorb_utils.icosahedron import get_centroids, get_centroid_spherical


class GLORBThreeJS(GLORBBase):
    """Glorb class to represent icosahedron of detail 1 in THREE.js."""

    NUM_FACES = GLORBBase.NUM_FACES
    FACEMAP = (63, 22, 6, 3, 24, 60, 61, 62, 23, 21, 20, 7, 5, 4, 0, 1, 2, 26, 25, 27, 46, 43, 41, 42, 59, 76, 77, 79, 38, 10, 9, 8, 12, 16, 17, 19, 28, 67, 65, 66, 45, 44, 40, 56, 57, 58, 78, 39, 37, 36, 11, 14, 13, 15, 18, 30, 29, 31, 64, 47, 49, 48, 52, 53, 55, 72, 73, 75, 34, 33, 32, 71, 69, 70, 50, 51, 54, 74, 35, 68)

    def __init__(self, geometry: 'IcosahedronGeometry', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._colors = self.get_off_colors()  # Start with all LED:s off
        self._update_rate = None
        self._geometry = geometry
        self._geometry_position: 'BufferAttribute' = self._geometry.getAttribute('position')
        self._centroids = get_centroids()
        # _centroids = get_centroids()
        # self._centroids = []
        # for face_index in range(self.NUM_FACES):
        #     self._centroids.append(_centroids[self.FACEMAP[face_index]])
        self._centroids_spherical = [to_spherical(*centroid) for centroid in self._centroids]

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(colors={self._colors[0]}...{self._colors[-1]})'

    @classmethod
    def get_off_colors(self) -> Colors:
        return [[0, 0, 0] for _ in range(self.NUM_FACES)]

    @classmethod
    def get_on_colors(self) -> Colors:
        return [[255, 255, 255] for _ in range(self.NUM_FACES)]

    @classmethod
    def map_colors(cls, colors: Colors) -> Colors:
        result = [*colors]
        for i in range(cls.NUM_FACES):
            result[cls.FACEMAP[i]] = colors[i]
        return result

    @classmethod
    def get_colors_from_color(cls, *rgb: Color) -> Colors:
        return [(*rgb,) for _ in range(cls.NUM_FACES)]

    def turn_off(self):
        self._colors = [[0, 0, 0] for _ in range(self.NUM_FACES)]

    # TODO: Irrelevant for this class?
    def get_default_geometry(self) -> tuple[GeometryData, GeometryData, GeometryData, GeometryData]:
        return [], [], [], []

    @property
    def update_rate(self) -> int | None:
        return self._update_rate

    @update_rate.setter
    def update_rate(self, rate: int) -> int | None:
        self._update_rate = int(rate) if rate >= 10 else None

    @property
    def centroids(self) -> list['Vector3']:
        return self._centroids

    @property
    def centroids_spherical(self) -> list['Vector3']:
        return self._centroids_spherical

    def get_centroid_spherical(self, index: int) -> 'Vector3':
        return self._centroids_spherical[index]

    def get_centroid(self, index: int) -> 'Vector3':
        return self._centroids[index]

    @property
    def geometry(self) -> 'IcosahedronGeometry':
        return self._geometry

    @property
    def colors(self) -> list[list[PointValue]]:
        return self._colors

    @property
    def colors_mapped(self) -> dict[int, list[PointValue]]:
        return self.map_colors(self._colors)

    @colors.setter
    def colors(self, colors) -> list[list[PointValue]]:
        self.set_colors(colors)

    def set_color(self, index: int, color: Color):
        if not self._is_color(color):
            raise ValueError(f"Color must be an RGB color with values either between 0.0-1.0 or 0-255")
        self._colors[index] = color

    def set_colors(self, colors: Colors):
        try:
            if len(colors) == self.NUM_FACES and all(self._is_color(c) for c in colors):
                self._colors = colors
            else:
                raise ValueError
        except Exception as e:
            raise ValueError(f"Colors must be a list of {self.NUM_FACES} RGB colors with values either between 0.0-1.0 as floats or 0-255 as integers") from e

    @staticmethod
    def _is_color(color) -> bool:
        if isinstance(color, (list, tuple)) and len(color) == 3:
            min_value, max_value = min(color), max(color)
            if all(isinstance(c, int) for c in color):
                return min_value >= 0 and max_value <= 255
            elif all(isinstance(c, (float)) for c in color):
                return min_value >= 0.0 and max_value <= 1.0
        return False

    @classmethod
    def is_even_cycle(cls, iteration_count: int) -> bool:
        """Check if the current iteration count is part of an even cycle."""
        return iteration_count // cls.NUM_FACES % 2 == 0

    @classmethod
    def is_odd_cycle(cls, iteration_count: int) -> bool:
        """Check if the current iteration count is part of an odd cycle."""
        return not cls.is_even_cycle(iteration_count)

    @classmethod
    def cycle_iteration(cls, iteration_count: int, cycle_size: int = GLORBBase.NUM_FACES) -> int:
        """Set current iteration count to loop after <cycle_size> iterations."""
        return iteration_count % cycle_size

    @property
    def update_rate(self) -> int | None:
        return self._update_rate

    @update_rate.setter
    def update_rate(self, rate: int | None) -> float:
        """Set update rate in milliseconds, for development/testing."""
        if rate is not None and rate >= 10:
            self._update_rate = rate
        else:
            self._update_rate = None

    @classmethod
    def reverse_index(cls, index: int, condition: bool) -> int:
        """Reverse the current index to go backwards."""
        return cls.NUM_FACES - index - 1 if condition else index
