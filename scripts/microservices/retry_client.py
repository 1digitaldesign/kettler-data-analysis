#!/usr/bin/env python3
"""
Retry Client - Provides retry logic for inter-service communication
"""

import time
import requests
from typing import Callable, Optional, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def retry_on_failure(
    max_retries: int = 3,
    backoff_factor: float = 1.0,
    retry_on_status: Optional[list] = None,
    retry_on_exception: Optional[tuple] = None
):
    """
    Decorator for retrying failed requests

    Args:
        max_retries: Maximum number of retry attempts
        backoff_factor: Multiplier for exponential backoff
        retry_on_status: HTTP status codes to retry on
        retry_on_exception: Exception types to retry on
    """
    if retry_on_status is None:
        retry_on_status = [500, 502, 503, 504]
    if retry_on_exception is None:
        retry_on_exception = (requests.exceptions.RequestException,)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries + 1):
                try:
                    response = func(*args, **kwargs)

                    # Check if response is a requests.Response
                    if hasattr(response, 'status_code'):
                        if response.status_code in retry_on_status:
                            if attempt < max_retries:
                                wait_time = backoff_factor * (2 ** attempt)
                                logger.warning(
                                    f"Request failed with status {response.status_code}, "
                                    f"retrying in {wait_time}s (attempt {attempt + 1}/{max_retries + 1})"
                                )
                                time.sleep(wait_time)
                                continue
                        return response
                    else:
                        return response

                except retry_on_exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        wait_time = backoff_factor * (2 ** attempt)
                        logger.warning(
                            f"Request failed with exception {type(e).__name__}: {e}, "
                            f"retrying in {wait_time}s (attempt {attempt + 1}/{max_retries + 1})"
                        )
                        time.sleep(wait_time)
                    else:
                        logger.error(f"Request failed after {max_retries + 1} attempts: {e}")
                        raise

            if last_exception:
                raise last_exception

            return None

        return wrapper
    return decorator

class RetryClient:
    """HTTP client with built-in retry logic"""

    def __init__(
        self,
        max_retries: int = 3,
        backoff_factor: float = 1.0,
        timeout: int = 30
    ):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout
        self.session = requests.Session()

    @retry_on_failure(max_retries=3, backoff_factor=1.0)
    def get(self, url: str, **kwargs) -> requests.Response:
        """GET request with retry"""
        kwargs.setdefault('timeout', self.timeout)
        return self.session.get(url, **kwargs)

    @retry_on_failure(max_retries=3, backoff_factor=1.0)
    def post(self, url: str, **kwargs) -> requests.Response:
        """POST request with retry"""
        kwargs.setdefault('timeout', self.timeout)
        return self.session.post(url, **kwargs)

    @retry_on_failure(max_retries=3, backoff_factor=1.0)
    def put(self, url: str, **kwargs) -> requests.Response:
        """PUT request with retry"""
        kwargs.setdefault('timeout', self.timeout)
        return self.session.put(url, **kwargs)

    @retry_on_failure(max_retries=3, backoff_factor=1.0)
    def delete(self, url: str, **kwargs) -> requests.Response:
        """DELETE request with retry"""
        kwargs.setdefault('timeout', self.timeout)
        return self.session.delete(url, **kwargs)
