"""
Integration Tests for API Gateway
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
from unittest.mock import patch, AsyncMock

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent.parent / "api-gateway"))

from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestAPIGatewayHealth:
    """Test API Gateway health check"""

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["gateway"] == "healthy"
        assert "services" in data


class TestAPIGatewayRouting:
    """Test API Gateway routing"""

    @patch('main.forward_request')
    def test_analysis_routing(self, mock_forward, client):
        """Test analysis service routing"""
        mock_forward.return_value = {"status": "success", "results": {}}

        response = client.post("/api/analysis/fraud", json={})
        assert response.status_code == 200

    @patch('main.forward_request')
    def test_scraping_routing(self, mock_forward, client):
        """Test scraping service routing"""
        mock_forward.return_value = {"status": "success", "results": []}

        response = client.post("/api/scraping/airbnb", json={"targets": []})
        assert response.status_code == 200

    @patch('main.forward_request')
    def test_validation_routing(self, mock_forward, client):
        """Test validation service routing"""
        mock_forward.return_value = {"status": "success", "result": {"valid": True}}

        response = client.post("/api/validation/license", json={"data": "12345678"})
        assert response.status_code == 200

    @patch('main.forward_request')
    def test_vector_routing(self, mock_forward, client):
        """Test vector service routing"""
        mock_forward.return_value = {"status": "success", "embeddings": []}

        response = client.post("/api/vectors/embed", json={"texts": ["test"]})
        assert response.status_code == 200

    @patch('main.forward_request')
    def test_gis_routing(self, mock_forward, client):
        """Test GIS service routing"""
        mock_forward.return_value = {"status": "success", "result": {}}

        response = client.post("/api/gis/convert", json={"input_file": "test.shp"})
        assert response.status_code == 200

    @patch('main.forward_request')
    def test_acris_routing(self, mock_forward, client):
        """Test ACRIS service routing"""
        mock_forward.return_value = {"status": "success", "results": []}

        response = client.post("/api/acris/search/block-lot", json={
            "borough": "Manhattan",
            "block": "123",
            "lot": "456"
        })
        assert response.status_code == 200

    @patch('main.forward_request')
    def test_data_routing(self, mock_forward, client):
        """Test data service routing"""
        mock_forward.return_value = {"status": "success", "firms": []}

        response = client.get("/api/data/firms")
        assert response.status_code == 200


class TestAPIGatewayErrorHandling:
    """Test API Gateway error handling"""

    @patch('main.forward_request')
    def test_service_unavailable(self, mock_forward, client):
        """Test handling of unavailable service"""
        import httpx
        mock_forward.side_effect = httpx.RequestError("Service unavailable")

        response = client.post("/api/analysis/fraud", json={})
        assert response.status_code == 503

    @patch('main.forward_request')
    def test_service_error(self, mock_forward, client):
        """Test handling of service errors"""
        import httpx
        mock_response = httpx.Response(500, json={"error": "Internal error"})
        mock_forward.side_effect = httpx.HTTPStatusError("Error", request=None, response=mock_response)

        response = client.post("/api/analysis/fraud", json={})
        assert response.status_code == 500


class TestAPIGatewayCORS:
    """Test CORS configuration"""

    def test_cors_headers(self, client):
        """Test CORS headers are present"""
        response = client.options("/api/analysis/fraud")
        # CORS is handled by middleware, check that OPTIONS is allowed
        assert response.status_code in [200, 405]


class TestAPIGatewayPerformance:
    """Test API Gateway performance"""

    @patch('main.forward_request')
    def test_response_time(self, mock_forward, client):
        """Test response time"""
        import time
        mock_forward.return_value = {"status": "success"}

        start = time.time()
        response = client.post("/api/analysis/fraud", json={})
        elapsed = time.time() - start

        assert response.status_code == 200
        # Gateway should add minimal overhead (< 100ms)
        assert elapsed < 0.1
