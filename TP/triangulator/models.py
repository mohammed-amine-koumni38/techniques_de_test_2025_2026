from typing import List, Tuple

class PointSet:
    def __init__(self, points: List[Tuple[float, float]]):
        self.points = points

class Triangles:
    def __init__(self, vertices: List[Tuple[float, float]], triangles: List[Tuple[int, int, int]]):
        self.vertices = vertices
        self.triangles = triangles