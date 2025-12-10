import pytest
from triangulator.triangulation import compute_triangulation_simple

def test_compute_triangulation_simple_3points():
    from triangulator.models import PointSet
    ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
    triangles = compute_triangulation_simple(ps)
    assert len(triangles.vertices) == 3
    assert len(triangles.triangles) == 1
    assert triangles.triangles[0] == (0, 1, 2)

def test_compute_triangulation_simple_4points():
    from triangulator.models import PointSet
    ps = PointSet([(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)])
    triangles = compute_triangulation_simple(ps)
    assert len(triangles.vertices) == 4
    assert len(triangles.triangles) >= 2  # Au moins 2 triangles pour 4 points

def test_compute_triangulation_simple_empty():
    from triangulator.models import PointSet
    ps = PointSet([])
    with pytest.raises(ValueError):
        compute_triangulation_simple(ps)