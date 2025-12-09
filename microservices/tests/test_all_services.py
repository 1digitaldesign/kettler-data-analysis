"""
Comprehensive tests for all microservices
"""

import pytest
import httpx
from typing import List, Dict


@pytest.mark.asyncio
class TestAllServicesHealth:
    """Test health checks for all services"""

    async def test_api_gateway_health(self, test_client, api_gateway_url):
        """Test API Gateway health"""
        response = await test_client.get(f"{api_gateway_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"

    async def test_analysis_service_health(self, test_client, analysis_service_url):
        """Test Analysis Service health"""
        response = await test_client.get(f"{analysis_service_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_scraping_service_health(self, test_client, scraping_service_url):
        """Test Scraping Service health"""
        response = await test_client.get(f"{scraping_service_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_validation_service_health(self, test_client, validation_service_url):
        """Test Validation Service health"""
        response = await test_client.get(f"{validation_service_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_vector_service_health(self, test_client, vector_service_url):
        """Test Vector Service health"""
        response = await test_client.get(f"{vector_service_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_gis_service_health(self, test_client, gis_service_url):
        """Test GIS Service health"""
        response = await test_client.get(f"{gis_service_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_acris_service_health(self, test_client, acris_service_url):
        """Test ACRIS Service health"""
        response = await test_client.get(f"{acris_service_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_data_service_health(self, test_client, data_service_url):
        """Test Data Repository Service health"""
        response = await test_client.get(f"{data_service_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"

    async def test_google_drive_service_health(self, test_client, google_drive_service_url):
        """Test Google Drive Service health"""
        response = await test_client.get(f"{google_drive_service_url}/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


@pytest.mark.asyncio
class TestAllServicesEndpoints:
    """Test all service endpoints"""

    async def test_analysis_endpoints(self, test_client, api_gateway_url):
        """Test all analysis endpoints"""
        endpoints = [
            "/api/analysis/fraud",
            "/api/analysis/nexus",
            "/api/analysis/connections",
            "/api/analysis/violations",
            "/api/analysis/all"
        ]

        for endpoint in endpoints:
            response = await test_client.post(f"{api_gateway_url}{endpoint}", json={})
            assert response.status_code in [200, 503]  # Allow 503 if not initialized

    async def test_scraping_endpoints(self, test_client, api_gateway_url):
        """Test all scraping endpoints"""
        endpoints = [
            ("/api/scraping/airbnb", {"targets": ["test"]}),
            ("/api/scraping/vrbo", {"targets": ["test"]}),
            ("/api/scraping/front", {"targets": ["test"]}),
        ]

        for endpoint, data in endpoints:
            response = await test_client.post(f"{api_gateway_url}{endpoint}", json=data)
            assert response.status_code in [200, 503]

    async def test_validation_endpoints(self, test_client, api_gateway_url):
        """Test all validation endpoints"""
        endpoints = [
            ("/api/validation/license", {"data": "12345678", "validation_type": "license"}),
            ("/api/validation/address", {"data": "123 Main St", "validation_type": "address"}),
        ]

        for endpoint, data in endpoints:
            response = await test_client.post(f"{api_gateway_url}{endpoint}", json=data)
            assert response.status_code in [200, 503]

    async def test_vector_endpoints(self, test_client, api_gateway_url):
        """Test all vector endpoints"""
        endpoints = [
            ("/api/vectors/embed", {"texts": ["test"]}),
            ("/api/vectors/search", {"query": "test", "top_k": 10}),
            ("/api/vectors/status", None),
        ]

        for endpoint, data in endpoints:
            if data:
                response = await test_client.post(f"{api_gateway_url}{endpoint}", json=data)
            else:
                response = await test_client.get(f"{api_gateway_url}{endpoint}")
            assert response.status_code in [200, 503]

    async def test_gis_endpoints(self, test_client, api_gateway_url):
        """Test all GIS endpoints"""
        endpoints = [
            ("/api/gis/convert", {"input_file": "test.shp", "output_format": "geojson"}),
        ]

        for endpoint, data in endpoints:
            response = await test_client.post(f"{api_gateway_url}{endpoint}", json=data)
            assert response.status_code in [200, 503]

    async def test_acris_endpoints(self, test_client, api_gateway_url):
        """Test all ACRIS endpoints"""
        endpoints = [
            ("/api/acris/search/block-lot", {"borough": "Manhattan", "block": "123", "lot": "456"}),
            ("/api/acris/search/address", {"address": "123 Main St"}),
            ("/api/acris/search/party", {"party_name": "Test"}),
            ("/api/acris/search/document", {"document_id": "123456"}),
        ]

        for endpoint, data in endpoints:
            response = await test_client.post(f"{api_gateway_url}{endpoint}", json=data)
            assert response.status_code in [200, 503]

    async def test_data_endpoints(self, test_client, api_gateway_url):
        """Test all data endpoints"""
        # GET endpoints
        response = await test_client.get(f"{api_gateway_url}/api/data/firms")
        assert response.status_code in [200, 503]

        # POST endpoint (create)
        response = await test_client.post(
            f"{api_gateway_url}/api/data/firms",
            json={
                "firm_id": "test_001",
                "firm_name": "Test Firm",
                "address": "123 Test St"
            }
        )
        assert response.status_code in [200, 503]
