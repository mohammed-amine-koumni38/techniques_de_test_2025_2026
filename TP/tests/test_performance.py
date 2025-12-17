"""Performance tests for triangulation algorithm."""

import time

import pytest

from triangulator.models import PointSet
from triangulator.triangulation import compute_triangulation_simple


@pytest.mark.performance
def test_triangulation_100_points():
    """Test triangulation performance with 100 points."""
    points = [(i, i % 10) for i in range(100)]
    ps = PointSet(points)

    start = time.perf_counter()
    triangles = compute_triangulation_simple(ps)
    duration = time.perf_counter() - start

    assert len(triangles.triangles) == 98
    assert duration < 0.1


@pytest.mark.performance
def test_triangulation_1000_points():
    """Test triangulation performance with 1000 points."""
    points = [(i, i % 100) for i in range(1000)]
    ps = PointSet(points)

    start = time.perf_counter()
    triangles = compute_triangulation_simple(ps)
    duration = time.perf_counter() - start

    assert len(triangles.triangles) == 998
    assert duration < 2.0
