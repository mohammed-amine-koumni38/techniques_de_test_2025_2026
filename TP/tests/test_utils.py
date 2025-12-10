import pytest
import struct
from triangulator.utils import encode_pointset, decode_pointset, encode_triangles, decode_triangles

def test_encode_decode_pointset(sample_pointset_bytes):
    from triangulator.models import PointSet
    ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
    encoded = encode_pointset(ps)
    decoded = decode_pointset(encoded)
    assert len(decoded.points) == 3
    assert decoded.points[0] == (0.0, 0.0)

def test_encode_decode_triangles(sample_triangle_bytes):
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
    with pytest.raises(ValueError):
        decode_pointset(b"")  # Trop court

def test_decode_triangles_invalid_format():
    with pytest.raises(ValueError):
        decode_triangles(b"")  # Trop court