import math
from pathlib import Path

from abc import ABC, abstractmethod
from glorb_utils.gtypes import Map


class GLORBBase(ABC):
    """Glorb base class."""

    # Number of faces and LED:s is constant between sub classes
    NUM_FACES = 80
    NUM_LEDS = 120

    FACEMAP: Map

    @abstractmethod
    def __init__(self, obj_file: str = None):
        self.set_default_geometry()

        # Load coordinate data from the OBJ file
        if obj_file is not None and Path(obj_file).exists():
            self.load_obj_file(obj_file)

        self._dmx_data = [0] * self.NUM_LEDS * 3

    def __len__(self) -> int:
        """
        Returns the number of faces/active LED:s as the length of the object.

        Returns:
            int: The number of faces
        """
        return self.NUM_FACES

    @property
    def face_count(self) -> int:
        return self.NUM_FACES

    @property
    def led_count(self) -> int:
        return self.NUM_LEDS

    @property
    def facemap(self) -> Map:
        return self.FACEMAP

    @property
    def faces(self) -> list[list[int]]:
        return self._faces

    @property
    def vertices(self) -> list[list[int]]:
        return self._vertices

    @property
    def centroids(self) -> list[list[float]]:
        """Get the centroids in cartesian coordinates properly remapped."""
        return self._centroids

    @property
    def centroids_spherical(self) -> list[list[float]]:
        """Get the centroids in spherical coordinates properly remapped."""
        return self._centroids_spherical

    @property
    def dmx_data(self) -> list[float]:
        return self._dmx_data

    def load_obj_file(self, filename):
        try:
            with open(filename, 'r') as file:
                for line in file:
                    parts = line.strip().split()
                    if not parts:
                        continue
                    if parts[0] == 'v':
                        vertex = [float(v) for v in parts[1:]]
                        self.vertices.append(vertex)
                    elif parts[0] == 'f':
                        face = [int(f.split('/')[0]) for f in parts[1:]]
                        self.faces.append(face)
            for face in self.faces:
                centroid = [sum(self.vertices[vertex - 1][j] for vertex in face) / 3 for j in range(3)]
                self.centroids.append(centroid)
            for c in self.centroids:
                x, y, z = c
                self.centroids_spherical.append(list(to_spherical(x, y, z)))
        except FileNotFoundError as e:
            raise ValueError(f"Error: File not found - {filename}") from e
        except Exception as e:
            print(f"Error loading OBJ file: {e}")

        return

    # def get_centroid(self, index) -> list[float]:
    #     return self.centroids[index]

    # def get_centroid_spherical(self, index):
    #     return self.centroids_spherical[index]

    # def getVertex(self, index):
    #     return self.vertices[index]

    # def getNumFaces(self):
    #     return self.num_faces

    # def clearColors(self):
    #     self.dmx_data = [0] * self.num_leds * 3

    # def setColor(self, index, color: list[float, float, float]):
    #     i = self.ledmap[index]
    #     for j in range(3):
    #         self.dmx_data[3*i + j] = int(color[j] * 255)

    # def getDmxData(self):
    #     return self.dmx_data

    def get_default_geometry(cls) -> tuple[list[list[int]], list[list[float]], list[list[float]]]:
        """Get default values for faces, vertices and centroids (properly mapped)."""
        raise NotImplementedError

    def set_default_geometry(self):
        (
            self._faces,
            self._vertices,
            self._centroids,
            self._centroids_spherical,
        ) = self.get_default_geometry()

    def _clear_geometry(self):
        """Clear all geometry data excluding DMX data."""
        self._faces = []
        self._vertices = []
        self._centroids = []
        self._centroids_spherical = []

    # def _map_single_geometry_data(self, geometry_data: list[int | float]) -> list[list[int | float]]:
    #     """Remap the indices of the geometry data using facemap."""
    #     return [geometry_data[self.facemap[i]] for i in range(self.face_count)]

    # def _map_geometry_data(self) -> tuple[GeometryData, GeometryData]:
    #     """Map geometry data to faces, vertices and centroids."""
    #     if geometry_data is not None:
    #         return self
    #         self._faces = geometry_data[0]
    #         self._vertices = geometry_data[1]
    #         self._centroids = geometry_data[2]
    #         for c in self._centroids:
    #             x, y, z = c
    #             self._centroids_spherical.append(list(to_spherical(x, y, z)))


def magnitude(x, y, z):
    """Returns the magnitude of the vector."""
    return math.sqrt(x * x + y * y + z * z)

def to_spherical(x, y, z):
    """Converts a cartesian coordinate (x, y, z) into a spherical one (radius, theta, phi)."""
    radius = magnitude(x, y, z)
    theta = math.atan2(math.sqrt(x * x + y * y), z) # (0, PI)
    phi = math.atan2(y, x) # (-PI, PI)
    return [radius, theta, phi]
