"""Triangulation algorithms for computing triangles from point sets."""

from .models import PointSet, Triangles


def compute_triangulation_simple(pointset: PointSet) -> Triangles:
    """Compute triangulation using a simple fan-based algorithm.

    For 3 points, returns one triangle.
    For 4+ points, uses fan triangulation.
    """
    if len(pointset.points) < 3:
        raise ValueError("Need at least 3 points for triangulation")

    points = pointset.points
    triangles = []

    # Fan triangulation: all triangles share the first point
    for i in range(1, len(points) - 1):
        triangles.append((0, i, i + 1))

    return Triangles(points, triangles)
