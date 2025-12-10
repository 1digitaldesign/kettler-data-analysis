#!/usr/bin/env python3
"""
Progress-Guided Workflow System

Interactive workflow that guides through data collection tasks with live progress bars.
"""

from pathlib import Path
import json
import sys
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent


def draw_progress_bar(progress: int, width: int = 30, show_percent: bool = True) -> str:
    """Draw a progress bar."""
    filled = int((progress / 100) * width)
    empty = width - filled
    bar = '█' * filled + '░' * empty
    if show_percent:
        return f"{bar} {progress}%"
    return bar


def get_category_progress():
    """Get progress for all categories."""
    stats = {}

    # License Searches
    license_dir = PROJECT_ROOT / 'research/license_searches/data'
    if license_dir.exists():
        total_files = len(list(license_dir.rglob('*_finding.json')))
        states_complete = sum(1 for state_dir in license_dir.iterdir()
                             if state_dir.is_dir() and
                             len(list(state_dir.glob('*_finding.json'))) >= 15)
        stats['license'] = {
            'progress': round((states_complete / 15) * 100),
            'complete': states_complete,
            'total': 15,
            'files': total_files,
        }
    else:
        stats['license'] = {'progress': 0, 'complete': 0, 'total': 15, 'files': 0}

    # Company Registrations
    reg_dir = PROJECT_ROOT / 'research/company_registrations'
    if reg_dir.exists():
        total = 12
        complete = sum(1 for f in reg_dir.rglob('*_registration.json')
                      if json.loads(f.read_text()).get('findings', {}).get('registered') is not None)
        stats['registrations'] = {
            'progress': round((complete / total) * 100) if total > 0 else 0,
            'complete': complete,
            'total': total,
        }
    else:
        stats['registrations'] = {'progress': 0, 'complete': 0, 'total': 12}

    # Employee Roles
    emp_dir = PROJECT_ROOT / 'research/employees'
    required = ['employee_roles.json', 'organizational_chart.json']
    found = sum(1 for f in required if (emp_dir / f).exists())
    stats['employees'] = {
        'progress': round((found / len(required)) * 100),
        'complete': found,
        'total': len(required),
    }

    return stats


def display_progress_header():
    """Display progress header with current status."""
    stats = get_category_progress()

    print("\n" + "=" * 80)
    print(" PROGRESS-GUIDED DATA COLLECTION WORKFLOW".center(80))
    print("=" * 80 + "\n")

    print("📊 CURRENT PROGRESS")
    print("-" * 80)

    # License Searches
    lic = stats['license']
    bar = draw_progress_bar(lic['progress'])
    print(f"\n1. License Searches:        {bar}")
    print(f"   Status: {lic['complete']}/{lic['total']} states complete ({lic['files']} files)")

    # Company Registrations
    reg = stats['registrations']
    bar = draw_progress_bar(reg['progress'])
    print(f"\n2. Company Registrations:  {bar}")
    print(f"   Status: {reg['complete']}/{reg['total']} searches complete")

    # Employee Roles
    emp = stats['employees']
    bar = draw_progress_bar(emp['progress'])
    print(f"\n3. Employee Roles:         {bar}")
    print(f"   Status: {emp['complete']}/{emp['total']} files complete")

    # Overall
    overall = round((lic['progress'] + reg['progress'] + emp['progress']) / 3)
    overall_bar = draw_progress_bar(overall, width=40)
    print(f"\n   Overall Progress:        {overall_bar}")

    print("\n" + "=" * 80 + "\n")

    return stats


def show_next_tasks():
    """Show next priority tasks with progress tracking."""
    stats = get_category_progress()

    print("🎯 NEXT PRIORITY TASKS")
    print("-" * 80 + "\n")

    tasks = []

    # License Searches
    if stats['license']['progress'] < 100:
        remaining = stats['license']['total'] - stats['license']['complete']
        tasks.append({
            'priority': 1,
            'category': 'License Searches',
            'task': f'Complete {remaining} remaining state(s)',
            'progress': stats['license']['progress'],
            'action': 'Use complete_license_searches.py to identify remaining searches',
        })

    # Company Registrations
    if stats['registrations']['progress'] < 100:
        remaining = stats['registrations']['total'] - stats['registrations']['complete']
        tasks.append({
            'priority': 2,
            'category': 'Company Registrations',
            'task': f'Complete {remaining} registration searches',
            'progress': stats['registrations']['progress'],
            'action': 'Use start_company_searches.py to view search queue',
        })

    # Property Contracts
    contracts_dir = PROJECT_ROOT / 'research/contracts'
    if contracts_dir.exists():
        contract_file = contracts_dir / 'property_management_contracts.json'
        if contract_file.exists():
            data = json.loads(contract_file.read_text())
            total_properties = sum(
                len(state_data.get('properties', []))
                for state_data in data.get('properties_by_state', {}).values()
            )
            if total_properties == 0:
                tasks.append({
                    'priority': 3,
                    'category': 'Property Contracts',
                    'task': 'Identify properties under management',
                    'progress': 0,
                    'action': 'Search company website and property databases',
                })

    if not tasks:
        print("✅ All high-priority tasks complete!")
        print("   Move to next categories: Regulatory Complaints, News Coverage, etc.\n")
    else:
        for i, task in enumerate(tasks, 1):
            bar = draw_progress_bar(task['progress'], width=20)
            print(f"{i}. {task['category']}")
            print(f"   Task: {task['task']}")
            print(f"   Progress: {bar}")
            print(f"   Action: {task['action']}")
            print()

    return tasks


def interactive_workflow():
    """Interactive workflow menu."""
    while True:
        display_progress_header()
        tasks = show_next_tasks()

        print("=" * 80)
        print("WORKFLOW OPTIONS")
        print("-" * 80)
        print("1. View detailed progress (live_progress.py)")
        print("2. View company search queue")
        print("3. Update progress tracker")
        print("4. View progress summary")
        print("5. Exit")
        print("-" * 80)

        choice = input("\nSelect option (1-5): ").strip()

        if choice == '1':
            import subprocess
            subprocess.run(['python3.14', 'scripts/data_collection/live_progress.py'])
        elif choice == '2':
            import subprocess
            subprocess.run(['python3.14', 'scripts/data_collection/start_company_searches.py'])
        elif choice == '3':
            import subprocess
            subprocess.run(['python3.14', 'scripts/data_collection/update_progress.py'])
        elif choice == '4':
            summary_file = PROJECT_ROOT / 'research/reports/PROGRESS_SUMMARY.md'
            if summary_file.exists():
                print(f"\n📄 Progress Summary: {summary_file}")
                print("   Open in your editor or view on GitHub\n")
            else:
                print("\n⚠️  Progress summary not found\n")
        elif choice == '5':
            print("\n👋 Exiting workflow. Progress saved.\n")
            break
        else:
            print("\n⚠️  Invalid option. Please select 1-5.\n")

        input("Press Enter to continue...")


def quick_status():
    """Quick status display."""
    stats = get_category_progress()

    print("\n" + "=" * 60)
    print(" QUICK STATUS".center(60))
    print("=" * 60)

    categories = [
        ('License Searches', stats['license']),
        ('Company Registrations', stats['registrations']),
        ('Employee Roles', stats['employees']),
    ]

    for name, stat in categories:
        bar = draw_progress_bar(stat['progress'], width=25)
        print(f"\n{name:<25} {bar}")
        print(f"{' ' * 25} {stat['complete']}/{stat['total']} complete")

    overall = round(sum(s['progress'] for _, s in categories) / len(categories))
    overall_bar = draw_progress_bar(overall, width=25)
    print(f"\n{'Overall':<25} {overall_bar}")

    print("\n" + "=" * 60 + "\n")


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == '--quick':
            quick_status()
        elif sys.argv[1] == '--interactive':
            interactive_workflow()
        else:
            display_progress_header()
            show_next_tasks()
    else:
        display_progress_header()
        show_next_tasks()
        print("\n💡 Tip: Use --interactive for full workflow menu")
        print("        Use --quick for quick status\n")
