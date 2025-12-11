#!/usr/bin/env python3
"""
Enhanced Live Progress Bar Display
Shows detailed, visually appealing progress bars with real-time updates.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
RESEARCH_DIR = BASE_DIR / "research"

def count_license_searches():
    """Count license search files."""
    license_dir = RESEARCH_DIR / "license_searches"
    if not license_dir.exists():
        return 0, 0, 0

    # Count state directories
    states = [d for d in license_dir.iterdir() if d.is_dir()]
    total_states = 15  # Expected states
    completed_states = len(states)

    # Count total files
    total_files = sum(1 for f in license_dir.rglob("*.json") if f.is_file())

    return completed_states, total_states, total_files

def count_company_registrations():
    """Count company registration files."""
    reg_dir = RESEARCH_DIR / "company_registrations"
    if not reg_dir.exists():
        return 0, 12, 0

    # Count JSON files
    files = list(reg_dir.rglob("*.json"))
    complete = len([f for f in files if f.stat().st_size > 100])  # Non-empty files
    templates = len([f for f in files if f.stat().st_size <= 100])  # Template files

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
    templates = len([f for f in files if f.stat().st_size <= 500])  # Template files
    return templates, expected_templates

def get_all_stats():
    """Get statistics for all categories."""
    stats = {}

    # License Searches
    completed_states, total_states, total_files = count_license_searches()
    stats['license_searches'] = {
        'completed': completed_states,
        'total': total_states,
        'files': total_files,
        'progress': int((completed_states / total_states) * 100) if total_states > 0 else 0,
        'status': 'complete' if completed_states == total_states else 'in_progress'
    }

    # Company Registrations
    complete, total, templates = count_company_registrations()
    stats['company_registrations'] = {
        'completed': complete,
        'total': total,
        'templates': templates,
        'progress': int((complete / total) * 100) if total > 0 else 0,
        'status': 'complete' if complete == total else ('templates_ready' if templates > 0 else 'not_started')
    }

    # Employee Roles
    emp_files, emp_total = count_employee_roles()
    stats['employee_roles'] = {
        'completed': emp_files,
        'total': emp_total,
        'progress': int((emp_files / emp_total) * 100) if emp_total > 0 else 0,
        'status': 'complete' if emp_files == emp_total else 'in_progress'
    }

    # Template categories
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

def format_time_estimate(progress_percent):
    """Estimate time remaining based on progress."""
    if progress_percent == 0:
        return "Not started"
    elif progress_percent >= 100:
        return "Complete"
    elif progress_percent < 10:
        return "~2-3 weeks remaining"
    elif progress_percent < 25:
        return "~1-2 weeks remaining"
    elif progress_percent < 50:
        return "~3-5 days remaining"
    elif progress_percent < 75:
        return "~1-2 days remaining"
    else:
        return "~Few hours remaining"

def draw_enhanced_progress_bar(progress, width=40, show_percentage=True):
    """Draw an enhanced progress bar with gradient effect."""
    filled = int((progress / 100) * width)
    empty = width - filled

    # Use different characters for visual effect
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

    if show_percentage:
        return f"{bar} {progress:.1f}%"
    return bar

def display_live_progress():
    """Display enhanced live progress dashboard."""
    stats = get_all_stats()

    # Calculate overall progress
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

    # Category names
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

    # Clear screen and display header
    print("\033[2J\033[H", end="")  # Clear screen and move to top
    print("=" * 80)
    print(" " * 20 + "📊 LIVE DATA COLLECTION PROGRESS DASHBOARD" + " " * 20)
    print("=" * 80)
    print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Overall progress section
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 25 + "OVERALL PROGRESS" + " " * 37 + "║")
    print("╠" + "═" * 78 + "╣")
    print("║", end="")
    overall_bar = draw_enhanced_progress_bar(overall_progress, width=60)
    print(f" {overall_bar:76s}", end="")
    print("║")
    print("╠" + "═" * 78 + "╣")
    print("║", end="")
    print(f" Status: ✅ Complete: {complete_count:2d}  ⚠️  In Progress: {in_progress_count:2d}  ❌ Not Started: {not_started_count:2d}", end="")
    print(" " * (78 - 60), end="")
    print("║")
    print("║", end="")
    estimate = format_time_estimate(overall_progress)
    print(f" Estimated Time: {estimate}", end="")
    print(" " * (78 - len(f" Estimated Time: {estimate}")), end="")
    print("║")
    print("╚" + "═" * 78 + "╝")
    print()

    # Category details
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "CATEGORY BREAKDOWN" + " " * 31 + "║")
    print("╠" + "═" * 78 + "╣")

    for i, (key, name) in enumerate(category_names.items(), 1):
        cat_stats = stats[key]
        progress = cat_stats['progress']
        status = cat_stats['status']

        # Status emoji and text
        if status == 'complete':
            status_emoji = '✅'
            status_text = 'Complete'
        elif status == 'in_progress':
            status_emoji = '⚠️'
            status_text = 'In Progress'
        elif status == 'templates_ready':
            status_emoji = '📝'
            status_text = 'Templates Ready'
        else:
            status_emoji = '❌'
            status_text = 'Not Started'

        # Details
        if key == 'license_searches':
            details = f"{cat_stats['completed']}/{cat_stats['total']} states | {cat_stats['files']} files"
        elif key == 'company_registrations':
            details = f"{cat_stats['completed']}/{cat_stats['total']} complete"
        elif key == 'employee_roles':
            details = f"{cat_stats['completed']}/{cat_stats['total']} files"
        else:
            details = f"{cat_stats['templates']}/{cat_stats['total_templates']} templates"

        # Draw progress bar
        bar = draw_enhanced_progress_bar(progress, width=50)

        # Print category line
        print("║", end="")
        print(f" {i:2d}. {status_emoji} {name:<28s} {bar:54s}", end="")
        print("║")
        print("║", end="")
        print(f"     └─ {details:<72s}", end="")
        print("║")

        if i < len(category_names):
            print("║" + " " * 78 + "║")

    print("╚" + "═" * 78 + "╝")
    print()

    # Quick stats footer
    print("─" * 80)
    print(f"📈 Overall: {overall_progress:.1f}%  |  ✅ Complete: {complete_count}  |  ⚠️  Active: {in_progress_count}  |  ❌ Pending: {not_started_count}")
    print("─" * 80)
    print()
    print("💡 Tip: Run this script periodically to see live progress updates")
    print("   Files: HTML Dashboard (outputs/reports/progress_dashboard.html)")
    print("          Markdown Summary (research/reports/VISUAL_PROGRESS_SUMMARY.md)")

if __name__ == "__main__":
    try:
        display_live_progress()
    except KeyboardInterrupt:
        print("\n\nProgress display interrupted.")
        sys.exit(0)
