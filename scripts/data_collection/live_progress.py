#!/usr/bin/env python3
"""
Live Progress Bar System

Continuous progress tracking with real-time updates and detailed breakdowns.
"""

from pathlib import Path
import json
import time
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent


def draw_progress_bar(progress: int, width: int = 20, show_percent: bool = True) -> str:
    """Draw a progress bar with percentage."""
    filled = int((progress / 100) * width)
    empty = width - filled
    bar = '█' * filled + '░' * empty
    if show_percent:
        return f"{bar} {progress}%"
    return bar


def get_detailed_stats():
    """Get detailed statistics for all categories."""
    stats = {}

    # License Searches
    license_dir = PROJECT_ROOT / 'research/license_searches/data'
    if license_dir.exists():
        total_files = len(list(license_dir.rglob('*_finding.json')))
        states_complete = sum(1 for state_dir in license_dir.iterdir()
                             if state_dir.is_dir() and
                             len(list(state_dir.glob('*_finding.json'))) >= 15)
        stats['license'] = {
            'files': total_files,
            'states_complete': states_complete,
            'total_states': 15,
            'progress': round((states_complete / 15) * 100),
            'expected_files': 15 * 15,  # 15 states × 15 employees
        }
    else:
        stats['license'] = {'files': 0, 'states_complete': 0, 'total_states': 15, 'progress': 0, 'expected_files': 225}

    # Company Registrations
    reg_dir = PROJECT_ROOT / 'research/company_registrations'
    if reg_dir.exists():
        total_templates = len(list(reg_dir.rglob('*_registration.json')))
        complete = sum(1 for f in reg_dir.rglob('*_registration.json')
                      if json.loads(f.read_text()).get('findings', {}).get('registered') is not None)
        stats['registrations'] = {
            'templates': total_templates,
            'complete': complete,
            'total': 12,
            'progress': round((complete / 12) * 100) if total_templates > 0 else 0,
        }
    else:
        stats['registrations'] = {'templates': 0, 'complete': 0, 'total': 12, 'progress': 0}

    # Employee Roles
    emp_dir = PROJECT_ROOT / 'research/employees'
    required = ['employee_roles.json', 'organizational_chart.json']
    found = sum(1 for f in required if (emp_dir / f).exists())
    stats['employees'] = {
        'files': found,
        'total': len(required),
        'progress': round((found / len(required)) * 100),
    }

    # Templates Ready
    template_categories = {
        'contracts': 'Property Contracts',
        'complaints': 'Regulatory Complaints',
        'financial': 'Financial Records',
        'news': 'News Coverage',
        'discrimination': 'Fair Housing',
        'professional': 'Professional Memberships',
        'online': 'Social Media',
    }

    templates_ready = {}
    for cat_dir, cat_name in template_categories.items():
        cat_path = PROJECT_ROOT / 'research' / cat_dir
        if cat_path.exists():
            count = len(list(cat_path.rglob('*.json')))
            templates_ready[cat_name] = count

    stats['templates'] = templates_ready

    return stats


def display_live_progress():
    """Display live progress dashboard."""
    stats = get_detailed_stats()

    print("\n" + "=" * 80)
    print(" LIVE DATA COLLECTION PROGRESS DASHBOARD".center(80))
    print("=" * 80 + "\n")

    # High Priority Categories
    print("📊 HIGH PRIORITY CATEGORIES")
    print("-" * 80)

    # License Searches
    lic = stats['license']
    bar = draw_progress_bar(lic['progress'], width=30)
    print(f"\n1. License Searches")
    print(f"   {bar}")
    print(f"   Files: {lic['files']}/{lic['expected_files']} ({round((lic['files']/lic['expected_files']*100))}%)")
    print(f"   States: {lic['states_complete']}/{lic['total_states']} complete")
    if lic['states_complete'] < lic['total_states']:
        remaining = lic['total_states'] - lic['states_complete']
        print(f"   ⚠️  {remaining} state(s) need completion")

    # Company Registrations
    reg = stats['registrations']
    bar = draw_progress_bar(reg['progress'], width=30)
    print(f"\n2. Company Registrations")
    print(f"   {bar}")
    print(f"   Complete: {reg['complete']}/{reg['total']} searches")
    print(f"   Templates: {reg['templates']} ready")
    if reg['complete'] < reg['total']:
        remaining = reg['total'] - reg['complete']
        print(f"   ⚠️  {remaining} searches pending")

    # Employee Roles
    emp = stats['employees']
    bar = draw_progress_bar(emp['progress'], width=30)
    print(f"\n3. Employee Roles")
    print(f"   {bar}")
    print(f"   Files: {emp['files']}/{emp['total']} complete")
    if emp['progress'] == 100:
        print(f"   ✅ Complete!")

    # Templates Ready
    print("\n" + "-" * 80)
    print("📋 TEMPLATES READY FOR DATA COLLECTION")
    print("-" * 80)

    if stats['templates']:
        for cat_name, count in sorted(stats['templates'].items()):
            if count > 0:
                print(f"   ✅ {cat_name}: {count} template(s)")
    else:
        print("   No templates found")

    # Overall Progress
    print("\n" + "-" * 80)
    print("📈 OVERALL PROGRESS")
    print("-" * 80)

    category_progress = [
        lic['progress'],
        reg['progress'],
        emp['progress'],
    ]

    # Add template categories (5% each if template exists)
    for cat_name, count in stats['templates'].items():
        if count > 0:
            category_progress.append(5)

    overall = round(sum(category_progress) / len(category_progress)) if category_progress else 0
    overall_bar = draw_progress_bar(overall, width=40)

    print(f"\n   {overall_bar}")
    print(f"\n   Categories Complete: {sum(1 for p in category_progress if p == 100)}/{len(category_progress)}")
    print(f"   Categories In Progress: {sum(1 for p in category_progress if 0 < p < 100)}/{len(category_progress)}")
    print(f"   Categories Not Started: {sum(1 for p in category_progress if p == 0)}/{len(category_progress)}")

    # Next Actions
    print("\n" + "-" * 80)
    print("🎯 NEXT ACTIONS")
    print("-" * 80)

    actions = []
    if lic['states_complete'] < lic['total_states']:
        actions.append(f"Complete license searches ({lic['total_states'] - lic['states_complete']} states remaining)")
    if reg['complete'] < reg['total']:
        actions.append(f"Start company registration searches ({reg['total'] - reg['complete']} searches)")
    if not actions:
        actions.append("All high-priority tasks complete! Move to next categories.")

    for i, action in enumerate(actions, 1):
        print(f"   {i}. {action}")

    print("\n" + "=" * 80 + "\n")

    return stats


def continuous_monitor(interval: int = 5):
    """Continuously monitor progress (for testing/demo)."""
    print("Starting continuous progress monitoring...")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            display_live_progress()
            print(f"Next update in {interval} seconds...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--monitor':
        continuous_monitor()
    else:
        display_live_progress()
