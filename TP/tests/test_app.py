"""Tests for the Flask application."""

import os
from unittest.mock import patch

import pytest

from triangulator.app import ServiceUnavailableError, create_app


@pytest.fixture
def client():
    """Provide a Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_triangulation_happy_path_integration(client):
    """Test successful triangulation integration."""
    os.environ["TEST_MODE"] = "1"
    response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")
    assert response.status_code == 200
    assert response.content_type == "application/octet-stream"
    assert len(response.data) == 44


def test_get_triangulation_not_found(client):
    """Test triangulation with non-existent UUID."""
    os.environ["TEST_MODE"] = "1"
    response = client.get("/triangulation/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json["code"] == "NOT_FOUND"


@patch("triangulator.app.get_pointset_from_manager")
def test_get_triangulation_internal_error(mock_get_pointset, client):
    """Test triangulation with internal error."""
    mock_get_pointset.return_value = (
        b"\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x3f\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        b"\x3f\x80\x00\x00"
    )
    with patch(
        "triangulator.app.compute_triangulation",
        side_effect=Exception("Triangulation failed"),
    ):
        response = client.get(
            "/triangulation/123e4567-e89b-12d3-a456-426614174000"
        )
        assert response.status_code == 500
        assert response.json["code"] == "TRIANGULATION_FAILED"


def test_get_triangulation_invalid_uuid_format_returns_400(client):
    """Test invalid UUID format returns 400."""
    response = client.get("/triangulation/invalid-id")
    assert response.status_code == 400
    assert response.json["code"] == "BAD_REQUEST"
    msg = response.json["message"].lower()
    assert "format" in msg or "uuid" in msg


def test_get_triangulation_valid_uuid_but_not_found_returns_404(client):
    """Test valid UUID but non-existent returns 404."""
    os.environ["TEST_MODE"] = "1"
    response = client.get("/triangulation/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404
    assert response.json["code"] == "NOT_FOUND"


def test_get_triangulation_pointsetmanager_down_returns_503(client):
    """Test PointSetManager unavailable returns 503."""
    with patch(
        "triangulator.app.get_pointset_from_manager",
        side_effect=ServiceUnavailableError("unreachable"),
    ):
        response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == 503


def test_get_triangulation_corrupted_pointset_returns_400(client):
    """Test corrupted pointset data returns 400."""
    with patch(
        "triangulator.app.get_pointset_from_manager", return_value=b"corrupted"
    ):
        response = client.get("/triangulation/123e4567-e89b-12d3-a456-426614174000")
        assert response.status_code == 400
