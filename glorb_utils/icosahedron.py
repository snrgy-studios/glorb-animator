from js import THREE  # type: ignore
from glorb_utils.gtypes import IcosahedronGeometry, Vector3
from glorb_utils.glorb import GLORBBase as GLORB, to_spherical


geometry: 'IcosahedronGeometry' = THREE.IcosahedronGeometry.new(1, 1)
geometry_position = geometry.getAttribute('position')


def get_vertices() -> list['Vector3']:
    return [get_vertex(index) for index in range(geometry_position.count)]


def get_vertex(index: int) -> 'Vector3':
    return list(THREE.Vector3.new().fromBufferAttribute(geometry_position, index))


def get_faces() -> list['Vector3']:
    return [get_face(index) for index in range(0, geometry_position.count, 3)]


def get_face(index: int) -> 'Vector3':
    return [get_vertices()[index + i] for i in range(3)]


def get_centroids() -> list['Vector3']:
    return [get_centroid(index) for index in range(GLORB.NUM_FACES)]


def get_centroids_spherical() -> list['Vector3']:
    return [get_centroid_spherical(index) for index in range(GLORB.NUM_FACES)]


def get_centroid(face_index: list['Vector3']) -> 'Vector3':
    """Calculate the centroid of a face."""
    face = get_face(face_index)
    x_sum = sum(vertex[0] for vertex in face)
    y_sum = sum(vertex[1] for vertex in face)
    z_sum = sum(vertex[2] for vertex in face)
    num_vertices = len(face)
    return x_sum / num_vertices, y_sum / num_vertices, z_sum / num_vertices


def get_centroid_spherical(face_index: list['Vector3']) -> 'Vector3':
    """Calculate the centroid of a face in spherical coordinates."""
    centroid = get_centroid(face_index)
    return list(to_spherical(*centroid))
