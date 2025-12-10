#!/usr/bin/env python3
"""
Complete License Searches

Script to help complete remaining license searches for Maryland and Connecticut.
"""

from pathlib import Path
import json

PROJECT_ROOT = Path(__file__).parent.parent.parent
LICENSE_DIR = PROJECT_ROOT / 'research/license_searches/data'

# 15 employees to search
EMPLOYEES = [
    'caitlin_skidmore',
    'robert_kettler',
    'cindy_fisher',
    'luke_davis',
    'pat_cassada',
    'sean_curtin',
    'edward_hyland',
    'amy_groff',
    'robert_grealy',
    'todd_bowen',
    'djene_moyer',
    'henry_ramos',
    'kristina_thoummarath',
    'christina_chang',
    'liddy_bisanz',
]

# States to complete
STATES_TO_COMPLETE = {
    'maryland': {
        'url': 'https://www.dllr.state.md.us/license/',
        'agency': 'Maryland Real Estate Commission',
        'status': 'partial',
    },
    'connecticut': {
        'url': 'https://www.elicense.ct.gov/',
        'agency': 'Connecticut Department of Consumer Protection',
        'status': 'not_started',
    },
}


def check_missing_searches(state: str) -> list[str]:
    """Check which employee searches are missing for state."""
    state_dir = LICENSE_DIR / state
    if not state_dir.exists():
        return EMPLOYEES.copy()

    existing_files = {f.stem for f in state_dir.glob('*_finding.json')}
    missing = []

    # State code mapping
    state_codes = {
        'maryland': 'md',
        'connecticut': 'ct',
        'virginia': 'va',
        'dc': 'dc',
        'new_jersey': 'nj',
        'new_york': 'ny',
    }
    
    state_code = state_codes.get(state, state[:2])
    
    for employee in EMPLOYEES:
        expected_file = f'{state_code}_{employee}_finding'
        if expected_file not in existing_files:
            missing.append(employee)

    return missing


def create_search_template(state: str, employee: str) -> dict:
    """Create a search template for an employee."""
    state_info = STATES_TO_COMPLETE[state]

    return {
        'metadata': {
            'date': None,  # To be filled
            'state': state.title(),
            'search_url': state_info['url'],
            'employee': employee.replace('_', ' ').title(),
            'search_method': 'Browser automation or manual',
            'license_types_searched': ['Real Estate Broker', 'Real Estate Salesperson'],
        },
        'findings': {},
        'conclusion': None,  # To be filled after search
    }


def generate_search_list():
    """Generate list of searches needed."""
    print("=== Remaining License Searches ===\n")

    for state, info in STATES_TO_COMPLETE.items():
        missing = check_missing_searches(state)
        print(f"{state.upper()}:")
        print(f"  Agency: {info['agency']}")
        print(f"  URL: {info['url']}")
        print(f"  Missing searches: {len(missing)}/{len(EMPLOYEES)}")

        if missing:
            print("  Employees to search:")
            for emp in missing:
                print(f"    - {emp.replace('_', ' ').title()}")
        else:
            print("  ✅ All searches complete")
        print()


def create_missing_templates():
    """Create JSON templates for missing searches."""
    templates_created = 0

    for state in STATES_TO_COMPLETE.keys():
        missing = check_missing_searches(state)
        state_dir = LICENSE_DIR / state
        state_dir.mkdir(parents=True, exist_ok=True)

        for employee in missing:
            template = create_search_template(state, employee)
            filename = f'{state[:2]}_{employee}_finding.json'
            filepath = state_dir / filename

            if not filepath.exists():
                filepath.write_text(json.dumps(template, indent=2) + '\n')
                templates_created += 1

    print(f"Created {templates_created} search templates")
    return templates_created


if __name__ == '__main__':
    generate_search_list()
    create_missing_templates()
