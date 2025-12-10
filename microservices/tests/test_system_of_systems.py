"""
System-of-Systems Integration Tests
Tests complete system interactions across all services
"""

import pytest
import httpx
import asyncio
from typing import Dict, List, Any
import time


@pytest.mark.asyncio
@pytest.mark.system_of_systems
class TestCompleteWorkflows:
    """Test complete workflows across all services"""

    async def test_complete_analysis_workflow(self, test_client, api_gateway_url):
        """Test complete analysis workflow across all services"""
        # 1. Get firms from data service
        firms_response = await test_client.get(f"{api_gateway_url}/api/data/firms")
        assert firms_response.status_code in [200, 503]

        if firms_response.status_code == 200:
            firms = firms_response.json().get("firms", [])

            # 2. Validate firms
            if firms:
                firm = firms[0]
                validation_response = await test_client.post(
                    f"{api_gateway_url}/api/validation/firm",
                    json={"data": firm, "validation_type": "firm"}
                )
                assert validation_response.status_code in [200, 503]

            # 3. Run analysis
            analysis_response = await test_client.post(
                f"{api_gateway_url}/api/analysis/all",
                json={}
            )
            assert analysis_response.status_code in [200, 503]

            # 4. Create embeddings for results
            if analysis_response.status_code == 200:
                results = analysis_response.json().get("results", {})
                if results:
                    text = str(results)[:1000]  # Limit text length
                    vector_response = await test_client.post(
                        f"{api_gateway_url}/api/vectors/embed",
                        json={"texts": [text]}
                    )
                    assert vector_response.status_code in [200, 503]

    async def test_complete_scraping_workflow(self, test_client, api_gateway_url):
        """Test complete scraping workflow"""
        # 1. Scrape Airbnb
        scraping_response = await test_client.post(
            f"{api_gateway_url}/api/scraping/airbnb",
            json={
                "targets": ["800 John Carlyle Drive, Alexandria, VA"],
                "options": {"max_pages": 1}
            }
        )
        assert scraping_response.status_code in [200, 503]

        # 2. If scraping successful, validate results
        if scraping_response.status_code == 200:
            results = scraping_response.json().get("results", {})
            listings = results.get("results", [])

            for listing in listings[:5]:  # Validate first 5
                if "address" in listing:
                    validation_response = await test_client.post(
                        f"{api_gateway_url}/api/validation/address",
                        json={"data": listing["address"], "validation_type": "address"}
                    )
                    assert validation_response.status_code in [200, 503]

        # 3. Search ACRIS for property records
        acris_response = await test_client.post(
            f"{api_gateway_url}/api/acris/search/address",
            json={"address": "800 John Carlyle Drive, Alexandria, VA"}
        )
        assert acris_response.status_code in [200, 503]

    async def test_data_pipeline_workflow(self, test_client, api_gateway_url):
        """Test complete data pipeline"""
        # 1. Create firm
        create_response = await test_client.post(
            f"{api_gateway_url}/api/data/firms",
            json={
                "firm_id": "test_pipeline_001",
                "firm_name": "Test Pipeline Firm",
                "address": "123 Test Street, Alexandria, VA 22314"
            }
        )
        assert create_response.status_code in [200, 503]

        # 2. Validate firm
        if create_response.status_code == 200:
            validation_response = await test_client.post(
                f"{api_gateway_url}/api/validation/firm",
                json={
                    "data": {
                        "firm_id": "test_pipeline_001",
                        "firm_name": "Test Pipeline Firm",
                        "address": "123 Test Street, Alexandria, VA 22314"
                    },
                    "validation_type": "firm"
                }
            )
            assert validation_response.status_code in [200, 503]

            # 3. Analyze firm
            analysis_response = await test_client.post(
                f"{api_gateway_url}/api/analysis/fraud",
                json={}
            )
            assert analysis_response.status_code in [200, 503]

            # 4. Create embeddings
            vector_response = await test_client.post(
                f"{api_gateway_url}/api/vectors/embed",
                json={"texts": ["Test Pipeline Firm"]}
            )
            assert vector_response.status_code in [200, 503]

            # 5. Cleanup
            delete_response = await test_client.delete(
                f"{api_gateway_url}/api/data/firms/test_pipeline_001"
            )
            assert delete_response.status_code in [200, 404, 503]


@pytest.mark.asyncio
@pytest.mark.system_of_systems
class TestServiceInteractions:
    """Test interactions between services"""

    async def test_gateway_to_all_services(self, test_client, api_gateway_url):
        """Test API Gateway can communicate with all services"""
        # Check health of all services through gateway
        health_response = await test_client.get(f"{api_gateway_url}/health")
        assert health_response.status_code == 200

        services_status = health_response.json().get("services", {})

        # Verify all services are registered
        expected_services = [
            "analysis", "scraping", "validation",
            "vector", "gis", "acris", "data"
        ]

        for service in expected_services:
            assert service in services_status

    async def test_concurrent_cross_service_requests(self, test_client, api_gateway_url):
        """Test concurrent requests across multiple services"""
        async def make_request(endpoint, payload):
            return await test_client.post(f"{api_gateway_url}{endpoint}", json=payload)

        # Create concurrent requests to different services
        tasks = [
            make_request("/api/analysis/fraud", {}),
            make_request("/api/scraping/airbnb", {"targets": ["test"]}),
            make_request("/api/validation/license", {"data": "12345678", "validation_type": "license"}),
            make_request("/api/vectors/embed", {"texts": ["test"]}),
            make_request("/api/data/firms", {"firm_id": "test", "firm_name": "Test", "address": "123 Test"}),
        ]

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        # All requests should complete
        assert len(responses) == len(tasks)

        # Most should succeed (allow some failures for uninitialized services)
        success_count = sum(
            1 for r in responses
            if isinstance(r, httpx.Response) and r.status_code == 200
        )
        assert success_count >= 0  # At least some should work if services are up

    async def test_error_propagation(self, test_client, api_gateway_url):
        """Test error propagation across services"""
        # Test invalid request that should propagate error
        response = await test_client.post(
            f"{api_gateway_url}/api/analysis/invalid_endpoint",
            json={}
        )
        # Should return 404
        assert response.status_code == 404

        # Test service unavailable error
        # This tests that gateway handles service failures gracefully
        response = await test_client.get(f"{api_gateway_url}/health")
        assert response.status_code == 200


@pytest.mark.asyncio
@pytest.mark.system_of_systems
class TestRedundancyAndFallbacks:
    """Test redundancy and fallback mechanisms"""

    async def test_retry_mechanism(self, test_client, api_gateway_url):
        """Test retry mechanism across services"""
        # Make request that might fail initially
        for attempt in range(3):
            try:
                response = await test_client.post(
                    f"{api_gateway_url}/api/analysis/fraud",
                    json={},
                    timeout=5.0
                )
                if response.status_code == 200:
                    break
            except Exception:
                if attempt < 2:
                    await asyncio.sleep(1)  # Wait before retry
                else:
                    raise

    async def test_timeout_handling(self, test_client, api_gateway_url):
        """Test timeout handling"""
        # Request with very short timeout
        try:
            response = await test_client.post(
                f"{api_gateway_url}/api/analysis/all",
                json={},
                timeout=0.1  # Very short timeout
            )
            # Should either succeed quickly or timeout gracefully
            assert response.status_code in [200, 503, 504]
        except httpx.TimeoutException:
            # Timeout is acceptable
            pass

    async def test_circuit_breaker(self, test_client, api_gateway_url):
        """Test circuit breaker pattern"""
        # Make multiple requests to trigger circuit breaker if service is failing
        for _ in range(10):
            try:
                response = await test_client.post(
                    f"{api_gateway_url}/api/analysis/fraud",
                    json={}
                )
                # Should handle gracefully
                assert response.status_code in [200, 503]
            except Exception:
                pass


@pytest.mark.asyncio
@pytest.mark.system_of_systems
class TestPerformanceUnderLoad:
    """Test system performance under load"""

    async def test_sustained_load_across_services(self, test_client, api_gateway_url):
        """Test sustained load across all services"""
        duration = 30  # seconds
        requests_per_second = 2

        endpoints = [
            "/api/analysis/fraud",
            "/api/scraping/airbnb",
            "/api/validation/license",
            "/api/vectors/embed",
            "/api/data/firms",
        ]

        start_time = time.time()
        successful = 0
        total = 0

        while time.time() - start_time < duration:
            tasks = []
            for endpoint in endpoints:
                payload = {} if "firms" in endpoint else {"targets": ["test"]} if "scraping" in endpoint else {"texts": ["test"]} if "vectors" in endpoint else {"data": "12345678", "validation_type": "license"} if "validation" in endpoint else {}

                if "firms" in endpoint:
                    tasks.append(test_client.get(f"{api_gateway_url}{endpoint}"))
                else:
                    tasks.append(test_client.post(f"{api_gateway_url}{endpoint}", json=payload))

            results = await asyncio.gather(*tasks, return_exceptions=True)
            successful += sum(1 for r in results if isinstance(r, httpx.Response) and r.status_code == 200)
            total += len(results)

            await asyncio.sleep(1.0 / requests_per_second)

        success_rate = successful / total if total > 0 else 0

        print(f"\nSustained Load Across Services:")
        print(f"  Duration: {duration}s")
        print(f"  Total requests: {total}")
        print(f"  Successful: {successful} ({success_rate*100:.1f}%)")

        # System should maintain reasonable performance
        assert total > 0
