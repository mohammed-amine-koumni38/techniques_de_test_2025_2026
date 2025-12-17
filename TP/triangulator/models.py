"""Data models for the Triangulator."""



class PointSet:
    """Represents a set of points in 2D space."""

    def __init__(self, points: list[tuple[float, float]]):
        """Initialize PointSet with a list of points."""
        self.points = points


class Triangles:
    """Represents triangles formed from a set of vertices."""

    def __init__(
        self,
        vertices: list[tuple[float, float]],
        triangles: list[tuple[int, int, int]],
    ):
        """Initialize Triangles with vertices and triangle indices."""
        self.vertices = vertices
        self.triangles = triangles
