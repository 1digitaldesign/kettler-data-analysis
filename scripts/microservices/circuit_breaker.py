#!/usr/bin/env python3
"""
Circuit Breaker Pattern Implementation
Prevents cascading failures by stopping requests to failing services
"""

import time
from enum import Enum
from typing import Callable, Optional, Any
from functools import wraps
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if service recovered

class CircuitBreaker:
    """Circuit breaker implementation"""

    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        expected_exception: tuple = (Exception,)
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.expected_exception = expected_exception

        self.failure_count = 0
        self.last_failure_time: Optional[float] = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time > self.recovery_timeout:
                logger.info("Circuit breaker transitioning to HALF_OPEN")
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN - service unavailable")

        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except self.expected_exception as e:
            self.on_failure()
            raise

    def on_success(self):
        """Handle successful call"""
        if self.state == CircuitState.HALF_OPEN:
            logger.info("Circuit breaker transitioning to CLOSED")
            self.state = CircuitState.CLOSED
            self.failure_count = 0

    def on_failure(self):
        """Handle failed call"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= self.failure_threshold:
            if self.state != CircuitState.OPEN:
                logger.warning(
                    f"Circuit breaker opening after {self.failure_count} failures"
                )
            self.state = CircuitState.OPEN

    def reset(self):
        """Manually reset circuit breaker"""
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
        logger.info("Circuit breaker manually reset")

def circuit_breaker(
    failure_threshold: int = 5,
    recovery_timeout: float = 60.0,
    expected_exception: tuple = (Exception,)
):
    """Decorator for circuit breaker pattern"""
    breaker = CircuitBreaker(failure_threshold, recovery_timeout, expected_exception)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            return breaker.call(func, *args, **kwargs)

        wrapper.circuit_breaker = breaker
        return wrapper

    return decorator
