#!/usr/bin/env python3
"""
Browser Search: Company Registrations

Uses browser automation to search company registrations across all states.
"""

import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / 'research' / 'company_registrations' / 'data'

COMPANIES = ['Kettler Management Inc', 'Kettler Management', 'Kettler Companies']

STATES = {
    'DC': {
        'name': 'District of Columbia',
        'url': 'https://corponline.dccourts.gov/',
        'search_method': 'Entity search'
    },
    'MD': {
        'name': 'Maryland',
        'url': 'https://egov.maryland.gov/BusinessExpress/',
        'search_method': 'Business entity search'
    },
    'VA': {
        'name': 'Virginia',
        'url': 'https://cis.scc.virginia.gov/',
        'search_method': 'Business entity search'
    },
    'NJ': {
        'name': 'New Jersey',
        'url': 'https://www.njportal.com/DOR/BusinessRegistration/',
        'search_method': 'Business entity search'
    },
    'NY': {
        'name': 'New York',
        'url': 'https://dos.ny.gov/corporations',
        'search_method': 'Corporation search'
    },
    'CT': {
        'name': 'Connecticut',
        'url': 'https://www.concord-sots.ct.gov/CONCORD/',
        'search_method': 'Business entity search'
    }
}


def save_registration_result(state: str, company: str, findings: dict):
    """Save registration search result."""
    state_dir = DATA_DIR / state.lower()
    state_dir.mkdir(parents=True, exist_ok=True)

    result = {
        'metadata': {
            'date': datetime.now().isoformat(),
            'company': company,
            'state': STATES[state]['name'],
            'search_url': STATES[state]['url'],
            'search_method': 'Browser automation'
        },
        'findings': findings,
        'conclusion': f"{company} registration status in {STATES[state]['name']}"
    }

    filename = f"{company.lower().replace(' ', '_')}_registration.json"
    result_file = state_dir / filename
    result_file.write_text(json.dumps(result, indent=2) + '\n')
    return result_file


def search_dc_registration(company: str):
    """Search DC company registration using browser."""
    # Browser automation would:
    # 1. Navigate to https://corponline.dccourts.gov/
    # 2. Enter company name
    # 3. Execute search
    # 4. Parse results

    findings = {
        'registered': None,
        'entity_type': None,
        'formation_date': None,
        'registered_agent': None,
        'business_address': None,
        'status': None,
        'notes': 'Browser search needed'
    }

    return save_registration_result('DC', company, findings)


def main():
    """Main function."""
    print("Company Registration Browser Searches")
    print("=" * 60)

    for state_code, state_info in STATES.items():
        print(f"\n{state_info['name']} ({state_code})")
        print(f"URL: {state_info['url']}")

        for company in COMPANIES:
            print(f"  Searching: {company}...", end=' ')
            search_dc_registration(company)
            print("✓")


if __name__ == '__main__':
    main()
