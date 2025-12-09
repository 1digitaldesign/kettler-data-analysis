"""
Redundancy and Fallback Mechanisms
6 fallback mechanisms for each failure point
"""

import asyncio
import logging
from typing import List, Callable, Any, Optional, Dict
from functools import wraps
import time
import random
from enum import Enum

logger = logging.getLogger(__name__)


class FallbackStrategy(Enum):
    """Fallback strategy types"""
    RETRY = "retry"
    CIRCUIT_BREAKER = "circuit_breaker"
    TIMEOUT = "timeout"
    CACHE = "cache"
    ALTERNATIVE_SERVICE = "alternative_service"
    GRACEFUL_DEGRADATION = "graceful_degradation"


class CircuitBreaker:
    """Circuit breaker pattern implementation"""

    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half_open

    def call(self, func: Callable, *args, **kwargs):
        """Execute function with circuit breaker"""
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half_open"
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            if self.state == "half_open":
                self.state = "closed"
                self.failure_count = 0
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "open"

            raise e


class RetryHandler:
    """Retry mechanism with exponential backoff"""

    def __init__(self, max_retries: int = 3, base_delay: float = 1.0, max_delay: float = 60.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay

    async def execute(self, func: Callable, *args, **kwargs):
        """Execute function with retry logic"""
        last_exception = None

        for attempt in range(self.max_retries + 1):
            try:
                if asyncio.iscoroutinefunction(func):
                    return await func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                if attempt < self.max_retries:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    # Add jitter
                    delay += random.uniform(0, delay * 0.1)
                    await asyncio.sleep(delay)
                    logger.warning(f"Retry attempt {attempt + 1}/{self.max_retries} after {delay:.2f}s")

        raise last_exception


class TimeoutHandler:
    """Timeout mechanism"""

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout

    async def execute(self, func: Callable, *args, **kwargs):
        """Execute function with timeout"""
        try:
            if asyncio.iscoroutinefunction(func):
                return await asyncio.wait_for(func(*args, **kwargs), timeout=self.timeout)
            else:
                # For sync functions, run in executor
                loop = asyncio.get_event_loop()
                return await asyncio.wait_for(
                    loop.run_in_executor(None, lambda: func(*args, **kwargs)),
                    timeout=self.timeout
                )
        except asyncio.TimeoutError:
            raise Exception(f"Operation timed out after {self.timeout}s")


class CacheHandler:
    """Cache fallback mechanism"""

    def __init__(self, ttl: int = 300):
        self.cache: Dict[str, tuple] = {}
        self.ttl = ttl

    def get(self, key: str) -> Optional[Any]:
        """Get from cache"""
        if key in self.cache:
            value, timestamp = self.cache[key]
            if time.time() - timestamp < self.ttl:
                return value
            else:
                del self.cache[key]
        return None

    def set(self, key: str, value: Any):
        """Set cache value"""
        self.cache[key] = (value, time.time())


class AlternativeServiceHandler:
    """Alternative service fallback"""

    def __init__(self, alternatives: List[Callable]):
        self.alternatives = alternatives

    async def execute(self, *args, **kwargs):
        """Try alternatives in order"""
        last_exception = None

        for alt_func in self.alternatives:
            try:
                if asyncio.iscoroutinefunction(alt_func):
                    return await alt_func(*args, **kwargs)
                else:
                    return alt_func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                logger.warning(f"Alternative service failed: {e}")
                continue

        raise last_exception or Exception("All alternative services failed")


class GracefulDegradationHandler:
    """Graceful degradation fallback"""

    def __init__(self, fallback_func: Callable):
        self.fallback_func = fallback_func

    async def execute(self, primary_func: Callable, *args, **kwargs):
        """Execute primary, fallback to degraded mode"""
        try:
            if asyncio.iscoroutinefunction(primary_func):
                return await primary_func(*args, **kwargs)
            else:
                return primary_func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Primary function failed, using graceful degradation: {e}")
            if asyncio.iscoroutinefunction(self.fallback_func):
                return await self.fallback_func(*args, **kwargs)
            else:
                return self.fallback_func(*args, **kwargs)


class RedundancyManager:
    """
    Manages 6 fallback mechanisms for each failure point:
    1. Retry with exponential backoff
    2. Circuit breaker
    3. Timeout handling
    4. Cache fallback
    5. Alternative service
    6. Graceful degradation
    """

    def __init__(self):
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.retry_handler = RetryHandler(max_retries=3)
        self.timeout_handler = TimeoutHandler(timeout=30.0)
        self.cache_handler = CacheHandler(ttl=300)
        self.alternative_handlers: Dict[str, AlternativeServiceHandler] = {}
        self.degradation_handlers: Dict[str, GracefulDegradationHandler] = {}

    def get_circuit_breaker(self, key: str) -> CircuitBreaker:
        """Get or create circuit breaker"""
        if key not in self.circuit_breakers:
            self.circuit_breakers[key] = CircuitBreaker()
        return self.circuit_breakers[key]

    async def execute_with_fallbacks(
        self,
        func: Callable,
        func_key: str,
        cache_key: Optional[str] = None,
        alternatives: Optional[List[Callable]] = None,
        fallback_func: Optional[Callable] = None,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute function with all 6 fallback mechanisms
        """
        # Fallback 1: Check cache
        if cache_key:
            cached = self.cache_handler.get(cache_key)
            if cached is not None:
                logger.info(f"Cache hit for {cache_key}")
                return cached

        # Fallback 2: Circuit breaker
        circuit_breaker = self.get_circuit_breaker(func_key)

        # Fallback 3: Timeout + Retry wrapper
        async def execute_with_timeout_and_retry():
            return await self.retry_handler.execute(
                lambda: self.timeout_handler.execute(func, *args, **kwargs)
            )

        # Fallback 4: Alternative services
        if alternatives:
            alternative_handler = AlternativeServiceHandler([execute_with_timeout_and_retry] + alternatives)
            execute_func = lambda: alternative_handler.execute(*args, **kwargs)
        else:
            execute_func = execute_with_timeout_and_retry

        # Fallback 5: Graceful degradation
        if fallback_func:
            degradation_handler = GracefulDegradationHandler(fallback_func)
            execute_func = lambda: degradation_handler.execute(execute_func, *args, **kwargs)

        # Execute with circuit breaker
        try:
            result = await circuit_breaker.call(execute_func)

            # Cache result
            if cache_key:
                self.cache_handler.set(cache_key, result)

            return result

        except Exception as e:
            logger.error(f"All fallback mechanisms exhausted for {func_key}: {e}")
            raise


# Global redundancy manager
redundancy_manager = RedundancyManager()


def with_redundancy(
    func_key: str,
    cache_key: Optional[str] = None,
    alternatives: Optional[List[Callable]] = None,
    fallback_func: Optional[Callable] = None
):
    """Decorator for adding redundancy to functions"""
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await redundancy_manager.execute_with_fallbacks(
                func,
                func_key,
                cache_key,
                alternatives,
                fallback_func,
                *args,
                **kwargs
            )
        return wrapper
    return decorator
