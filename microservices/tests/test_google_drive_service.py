"""
Tests for Google Drive Service
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent.parent / "google-drive-service"))

from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestGoogleDriveServiceHealth:
    """Test health check endpoint"""

    def test_health_check(self, client):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "google-drive"
        assert "google_drive_available" in data
        assert "drive_client_initialized" in data


class TestGoogleDriveServiceEndpoints:
    """Test Google Drive endpoints"""

    @patch('main.drive_client')
    def test_list_folder(self, mock_drive_client, client):
        """Test list folder endpoint"""
        # Mock drive client
        mock_service = MagicMock()
        mock_files = MagicMock()
        mock_list = MagicMock()
        mock_list.execute.return_value = {
            'files': [
                {'id': '1', 'name': 'test_file.pdf', 'mimeType': 'application/pdf'},
                {'id': '2', 'name': 'test_folder', 'mimeType': 'application/vnd.google-apps.folder'}
            ]
        }
        mock_files.list.return_value = mock_list
        mock_service.files.return_value = mock_files
        mock_drive_client.files = mock_files

        response = client.post("/drive/list", json={
            "folder_id": "1gj6Z0k2N8GO8PCVOrH47RJN3MI8vKff8",
            "include_files": True,
            "include_folders": True,
            "max_results": 100
        })

        assert response.status_code in [200, 503]  # 503 if client not initialized

        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "items" in data

    @patch('main.drive_client')
    def test_download_file(self, mock_drive_client, client):
        """Test download file endpoint"""
        response = client.post("/drive/download", json={
            "file_id": "test_file_id",
            "output_path": "/tmp/test.pdf"
        })

        assert response.status_code in [200, 503]

    @patch('main.drive_client')
    def test_export_file(self, mock_drive_client, client):
        """Test export file endpoint"""
        response = client.post("/drive/export", json={
            "file_id": "test_file_id",
            "format": "pdf",
            "output_path": "/tmp/test.pdf"
        })

        assert response.status_code in [200, 503]

    @patch('main.drive_client')
    def test_get_file_info(self, mock_drive_client, client):
        """Test get file info endpoint"""
        response = client.get("/drive/info/test_file_id")

        assert response.status_code in [200, 503]


class TestGoogleDriveServiceValidation:
    """Test input validation"""

    def test_invalid_folder_id(self, client):
        """Test invalid folder ID"""
        response = client.post("/drive/list", json={
            "folder_id": "",  # Empty folder ID
            "include_files": True,
            "include_folders": True
        })

        assert response.status_code == 422  # Validation error

    def test_invalid_format(self, client):
        """Test invalid export format"""
        response = client.post("/drive/export", json={
            "file_id": "test_file_id",
            "format": "invalid_format"
        })

        assert response.status_code == 422  # Validation error

    def test_invalid_max_results(self, client):
        """Test invalid max results"""
        response = client.post("/drive/list", json={
            "folder_id": "test_folder_id",
            "max_results": 2000  # Too large
        })

        assert response.status_code == 422  # Validation error


class TestGoogleDriveServiceErrorHandling:
    """Test error handling"""

    def test_service_not_initialized(self, client):
        """Test behavior when service not initialized"""
        # This tests the error handling when drive_client is None
        with patch('main.drive_client', None):
            response = client.post("/drive/list", json={
                "folder_id": "test_folder_id"
            })
            assert response.status_code == 503
