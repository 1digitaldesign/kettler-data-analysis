#!/usr/bin/env python3
"""
Collect Financial Records (Public)

Script to help collect public financial records and property value data.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
FINANCIAL_DIR = PROJECT_ROOT / 'research/financial'

# States to search
STATES = [
    'District of Columbia',
    'Maryland',
    'Virginia',
    'New Jersey',
    'New York',
    'Connecticut',
]


def create_financial_template():
    """Create template for financial records."""
    FINANCIAL_DIR.mkdir(parents=True, exist_ok=True)
    
    template = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Public financial records documentation',
        },
        'sec_filings': {
            'is_publicly_traded': None,
            'is_reit': None,
            'filings': [],
            'note': 'Check if company is publicly traded or REIT',
        },
        'state_business_filings': {},
        'property_values': {
            'total_properties': 0,
            'total_value': None,
            'properties_by_state': {},
        },
        'revenue_estimates': {
            'estimated_annual_revenue': None,
            'basis': None,
            'calculation_method': None,
        },
        'tax_records': {
            'public_tax_filings': [],
            'note': 'Public tax records if available',
        },
    }
    
    for state in STATES:
        template['state_business_filings'][state] = {
            'annual_reports': [],
            'financial_statements': [],
            'filing_dates': [],
        }
        
        template['property_values']['properties_by_state'][state] = {
            'properties': [],
            'total_value': None,
            'property_count': 0,
        }
    
    filepath = FINANCIAL_DIR / 'public_filings.json'
    filepath.write_text(json.dumps(template, indent=2) + '\n')
    print(f"Created {filepath}")
    return filepath


def print_search_instructions():
    """Print search instructions."""
    print("=== Financial Records Search Instructions ===\n")
    
    print("1. SEC Filings:")
    print("   - Check if Kettler Management is publicly traded")
    print("   - Check if company is a REIT")
    print("   - URL: https://www.sec.gov/edgar/searchedgar/companysearch.html")
    print()
    
    print("2. State Business Filings:")
    for state in STATES:
        print(f"   {state}: Secretary of State annual reports")
    print()
    
    print("3. Property Value Assessments:")
    print("   - County assessor databases")
    print("   - Property tax records")
    print("   - Real estate databases")
    print()
    
    print("4. Revenue Estimates:")
    print("   - Based on property values")
    print("   - Industry benchmarks")
    print("   - Public disclosures")
    print()


if __name__ == '__main__':
    create_financial_template()
    print_search_instructions()
