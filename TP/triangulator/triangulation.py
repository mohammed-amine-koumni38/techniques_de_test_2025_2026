from .models import PointSet, Triangles

def compute_triangulation_simple(pointset: PointSet) -> Triangles:
    """
    Algorithme simple de triangulation.
    Pour 3 points, retourne un triangle.
    Pour 4 points ou plus, utilise une triangulation par fan.
    """
    if len(pointset.points) < 3:
        raise ValueError("Need at least 3 points for triangulation")
    
    points = pointset.points
    triangles = []
    
    # Triangulation par fan : tous les triangles partagent le premier point
    for i in range(1, len(points) - 1):
        triangles.append((0, i, i + 1))
    
    return Triangles(points, triangles)