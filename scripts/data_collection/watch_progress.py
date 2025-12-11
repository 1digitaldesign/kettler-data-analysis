#!/usr/bin/env python3
"""
Auto-refreshing Progress Bar Watcher
Continuously updates and displays progress with automatic refresh.
"""

import sys
import time
import signal
from pathlib import Path
from datetime import datetime

# Import from live_progress_bar
BASE_DIR = Path(__file__).parent.parent.parent
RESEARCH_DIR = BASE_DIR / "research"

def count_license_searches():
    """Count license search files."""
    license_dir = RESEARCH_DIR / "license_searches"
    if not license_dir.exists():
        return 0, 0, 0

    states = [d for d in license_dir.iterdir() if d.is_dir()]
    total_states = 15
    completed_states = len(states)
    total_files = sum(1 for f in license_dir.rglob("*.json") if f.is_file())
    return completed_states, total_states, total_files

def count_company_registrations():
    """Count company registration files."""
    reg_dir = RESEARCH_DIR / "company_registrations"
    if not reg_dir.exists():
        return 0, 12, 0

    files = list(reg_dir.rglob("*.json"))
    complete = len([f for f in files if f.stat().st_size > 100])
    templates = len([f for f in files if f.stat().st_size <= 100])
    return complete, 12, templates

def count_employee_roles():
    """Count employee role files."""
    emp_dir = RESEARCH_DIR / "employees"
    if not emp_dir.exists():
        return 0, 2
    files = list(emp_dir.glob("*.json"))
    return len(files), 2

def count_template_files(category_dir, expected_templates):
    """Count template files for a category."""
    if not category_dir.exists():
        return 0, expected_templates
    files = list(category_dir.rglob("*.json"))
    templates = len([f for f in files if f.stat().st_size <= 500])
    return templates, expected_templates

def get_all_stats():
    """Get statistics for all categories."""
    stats = {}

    completed_states, total_states, total_files = count_license_searches()
    stats['license_searches'] = {
        'completed': completed_states,
        'total': total_states,
        'files': total_files,
        'progress': int((completed_states / total_states) * 100) if total_states > 0 else 0,
        'status': 'complete' if completed_states == total_states else 'in_progress'
    }

    complete, total, templates = count_company_registrations()
    stats['company_registrations'] = {
        'completed': complete,
        'total': total,
        'templates': templates,
        'progress': int((complete / total) * 100) if total > 0 else 0,
        'status': 'complete' if complete == total else ('templates_ready' if templates > 0 else 'not_started')
    }

    emp_files, emp_total = count_employee_roles()
    stats['employee_roles'] = {
        'completed': emp_files,
        'total': emp_total,
        'progress': int((emp_files / emp_total) * 100) if emp_total > 0 else 0,
        'status': 'complete' if emp_files == emp_total else 'in_progress'
    }

    template_categories = {
        'property_contracts': (RESEARCH_DIR / "contracts", 1),
        'regulatory_complaints': (RESEARCH_DIR / "complaints", 1),
        'financial_records': (RESEARCH_DIR / "financial", 1),
        'news_coverage': (RESEARCH_DIR / "news", 2),
        'fair_housing': (RESEARCH_DIR / "discrimination", 3),
        'professional_memberships': (RESEARCH_DIR / "professional", 2),
        'social_media': (RESEARCH_DIR / "online", 3),
    }

    for key, (dir_path, expected) in template_categories.items():
        templates, total_templates = count_template_files(dir_path, expected)
        stats[key] = {
            'templates': templates,
            'total_templates': total_templates,
            'progress': int((templates / total_templates) * 100) if total_templates > 0 else 0,
            'status': 'templates_ready' if templates > 0 else 'not_started'
        }

    return stats

def draw_progress_bar(progress, width=50):
    """Draw a progress bar."""
    filled = int((progress / 100) * width)
    empty = width - filled

    if progress == 100:
        bar = '█' * filled
    elif progress >= 75:
        bar = '█' * (filled - 1) + '▉' + '░' * empty
    elif progress >= 50:
        bar = '█' * (filled - 1) + '▊' + '░' * empty
    elif progress >= 25:
        bar = '█' * (filled - 1) + '▋' + '░' * empty
    else:
        bar = '█' * filled + '░' * empty

    return f"{bar} {progress:.1f}%"

def display_progress():
    """Display progress dashboard."""
    stats = get_all_stats()

    categories = [
        stats['license_searches'],
        stats['company_registrations'],
        stats['employee_roles'],
        stats['property_contracts'],
        stats['regulatory_complaints'],
        stats['financial_records'],
        stats['news_coverage'],
        stats['fair_housing'],
        stats['professional_memberships'],
        stats['social_media'],
    ]

    overall_progress = sum(cat['progress'] for cat in categories) / len(categories)
    complete_count = sum(1 for cat in categories if cat['status'] == 'complete')
    in_progress_count = sum(1 for cat in categories if cat['status'] in ['in_progress', 'templates_ready'])
    not_started_count = sum(1 for cat in categories if cat['status'] == 'not_started')

    category_names = {
        'license_searches': 'License Searches',
        'company_registrations': 'Company Registrations',
        'employee_roles': 'Employee Roles',
        'property_contracts': 'Property Contracts',
        'regulatory_complaints': 'Regulatory Complaints',
        'financial_records': 'Financial Records',
        'news_coverage': 'News Coverage',
        'fair_housing': 'Fair Housing',
        'professional_memberships': 'Professional Memberships',
        'social_media': 'Social Media',
    }

    # Clear and display
    print("\033[2J\033[H", end="")
    print("=" * 80)
    print(" " * 15 + "🔄 AUTO-REFRESHING PROGRESS BAR (Press Ctrl+C to stop)" + " " * 15)
    print("=" * 80)
    print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Refresh: Every 5 seconds")
    print()

    # Overall progress
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "OVERALL PROGRESS" + " " * 34 + "║")
    print("╠" + "═" * 78 + "╣")
    overall_bar = draw_progress_bar(overall_progress, width=60)
    print(f"║ {overall_bar:76s} ║")
    print("╠" + "═" * 78 + "╣")
    print(f"║ Status: ✅ Complete: {complete_count:2d}  ⚠️  In Progress: {in_progress_count:2d}  ❌ Not Started: {not_started_count:2d}", end="")
    print(" " * (78 - 60), end="")
    print("║")
    print("╚" + "═" * 78 + "╝")
    print()

    # Top 5 categories
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "TOP CATEGORIES" + " " * 33 + "║")
    print("╠" + "═" * 78 + "╣")

    # Sort by progress
    sorted_cats = sorted(
        [(key, name, stats[key]) for key, name in category_names.items()],
        key=lambda x: x[2]['progress'],
        reverse=True
    )

    for i, (key, name, cat_stats) in enumerate(sorted_cats[:5], 1):
        progress = cat_stats['progress']
        status = cat_stats['status']

        if status == 'complete':
            status_emoji = '✅'
        elif status == 'in_progress':
            status_emoji = '⚠️'
        elif status == 'templates_ready':
            status_emoji = '📝'
        else:
            status_emoji = '❌'

        bar = draw_progress_bar(progress, width=50)
        print(f"║ {i}. {status_emoji} {name:<25s} {bar:45s} ║")

    print("╚" + "═" * 78 + "╝")
    print()
    print("─" * 80)
    print(f"📈 Overall: {overall_progress:.1f}%  |  ✅ Complete: {complete_count}  |  ⚠️  Active: {in_progress_count}  |  ❌ Pending: {not_started_count}")
    print("─" * 80)
    print("\n💡 Watching for changes... (Ctrl+C to exit)")

# Global flag for graceful exit
running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    global running
    print("\n\n🛑 Stopping progress watcher...")
    running = False
    sys.exit(0)

def main():
    """Main watch loop."""
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting auto-refreshing progress bar...")
    print("Press Ctrl+C to stop\n")
    time.sleep(2)

    try:
        while running:
            display_progress()
            time.sleep(5)  # Refresh every 5 seconds
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()
