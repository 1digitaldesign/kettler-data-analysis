#!/usr/bin/env python3
"""
Collect Regulatory Complaint History

Script to help search for regulatory complaints and enforcement actions.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
COMPLAINTS_DIR = PROJECT_ROOT / 'research/complaints'

# States to search
STATES = [
    'District of Columbia',
    'Maryland',
    'Virginia',
    'New Jersey',
    'New York',
    'Connecticut',
]

# Regulatory agency URLs
AGENCY_URLS = {
    'District of Columbia': {
        'real_estate': 'https://www.dcopla.com/',
        'consumer_affairs': 'https://dcra.dc.gov/',
    },
    'Maryland': {
        'real_estate': 'https://www.dllr.state.md.us/license/',
        'consumer_affairs': 'https://www.dllr.state.md.us/',
    },
    'Virginia': {
        'real_estate': 'https://www.dpor.virginia.gov/',
        'consumer_affairs': 'https://www.vdacs.virginia.gov/',
    },
    'New Jersey': {
        'real_estate': 'https://www.njconsumeraffairs.gov/',
        'consumer_affairs': 'https://www.njconsumeraffairs.gov/',
    },
    'New York': {
        'real_estate': 'https://www.dos.ny.gov/',
        'consumer_affairs': 'https://www.dos.ny.gov/',
    },
    'Connecticut': {
        'real_estate': 'https://www.elicense.ct.gov/',
        'consumer_affairs': 'https://portal.ct.gov/DCP',
    },
}


def create_complaint_template():
    """Create template for complaint records."""
    COMPLAINTS_DIR.mkdir(parents=True, exist_ok=True)

    template = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Regulatory complaint history documentation',
        },
        'complaints_by_state': {},
        'enforcement_actions': [],
        'settlements': [],
        'violations': [],
        'penalties': [],
    }

    for state in STATES:
        template['complaints_by_state'][state] = {
            'regulatory_complaints': [],
            'consumer_complaints': [],
            'enforcement_actions': [],
            'settlements': [],
            'violations': [],
            'penalties': [],
            'agency_urls': AGENCY_URLS.get(state, {}),
        }

    filepath = COMPLAINTS_DIR / 'regulatory_complaints.json'
    filepath.write_text(json.dumps(template, indent=2) + '\n')
    print(f"Created {filepath}")
    return filepath


def print_search_instructions():
    """Print instructions for complaint searches."""
    print("=== Regulatory Complaint Search Instructions ===\n")

    for state, urls in AGENCY_URLS.items():
        print(f"{state}:")
        print(f"  Real Estate Commission: {urls.get('real_estate', 'N/A')}")
        print(f"  Consumer Affairs: {urls.get('consumer_affairs', 'N/A')}")
        print(f"  Search terms:")
        print(f"    - Kettler Management")
        print(f"    - Kettler Management Inc.")
        print(f"    - Caitlin Skidmore")
        print(f"    - Edward Hyland")
        print(f"    - Robert Kettler")
        print()


if __name__ == '__main__':
    create_complaint_template()
    print_search_instructions()
