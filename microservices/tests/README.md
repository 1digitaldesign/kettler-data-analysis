# Microservices Test Suite

**Production-Grade Testing for Microservices Architecture**

## Overview

Comprehensive test suite covering:
- Unit tests for individual services
- Integration tests for service communication
- End-to-end workflow tests
- Load and stress tests
- Health check tests

## Test Structure

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures and configuration
├── test_analysis_service.py # Analysis service unit tests
├── test_api_gateway.py      # API Gateway integration tests
├── test_integration.py      # End-to-end integration tests
├── test_load.py             # Load and stress tests
├── test_all_services.py     # Comprehensive service tests
├── pytest.ini               # Pytest configuration
├── requirements.txt         # Test dependencies
└── run_tests.sh             # Test runner script
```

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install -r tests/requirements.txt

# Start services (for integration tests)
cd microservices
docker-compose up -d
```

### Run All Tests

```bash
cd microservices
./tests/run_tests.sh all
```

### Run Specific Test Types

```bash
# Unit tests only
./tests/run_tests.sh unit

# Integration tests
./tests/run_tests.sh integration

# Load tests
./tests/run_tests.sh load

# All services health checks
./tests/run_tests.sh all-services

# With coverage report
./tests/run_tests.sh coverage
```

### Using Pytest Directly

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_analysis_service.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific markers
pytest tests/ -m "unit" -v
pytest tests/ -m "integration" -v
pytest tests/ -m "load" -v
```

## Test Types

### Unit Tests

Test individual service components in isolation:
- Service initialization
- Endpoint handlers
- Error handling
- Response formatting

**Files:** `test_analysis_service.py`, `test_api_gateway.py`

### Integration Tests

Test service-to-service communication:
- API Gateway routing
- Service communication
- End-to-end workflows
- Error propagation

**Files:** `test_integration.py`, `test_api_gateway.py`

### Load Tests

Test performance under load:
- Concurrent requests
- Sustained load
- High concurrency
- Large payloads

**Files:** `test_load.py`

**Note:** Load tests are marked as `@pytest.mark.slow` and may take longer to run.

### Health Check Tests

Test all service health endpoints:
- Service availability
- Health check responses
- Service status

**Files:** `test_all_services.py`

## Test Coverage

Target coverage: **70% minimum**

Generate coverage report:
```bash
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

## CI/CD Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Daily schedule (2 AM UTC)

See `.github/workflows/tests.yml` for CI/CD configuration.

## Test Fixtures

Common fixtures available in `conftest.py`:
- `test_client` - Async HTTP client
- `sync_client` - Sync HTTP client
- `*_service_url` - Service URLs
- `sample_firm_data` - Sample test data
- `sample_analysis_request` - Sample requests

## Writing New Tests

### Example Unit Test

```python
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
```

### Example Integration Test

```python
@pytest.mark.asyncio
async def test_service_communication(test_client, api_gateway_url):
    response = await test_client.get(f"{api_gateway_url}/health")
    assert response.status_code == 200
```

### Example Load Test

```python
@pytest.mark.asyncio
@pytest.mark.slow
async def test_concurrent_requests(test_client, api_gateway_url):
    tasks = [make_request() for _ in range(50)]
    results = await asyncio.gather(*tasks)
    assert len(results) == 50
```

## Best Practices

1. **Isolation**: Each test should be independent
2. **Cleanup**: Clean up test data after tests
3. **Mocking**: Mock external dependencies
4. **Assertions**: Use descriptive assertions
5. **Performance**: Mark slow tests with `@pytest.mark.slow`
6. **Coverage**: Aim for high coverage but focus on critical paths

## Troubleshooting

### Services Not Running

If tests fail with connection errors:
```bash
# Start services
docker-compose up -d

# Check service health
curl http://localhost:8000/health
```

### Timeout Errors

Increase timeout in `conftest.py`:
```python
TEST_TIMEOUT = 60.0  # Increase from 30.0
```

### Coverage Issues

Ensure all services are tested:
```bash
pytest tests/ --cov=. --cov-report=term-missing
```

## Continuous Improvement

- Add tests for new features
- Increase coverage over time
- Optimize slow tests
- Add performance benchmarks
- Monitor test execution time
