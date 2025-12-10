import pytest
from triangulator.models import PointSet, Triangles

def test_pointset_init_empty():
    ps = PointSet([])
    assert len(ps.points) == 0

def test_pointset_init_with_points():
    points = [(0.0, 0.0), (1.0, 1.0)]
    ps = PointSet(points)
    assert len(ps.points) == 2
    assert ps.points[0] == (0.0, 0.0)

def test_triangles_init():
    vertices = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    tris = Triangles(vertices, triangles)
    assert len(tris.vertices) == 3
    assert len(tris.triangles) == 1
    assert tris.triangles[0] == (0, 1, 2)