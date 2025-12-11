#!/usr/bin/env python3
"""
Search Progress Dashboard
Unified dashboard showing search status and progress.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_widget import ProgressWidget
from progress_integration import get_progress_string, log_progress
from search_with_progress import SearchWithProgress

PROJECT_ROOT = Path(__file__).parent.parent.parent
LICENSE_DIR = PROJECT_ROOT / 'research/license_searches/data'

def display_search_dashboard():
    """Display comprehensive search progress dashboard."""
    pb = ProgressBar()
    widget = ProgressWidget()
    swp = SearchWithProgress()

    print("\n" + "=" * 80)
    print(" " * 20 + "🔍 SEARCH PROGRESS DASHBOARD" + " " * 20)
    print("=" * 80)
    print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Overall Progress
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "OVERALL PROGRESS" + " " * 35 + "║")
    print("╠" + "═" * 78 + "╣")
    overall = pb.get_overall_progress()
    counts = pb.get_status_counts()
    overall_bar = widget.sparkline(width=50)
    print(f"║ {overall_bar:76s} ║")
    print("╠" + "═" * 78 + "╣")
    print(f"║ Status: ✅ Complete: {counts['complete']:2d}  ⚠️  In Progress: {counts['in_progress']:2d}  ❌ Not Started: {counts['not_started']:2d}", end="")
    print(" " * (78 - 60), end="")
    print("║")
    print("╚" + "═" * 78 + "╝")
    print()

    # License Search Status
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "LICENSE SEARCHES" + " " * 35 + "║")
    print("╠" + "═" * 78 + "╣")

    license_status = swp.check_license_searches_status()
    license_progress = license_status['progress']
    license_bar = pb.draw_bar(license_progress, width=50, style='enhanced')

    print(f"║ Overall: {license_bar:68s} ║")
    print(f"║ Complete: {license_status['complete']}/{license_status['total']} states ({license_progress:.1f}%)", end="")
    print(" " * (78 - 50), end="")
    print("║")

    if license_status['missing']:
        print("╠" + "═" * 78 + "╣")
        print("║ Missing Searches:", end="")
        print(" " * (78 - 18), end="")
        print("║")
        for state_info in license_status['missing'][:5]:  # Show first 5
            state_name = state_info['state'].replace('_', ' ').title()
            print(f"║   • {state_name:<30s} {state_info['complete']}/15 complete ({state_info['missing']} missing)", end="")
            print(" " * (78 - 70), end="")
            print("║")
        if len(license_status['missing']) > 5:
            print(f"║   ... and {len(license_status['missing']) - 5} more", end="")
            print(" " * (78 - 20), end="")
            print("║")

    print("╚" + "═" * 78 + "╝")
    print()

    # Category Progress
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "CATEGORY PROGRESS" + " " * 32 + "║")
    print("╠" + "═" * 78 + "╣")

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

    # Show top 5 categories
    sorted_cats = sorted(
        [(name, pb.stats[key]) for key, name in category_names.items()],
        key=lambda x: x[1]['progress'],
        reverse=True
    )

    for i, (name, cat) in enumerate(sorted_cats[:5], 1):
        status_emoji = {
            'complete': '✅',
            'in_progress': '⚠️',
            'templates_ready': '📝',
            'not_started': '❌'
        }.get(cat['status'], '❓')

        bar = pb.draw_bar(cat['progress'], width=35, style='simple')
        print(f"║ {i}. {status_emoji} {name:<25s} {bar:40s} ║")

    print("╚" + "═" * 78 + "╝")
    print()

    # Quick Actions
    print("─" * 80)
    print("Quick Actions:")
    print("  • Run search workflow: python3 scripts/data_collection/search_workflow.py")
    print("  • Check progress: python3 scripts/data_collection/progress.py")
    print("  • Monitor progress: python3 scripts/data_collection/watch_progress.py")
    print("─" * 80)
    print()

if __name__ == "__main__":
    display_search_dashboard()
