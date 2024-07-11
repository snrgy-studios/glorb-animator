from icosphere import icosphere


class Glorb:
    """Defining the geometry of a glorb"""

    def __init__(self):
        # Set up 2v icosahedron description
        self.vertices, self.faces = icosphere(nu=2)
        self.no_faces = len(self.faces)

        # Each pixel has 3 neighboring pixels, described by their index in faces
        self.neighbors = [[] for _ in range(self.no_faces)]
        for i in range(self.no_faces):
            for j in range(self.no_faces):
                if j == i:
                    continue

                # Whichever face share two vertices with this one is a neighbor
                vertex_idx_intersection = list(set(self.faces[i]) & set(self.faces[j]))
                if len(vertex_idx_intersection) == 2:
                    self.neighbors[i].append(j)
            assert len(self.neighbors[i]) == 3

        # xyz coordinate of the center of each face
        self.centroids = [[0.0, 0.0, 0.0] for _ in range(self.no_faces)]
        for i in range(self.no_faces):  # every face
            for j in range(3):  # every vertex
                for k in range(3):  # x y z
                    self.centroids[i][k] += self.vertices[self.faces[i][j]][k] / 3.0

    def __repr__(self) -> str:
        return (
            f"vertices: {self.vertices}"
            f"\nfaces: {self.faces}"
            f"\nneighbors: {self.neighbors}"
            f"\ncentroids: {self.centroids}"
        )
