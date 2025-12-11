#!/usr/bin/env python3
"""
Quick Status Check
One-command status check for progress and searches.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_widget import ProgressWidget
from search_with_progress import SearchWithProgress

def show_status():
    """Show quick status overview."""
    pb = ProgressBar()
    widget = ProgressWidget()
    swp = SearchWithProgress()

    # Overall progress
    overall = pb.get_overall_progress()
    counts = pb.get_status_counts()

    print("\n" + "=" * 80)
    print(" " * 30 + "📊 STATUS" + " " * 30)
    print("=" * 80)
    print()

    # Progress bar
    print("Overall Progress:")
    print(f"  {widget.sparkline(width=50)}")
    print()

    # Status counts
    print("Status:")
    print(f"  ✅ Complete: {counts['complete']:2d}  ⚠️  In Progress: {counts['in_progress']:2d}  ❌ Not Started: {counts['not_started']:2d}")
    print()

    # License searches
    license_status = swp.check_license_searches_status()
    print("License Searches:")
    print(f"  {license_status['complete']}/{license_status['total']} states complete ({license_status['progress']:.1f}%)")
    if license_status['missing']:
        print(f"  Missing: {len(license_status['missing'])} search categories")
    print()

    # Top categories
    print("Top Categories:")
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

    sorted_cats = sorted(
        [(name, pb.stats[key]) for key, name in category_names.items()],
        key=lambda x: x[1]['progress'],
        reverse=True
    )

    for i, (name, cat) in enumerate(sorted_cats[:3], 1):
        status_emoji = {
            'complete': '✅',
            'in_progress': '⚠️',
            'templates_ready': '📝',
            'not_started': '❌'
        }.get(cat['status'], '❓')

        bar = pb.draw_bar(cat['progress'], width=25, style='simple')
        print(f"  {i}. {status_emoji} {name:<25s} {bar}")

    print()
    print("=" * 80)
    print()

if __name__ == "__main__":
    show_status()
