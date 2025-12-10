#!/usr/bin/env python3
"""
Collect Company Registration Data

Script to help collect company registration data from state databases.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
REGISTRATIONS_DIR = PROJECT_ROOT / 'research/company_registrations'

# Companies to search
COMPANIES = [
    'Kettler Management Inc.',
    'Kettler Management',
]

# States and their SOS URLs
STATE_SOS_URLS = {
    'District of Columbia': 'https://corponline.dccorporations.gov/',
    'Maryland': 'https://egov.maryland.gov/BusinessExpress/EntitySearch',
    'Virginia': 'https://cis.scc.virginia.gov/EntitySearch/Index',
    'New Jersey': 'https://www.njportal.com/DOR/BusinessNameSearch/',
    'New York': 'https://apps.dos.ny.gov/publicInquiry/',
    'Connecticut': 'https://www.concord-sots.ct.gov/CONCORD/PublicInquiry',
}

# Skidmore-affiliated companies (from DC license records)
SKIDMORE_COMPANIES = [
    # These should be extracted from DC license records
    # Placeholder - will be populated from actual data
]


def update_registration_file(state: str, company: str, data: dict):
    """Update a registration file with collected data."""
    state_slug = state.lower().replace(' ', '_')
    company_slug = company.lower().replace(' ', '_').replace('.', '').replace(',', '')
    filename = f'{state_slug}_{company_slug}_registration.json'
    filepath = REGISTRATIONS_DIR / state_slug / filename
    
    if filepath.exists():
        existing = json.loads(filepath.read_text())
        existing['metadata']['date'] = datetime.now().strftime('%Y-%m-%d')
        existing['findings'].update(data.get('findings', {}))
        existing['conclusion'] = data.get('conclusion', existing.get('conclusion'))
        filepath.write_text(json.dumps(existing, indent=2) + '\n')
        return True
    return False


def create_search_checklist():
    """Create a checklist for manual searches."""
    print("=== Company Registration Search Checklist ===\n")
    
    for state, url in STATE_SOS_URLS.items():
        print(f"{state}:")
        print(f"  URL: {url}")
        print(f"  Search terms:")
        for company in COMPANIES:
            print(f"    - {company}")
        print(f"  Information to collect:")
        print(f"    - Entity type (Corporation, LLC, etc.)")
        print(f"    - Formation date")
        print(f"    - Registered agent name and address")
        print(f"    - Business address")
        print(f"    - Status (Active, Inactive, etc.)")
        print(f"    - File number/Entity ID")
        print()


def list_pending_searches():
    """List all pending registration searches."""
    pending = []
    
    for state in STATE_SOS_URLS.keys():
        state_slug = state.lower().replace(' ', '_')
        state_dir = REGISTRATIONS_DIR / state_slug
        
        if state_dir.exists():
            for company in COMPANIES:
                company_slug = company.lower().replace(' ', '_').replace('.', '').replace(',', '')
                filename = f'{state_slug}_{company_slug}_registration.json'
                filepath = state_dir / filename
                
                if filepath.exists():
                    data = json.loads(filepath.read_text())
                    # Check if search is incomplete
                    if not data.get('findings', {}).get('registered') is not None:
                        pending.append((state, company, filepath))
    
    return pending


if __name__ == '__main__':
    create_search_checklist()
    pending = list_pending_searches()
    print(f"\nPending searches: {len(pending)}")
    for state, company, filepath in pending[:5]:
        print(f"  {state}: {company}")
