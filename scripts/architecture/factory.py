#!/usr/bin/env python3
"""
Factory Pattern Implementation
Creates processors, analyzers, and scrapers
"""

from typing import Dict, Any, Optional, Type
from .base import BaseProcessor, BaseAnalyzer, BaseScraper, BaseValidator
from .repository import FirmRepository, FileRepository, VectorRepository
import logging

logger = logging.getLogger(__name__)


class ProcessorFactory:
    """
    Factory Pattern: Creates processor instances
    """
    
    _registry: Dict[str, Type[BaseProcessor]] = {}
    
    @classmethod
    def register(cls, processor_type: str, processor_class: Type[BaseProcessor]):
        """Register a processor type"""
        cls._registry[processor_type] = processor_class
    
    @classmethod
    def create(cls, processor_type: str, config: Optional[Dict[str, Any]] = None) -> BaseProcessor:
        """Create processor instance"""
        if processor_type not in cls._registry:
            raise ValueError(f"Unknown processor type: {processor_type}")
        
        processor_class = cls._registry[processor_type]
        return processor_class(config or {})
    
    @classmethod
    def get_available_types(cls) -> List[str]:
        """Get list of available processor types"""
        return list(cls._registry.keys())


class AnalyzerFactory(ProcessorFactory):
    """
    Factory for creating analyzers
    """
    
    @classmethod
    def create_analyzer(cls, analyzer_type: str, config: Optional[Dict[str, Any]] = None) -> BaseAnalyzer:
        """Create analyzer instance"""
        processor = cls.create(analyzer_type, config)
        if not isinstance(processor, BaseAnalyzer):
            raise ValueError(f"{analyzer_type} is not an analyzer")
        return processor


class ScraperFactory(ProcessorFactory):
    """
    Factory for creating scrapers
    """
    
    @classmethod
    def create_scraper(cls, scraper_type: str, config: Optional[Dict[str, Any]] = None) -> BaseScraper:
        """Create scraper instance"""
        processor = cls.create(scraper_type, config)
        if not isinstance(processor, BaseScraper):
            raise ValueError(f"{scraper_type} is not a scraper")
        return processor


class RepositoryFactory:
    """
    Factory for creating repositories
    """
    
    @staticmethod
    def create_firm_repository(data_source: str) -> FirmRepository:
        """Create firm repository"""
        from pathlib import Path
        return FirmRepository(Path(data_source))
    
    @staticmethod
    def create_file_repository(base_path: str) -> FileRepository:
        """Create file repository"""
        from pathlib import Path
        return FileRepository(Path(base_path))
    
    @staticmethod
    def create_vector_repository(vector_store_path: str) -> VectorRepository:
        """Create vector repository"""
        from pathlib import Path
        return VectorRepository(Path(vector_store_path))
