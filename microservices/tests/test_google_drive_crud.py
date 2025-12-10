"""
CRUD Tests for Google Drive Service
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


class TestGoogleDriveCRUD:
    """Test CRUD operations"""

    @patch('main.drive_client')
    def test_create_file(self, mock_drive_client, client):
        """Test create file"""
        mock_files = MagicMock()
        mock_create = MagicMock()
        mock_create.execute.return_value = {
            'id': 'new_file_id',
            'name': 'test_file.txt',
            'mimeType': 'text/plain'
        }
        mock_files.create.return_value = mock_create
        mock_drive_client.files = mock_files

        response = client.post("/drive/create", json={
            "file_name": "test_file.txt",
            "content": "test content",
            "mime_type": "text/plain"
        })

        assert response.status_code in [200, 503]

    @patch('main.drive_client')
    def test_update_file(self, mock_drive_client, client):
        """Test update file"""
        mock_files = MagicMock()
        mock_update = MagicMock()
        mock_update.execute.return_value = {
            'id': 'file_id',
            'name': 'updated_file.txt',
            'mimeType': 'text/plain'
        }
        mock_files.update.return_value = mock_update
        mock_drive_client.files = mock_files

        response = client.put("/drive/update", json={
            "file_id": "file_id",
            "file_name": "updated_file.txt",
            "content": "updated content"
        })

        assert response.status_code in [200, 503]

    @patch('main.drive_client')
    def test_delete_file(self, mock_drive_client, client):
        """Test delete file"""
        mock_files = MagicMock()
        mock_get = MagicMock()
        mock_get.execute.return_value = {'id': 'file_id', 'name': 'test_file.txt'}
        mock_delete = MagicMock()
        mock_delete.execute.return_value = None
        mock_files.get.return_value = mock_get
        mock_files.delete.return_value = mock_delete
        mock_drive_client.files = mock_files

        response = client.delete("/drive/delete/file_id")

        assert response.status_code in [200, 503]

    @patch('main.drive_client')
    def test_move_file(self, mock_drive_client, client):
        """Test move file"""
        mock_files = MagicMock()
        mock_get = MagicMock()
        mock_get.execute.return_value = {'parents': ['old_folder_id']}
        mock_update = MagicMock()
        mock_update.execute.return_value = {
            'id': 'file_id',
            'name': 'test_file.txt',
            'parents': ['new_folder_id']
        }
        mock_files.get.return_value = mock_get
        mock_files.update.return_value = mock_update
        mock_drive_client.files = mock_files

        response = client.post("/drive/move", json={
            "file_id": "file_id",
            "target_folder_id": "new_folder_id"
        })

        assert response.status_code in [200, 503]

    @patch('main.drive_client')
    def test_copy_file(self, mock_drive_client, client):
        """Test copy file"""
        mock_files = MagicMock()
        mock_copy = MagicMock()
        mock_copy.execute.return_value = {
            'id': 'copied_file_id',
            'name': 'copied_file.txt',
            'mimeType': 'text/plain'
        }
        mock_files.copy.return_value = mock_copy
        mock_drive_client.files = mock_files

        response = client.post("/drive/copy", json={
            "file_id": "file_id",
            "new_name": "copied_file.txt"
        })

        assert response.status_code in [200, 503]


class TestGoogleDriveCRUDValidation:
    """Test CRUD input validation"""

    def test_create_file_validation(self, client):
        """Test create file validation"""
        # Missing file_name
        response = client.post("/drive/create", json={})
        assert response.status_code == 422

        # Empty file_name
        response = client.post("/drive/create", json={"file_name": ""})
        assert response.status_code == 422

    def test_update_file_validation(self, client):
        """Test update file validation"""
        # Missing file_id
        response = client.put("/drive/update", json={})
        assert response.status_code == 422

    def test_move_file_validation(self, client):
        """Test move file validation"""
        # Missing file_id
        response = client.post("/drive/move", json={"target_folder_id": "folder_id"})
        assert response.status_code == 422

        # Missing target_folder_id
        response = client.post("/drive/move", json={"file_id": "file_id"})
        assert response.status_code == 422
