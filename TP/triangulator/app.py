from flask import Flask, send_file, jsonify
from io import BytesIO
import os
from triangulator.triangulation import compute_triangulation_simple
from triangulator.utils import decode_pointset


def get_pointset_from_manager(pointset_id):
    """Récupère un PointSet depuis le PointSetManager"""
    # Implémentation simplifiée - à adapter selon les besoins
    raise NotImplementedError("À implémenter selon votre architecture")


def compute_triangulation(pointset_bytes):
    """Wrapper pour calculer la triangulation"""
    points = decode_pointset(pointset_bytes)
    return compute_triangulation_simple(points)


def create_app():
    """Crée et configure l'application Flask"""
    app = Flask(__name__)
    
    @app.route('/triangulation/<pointset_id>', methods=['GET'])
    def get_triangulation(pointset_id):
        try:
            # Récupère le PointSet
            pointset_bytes = get_pointset_from_manager(pointset_id)
            
            # Calcule la triangulation
            triangles_bytes = compute_triangulation(pointset_bytes)
            
            # Retourne le résultat
            return send_file(
                BytesIO(triangles_bytes),
                mimetype='application/octet-stream',
                download_name='triangles.bin'
            )
        except KeyError:
            return jsonify({'code': 'NOT_FOUND', 'message': 'PointSet not found'}), 404
        except Exception as e:
            return jsonify({'code': 'TRIANGULATION_FAILED', 'message': str(e)}), 500
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
