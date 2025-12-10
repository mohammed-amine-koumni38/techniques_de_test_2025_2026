import pytest
from flask import Flask
from unittest.mock import patch, MagicMock
from triangulator.app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('triangulator.app.get_pointset_from_manager')
def test_get_triangulation_happy_path(mock_get_pointset, client, sample_triangle_bytes):
    # Mock du PointSetManager
    mock_get_pointset.return_value = b"valid_pointset_bytes"  # On ne vérifie pas le contenu ici

    # Mock de la fonction de triangulation
    with patch('triangulator.app.compute_triangulation') as mock_compute:
        mock_compute.return_value = sample_triangle_bytes

        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')

        assert response.status_code == 200
        assert response.content_type == 'application/octet-stream'
        assert response.data == sample_triangle_bytes

@patch('triangulator.app.get_pointset_from_manager')
def test_get_triangulation_not_found(mock_get_pointset, client):
    mock_get_pointset.side_effect = KeyError("PointSet not found")

    response = client.get('/triangulation/invalid-id')

    assert response.status_code == 404
    assert response.json['code'] == 'NOT_FOUND'

@patch('triangulator.app.get_pointset_from_manager')
def test_get_triangulation_internal_error(mock_get_pointset, client):
    mock_get_pointset.return_value = b"valid_pointset_bytes"

    with patch('triangulator.app.compute_triangulation') as mock_compute:
        mock_compute.side_effect = Exception("Something went wrong")

        response = client.get('/triangulation/123e4567-e89b-12d3-a456-426614174000')

        assert response.status_code == 500
        assert response.json['code'] == 'TRIANGULATION_FAILED'