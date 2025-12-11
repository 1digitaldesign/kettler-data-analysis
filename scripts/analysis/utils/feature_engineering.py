#!/usr/bin/env python3
"""
Feature engineering utilities for ML analysis
"""

import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict


def extract_temporal_features(entity: Dict[str, Any]) -> Dict[str, float]:
    """Extract temporal features from entity data"""
    features = {}

    # Parse dates
    filing_date_str = entity.get('original_filing_date')
    filing_date = None
    if filing_date_str:
        try:
            filing_date = datetime.fromisoformat(filing_date_str)
        except:
            pass

    # Days since formation
    if filing_date:
        days_since_formation = (datetime.now() - filing_date).days
        features['days_since_formation'] = days_since_formation
        features['years_since_formation'] = days_since_formation / 365.25
    else:
        features['days_since_formation'] = 0.0
        features['years_since_formation'] = 0.0

    # Filing history frequency
    filing_history = entity.get('filing_history', [])
    if filing_history and filing_date:
        filing_dates = []
        for filing in filing_history:
            date_str = filing.get('filing_date') or filing.get('effective_date')
            if date_str:
                try:
                    filing_dates.append(datetime.fromisoformat(date_str))
                except:
                    pass

        if len(filing_dates) > 1:
            filing_dates.sort()
            avg_gap = sum(
                (filing_dates[i+1] - filing_dates[i]).days
                for i in range(len(filing_dates)-1)
            ) / (len(filing_dates) - 1)
            features['avg_filing_gap_days'] = avg_gap
            features['filing_frequency'] = 365.25 / avg_gap if avg_gap > 0 else 0.0
        else:
            features['avg_filing_gap_days'] = 0.0
            features['filing_frequency'] = 0.0
    else:
        features['avg_filing_gap_days'] = 0.0
        features['filing_frequency'] = 0.0

    return features


def extract_structural_features(entity: Dict[str, Any]) -> Dict[str, Any]:
    """Extract structural features"""
    features = {}

    # Entity type encoding
    entity_type = entity.get('entity_type') or ''
    entity_type = str(entity_type).lower()
    features['is_corporation'] = 1.0 if 'corporation' in entity_type else 0.0
    features['is_llc'] = 1.0 if 'llc' in entity_type or 'limited liability' in entity_type else 0.0
    features['is_foreign'] = 1.0 if 'foreign' in entity_type else 0.0

    # Status encoding
    status = entity.get('status') or ''
    status = str(status).lower()
    features['is_forfeited'] = 1.0 if 'forfeited' in status else 0.0
    features['is_in_existence'] = 1.0 if 'existence' in status else 0.0

    # Tax ID presence
    features['has_tax_id'] = 1.0 if entity.get('tax_id') else 0.0
    features['has_fein'] = 1.0 if entity.get('fein') else 0.0

    # Address features
    address = entity.get('address') or ''
    address = str(address).upper()
    features['address_length'] = len(address)
    features['has_suite'] = 1.0 if 'SUITE' in address or 'STE' in address else 0.0

    return features


def extract_network_features(entity: Dict[str, Any],
                           relationship_graph: Dict[str, Any]) -> Dict[str, float]:
    """Extract network features"""
    features = {}

    filing_number = entity.get('filing_number')
    if not filing_number:
        return {'associated_entity_count': 0.0, 'management_change_count': 0.0}

    # Count associated entities
    edges = relationship_graph.get('edges', [])
    associated_count = sum(
        1 for edge in edges
        if edge.get('source') == filing_number or edge.get('target') == filing_number
    )
    features['associated_entity_count'] = float(associated_count)

    # Management changes count
    management = entity.get('management', [])
    features['management_change_count'] = float(len(management))

    return features


def extract_violation_features(entity: Dict[str, Any],
                              violations: Dict[str, List]) -> Dict[str, float]:
    """Extract violation-related features"""
    features = {}

    filing_number = entity.get('filing_number')
    if not filing_number:
        return {
            'violation_count': 0.0,
            'has_tax_forfeiture': 0.0,
            'has_forfeited_status': 0.0,
            'has_reinstatement': 0.0,
            'violation_velocity': 0.0
        }

    # Count violations for this entity
    entity_violations = []
    for violation_type, violation_list in violations.items():
        for violation in violation_list:
            if violation.get('filing_number') == filing_number:
                entity_violations.append(violation)

    features['violation_count'] = float(len(entity_violations))

    # Specific violation types
    features['has_tax_forfeiture'] = 1.0 if any(
        v.get('violation_type') == 'Tax Forfeiture' for v in entity_violations
    ) else 0.0

    features['has_forfeited_status'] = 1.0 if any(
        v.get('violation_type') == 'Forfeited Existence' for v in entity_violations
    ) else 0.0

    features['has_reinstatement'] = 1.0 if any(
        'reinstatement' in str(v).lower() for v in entity_violations
    ) else 0.0

    # Violation velocity (violations per year)
    filing_date_str = entity.get('original_filing_date')
    if filing_date_str and entity_violations:
        try:
            filing_date = datetime.fromisoformat(filing_date_str)
            years_existed = (datetime.now() - filing_date).days / 365.25
            if years_existed > 0:
                features['violation_velocity'] = len(entity_violations) / years_existed
            else:
                features['violation_velocity'] = 0.0
        except:
            features['violation_velocity'] = 0.0
    else:
        features['violation_velocity'] = 0.0

    return features


def create_composite_features(base_features: Dict[str, float]) -> Dict[str, float]:
    """Create composite features"""
    features = base_features.copy()

    # Address clustering score (would need entity list to calculate properly)
    # For now, set to 0
    features['address_clustering_score'] = 0.0

    # Management stability index
    mgmt_changes = features.get('management_change_count', 0.0)
    years_existed = features.get('years_since_formation', 1.0)
    if years_existed > 0:
        features['management_stability_index'] = 1.0 / (1.0 + mgmt_changes / years_existed)
    else:
        features['management_stability_index'] = 1.0

    # Reinstatement risk (time between forfeiture and reinstatement)
    # Would need detailed filing history, set to 0 for now
    features['reinstatement_risk'] = 0.0

    return features


def extract_all_features(entity: Dict[str, Any],
                        relationship_graph: Dict[str, Any],
                        violations: Dict[str, List]) -> Dict[str, float]:
    """Extract all features for an entity"""
    features = {}

    # Temporal features
    features.update(extract_temporal_features(entity))

    # Structural features
    features.update(extract_structural_features(entity))

    # Network features
    features.update(extract_network_features(entity, relationship_graph))

    # Violation features
    features.update(extract_violation_features(entity, violations))

    # Composite features
    features = create_composite_features(features)

    return features
