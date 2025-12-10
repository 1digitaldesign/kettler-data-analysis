#!/usr/bin/env python3
"""
Collect Fair Housing and Discrimination Records

Script to help search HUD, EEOC, and state discrimination databases.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
DISCRIMINATION_DIR = PROJECT_ROOT / 'research/discrimination'

# Federal agency URLs
FEDERAL_URLS = {
    'HUD': {
        'name': 'U.S. Department of Housing and Urban Development',
        'complaints': 'https://www.hud.gov/program_offices/fair_housing_equal_opp',
        'database': 'https://www.hud.gov/program_offices/fair_housing_equal_opp/online-complaint',
    },
    'EEOC': {
        'name': 'Equal Employment Opportunity Commission',
        'complaints': 'https://www.eeoc.gov/',
        'database': 'https://www.eeoc.gov/data/',
    },
}

# State discrimination agencies
STATE_AGENCIES = {
    'District of Columbia': 'DC Office of Human Rights',
    'Maryland': 'Maryland Commission on Civil Rights',
    'Virginia': 'Virginia Division of Human Rights',
    'New Jersey': 'New Jersey Division on Civil Rights',
    'New York': 'New York State Division of Human Rights',
    'Connecticut': 'Connecticut Commission on Human Rights and Opportunities',
}


def create_discrimination_template():
    """Create template for discrimination records."""
    DISCRIMINATION_DIR.mkdir(parents=True, exist_ok=True)
    
    template = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Fair Housing and discrimination records',
        },
        'hud_complaints': [],
        'eeoc_records': [],
        'state_complaints': {},
        'settlements': [],
        'court_cases': [],
    }
    
    for state, agency in STATE_AGENCIES.items():
        template['state_complaints'][state] = {
            'agency': agency,
            'complaints': [],
            'settlements': [],
        }
    
    # HUD template
    hud_file = DISCRIMINATION_DIR / 'hud_complaints.json'
    hud_data = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'agency': FEDERAL_URLS['HUD']['name'],
            'url': FEDERAL_URLS['HUD']['database'],
        },
        'complaints': [],
        'search_terms': [
            'Kettler Management',
            'Kettler Management Inc.',
            '800 Carlyle',
            'Sinclaire on Seminary',
        ],
    }
    hud_file.write_text(json.dumps(hud_data, indent=2) + '\n')
    print(f"Created {hud_file}")
    
    # EEOC template
    eeoc_file = DISCRIMINATION_DIR / 'eeoc_records.json'
    eeoc_data = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'agency': FEDERAL_URLS['EEOC']['name'],
            'url': FEDERAL_URLS['EEOC']['database'],
        },
        'records': [],
        'search_terms': [
            'Kettler Management',
            'Kettler Management Inc.',
        ],
    }
    eeoc_file.write_text(json.dumps(eeoc_data, indent=2) + '\n')
    print(f"Created {eeoc_file}")
    
    # Main template
    main_file = DISCRIMINATION_DIR / 'discrimination_records.json'
    main_file.write_text(json.dumps(template, indent=2) + '\n')
    print(f"Created {main_file}")
    
    return main_file


def print_search_instructions():
    """Print search instructions."""
    print("=== Fair Housing and Discrimination Search Instructions ===\n")
    
    print("HUD (Fair Housing):")
    print(f"  URL: {FEDERAL_URLS['HUD']['database']}")
    print("  Search for:")
    print("    - Kettler Management")
    print("    - Property addresses")
    print("    - Fair Housing Act violations")
    print()
    
    print("EEOC (Employment Discrimination):")
    print(f"  URL: {FEDERAL_URLS['EEOC']['database']}")
    print("  Search for:")
    print("    - Kettler Management Inc.")
    print("    - Employment discrimination complaints")
    print()
    
    print("State Agencies:")
    for state, agency in STATE_AGENCIES.items():
        print(f"  {state}: {agency}")


if __name__ == '__main__':
    create_discrimination_template()
    print_search_instructions()
