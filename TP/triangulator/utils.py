"""Utilities for encoding/decoding PointSet and Triangles data."""

import struct

from .models import PointSet, Triangles


def decode_pointset(data: bytes) -> PointSet:
    """Decode a binary PointSet."""
    if len(data) < 4:
        raise ValueError("Data too short")
    num_points = struct.unpack(">I", data[:4])[0]
    expected_len = 4 + num_points * 8
    if len(data) != expected_len:
        msg = f"Invalid length: expected {expected_len}, got {len(data)}"
        raise ValueError(msg)

    points = []
    for i in range(num_points):
        start = 4 + i * 8
        x, y = struct.unpack(">ff", data[start : start + 8])
        points.append((x, y))
    return PointSet(points)


def encode_pointset(pointset: PointSet) -> bytes:
    """Encode a PointSet to binary."""
    num_points = len(pointset.points)
    header = struct.pack(">I", num_points)
    body = b"".join(
        struct.pack(">ff", x, y) for x, y in pointset.points
    )
    return header + body


def decode_triangles(data: bytes) -> Triangles:
    """Decode a binary Triangles structure."""
    # Part 1: vertices (same as PointSet)
    if len(data) < 4:
        raise ValueError("Data too short")
    num_vertices = struct.unpack(">I", data[:4])[0]
    vertices_size = 4 + num_vertices * 8
    if len(data) < vertices_size + 4:
        raise ValueError("Not enough data for triangles header")

    # Decode vertices
    vertices_data = data[:vertices_size]
    pointset = decode_pointset(vertices_data)
    vertices = pointset.points

    # Part 2: triangles
    triangles_header_start = vertices_size
    num_triangles = struct.unpack(
        ">I", data[triangles_header_start : triangles_header_start + 4]
    )[0]
    triangles_start = triangles_header_start + 4
    expected_triangles_size = num_triangles * 12
    if len(data) != vertices_size + 4 + expected_triangles_size:
        raise ValueError("Invalid triangles data length")

    triangles = []
    for i in range(num_triangles):
        start = triangles_start + i * 12
        idx0, idx1, idx2 = struct.unpack(">III", data[start : start + 12])
        triangles.append((idx0, idx1, idx2))

    return Triangles(vertices, triangles)


def encode_triangles(triangles: Triangles) -> bytes:
    """Encode a Triangles structure to binary."""
    # Part 1: vertices (same as PointSet)
    ps = PointSet(triangles.vertices)
    vertices_bytes = encode_pointset(ps)

    # Part 2: triangles
    num_triangles = len(triangles.triangles)
    header = struct.pack(">I", num_triangles)
    body = b"".join(
        struct.pack(">III", a, b, c) for a, b, c in triangles.triangles
    )

    return vertices_bytes + header + body
