from __init__ import GlorbBaseClass, to_spherical
from gtypes import BufferAttribute, Color, Colors, GeometryData, IcosahedronGeometry, PointValue, Vector3
from js import THREE  # type: ignore


class GlorbThreeJs(GlorbBaseClass):
    """Glorb class to represent icosahedron of detail 1 in THREE.js."""

    NUM_FACES = GlorbBaseClass.NUM_FACES
    FACEMAP = (63, 22, 6, 3, 24, 60, 61, 62, 23, 21, 20, 7, 5, 4, 0, 1, 2, 26, 25, 27, 46, 43, 41, 42, 59, 76, 77, 79, 38, 10, 9, 8, 12, 16, 17, 19, 28, 67, 65, 66, 45, 44, 40, 56, 57, 58, 78, 39, 37, 36, 11, 14, 13, 15, 18, 30, 29, 31, 64, 47, 49, 48, 52, 53, 55, 72, 73, 75, 34, 33, 32, 71, 69, 70, 50, 51, 54, 74, 35, 68)

    def __init__(self, geometry: 'IcosahedronGeometry', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._colors = self.off_colors  # Start with all LED:s off
        self._update_rate = None
        self._geometry = geometry
        self._geometry_position: 'BufferAttribute' = self._geometry.getAttribute('position')

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(colors={self._colors[0]}...{self._colors[-1]})'

    @classmethod
    def off_colors(self) -> Colors:
        return [[0, 0, 0] for _ in range(self.NUM_FACES)]

    @classmethod
    def on_colors(self) -> Colors:
        return [[255, 255, 255] for _ in range(self.NUM_FACES)]

    def turn_off(self):
        self._colors = [[0, 0, 0] for _ in range(self.NUM_FACES)]

    # TODO: Irrelevant for this class?
    def get_default_geometry(self) -> tuple[GeometryData, GeometryData, GeometryData, GeometryData]:
        return [], [], [], []

    @property
    def colors(self) -> list[list[PointValue]]:
        result = [*self._colors]
        return result
        for i in range(self.NUM_FACES):
            result[self.FACEMAP[i]] = self._colors[i]
        return result

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
    def cycle_iteration(cls, iteration_count: int, cycle_size: int = GlorbBaseClass.NUM_FACES) -> int:
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

    def get_vertices(self) -> list['Vector3']:
        return [self.get_vertex(index) for index in range(self._geometry_position.count)]

    def get_vertex(self, index: int) -> 'Vector3':
        return list(THREE.Vector3.new().fromBufferAttribute(self._geometry_position, index))

    def get_faces(self) -> list['Vector3']:
        return [self.get_face(index) for index in range(0, self._geometry_position.count, 3)]

    def get_face(self, index: int) -> 'Vector3':
        return [self.get_vertices()[index + i] for i in range(3)]

    def get_centroids(self) -> list['Vector3']:
        return [self.get_centroid(index) for index in range(self.NUM_FACES)]

    def get_centroid(self, face_index: list['Vector3']) -> 'Vector3':
        """Calculate the centroid of a face."""
        face = self.get_face(face_index)
        x_sum = sum(vertex[0] for vertex in face)
        y_sum = sum(vertex[1] for vertex in face)
        z_sum = sum(vertex[2] for vertex in face)
        num_vertices = len(face)
        return x_sum / num_vertices, y_sum / num_vertices, z_sum / num_vertices

    def get_centroid_sperical(self, face_index: list['Vector3']) -> 'Vector3':
        """Calculate the centroid of a face in spherical coordinates."""
        centroid = self.get_centroid(face_index)
        return list(to_spherical(*centroid))
