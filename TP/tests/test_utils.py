"""Unit tests for encoding/decoding utilities."""

import pytest

from triangulator.utils import (
    decode_pointset,
    decode_triangles,
    encode_pointset,
    encode_triangles,
)


def test_encode_decode_pointset(sample_pointset_bytes):
    """Encode and decode a PointSet roundtrip."""
    from triangulator.models import PointSet

    ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)
    assert len(decoded.points) == 3
    assert decoded.points[0] == (0.0, 0.0)


def test_encode_decode_triangles(sample_triangle_bytes):
    """Encode and decode Triangles roundtrip."""
    from triangulator.models import Triangles

    vertices = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    triangles = [(0, 1, 2)]
    tris = Triangles(vertices, triangles)
    encoded = encode_triangles(tris)
    decoded = decode_triangles(encoded)
    assert len(decoded.vertices) == 3
    assert len(decoded.triangles) == 1
    assert decoded.triangles[0] == (0, 1, 2)


def test_decode_pointset_invalid_format():
    """Invalid pointset bytes raise ValueError."""
    with pytest.raises(ValueError):
        decode_pointset(b"")


def test_decode_triangles_invalid_format():
    """Invalid triangles bytes raise ValueError."""
    with pytest.raises(ValueError):
        decode_triangles(b"")
