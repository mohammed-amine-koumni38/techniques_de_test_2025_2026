"""Fixtures for testing triangulator module."""

from uuid import uuid4

import pytest


class MockPointSetManager:
    """Mock implementation of PointSetManager."""

    def __init__(self):
        """Initialize the mock manager."""
        self.storage = {}

    def register_pointset(self, data: bytes) -> str:
        """Register a new point set."""
        pointset_id = str(uuid4())
        self.storage[pointset_id] = data
        return pointset_id

    def get_pointset(self, pointset_id: str) -> bytes:
        """Retrieve a point set by ID."""
        if pointset_id not in self.storage:
            raise KeyError("PointSet not found")
        return self.storage[pointset_id]


@pytest.fixture
def mock_pointset_manager():
    """Fixture providing a mock PointSetManager."""
    return MockPointSetManager()


@pytest.fixture
def sample_pointset_bytes():
    """Return a binary PointSet with 3 points."""
    import struct

    # Number of points (4 bytes)
    num_points = 3
    header = struct.pack(">I", num_points)
    # Points : (0.0, 0.0), (1.0, 0.0), (0.0, 1.0)
    points = b""
    points += struct.pack(">ff", 0.0, 0.0)
    points += struct.pack(">ff", 1.0, 0.0)
    points += struct.pack(">ff", 0.0, 1.0)
    return header + points


@pytest.fixture
def sample_triangle_bytes():
    """Return a binary Triangles with 1 triangle."""
    import struct

    # Part 1 : vertices (same as PointSet)
    num_vertices = 3
    header = struct.pack(">I", num_vertices)
    vertices = b""
    vertices += struct.pack(">ff", 0.0, 0.0)
    vertices += struct.pack(">ff", 1.0, 0.0)
    vertices += struct.pack(">ff", 0.0, 1.0)
    # Part 2 : triangles
    num_triangles = 1
    tri_header = struct.pack(">I", num_triangles)
    triangles = struct.pack(">III", 0, 1, 2)  # vertex indices
    return header + vertices + tri_header + triangles
