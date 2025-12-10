#!/usr/bin/env python3
"""
Start Company Registration Searches

Interactive script to begin company registration searches with progress tracking.
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


def get_pending_searches():
    """Get list of pending searches."""
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
                    if data.get('findings', {}).get('registered') is None:
                        pending.append({
                            'state': state,
                            'company': company,
                            'filepath': filepath,
                            'url': STATE_SOS_URLS[state],
                        })
    
    return pending


def update_registration_file(filepath: Path, findings: dict):
    """Update a registration file with findings."""
    if not filepath.exists():
        print(f"File not found: {filepath}")
        return False
    
    data = json.loads(filepath.read_text())
    data['metadata']['date'] = datetime.now().strftime('%Y-%m-%d')
    data['findings'].update(findings)
    
    filepath.write_text(json.dumps(data, indent=2) + '\n')
    return True


def display_search_queue():
    """Display pending searches with progress."""
    pending = get_pending_searches()
    total = len(STATE_SOS_URLS) * len(COMPANIES)
    completed = total - len(pending)
    progress = round((completed / total) * 100) if total > 0 else 0
    
    print("\n" + "=" * 70)
    print(" COMPANY REGISTRATION SEARCHES".center(70))
    print("=" * 70 + "\n")
    
    bar_width = 30
    filled = int((progress / 100) * bar_width)
    empty = bar_width - filled
    bar = '█' * filled + '░' * empty
    
    print(f"Progress: {bar} {progress}% ({completed}/{total})")
    print(f"\nPending Searches: {len(pending)}\n")
    
    if pending:
        print("Next Searches to Complete:\n")
        for i, search in enumerate(pending[:5], 1):
            print(f"{i}. {search['state']}: {search['company']}")
            print(f"   URL: {search['url']}")
            print(f"   File: {search['filepath'].relative_to(PROJECT_ROOT)}")
            print()
    else:
        print("✅ All searches complete!\n")
    
    return pending


if __name__ == '__main__':
    display_search_queue()
