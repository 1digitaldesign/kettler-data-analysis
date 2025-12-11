#!/usr/bin/env python3
"""
Show All Progress Information
Displays all progress information in one comprehensive view.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_widget import ProgressWidget
from progress_integration import get_progress_string, print_progress
from search_with_progress import SearchWithProgress
from progress_notifier import ProgressNotifier

def show_all():
    """Show all progress information."""
    pb = ProgressBar()
    widget = ProgressWidget()
    swp = SearchWithProgress()
    notifier = ProgressNotifier()

    print("\n" + "=" * 80)
    print(" " * 20 + "📊 COMPLETE PROGRESS OVERVIEW" + " " * 20)
    print("=" * 80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Overall Progress
    overall = pb.get_overall_progress()
    counts = pb.get_status_counts()

    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "OVERALL PROGRESS" + " " * 35 + "║")
    print("╠" + "═" * 78 + "╣")
    overall_bar = widget.sparkline(width=50)
    print(f"║ {overall_bar:76s} ║")
    print("╠" + "═" * 78 + "╣")
    print(f"║ Status: ✅ Complete: {counts['complete']:2d}  ⚠️  In Progress: {counts['in_progress']:2d}  ❌ Not Started: {counts['not_started']:2d}", end="")
    print(" " * (78 - 60), end="")
    print("║")
    print("╚" + "═" * 78 + "╝")
    print()

    # License Search Status
    license_status = swp.check_license_searches_status()
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 28 + "LICENSE SEARCHES" + " " * 35 + "║")
    print("╠" + "═" * 78 + "╣")
    license_bar = pb.draw_bar(license_status['progress'], width=50, style='enhanced')
    print(f"║ {license_bar:76s} ║")
    print(f"║ Complete: {license_status['complete']}/{license_status['total']} states ({license_status['progress']:.1f}%)", end="")
    print(" " * (78 - 50), end="")
    print("║")
    print("╚" + "═" * 78 + "╝")
    print()

    # Category Progress
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 30 + "ALL CATEGORIES" + " " * 33 + "║")
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

    for i, (key, name) in enumerate(category_names.items(), 1):
        cat = pb.stats[key]
        status_emoji = {
            'complete': '✅',
            'in_progress': '⚠️',
            'templates_ready': '📝',
            'not_started': '❌'
        }.get(cat['status'], '❓')

        bar = pb.draw_bar(cat['progress'], width=35, style='simple')
        print(f"║ {i:2d}. {status_emoji} {name:<28s} {bar:38s} ║")

    print("╚" + "═" * 78 + "╝")
    print()

    # Next Milestone
    summary = notifier.get_progress_summary()
    if summary['next_milestone']:
        print("─" * 80)
        print(f"🎯 Next Milestone: {summary['next_milestone']}% ({summary['progress_to_next']:.1f}% away)")
        print("─" * 80)
        print()

    # Quick Actions
    print("Quick Commands:")
    print("  • Status: python3 scripts/data_collection/status.py")
    print("  • Progress: python3 scripts/data_collection/progress.py")
    print("  • Search: python3 scripts/data_collection/search_dashboard.py")
    print("  • Test: python3 scripts/data_collection/test_system.py")
    print()
    print("=" * 80)
    print()

if __name__ == "__main__":
    show_all()
