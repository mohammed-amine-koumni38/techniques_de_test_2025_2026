import struct
from triangulator.models import PointSet, Triangles  # ← Ajoute cette ligne

def encode_pointset(pointset) -> bytes:
    raise NotImplementedError("encode_pointset not implemented")

def decode_pointset(data: bytes) -> PointSet:  # ← Enlève les quotes
    raise NotImplementedError("decode_pointset not implemented")

def encode_triangles(triangles) -> bytes:
    raise NotImplementedError("encode_triangles not implemented")

def decode_triangles(data: bytes) -> Triangles:  # ← Enlève les quotes
    raise NotImplementedError("decode_triangles not implemented")