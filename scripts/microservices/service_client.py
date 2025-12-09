#!/usr/bin/env python3
"""
Service Client
Helper for inter-service communication in microservices architecture
"""

import os
import requests
from typing import Dict, Optional, Any
from functools import lru_cache

SERVICE_DISCOVERY_URL = os.getenv('SERVICE_DISCOVERY_URL', 'http://service-discovery:8080')

class ServiceClient:
    """Client for inter-service communication"""

    def __init__(self, service_discovery_url: str = SERVICE_DISCOVERY_URL):
        self.service_discovery_url = service_discovery_url
        self._service_cache = {}

    def get_service_url(self, service_name: str) -> Optional[str]:
        """Get service URL from service discovery"""
        # Check cache first
        if service_name in self._service_cache:
            return self._service_cache[service_name]

        try:
            response = requests.get(
                f"{self.service_discovery_url}/api/v1/services/{service_name}/url",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                url = data.get('url')
                self._service_cache[service_name] = url
                return url
        except Exception as e:
            print(f"Warning: Could not discover service {service_name}: {e}")

        # Fallback to environment variable or default
        env_var = f"{service_name.upper().replace('-', '_')}_SERVICE"
        return os.getenv(env_var, f"http://{service_name}:8000")

    def call_service(self, service_name: str, endpoint: str, method: str = 'GET',
                     data: Optional[Dict] = None, **kwargs) -> Optional[Any]:
        """Call a service endpoint"""
        base_url = self.get_service_url(service_name)
        url = f"{base_url}{endpoint}"

        try:
            if method.upper() == 'GET':
                response = requests.get(url, timeout=kwargs.get('timeout', 10), **kwargs)
            elif method.upper() == 'POST':
                response = requests.post(url, json=data, timeout=kwargs.get('timeout', 10), **kwargs)
            elif method.upper() == 'PUT':
                response = requests.put(url, json=data, timeout=kwargs.get('timeout', 10), **kwargs)
            elif method.upper() == 'DELETE':
                response = requests.delete(url, timeout=kwargs.get('timeout', 10), **kwargs)
            else:
                raise ValueError(f"Unsupported method: {method}")

            response.raise_for_status()

            if response.headers.get('content-type', '').startswith('application/json'):
                return response.json()
            return response.text
        except Exception as e:
            print(f"Error calling {service_name}{endpoint}: {e}")
            return None

    def is_service_healthy(self, service_name: str) -> bool:
        """Check if a service is healthy"""
        try:
            response = requests.get(
                f"{self.service_discovery_url}/api/v1/services/{service_name}",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('health', {}).get('status') == 'healthy'
        except:
            pass
        return False

# Global service client instance
_service_client = None

def get_service_client() -> ServiceClient:
    """Get global service client instance"""
    global _service_client
    if _service_client is None:
        _service_client = ServiceClient()
    return _service_client
