#!/usr/bin/env python3
"""
Base Classes for Data-Intensive Applications
Design Patterns: Template Method, Abstract Base Classes
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BaseProcessor(ABC):
    """
    Abstract base class for all data processors
    Template Method Pattern: Defines skeleton of algorithm
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.results = {}
        self.metadata = {
            'processor_type': self.__class__.__name__,
            'created_at': datetime.now().isoformat(),
            'status': 'initialized'
        }

    @abstractmethod
    def process(self, data: Any) -> Dict[str, Any]:
        """Process data - must be implemented by subclasses"""
        pass

    def validate_input(self, data: Any) -> bool:
        """Validate input data - can be overridden"""
        return data is not None

    def prepare_output(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Prepare output format - can be overridden"""
        return {
            'metadata': self.metadata,
            'results': results,
            'timestamp': datetime.now().isoformat()
        }

    def execute(self, data: Any) -> Dict[str, Any]:
        """
        Template method - defines the algorithm structure
        """
        try:
            self.metadata['status'] = 'processing'

            if not self.validate_input(data):
                raise ValueError("Invalid input data")

            results = self.process(data)
            output = self.prepare_output(results)

            self.metadata['status'] = 'completed'
            self.results = output

            return output

        except Exception as e:
            self.metadata['status'] = 'error'
            self.metadata['error'] = str(e)
            logger.error(f"Error in {self.__class__.__name__}: {e}")
            raise


class BaseAnalyzer(BaseProcessor):
    """
    Base class for analysis operations
    Strategy Pattern: Different analysis strategies
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.data_repository = None

    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Perform analysis - must be implemented"""
        pass

    def process(self, data: Any) -> Dict[str, Any]:
        """Template method implementation"""
        return self.analyze(data)

    def load_data(self, source: Path) -> Any:
        """Load data from source - can be overridden"""
        raise NotImplementedError("Subclass must implement load_data")

    def save_results(self, output_path: Path) -> None:
        """Save analysis results"""
        import json
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)


class BaseScraper(BaseProcessor):
    """
    Base class for web scraping operations
    Template Method Pattern with Strategy
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.anti_bot_enabled = config.get('anti_bot', True)
        self.rate_limiter = None

    @abstractmethod
    def scrape(self, target: str) -> Dict[str, Any]:
        """Perform scraping - must be implemented"""
        pass

    def process(self, data: Any) -> Dict[str, Any]:
        """Template method implementation"""
        return self.scrape(data)

    def setup_anti_bot(self) -> None:
        """Setup anti-bot measures - can be overridden"""
        pass

    def apply_rate_limiting(self) -> None:
        """Apply rate limiting - can be overridden"""
        pass


class BaseValidator(BaseProcessor):
    """
    Base class for data validation
    Chain of Responsibility Pattern
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.validation_rules = []
        self.next_validator = None

    @abstractmethod
    def validate(self, data: Any) -> Dict[str, Any]:
        """Perform validation - must be implemented"""
        pass

    def process(self, data: Any) -> Dict[str, Any]:
        """Template method implementation"""
        return self.validate(data)

    def set_next(self, validator: 'BaseValidator') -> 'BaseValidator':
        """Chain of Responsibility: Set next validator"""
        self.next_validator = validator
        return validator

    def validate_chain(self, data: Any) -> Dict[str, Any]:
        """Execute validation chain"""
        result = self.validate(data)

        if self.next_validator and result.get('valid', True):
            next_result = self.next_validator.validate_chain(data)
            result['chain_results'] = next_result

        return result


class BaseRepository(ABC):
    """
    Repository Pattern: Abstract data access layer
    """

    @abstractmethod
    def find_by_id(self, entity_id: str) -> Optional[Any]:
        """Find entity by ID"""
        pass

    @abstractmethod
    def find_all(self, filters: Optional[Dict[str, Any]] = None) -> List[Any]:
        """Find all entities matching filters"""
        pass

    @abstractmethod
    def save(self, entity: Any) -> Any:
        """Save entity"""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        pass


class BaseService(ABC):
    """
    Service Layer Pattern: Business logic abstraction
    """

    def __init__(self, repository: BaseRepository):
        self.repository = repository
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """Execute service operation"""
        pass
