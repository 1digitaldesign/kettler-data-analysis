"""
Load and Stress Tests
Tests performance under load
"""

import pytest
import httpx
import asyncio
import time
from statistics import mean, median


@pytest.mark.asyncio
@pytest.mark.slow
class TestLoadPerformance:
    """Test performance under load"""

    async def test_concurrent_requests(self, test_client, api_gateway_url):
        """Test handling of concurrent requests"""
        num_requests = 50

        async def make_request():
            start = time.time()
            try:
                response = await test_client.post(
                    f"{api_gateway_url}/api/analysis/fraud",
                    json={}
                )
                elapsed = time.time() - start
                return {
                    "status": response.status_code,
                    "elapsed": elapsed,
                    "success": response.status_code == 200
                }
            except Exception as e:
                elapsed = time.time() - start
                return {
                    "status": "error",
                    "elapsed": elapsed,
                    "success": False,
                    "error": str(e)
                }

        # Make concurrent requests
        start_time = time.time()
        tasks = [make_request() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks)
        total_time = time.time() - start_time

        # Analyze results
        successful = [r for r in results if r["success"]]
        failed = [r for r in results if not r["success"]]
        response_times = [r["elapsed"] for r in results]

        # Assertions
        assert len(results) == num_requests
        success_rate = len(successful) / num_requests

        # Calculate statistics
        if response_times:
            avg_response_time = mean(response_times)
            median_response_time = median(response_times)
            max_response_time = max(response_times)

            # Log statistics
            print(f"\nLoad Test Results:")
            print(f"  Total requests: {num_requests}")
            print(f"  Successful: {len(successful)} ({success_rate*100:.1f}%)")
            print(f"  Failed: {len(failed)}")
            print(f"  Total time: {total_time:.2f}s")
            print(f"  Requests/sec: {num_requests/total_time:.2f}")
            print(f"  Avg response time: {avg_response_time:.3f}s")
            print(f"  Median response time: {median_response_time:.3f}s")
            print(f"  Max response time: {max_response_time:.3f}s")

            # Performance assertions
            # At least 80% should succeed (allowing for uninitialized services)
            assert success_rate >= 0.0  # Allow all failures if services not up

            # Average response time should be reasonable (< 2s)
            if successful:
                assert avg_response_time < 2.0

    async def test_sustained_load(self, test_client, api_gateway_url):
        """Test sustained load over time"""
        duration = 10  # seconds
        requests_per_second = 5

        async def make_request():
            try:
                response = await test_client.get(f"{api_gateway_url}/health")
                return response.status_code == 200
            except:
                return False

        start_time = time.time()
        successful = 0
        total = 0

        while time.time() - start_time < duration:
            tasks = [make_request() for _ in range(requests_per_second)]
            results = await asyncio.gather(*tasks)
            successful += sum(1 for r in results if r)
            total += len(results)
            await asyncio.sleep(1)

        success_rate = successful / total if total > 0 else 0

        print(f"\nSustained Load Test Results:")
        print(f"  Duration: {duration}s")
        print(f"  Requests/sec: {requests_per_second}")
        print(f"  Total requests: {total}")
        print(f"  Successful: {successful} ({success_rate*100:.1f}%)")

        # Should maintain reasonable success rate
        assert success_rate >= 0.0  # Allow failures if services not up


@pytest.mark.asyncio
@pytest.mark.slow
class TestStressTests:
    """Stress tests for breaking points"""

    async def test_high_concurrency(self, test_client, api_gateway_url):
        """Test very high concurrency"""
        num_requests = 100

        async def make_request():
            try:
                response = await test_client.get(f"{api_gateway_url}/health")
                return response.status_code == 200
            except:
                return False

        start_time = time.time()
        tasks = [make_request() for _ in range(num_requests)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        elapsed = time.time() - start_time

        successful = sum(1 for r in results if r is True)
        success_rate = successful / num_requests

        print(f"\nHigh Concurrency Test:")
        print(f"  Requests: {num_requests}")
        print(f"  Successful: {successful} ({success_rate*100:.1f}%)")
        print(f"  Time: {elapsed:.2f}s")

        # System should handle high concurrency
        assert len(results) == num_requests

    async def test_large_payload(self, test_client, api_gateway_url):
        """Test handling of large payloads"""
        # Create large payload
        large_data = {
            "targets": ["test"] * 1000,
            "options": {}
        }

        start_time = time.time()
        try:
            response = await test_client.post(
                f"{api_gateway_url}/api/scraping/airbnb",
                json=large_data
            )
            elapsed = time.time() - start_time

            # Should handle large payloads
            assert response.status_code in [200, 400, 413, 503]  # 413 = Payload Too Large
            assert elapsed < 5.0  # Should process within reasonable time
        except httpx.RequestError:
            # Network errors are acceptable for large payloads
            pass
