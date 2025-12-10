#!/usr/bin/env python3
"""
Collect Property Management Contracts

Script to help identify and document property management contracts.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
CONTRACTS_DIR = PROJECT_ROOT / 'research/contracts'

# Operational states
STATES = [
    'District of Columbia',
    'Maryland',
    'Virginia',
    'New Jersey',
    'New York',
    'Connecticut',
]


def create_property_list_template():
    """Create template for property lists by state."""
    CONTRACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    template = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Property management contract documentation',
        },
        'properties_by_state': {},
        'service_scope': {
            'property_management': [],
            'leasing': [],
            'maintenance': [],
            'financial_management': [],
            'other': [],
        },
        'contract_terms': {
            'licensing_requirements': None,
            'geographic_scope': None,
            'compliance_language': None,
        },
    }
    
    for state in STATES:
        template['properties_by_state'][state] = {
            'properties': [],
            'total_properties': 0,
            'property_addresses': [],
        }
    
    filepath = CONTRACTS_DIR / 'property_management_contracts.json'
    filepath.write_text(json.dumps(template, indent=2) + '\n')
    print(f"Created {filepath}")
    return filepath


def create_search_instructions():
    """Print instructions for finding property contracts."""
    print("=== Property Management Contract Search Instructions ===\n")
    
    print("Sources to search:")
    print("  1. Company website - Property listings")
    print("  2. Public property records - County assessor databases")
    print("  3. Property management directories")
    print("  4. Real estate databases")
    print("  5. Public filings - If REIT or publicly traded")
    print()
    
    print("Information to collect:")
    print("  - Property addresses by state")
    print("  - Property types (residential, commercial, mixed-use)")
    print("  - Total units/bedrooms")
    print("  - Property values (if available)")
    print("  - Management start dates")
    print()
    
    print("Contract information (if publicly available):")
    print("  - Service scope")
    print("  - Geographic limitations")
    print("  - Licensing requirements mentioned")
    print("  - Compliance language")
    print()


if __name__ == '__main__':
    create_property_list_template()
    create_search_instructions()
