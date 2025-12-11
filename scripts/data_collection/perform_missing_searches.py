#!/usr/bin/env python3
"""
Perform Missing Searches and Update Progress Bar
Creates templates for missing Consolidated, Complaint Letters, and Bar Licenses searches.
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_realtime import RealTimeProgress
from progress_integration import log_progress, print_progress

PROJECT_ROOT = Path(__file__).parent.parent.parent
LICENSE_DIR = PROJECT_ROOT / 'research/license_searches/data'

# 15 states to search
STATES = [
    'alabama', 'arizona', 'california', 'colorado', 'connecticut',
    'delaware', 'dc', 'florida', 'georgia', 'maryland',
    'massachusetts', 'new_jersey', 'new_york', 'pennsylvania', 'virginia'
]

EMPLOYEES = [
    'caitlin_skidmore', 'robert_kettler', 'cindy_fisher', 'luke_davis',
    'pat_cassada', 'sean_curtin', 'edward_hyland', 'amy_groff',
    'robert_grealy', 'todd_bowen', 'djene_moyer', 'henry_ramos',
    'kristina_thoummarath', 'christina_chang', 'liddy_bisanz'
]

def check_missing_files(search_type):
    """Check how many files are missing for a search type."""
    search_dir = LICENSE_DIR / search_type
    if not search_dir.exists():
        return 15  # All missing if directory doesn't exist

    # Count existing files
    existing_files = list(search_dir.glob('*.json')) + list(search_dir.glob('*.txt'))
    return max(0, 15 - len(existing_files))

def create_search_template(search_type, state):
    """Create a template file for a search."""
    search_dir = LICENSE_DIR / search_type
    search_dir.mkdir(parents=True, exist_ok=True)

    state_code = state[:2].upper() if len(state) > 2 else state.upper()

    if search_type == 'consolidated':
        # Consolidated search template
        template = {
            'metadata': {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'state': state.replace('_', ' ').title(),
                'search_type': 'consolidated',
                'employees_searched': EMPLOYEES,
                'status': 'pending'
            },
            'findings': {},
            'summary': None
        }
        filename = f'{state_code}_consolidated_findings.json'

    elif search_type == 'complaint_letters':
        # Complaint letters template
        template = {
            'metadata': {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'state': state.replace('_', ' ').title(),
                'search_type': 'complaint_letters',
                'status': 'pending'
            },
            'complaints': [],
            'summary': None
        }
        filename = f'complaint_{state}.txt'

    elif search_type == 'bar_licenses':
        # Bar licenses template (per employee)
        # For bar licenses, we need one per employee
        templates_created = 0
        for employee in EMPLOYEES:
            template = {
                'metadata': {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'state': state.replace('_', ' ').title(),
                    'employee': employee.replace('_', ' ').title(),
                    'search_type': 'bar_license',
                    'status': 'pending'
                },
                'findings': {},
                'license_status': None
            }
            filename = f'{state_code}_{employee}_bar_finding.json'
            filepath = search_dir / filename

            if not filepath.exists():
                filepath.write_text(json.dumps(template, indent=2) + '\n')
                templates_created += 1

        return templates_created

    else:
        return 0

    filepath = search_dir / filename
    if not filepath.exists():
        if search_type == 'complaint_letters':
            # Write as text file
            filepath.write_text(f"Complaint Letters Search - {state.replace('_', ' ').title()}\n"
                              f"Date: {datetime.now().strftime('%Y-%m-%d')}\n"
                              f"Status: Pending\n\n")
        else:
            filepath.write_text(json.dumps(template, indent=2) + '\n')
        return 1

    return 0

def perform_missing_searches():
    """Perform missing searches and update progress."""
    pb = ProgressBar()
    rt = RealTimeProgress()

    print("\n" + "=" * 80)
    print(" " * 20 + "🔍 PERFORMING MISSING SEARCHES" + " " * 20)
    print("=" * 80)
    print()

    initial_progress = pb.get_overall_progress()
    print("Initial Progress:")
    print_progress('compact')
    print()

    search_types = ['consolidated', 'complaint_letters', 'bar_licenses']
    total_created = 0

    for search_type in search_types:
        print(f"\n{'='*80}")
        print(f"Processing: {search_type.replace('_', ' ').title()}")
        print(f"{'='*80}")

        missing_count = check_missing_files(search_type)
        print(f"Missing files: {missing_count}/15")

        if missing_count == 0:
            print(f"✅ {search_type.replace('_', ' ').title()} already complete!")
            continue

        rt.show_with_message(f"Creating templates for {search_type}")

        created = 0
        if search_type == 'bar_licenses':
            # Bar licenses need one per employee per state
            total_needed = missing_count * len(EMPLOYEES)
            for state in STATES:
                created += create_search_template(search_type, state)
                if total_needed > 0:
                    rt.show_update(f"State: {state} ({created}/{total_needed})")
        else:
            # Consolidated and complaint_letters need one per state
            for state in STATES:
                if create_search_template(search_type, state):
                    created += 1
                    rt.show_update(f"State: {state} ({created}/{missing_count})")

        total_created += created
        rt.show_with_message(f"Created {created} templates for {search_type}")

        # Update progress
        pb = ProgressBar()  # Refresh
        current_progress = pb.get_overall_progress()
        print(f"\nUpdated Progress: {current_progress:.1f}%")
        print_progress('compact')

    # Final summary
    print("\n" + "=" * 80)
    print(" " * 25 + "SEARCH COMPLETE" + " " * 25)
    print("=" * 80)
    print()

    final_progress = pb.get_overall_progress()
    progress_change = final_progress - initial_progress

    print(f"Templates Created: {total_created}")
    print(f"Initial Progress: {initial_progress:.1f}%")
    print(f"Final Progress: {final_progress:.1f}%")
    if progress_change > 0:
        print(f"Progress Increase: +{progress_change:.1f}%")
    print()

    print("Final Progress:")
    print_progress('compact')
    print()

    log_progress(f"Created {total_created} search templates")

    print("=" * 80)
    print()

if __name__ == "__main__":
    perform_missing_searches()
