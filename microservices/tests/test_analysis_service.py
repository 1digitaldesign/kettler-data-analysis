"""
Unit and Integration Tests for Analysis Service
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(Path(__file__).parent.parent / "analysis-service"))

from main import app


@pytest.fixture
def client():
    """Create test client"""
    return TestClient(app)


class TestAnalysisServiceHealth:
    """Test health check endpoint"""
    
    def test_health_check(self, client):
        """Test health check returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "analysis"


class TestAnalysisServiceEndpoints:
    """Test analysis endpoints"""
    
    def test_analyze_fraud(self, client):
        """Test fraud analysis endpoint"""
        response = client.post("/analyze/fraud", json={})
        assert response.status_code in [200, 503]  # 503 if service not initialized
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "results" in data
    
    def test_analyze_nexus(self, client):
        """Test nexus analysis endpoint"""
        response = client.post("/analyze/nexus", json={})
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "results" in data
    
    def test_analyze_connections(self, client):
        """Test connection analysis endpoint"""
        response = client.post("/analyze/connections", json={})
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "results" in data
    
    def test_analyze_violations(self, client):
        """Test violation analysis endpoint"""
        response = client.post("/analyze/violations", json={})
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "results" in data
    
    def test_analyze_all(self, client):
        """Test analyze all endpoint"""
        response = client.post("/analyze/all", json={})
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            data = response.json()
            assert "status" in data
            assert "results" in data


class TestAnalysisServiceErrorHandling:
    """Test error handling"""
    
    def test_invalid_request_body(self, client):
        """Test invalid request body"""
        response = client.post("/analyze/fraud", json={"invalid": "data"})
        # Should still process (filters/options are optional)
        assert response.status_code in [200, 503]
    
    def test_missing_service_initialization(self, client):
        """Test behavior when service not initialized"""
        # This tests the error handling when repository is not available
        response = client.post("/analyze/fraud", json={})
        # Should return 503 if not initialized, 200 if initialized
        assert response.status_code in [200, 503]


class TestAnalysisServicePerformance:
    """Test performance characteristics"""
    
    def test_response_time(self, client):
        """Test response time is acceptable"""
        import time
        start = time.time()
        response = client.post("/analyze/fraud", json={})
        elapsed = time.time() - start
        
        assert response.status_code in [200, 503]
        # Should respond within 5 seconds
        assert elapsed < 5.0
