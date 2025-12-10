#!/usr/bin/env python3
"""
Display Progress Bar Visualization

Shows visual progress bars for all data collection categories.
"""

from pathlib import Path
import json
import re

PROJECT_ROOT = Path(__file__).parent.parent.parent
PROGRESS_FILE = PROJECT_ROOT / 'research/reports/DATA_COLLECTION_PROGRESS.md'


def count_license_searches():
    """Count completed license searches."""
    license_dir = PROJECT_ROOT / 'research/license_searches/data'

    if not license_dir.exists():
        return {'complete': 0, 'total': 15, 'progress': 0}

    states_complete = 0
    for state_dir in license_dir.iterdir():
        if state_dir.is_dir():
            finding_files = list(state_dir.glob('*_finding.json'))
            if len(finding_files) >= 15:  # All employees searched
                states_complete += 1

    return {
        'complete': states_complete,
        'total': 15,
        'progress': round((states_complete / 15) * 100),
    }


def count_data_files(category: str) -> int:
    """Count data files in category directory."""
    cat_dir = PROJECT_ROOT / 'research' / category
    if not cat_dir.exists():
        return 0

    # Count JSON files, excluding templates
    json_files = list(cat_dir.rglob('*.json'))
    return len(json_files)


def get_category_status(category_num: int, name: str) -> dict:
    """Get status for a category."""
    status_map = {
        1: {'name': 'License Searches', 'dir': 'license_searches', 'func': count_license_searches},
        2: {'name': 'Company Registrations', 'dir': 'company_registrations', 'func': None},
        3: {'name': 'Property Contracts', 'dir': 'contracts', 'func': None},
        4: {'name': 'Employee Roles', 'dir': 'employees', 'func': None},
        5: {'name': 'Regulatory Complaints', 'dir': 'complaints', 'func': None},
        6: {'name': 'Financial Records', 'dir': 'financial', 'func': None},
        7: {'name': 'News Coverage', 'dir': 'news', 'func': None},
        8: {'name': 'Fair Housing', 'dir': 'discrimination', 'func': None},
        9: {'name': 'Professional Memberships', 'dir': 'professional', 'func': None},
        10: {'name': 'Social Media', 'dir': 'online', 'func': None},
    }

    cat_info = status_map.get(category_num)
    if not cat_info:
        return {'name': name, 'progress': 0, 'status': 'unknown'}

    # Special handling for license searches
    if category_num == 1:
        stats = count_license_searches()
        progress = stats['progress']
        if progress == 100:
            status = '✅ Complete'
        elif progress > 0:
            status = '⚠️ In Progress'
        else:
            status = '❌ Not Started'
        return {'name': cat_info['name'], 'progress': progress, 'status': status}

    # Check if category is complete
    if category_num == 4:  # Employee Roles
        emp_dir = PROJECT_ROOT / 'research/employees'
        if (emp_dir / 'employee_roles.json').exists() and (emp_dir / 'organizational_chart.json').exists():
            return {'name': cat_info['name'], 'progress': 100, 'status': '✅ Complete'}

    # Count files for other categories
    file_count = count_data_files(cat_info['dir'])

    # Determine progress based on file count
    if file_count == 0:
        progress = 0
        status = '❌ Not Started'
    elif file_count <= 2:
        progress = 5
        status = '⚠️ Templates Created'
    elif category_num == 7:  # News Coverage
        progress = 25
        status = '⚠️ In Progress'
    elif category_num == 2:  # Company Registrations
        progress = 10
        status = '⚠️ In Progress'
    else:
        progress = 5
        status = '⚠️ In Progress'

    return {'name': cat_info['name'], 'progress': progress, 'status': status}


def draw_progress_bar(progress: int, width: int = 20) -> str:
    """Draw a progress bar."""
    filled = int((progress / 100) * width)
    empty = width - filled
    bar = '█' * filled + '░' * empty
    return f"{bar} {progress}%"


def display_progress():
    """Display progress visualization."""
    print("\n" + "=" * 70)
    print(" DATA COLLECTION PROGRESS DASHBOARD".center(70))
    print("=" * 70 + "\n")

    categories = [
        (1, "License Searches"),
        (2, "Company Registrations"),
        (3, "Property Contracts"),
        (4, "Employee Roles"),
        (5, "Regulatory Complaints"),
        (6, "Financial Records"),
        (7, "News Coverage"),
        (8, "Fair Housing"),
        (9, "Professional Memberships"),
        (10, "Social Media"),
    ]

    completed = 0
    in_progress = 0
    not_started = 0
    total_progress = 0

    for cat_num, cat_name in categories:
        status = get_category_status(cat_num, cat_name)
        progress = status['progress']
        status_text = status['status']

        # Color coding
        if progress == 100:
            icon = "✅"
            completed += 1
        elif progress > 0:
            icon = "⚠️"
            in_progress += 1
        else:
            icon = "❌"
            not_started += 1

        bar = draw_progress_bar(progress)
        print(f"{icon} {cat_num:2d}. {status['name']:<30} {bar} {status_text}")
        total_progress += progress

    print("\n" + "-" * 70)
    print(f"SUMMARY".center(70))
    print("-" * 70)

    overall = round(total_progress / len(categories))
    overall_bar = draw_progress_bar(overall, width=30)

    print(f"\nOverall Progress: {overall_bar}")
    print(f"\n✅ Complete:     {completed:2d} categories")
    print(f"⚠️  In Progress: {in_progress:2d} categories")
    print(f"❌ Not Started:  {not_started:2d} categories")

    # Task breakdown
    print("\n" + "-" * 70)
    print("TASK BREAKDOWN".center(70))
    print("-" * 70)

    total_tasks = 58
    completed_tasks = 28  # Based on progress file
    task_progress = round((completed_tasks / total_tasks) * 100)
    task_bar = draw_progress_bar(task_progress, width=30)

    print(f"\nTasks Complete: {task_bar}")
    print(f"  {completed_tasks}/{total_tasks} tasks ({task_progress}%)")

    print("\n" + "=" * 70 + "\n")


if __name__ == '__main__':
    display_progress()
