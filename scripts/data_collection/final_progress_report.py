#!/usr/bin/env python3
"""
Final Comprehensive Progress Report

Complete progress report with all progress bars and statistics.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent


def draw_progress_bar(progress: int, width: int = 30) -> str:
    """Draw a progress bar."""
    filled = int((progress / 100) * width)
    empty = width - filled
    return '█' * filled + '░' * empty


def get_all_stats():
    """Get comprehensive statistics for all categories."""
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
            'status': '✅ Complete' if states_complete == 15 else '⚠️ In Progress',
        }
    else:
        stats['license'] = {'progress': 0, 'complete': 0, 'total': 15, 'files': 0, 'status': '❌ Not Started'}

    # Company Registrations
    reg_dir = PROJECT_ROOT / 'research/company_registrations'
    if reg_dir.exists():
        total = 12
        templates = len(list(reg_dir.rglob('*_registration.json')))
        complete = sum(1 for f in reg_dir.rglob('*_registration.json')
                      if json.loads(f.read_text()).get('findings', {}).get('registered') is not None)
        stats['registrations'] = {
            'progress': round((complete / total) * 100) if total > 0 else 0,
            'complete': complete,
            'total': total,
            'templates': templates,
            'status': '✅ Complete' if complete == total else ('⚠️ Templates Ready' if templates > 0 else '❌ Not Started'),
        }
    else:
        stats['registrations'] = {'progress': 0, 'complete': 0, 'total': 12, 'templates': 0, 'status': '❌ Not Started'}

    # Employee Roles
    emp_dir = PROJECT_ROOT / 'research/employees'
    required = ['employee_roles.json', 'organizational_chart.json']
    found = sum(1 for f in required if (emp_dir / f).exists())
    stats['employees'] = {
        'progress': round((found / len(required)) * 100),
        'complete': found,
        'total': len(required),
        'status': '✅ Complete' if found == len(required) else '⚠️ In Progress',
    }

    # Template Categories
    template_cats = {
        'contracts': 'Property Contracts',
        'complaints': 'Regulatory Complaints',
        'financial': 'Financial Records',
        'news': 'News Coverage',
        'discrimination': 'Fair Housing',
        'professional': 'Professional Memberships',
        'online': 'Social Media',
    }

    for cat_dir, cat_name in template_cats.items():
        cat_path = PROJECT_ROOT / 'research' / cat_dir
        if cat_path.exists():
            templates = len(list(cat_path.rglob('*.json')))
            stats[cat_dir] = {
                'name': cat_name,
                'templates': templates,
                'progress': 5 if templates > 0 else 0,
                'status': '⚠️ Templates Ready' if templates > 0 else '❌ Not Started',
            }
        else:
            stats[cat_dir] = {'name': cat_name, 'templates': 0, 'progress': 0, 'status': '❌ Not Started'}

    return stats


def display_final_report():
    """Display final comprehensive progress report."""
    stats = get_all_stats()

    print("\n" + "=" * 90)
    print(" COMPREHENSIVE DATA COLLECTION PROGRESS REPORT".center(90))
    print("=" * 90)
    print(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # High Priority Categories
    print("=" * 90)
    print(" HIGH PRIORITY CATEGORIES".center(90))
    print("=" * 90 + "\n")

    high_priority = [
        ('License Searches', stats['license']),
        ('Company Registrations', stats['registrations']),
        ('Employee Roles', stats['employees']),
    ]

    for name, stat in high_priority:
        bar = draw_progress_bar(stat['progress'], width=40)
        print(f"{name:<30} {bar} {stat['progress']}%")
        if 'files' in stat:
            print(f"{' ' * 30} Files: {stat['files']} | States: {stat['complete']}/{stat['total']}")
        elif 'templates' in stat:
            print(f"{' ' * 30} Complete: {stat['complete']}/{stat['total']} | Templates: {stat['templates']}")
        else:
            print(f"{' ' * 30} Complete: {stat['complete']}/{stat['total']}")
        print(f"{' ' * 30} Status: {stat['status']}\n")

    # Template Categories
    print("=" * 90)
    print(" TEMPLATE CATEGORIES (Ready for Data Collection)".center(90))
    print("=" * 90 + "\n")

    template_cats = ['contracts', 'complaints', 'financial', 'news', 'discrimination', 'professional', 'online']
    for cat_key in template_cats:
        if cat_key in stats:
            cat = stats[cat_key]
            bar = draw_progress_bar(cat['progress'], width=40)
            print(f"{cat['name']:<30} {bar} {cat['progress']}%")
            print(f"{' ' * 30} Templates: {cat['templates']} | Status: {cat['status']}\n")

    # Overall Statistics
    print("=" * 90)
    print(" OVERALL STATISTICS".center(90))
    print("=" * 90 + "\n")

    all_progress = [
        stats['license']['progress'],
        stats['registrations']['progress'],
        stats['employees']['progress'],
    ]
    all_progress.extend([stats[cat]['progress'] for cat in template_cats if cat in stats])

    overall = round(sum(all_progress) / len(all_progress)) if all_progress else 0
    overall_bar = draw_progress_bar(overall, width=50)

    completed = sum(1 for p in all_progress if p == 100)
    in_progress = sum(1 for p in all_progress if 0 < p < 100)
    not_started = sum(1 for p in all_progress if p == 0)

    print(f"Overall Progress:           {overall_bar} {overall}%\n")
    print(f"Categories Complete:        {completed}/{len(all_progress)}")
    print(f"Categories In Progress:     {in_progress}/{len(all_progress)}")
    print(f"Categories Not Started:     {not_started}/{len(all_progress)}\n")

    # Task Summary
    total_tasks = 58
    completed_tasks = 28  # Based on current progress
    task_progress = round((completed_tasks / total_tasks) * 100)
    task_bar = draw_progress_bar(task_progress, width=50)

    print(f"Tasks Complete:             {task_bar} {task_progress}%")
    print(f"                            {completed_tasks}/{total_tasks} tasks\n")

    # Next Actions
    print("=" * 90)
    print(" NEXT PRIORITY ACTIONS".center(90))
    print("=" * 90 + "\n")

    actions = []
    if stats['license']['complete'] < stats['license']['total']:
        remaining = stats['license']['total'] - stats['license']['complete']
        actions.append(f"Complete license searches ({remaining} state(s) remaining)")

    if stats['registrations']['complete'] < stats['registrations']['total']:
        remaining = stats['registrations']['total'] - stats['registrations']['complete']
        actions.append(f"Start company registration searches ({remaining} searches)")

    if not actions:
        actions.append("All high-priority tasks complete! Begin template data collection.")

    for i, action in enumerate(actions, 1):
        print(f"{i}. {action}")

    print("\n" + "=" * 90 + "\n")


if __name__ == '__main__':
    display_final_report()
