#!/usr/bin/env python3
"""
Strategy Pattern Implementation
Different analysis strategies
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from .base import BaseAnalyzer
from .models import Firm, Violation, Connection
from .repository import FirmRepository
import logging

logger = logging.getLogger(__name__)


class AnalysisStrategy(ABC):
    """
    Strategy Pattern: Abstract analysis strategy
    """

    @abstractmethod
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Perform analysis"""
        pass

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Get strategy name"""
        pass


class FraudAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for fraud pattern analysis
    """

    def __init__(self, firm_repository: FirmRepository):
        self.firm_repository = firm_repository

    def get_strategy_name(self) -> str:
        return "fraud_patterns"

    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze fraud patterns"""
        firms = self.firm_repository.find_all()

        # Principal broker pattern analysis
        broker_counts = {}
        for firm in firms:
            if firm.principal_broker:
                broker_counts[firm.principal_broker] = broker_counts.get(firm.principal_broker, 0) + 1

        # Find brokers with multiple firms
        suspicious_brokers = {
            broker: count for broker, count in broker_counts.items() if count > 1
        }

        # Address clustering
        address_counts = {}
        for firm in firms:
            normalized_addr = firm.address.lower().strip()
            address_counts[normalized_addr] = address_counts.get(normalized_addr, 0) + 1

        address_clusters = {
            addr: count for addr, count in address_counts.items() if count > 1
        }

        return {
            'principal_broker_pattern': suspicious_brokers,
            'address_clusters': address_clusters,
            'total_firms_analyzed': len(firms),
            'suspicious_patterns_found': len(suspicious_brokers) + len(address_clusters)
        }


class NexusAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for nexus pattern analysis
    """

    def __init__(self, firm_repository: FirmRepository):
        self.firm_repository = firm_repository

    def get_strategy_name(self) -> str:
        return "nexus_patterns"

    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze nexus patterns"""
        firms = self.firm_repository.find_all()

        # Find single principal broker pattern
        broker_firms = {}
        for firm in firms:
            if firm.principal_broker:
                if firm.principal_broker not in broker_firms:
                    broker_firms[firm.principal_broker] = []
                broker_firms[firm.principal_broker].append(firm)

        # Identify largest cluster
        largest_cluster = max(broker_firms.values(), key=len) if broker_firms else []
        largest_broker = max(broker_firms.keys(), key=lambda k: len(broker_firms[k])) if broker_firms else None

        return {
            'single_principal_broker': largest_broker,
            'largest_cluster_size': len(largest_cluster),
            'total_clusters': len(broker_firms),
            'front_person_indicator': len(largest_cluster) > 5 if largest_cluster else False,
            'centralized_control_indicator': len(broker_firms) == 1
        }


class ConnectionAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for connection analysis
    """

    def __init__(self, firm_repository: FirmRepository):
        self.firm_repository = firm_repository

    def get_strategy_name(self) -> str:
        return "connections"

    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze connections"""
        firms = self.firm_repository.find_all()
        connections = []

        # Find connections by principal broker
        broker_groups = {}
        for firm in firms:
            if firm.principal_broker:
                if firm.principal_broker not in broker_groups:
                    broker_groups[firm.principal_broker] = []
                broker_groups[firm.principal_broker].append(firm)

        # Create connections
        from .models import Connection, ConnectionType
        import uuid

        for broker, firm_list in broker_groups.items():
            if len(firm_list) > 1:
                for i, firm1 in enumerate(firm_list):
                    for firm2 in firm_list[i+1:]:
                        conn = Connection(
                            connection_id=str(uuid.uuid4()),
                            source_firm_id=firm1.firm_id,
                            target_firm_id=firm2.firm_id,
                            connection_type=ConnectionType.PRINCIPAL_BROKER,
                            strength=1.0,
                            evidence=[f"Shared principal broker: {broker}"]
                        )
                        connections.append(conn)

        return {
            'total_connections': len(connections),
            'connections': [c.to_dict() for c in connections],
            'connection_types': {
                'principal_broker': len([c for c in connections if c.connection_type == ConnectionType.PRINCIPAL_BROKER])
            }
        }


class ViolationAnalysisStrategy(AnalysisStrategy):
    """
    Strategy for violation analysis
    """

    def __init__(self, firm_repository: FirmRepository):
        self.firm_repository = firm_repository

    def get_strategy_name(self) -> str:
        return "violations"

    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze violations"""
        firms = self.firm_repository.find_all()
        violations = []

        from .models import Violation, ViolationType
        import uuid

        # Check for license violations
        for firm in firms:
            if not firm.license_number or firm.license_number.strip() == '':
                violation = Violation(
                    violation_id=str(uuid.uuid4()),
                    violation_type=ViolationType.LICENSE,
                    entity_id=firm.firm_id,
                    entity_type='firm',
                    description=f"Missing license number for {firm.firm_name}",
                    severity="high",
                    evidence=[f"Firm: {firm.firm_name}", f"Address: {firm.address}"]
                )
                violations.append(violation)

        return {
            'total_violations': len(violations),
            'violations': [v.to_dict() for v in violations],
            'by_type': {
                'license': len([v for v in violations if v.violation_type == ViolationType.LICENSE])
            }
        }
