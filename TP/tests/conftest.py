import pytest
from uuid import UUID, uuid4

# Mock du PointSetManager
class MockPointSetManager:
    def __init__(self):
        self.storage = {}

    def register_pointset(self, data: bytes) -> str:
        pointset_id = str(uuid4())
        self.storage[pointset_id] = data
        return pointset_id

    def get_pointset(self, pointset_id: str) -> bytes:
        if pointset_id not in self.storage:
            raise KeyError("PointSet not found")
        return self.storage[pointset_id]

@pytest.fixture
def mock_pointset_manager():
    return MockPointSetManager()

@pytest.fixture
def sample_pointset_bytes():
    """Retourne un PointSet binaire avec 3 points"""
    import struct
    # Nombre de points (4 bytes)
    num_points = 3
    header = struct.pack('>I', num_points)
    # Points : (0.0, 0.0), (1.0, 0.0), (0.0, 1.0)
    points = b""
    points += struct.pack('>ff', 0.0, 0.0)
    points += struct.pack('>ff', 1.0, 0.0)
    points += struct.pack('>ff', 0.0, 1.0)
    return header + points

@pytest.fixture
def sample_triangle_bytes():
    """Retourne un Triangles binaire avec 1 triangle"""
    import struct
    # Partie 1 : vertices (identique à PointSet)
    num_vertices = 3
    header = struct.pack('>I', num_vertices)
    vertices = b""
    vertices += struct.pack('>ff', 0.0, 0.0)
    vertices += struct.pack('>ff', 1.0, 0.0)
    vertices += struct.pack('>ff', 0.0, 1.0)
    # Partie 2 : triangles
    num_triangles = 1
    tri_header = struct.pack('>I', num_triangles)
    triangles = struct.pack('>III', 0, 1, 2)  # indices des sommets
    return header + vertices + tri_header + triangles
