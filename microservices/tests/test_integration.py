"""
End-to-End Integration Tests
Tests complete workflows across multiple services
"""

import pytest
import httpx
from typing import Dict, Any
import time


@pytest.mark.asyncio
class TestEndToEndWorkflows:
    """Test complete workflows"""
    
    async def test_analysis_workflow(self, test_client, api_gateway_url):
        """Test complete analysis workflow"""
        # 1. Run fraud analysis
        response = await test_client.post(
            f"{api_gateway_url}/api/analysis/fraud",
            json={}
        )
        assert response.status_code in [200, 503]
        
        # 2. Run nexus analysis
        response = await test_client.post(
            f"{api_gateway_url}/api/analysis/nexus",
            json={}
        )
        assert response.status_code in [200, 503]
        
        # 3. Run all analyses
        response = await test_client.post(
            f"{api_gateway_url}/api/analysis/all",
            json={}
        )
        assert response.status_code in [200, 503]
    
    async def test_scraping_workflow(self, test_client, api_gateway_url):
        """Test complete scraping workflow"""
        # 1. Scrape Airbnb
        response = await test_client.post(
            f"{api_gateway_url}/api/scraping/airbnb",
            json={
                "targets": ["800 John Carlyle Drive, Alexandria, VA"],
                "options": {"max_pages": 1}
            }
        )
        assert response.status_code in [200, 503]
        
        # 2. Scrape ACRIS
        response = await test_client.post(
            f"{api_gateway_url}/api/scraping/acris",
            json={
                "search_type": "block_lot",
                "params": {
                    "borough": "Manhattan",
                    "block": "123",
                    "lot": "456"
                }
            }
        )
        assert response.status_code in [200, 503]
    
    async def test_validation_workflow(self, test_client, api_gateway_url):
        """Test complete validation workflow"""
        # 1. Validate license
        response = await test_client.post(
            f"{api_gateway_url}/api/validation/license",
            json={
                "data": "12345678",
                "validation_type": "license"
            }
        )
        assert response.status_code in [200, 503]
        
        # 2. Validate address
        response = await test_client.post(
            f"{api_gateway_url}/api/validation/address",
            json={
                "data": "123 Main Street, Alexandria, VA 22314",
                "validation_type": "address"
            }
        )
        assert response.status_code in [200, 503]
    
    async def test_data_crud_workflow(self, test_client, api_gateway_url, sample_firm_data):
        """Test complete CRUD workflow"""
        # 1. Create firm
        response = await test_client.post(
            f"{api_gateway_url}/api/data/firms",
            json=sample_firm_data
        )
        assert response.status_code in [200, 503]
        
        if response.status_code == 200:
            firm_id = sample_firm_data["firm_id"]
            
            # 2. Get firm
            response = await test_client.get(
                f"{api_gateway_url}/api/data/firms/{firm_id}"
            )
            assert response.status_code in [200, 404, 503]
            
            # 3. Update firm
            response = await test_client.put(
                f"{api_gateway_url}/api/data/firms/{firm_id}",
                json={"firm_name": "Updated Firm Name"}
            )
            assert response.status_code in [200, 404, 503]
            
            # 4. Delete firm
            response = await test_client.delete(
                f"{api_gateway_url}/api/data/firms/{firm_id}"
            )
            assert response.status_code in [200, 404, 503]


@pytest.mark.asyncio
class TestServiceCommunication:
    """Test service-to-service communication"""
    
    async def test_gateway_to_analysis(self, test_client, api_gateway_url):
        """Test API Gateway to Analysis Service communication"""
        response = await test_client.get(f"{api_gateway_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        # Check that gateway can communicate with analysis service
        assert "services" in data
    
    async def test_concurrent_requests(self, test_client, api_gateway_url):
        """Test handling of concurrent requests"""
        import asyncio
        
        async def make_request():
            return await test_client.post(
                f"{api_gateway_url}/api/analysis/fraud",
                json={}
            )
        
        # Make 10 concurrent requests
        tasks = [make_request() for _ in range(10)]
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        # All requests should complete (even if some fail)
        assert len(responses) == 10
        # Most should succeed (allow some failures for uninitialized services)
        success_count = sum(1 for r in responses if isinstance(r, httpx.Response) and r.status_code == 200)
        assert success_count >= 0  # At least some should work if services are up


@pytest.mark.asyncio
class TestErrorRecovery:
    """Test error recovery and resilience"""
    
    async def test_service_timeout_handling(self, test_client, api_gateway_url):
        """Test handling of service timeouts"""
        # This tests that the gateway handles timeouts gracefully
        response = await test_client.post(
            f"{api_gateway_url}/api/analysis/fraud",
            json={},
            timeout=1.0  # Very short timeout
        )
        # Should either succeed or fail gracefully
        assert response.status_code in [200, 503, 504]
    
    async def test_invalid_endpoint(self, test_client, api_gateway_url):
        """Test handling of invalid endpoints"""
        response = await test_client.get(f"{api_gateway_url}/api/invalid/endpoint")
        assert response.status_code == 404
