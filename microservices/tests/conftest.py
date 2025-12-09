"""
Pytest configuration and fixtures for microservices tests
"""

import pytest
import sys
from pathlib import Path
from typing import Generator
import httpx
from fastapi.testclient import TestClient

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

# Test configuration
TEST_TIMEOUT = 30.0
TEST_BASE_URL = "http://localhost"


@pytest.fixture(scope="session")
def test_client() -> Generator[httpx.AsyncClient, None, None]:
    """Create async HTTP client for testing"""
    client = httpx.AsyncClient(timeout=TEST_TIMEOUT)
    yield client
    client.aclose()


@pytest.fixture(scope="session")
def sync_client() -> httpx.Client:
    """Create sync HTTP client for testing"""
    return httpx.Client(timeout=TEST_TIMEOUT)


@pytest.fixture
def api_gateway_url() -> str:
    """API Gateway URL"""
    return f"{TEST_BASE_URL}:8000"


@pytest.fixture
def analysis_service_url() -> str:
    """Analysis Service URL"""
    return f"{TEST_BASE_URL}:8001"


@pytest.fixture
def scraping_service_url() -> str:
    """Scraping Service URL"""
    return f"{TEST_BASE_URL}:8002"


@pytest.fixture
def validation_service_url() -> str:
    """Validation Service URL"""
    return f"{TEST_BASE_URL}:8003"


@pytest.fixture
def vector_service_url() -> str:
    """Vector Service URL"""
    return f"{TEST_BASE_URL}:8004"


@pytest.fixture
def gis_service_url() -> str:
    """GIS Service URL"""
    return f"{TEST_BASE_URL}:8005"


@pytest.fixture
def acris_service_url() -> str:
    """ACRIS Service URL"""
    return f"{TEST_BASE_URL}:8006"


@pytest.fixture
def data_service_url() -> str:
    """Data Repository Service URL"""
    return f"{TEST_BASE_URL}:8007"


@pytest.fixture
def google_drive_service_url() -> str:
    """Google Drive Service URL"""
    return f"{TEST_BASE_URL}:8008"


@pytest.fixture
def sample_firm_data() -> dict:
    """Sample firm data for testing"""
    return {
        "firm_id": "test_firm_001",
        "firm_name": "Test Property Management LLC",
        "address": "123 Test Street, Alexandria, VA 22314",
        "principal_broker": "Test Broker",
        "license_number": "12345678",
        "state": "VA",
        "phone": "703-555-1234",
        "email": "test@example.com"
    }


@pytest.fixture
def sample_analysis_request() -> dict:
    """Sample analysis request"""
    return {
        "filters": {},
        "options": {}
    }


@pytest.fixture
def sample_scraping_request() -> dict:
    """Sample scraping request"""
    return {
        "targets": ["800 John Carlyle Drive, Alexandria, VA"],
        "options": {
            "max_pages": 1
        }
    }


@pytest.fixture
def sample_acris_request() -> dict:
    """Sample ACRIS request"""
    return {
        "search_type": "block_lot",
        "params": {
            "borough": "Manhattan",
            "block": "123",
            "lot": "456"
        }
    }
