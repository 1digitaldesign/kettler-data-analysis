#!/usr/bin/env python3
"""
Start Company Registration Searches

Script to begin company registration data collection.
"""

from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
REGISTRATIONS_DIR = PROJECT_ROOT / 'research/company_registrations'

# Companies to search
COMPANIES = [
    'Kettler Management Inc.',
    'Kettler Management',
    'KETTLER MANAGEMENT INC',
]

# States to search (primary operational states)
STATES = [
    'dc',
    'Maryland',
    'Virginia',
    'New Jersey',
    'New York',
    'Connecticut',
]

# Skidmore-affiliated companies (from DC license records)
SKIDMORE_COMPANIES = [
    # These would be extracted from DC license records
    # Placeholder for now
]


def create_registration_template(state: str, company: str) -> dict:
    """Create a registration search template."""
    return {
        'metadata': {
            'date': None,
            'state': state,
            'company': company,
            'search_url': None,  # State-specific SOS URL
            'search_method': 'Secretary of State database',
        },
        'findings': {
            'registered': None,
            'entity_type': None,
            'formation_date': None,
            'registered_agent': None,
            'business_address': None,
            'status': None,
        },
        'conclusion': None,
    }


def get_state_sos_url(state: str) -> str:
    """Get Secretary of State URL for state."""
    urls = {
        'dc': 'https://corponline.dccorporations.gov/',
        'Maryland': 'https://egov.maryland.gov/BusinessExpress/EntitySearch',
        'Virginia': 'https://cis.scc.virginia.gov/EntitySearch/Index',
        'New Jersey': 'https://www.njportal.com/DOR/BusinessNameSearch/',
        'New York': 'https://apps.dos.ny.gov/publicInquiry/',
        'Connecticut': 'https://www.concord-sots.ct.gov/CONCORD/PublicInquiry',
    }
    return urls.get(state, '')


def create_search_templates():
    """Create search templates for all companies."""
    REGISTRATIONS_DIR.mkdir(parents=True, exist_ok=True)

    templates_created = 0

    for state in STATES:
        state_dir = REGISTRATIONS_DIR / state.lower().replace(' ', '_')
        state_dir.mkdir(parents=True, exist_ok=True)

        for company in COMPANIES:
            template = create_registration_template(state, company)
            template['metadata']['search_url'] = get_state_sos_url(state)

            # Create filename
            company_slug = company.lower().replace(' ', '_').replace('.', '').replace(',', '')
            filename = f'{state.lower().replace(" ", "_")}_{company_slug}_registration.json'
            filepath = state_dir / filename

            if not filepath.exists():
                filepath.write_text(json.dumps(template, indent=2) + '\n')
                templates_created += 1

    print(f"Created {templates_created} company registration templates")
    return templates_created


def print_search_instructions():
    """Print instructions for conducting searches."""
    print("=== Company Registration Search Instructions ===\n")

    for state in STATES:
        url = get_state_sos_url(state)
        print(f"{state}:")
        print(f"  URL: {url}")
        print(f"  Search for: Kettler Management Inc., Kettler Management")
        print(f"  Look for: Entity type, formation date, registered agent, status")
        print()


if __name__ == '__main__':
    print_search_instructions()
    create_search_templates()
