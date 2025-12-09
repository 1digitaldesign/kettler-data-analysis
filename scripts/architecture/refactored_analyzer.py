#!/usr/bin/env python3
"""
Refactored Analyzer using Design Patterns
Replaces unified_analysis.py with proper architecture
"""

from typing import Dict, List, Any, Optional
from .base import BaseAnalyzer
from .repository import FirmRepository, RepositoryFactory
from .services import AnalysisService
from .models import Firm, AnalysisResult
from .pipeline import AnalysisPipeline
from .strategy import (
    FraudAnalysisStrategy, NexusAnalysisStrategy,
    ConnectionAnalysisStrategy, ViolationAnalysisStrategy
)
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class RefactoredAnalyzer(BaseAnalyzer):
    """
    Refactored Analyzer using Design Patterns
    - Repository Pattern for data access
    - Strategy Pattern for different analyses
    - Service Layer for business logic
    - Pipeline Pattern for workflow
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.firm_repository: Optional[FirmRepository] = None
        self.analysis_service: Optional[AnalysisService] = None
        self._initialize_repositories()
    
    def _initialize_repositories(self) -> None:
        """Initialize repositories"""
        from scripts.utils.paths import DATA_SOURCE_DIR
        
        # Initialize firm repository
        firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"
        if not firms_file.exists():
            firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
        
        if firms_file.exists():
            self.firm_repository = RepositoryFactory.create_firm_repository(str(firms_file))
            self.analysis_service = AnalysisService(self.firm_repository)
        else:
            logger.warning("Firm data file not found")
    
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Perform analysis using service layer"""
        if not self.analysis_service:
            return {'error': 'Analysis service not initialized'}
        
        # Execute all analyses
        results = self.analysis_service.execute()
        
        return results
    
    def analyze_fraud_patterns(self) -> Dict[str, Any]:
        """Analyze fraud patterns"""
        if not self.analysis_service:
            return {'error': 'Analysis service not initialized'}
        return self.analysis_service.analyze_fraud_patterns()
    
    def analyze_nexus_patterns(self) -> Dict[str, Any]:
        """Analyze nexus patterns"""
        if not self.analysis_service:
            return {'error': 'Analysis service not initialized'}
        return self.analysis_service.analyze_nexus_patterns()
    
    def analyze_connections(self) -> Dict[str, Any]:
        """Analyze connections"""
        if not self.analysis_service:
            return {'error': 'Analysis service not initialized'}
        return self.analysis_service.analyze_connections()
    
    def analyze_violations(self) -> Dict[str, Any]:
        """Analyze violations"""
        if not self.analysis_service:
            return {'error': 'Analysis service not initialized'}
        return self.analysis_service.analyze_violations()
    
    def run_all_analyses(self) -> Dict[str, Any]:
        """Run all analyses"""
        if not self.analysis_service:
            return {'error': 'Analysis service not initialized'}
        
        return {
            'fraud_patterns': self.analyze_fraud_patterns(),
            'nexus_patterns': self.analyze_nexus_patterns(),
            'connections': self.analyze_connections(),
            'violations': self.analyze_violations(),
            'metadata': {
                'total_firms': len(self.firm_repository.find_all()) if self.firm_repository else 0,
                'analysis_date': self.metadata['created_at']
            }
        }
    
    def load_data(self, source: Path) -> Any:
        """Load data from source"""
        if self.firm_repository:
            return self.firm_repository.find_all()
        return []
