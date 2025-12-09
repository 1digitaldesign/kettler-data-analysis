#!/usr/bin/env python3
"""
Service Layer Pattern
Business logic abstraction for data-intensive applications
"""

from typing import Dict, List, Any, Optional
from .base import BaseService
from .repository import FirmRepository, FileRepository, VectorRepository
from .strategy import (
    FraudAnalysisStrategy, NexusAnalysisStrategy,
    ConnectionAnalysisStrategy, ViolationAnalysisStrategy
)
from .pipeline import AnalysisPipeline
from .models import Firm, Connection, Violation, Evidence
import logging

logger = logging.getLogger(__name__)


class AnalysisService(BaseService):
    """
    Service for analysis operations
    Facade Pattern: Simplified interface to complex subsystem
    """

    def __init__(self, firm_repository: FirmRepository):
        super().__init__(firm_repository)
        self.firm_repo = firm_repository
        self.pipeline = AnalysisPipeline("Main Analysis Pipeline")

        # Register strategies
        self.pipeline.add_strategy(FraudAnalysisStrategy(firm_repository))
        self.pipeline.add_strategy(NexusAnalysisStrategy(firm_repository))
        self.pipeline.add_strategy(ConnectionAnalysisStrategy(firm_repository))
        self.pipeline.add_strategy(ViolationAnalysisStrategy(firm_repository))

    def execute(self, analysis_type: Optional[str] = None) -> Dict[str, Any]:
        """Execute analysis"""
        firms = self.firm_repository.find_all()

        if analysis_type:
            # Execute specific analysis
            if analysis_type == 'fraud':
                strategy = FraudAnalysisStrategy(self.firm_repo)
                return strategy.analyze(firms)
            elif analysis_type == 'nexus':
                strategy = NexusAnalysisStrategy(self.firm_repo)
                return strategy.analyze(firms)
            elif analysis_type == 'connections':
                strategy = ConnectionAnalysisStrategy(self.firm_repo)
                return strategy.analyze(firms)
            elif analysis_type == 'violations':
                strategy = ViolationAnalysisStrategy(self.firm_repo)
                return strategy.analyze(firms)
        else:
            # Execute all analyses
            return self.pipeline.execute_all(firms)

    def analyze_fraud_patterns(self) -> Dict[str, Any]:
        """Analyze fraud patterns"""
        return self.execute('fraud')

    def analyze_nexus_patterns(self) -> Dict[str, Any]:
        """Analyze nexus patterns"""
        return self.execute('nexus')

    def analyze_connections(self) -> Dict[str, Any]:
        """Analyze connections"""
        return self.execute('connections')

    def analyze_violations(self) -> Dict[str, Any]:
        """Analyze violations"""
        return self.execute('violations')


class ValidationService(BaseService):
    """
    Service for validation operations
    Chain of Responsibility Pattern
    """

    def __init__(self, firm_repository: FirmRepository):
        super().__init__(firm_repository)
        self.firm_repo = firm_repository

    def execute(self, validation_type: str, data: Any) -> Dict[str, Any]:
        """Execute validation"""
        if validation_type == 'license':
            return self._validate_license(data)
        elif validation_type == 'address':
            return self._validate_address(data)
        elif validation_type == 'firm':
            return self._validate_firm(data)
        else:
            raise ValueError(f"Unknown validation type: {validation_type}")

    def _validate_license(self, license_number: str) -> Dict[str, Any]:
        """Validate license number"""
        import re

        if not license_number or len(license_number.strip()) == 0:
            return {'valid': False, 'issues': ['License number is empty']}

        # Check format (6-8 digits)
        if not re.match(r'^\d{6,8}$', license_number.strip()):
            return {'valid': False, 'issues': ['Invalid license format']}

        return {'valid': True, 'issues': []}

    def _validate_address(self, address: str) -> Dict[str, Any]:
        """Validate address"""
        if not address or len(address.strip()) < 10:
            return {'valid': False, 'issues': ['Address too short']}

        # Check for required components
        has_street = any(word in address.lower() for word in ['street', 'st', 'avenue', 'ave', 'road', 'rd', 'drive', 'dr'])
        has_city = any(word in address.lower() for word in ['alexandria', 'arlington', 'fairfax', 'mclean', 'vienna'])
        has_state = 'va' in address.lower() or 'virginia' in address.lower()

        issues = []
        if not has_street:
            issues.append('Missing street name')
        if not has_city:
            issues.append('Missing city')
        if not has_state:
            issues.append('Missing state')

        return {'valid': len(issues) == 0, 'issues': issues}

    def _validate_firm(self, firm: Firm) -> Dict[str, Any]:
        """Validate firm data"""
        issues = []

        if not firm.firm_name:
            issues.append('Missing firm name')

        if not firm.address:
            issues.append('Missing address')

        license_result = self._validate_license(firm.license_number) if firm.license_number else {'valid': False, 'issues': ['Missing license']}
        if not license_result['valid']:
            issues.extend(license_result['issues'])

        address_result = self._validate_address(firm.address) if firm.address else {'valid': False, 'issues': ['Missing address']}
        if not address_result['valid']:
            issues.extend(address_result['issues'])

        return {'valid': len(issues) == 0, 'issues': issues, 'firm_id': firm.firm_id}


class ScrapingService(BaseService):
    """
    Service for scraping operations
    Facade Pattern
    """

    def __init__(self, file_repository: FileRepository):
        super().__init__(file_repository)
        self.file_repo = file_repository

    def execute(self, scraper_type: str, targets: List[str], **kwargs) -> Dict[str, Any]:
        """Execute scraping"""
        from scripts.scraping.anti_bot_scraper import AntiBotScraper
        from scripts.scraping.acris_scraper import ACRISScraper

        if scraper_type == 'airbnb':
            scraper = AntiBotScraper()
            from scripts.scraping.anti_bot_scraper import AirbnbScraper
            airbnb_scraper = AirbnbScraper()
            results = []
            for target in targets:
                result = airbnb_scraper.scrape_airbnb(target, max_pages=kwargs.get('max_pages', 3))
                results.extend(result)
            return {'platform': 'airbnb', 'results': results}

        elif scraper_type == 'vrbo':
            scraper = AntiBotScraper()
            from scripts.scraping.anti_bot_scraper import AirbnbScraper
            vrbo_scraper = AirbnbScraper()  # Similar structure
            results = []
            for target in targets:
                # VRBO scraping logic
                results.append({'target': target, 'status': 'framework'})
            return {'platform': 'vrbo', 'results': results}

        elif scraper_type == 'acris':
            acris_scraper = ACRISScraper()
            search_type = kwargs.get('search_type', 'block_lot')

            if search_type == 'block_lot':
                results = acris_scraper.search_by_block_lot(
                    kwargs.get('borough'),
                    kwargs.get('block'),
                    kwargs.get('lot')
                )
            elif search_type == 'address':
                results = acris_scraper.search_by_address(
                    kwargs.get('address'),
                    kwargs.get('borough')
                )
            else:
                results = []

            return {'platform': 'acris', 'results': results}

        else:
            raise ValueError(f"Unknown scraper type: {scraper_type}")
