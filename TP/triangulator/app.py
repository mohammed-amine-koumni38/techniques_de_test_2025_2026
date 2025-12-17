"""Flask application for the Triangulator microservice."""

import os
import re
from io import BytesIO

from flask import Flask, jsonify, send_file

from triangulator.models import PointSet
from triangulator.triangulation import compute_triangulation_simple
from triangulator.utils import decode_pointset, encode_pointset


class ServiceUnavailableError(Exception):
    """Exception raised when PointSetManager is unreachable."""


def get_pointset_from_manager(pointset_id: str) -> bytes:
    """Fetch pointset from the PointSetManager."""
    if os.getenv("TEST_MODE") == "1":
        if "503" in pointset_id:
            raise ServiceUnavailableError("PointSetManager is unreachable")

        if pointset_id == "123e4567-e89b-12d3-a456-426614174000":
            ps = PointSet([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])
            return encode_pointset(ps)
        raise KeyError("PointSet not found")
    raise NotImplementedError("PointSetManager integration not done yet")


def compute_triangulation(pointset_bytes: bytes) -> bytes:
    """Calculate triangulation from encoded pointset bytes."""
    points = decode_pointset(pointset_bytes)
    triangles = compute_triangulation_simple(points)
    from .utils import encode_triangles

    return encode_triangles(triangles)


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    @app.route("/triangulation/<pointset_id>", methods=["GET"])
    def get_triangulation(pointset_id):
        """Get triangulation for a pointset."""
        uuid_pattern = (
            r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-"
            r"[0-9a-f]{4}-[0-9a-f]{12}$"
        )
        if not re.match(uuid_pattern, pointset_id, re.IGNORECASE):
            return jsonify({
                "code": "BAD_REQUEST",
                "message": "Invalid PointSetID format. Expected UUID.",
            }), 400

        try:
            pointset_bytes = get_pointset_from_manager(pointset_id)
            triangles_bytes = compute_triangulation(pointset_bytes)
            return send_file(
                BytesIO(triangles_bytes),
                mimetype="application/octet-stream",
                download_name="triangles.bin",
            )
        except KeyError:
            return jsonify({
                "code": "NOT_FOUND",
                "message": "PointSet not found",
            }), 404
        except ServiceUnavailableError:
            return jsonify({
                "code": "SERVICE_UNAVAILABLE",
                "message": "PointSetManager is unreachable",
            }), 503
        except ValueError as e:
            return jsonify({
                "code": "BAD_REQUEST",
                "message": f"Invalid point set data: {str(e)}",
            }), 400
        except Exception as e:
            return jsonify({
                "code": "TRIANGULATION_FAILED",
                "message": str(e),
            }), 500

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
