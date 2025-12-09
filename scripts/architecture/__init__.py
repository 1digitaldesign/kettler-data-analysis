"""
Architecture Module - Design Patterns for Data-Intensive Applications
"""

from .base import BaseProcessor, BaseAnalyzer, BaseScraper, BaseValidator
from .repository import DataRepository, FileRepository, VectorRepository
from .factory import ProcessorFactory, AnalyzerFactory, ScraperFactory
from .strategy import AnalysisStrategy, FraudAnalysisStrategy, NexusAnalysisStrategy
from .pipeline import DataPipeline, ETLPipeline, AnalysisPipeline
from .models import Firm, Connection, Violation, Evidence, PropertyRecord
from .services import AnalysisService, ValidationService, ScrapingService

__all__ = [
    'BaseProcessor', 'BaseAnalyzer', 'BaseScraper', 'BaseValidator',
    'DataRepository', 'FileRepository', 'VectorRepository',
    'ProcessorFactory', 'AnalyzerFactory', 'ScraperFactory',
    'AnalysisStrategy', 'FraudAnalysisStrategy', 'NexusAnalysisStrategy',
    'DataPipeline', 'ETLPipeline', 'AnalysisPipeline',
    'Firm', 'Connection', 'Violation', 'Evidence', 'PropertyRecord',
    'AnalysisService', 'ValidationService', 'ScrapingService',
]
