#!/usr/bin/env python3
"""
Domain Models for Data-Intensive Applications
Entity Pattern, Value Objects, Data Transfer Objects
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum


class ViolationType(Enum):
    """Violation type enumeration"""
    LICENSE = "license"
    ADDRESS = "address"
    TIMELINE = "timeline"
    CONNECTION = "connection"
    UPL = "upl"  # Unauthorized Practice of Law
    ZONING = "zoning"
    STR = "str"  # Short-Term Rental


class ConnectionType(Enum):
    """Connection type enumeration"""
    PRINCIPAL_BROKER = "principal_broker"
    SAME_ADDRESS = "same_address"
    SHARED_RESOURCES = "shared_resources"
    LICENSE_MATCH = "license_match"
    EMAIL_DOMAIN = "email_domain"


@dataclass
class Firm:
    """Firm entity model"""
    firm_id: str
    firm_name: str
    address: str
    principal_broker: Optional[str] = None
    license_number: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate firm data"""
        if not self.firm_name:
            raise ValueError("Firm name is required")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'firm_id': self.firm_id,
            'firm_name': self.firm_name,
            'address': self.address,
            'principal_broker': self.principal_broker,
            'license_number': self.license_number,
            'state': self.state,
            'phone': self.phone,
            'email': self.email,
            'metadata': self.metadata
        }


@dataclass
class Connection:
    """Connection entity model"""
    connection_id: str
    source_firm_id: str
    target_firm_id: str
    connection_type: ConnectionType
    strength: float = 1.0
    evidence: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'connection_id': self.connection_id,
            'source_firm_id': self.source_firm_id,
            'target_firm_id': self.target_firm_id,
            'connection_type': self.connection_type.value,
            'strength': self.strength,
            'evidence': self.evidence,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }


@dataclass
class Violation:
    """Violation entity model"""
    violation_id: str
    violation_type: ViolationType
    entity_id: str
    entity_type: str  # 'firm', 'individual', 'property'
    description: str
    severity: str = "medium"  # low, medium, high, critical
    evidence: List[str] = field(default_factory=list)
    status: str = "pending"  # pending, verified, resolved
    metadata: Dict[str, Any] = field(default_factory=dict)
    detected_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'violation_id': self.violation_id,
            'violation_type': self.violation_type.value,
            'entity_id': self.entity_id,
            'entity_type': self.entity_type,
            'description': self.description,
            'severity': self.severity,
            'evidence': self.evidence,
            'status': self.status,
            'metadata': self.metadata,
            'detected_at': self.detected_at.isoformat()
        }


@dataclass
class Evidence:
    """Evidence entity model"""
    evidence_id: str
    source_type: str  # 'pdf', 'excel', 'email', 'web', 'acris'
    source_path: str
    content: str
    entities_extracted: Dict[str, List[str]] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
    extracted_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'evidence_id': self.evidence_id,
            'source_type': self.source_type,
            'source_path': self.source_path,
            'content': self.content[:500] + '...' if len(self.content) > 500 else self.content,
            'entities_extracted': self.entities_extracted,
            'metadata': self.metadata,
            'extracted_at': self.extracted_at.isoformat()
        }


@dataclass
class PropertyRecord:
    """Property record entity model (ACRIS, etc.)"""
    record_id: str
    property_address: str
    borough: Optional[str] = None
    block: Optional[str] = None
    lot: Optional[str] = None
    document_id: Optional[str] = None
    grantor: Optional[str] = None
    grantee: Optional[str] = None
    document_type: Optional[str] = None
    recorded_date: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'record_id': self.record_id,
            'property_address': self.property_address,
            'borough': self.borough,
            'block': self.block,
            'lot': self.lot,
            'document_id': self.document_id,
            'grantor': self.grantor,
            'grantee': self.grantee,
            'document_type': self.document_type,
            'recorded_date': self.recorded_date.isoformat() if self.recorded_date else None,
            'metadata': self.metadata
        }


@dataclass
class AnalysisResult:
    """Analysis result DTO"""
    analysis_id: str
    analysis_type: str
    input_data: Dict[str, Any]
    results: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'analysis_id': self.analysis_id,
            'analysis_type': self.analysis_type,
            'input_data': self.input_data,
            'results': self.results,
            'metadata': self.metadata,
            'created_at': self.created_at.isoformat()
        }
