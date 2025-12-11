#!/usr/bin/env python3
"""
Master Progress Bar Script
Unified interface for all progress bar features and formats.
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_widget import ProgressWidget
from progress_notifier import ProgressNotifier
from progress_with_history import ProgressHistory

def main():
    """Main progress bar interface."""
    parser = argparse.ArgumentParser(
        description='Master Progress Bar - Unified interface for all progress features',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Show default dashboard
  %(prog)s --widget compact  # Show compact widget
  %(prog)s --widget sparkline # Show sparkline
  %(prog)s --notify          # Check notifications
  %(prog)s --history         # Show history trends
  %(prog)s --export json     # Export to JSON
  %(prog)s --export csv      # Export to CSV
  %(prog)s --export all      # Export all formats
  %(prog)s --all             # Show everything
        """
    )

    parser.add_argument('--widget', choices=['compact', 'mini', 'inline', 'sparkline', 'circle', 'badges', 'grid', 'all'],
                       help='Display specific widget format')
    parser.add_argument('--notify', action='store_true', help='Check for milestone notifications')
    parser.add_argument('--history', action='store_true', help='Show progress history and trends')
    parser.add_argument('--export', choices=['json', 'csv', 'all'], help='Export progress data')
    parser.add_argument('--summary', action='store_true', help='Show brief summary')
    parser.add_argument('--all', action='store_true', help='Show all features')
    parser.add_argument('--record', action='store_true', help='Record current progress to history')

    args = parser.parse_args()

    # If no arguments, show default dashboard
    if len(sys.argv) == 1:
        show_default_dashboard()
        return

    # Handle --all flag
    if args.all:
        show_all_features()
        return

    # Handle widget displays
    if args.widget:
        widget = ProgressWidget()
        if args.widget == 'compact':
            print(widget.compact_bar(show_details=True))
        elif args.widget == 'mini':
            print(widget.mini_dashboard())
        elif args.widget == 'inline':
            print(widget.inline_bar())
        elif args.widget == 'sparkline':
            print(widget.sparkline())
        elif args.widget == 'circle':
            print(widget.percentage_circle("large"))
        elif args.widget == 'badges':
            print(widget.status_badges())
        elif args.widget == 'grid':
            print(widget.category_grid())
        elif args.widget == 'all':
            widget.display_all_formats()

    # Handle notifications
    if args.notify:
        notifier = ProgressNotifier()
        notifier.display_notifications()
        summary = notifier.get_progress_summary()
        print(f"\n📊 Current: {summary['current_progress']:.1f}%")
        if summary['next_milestone']:
            print(f"🎯 Next Milestone: {summary['next_milestone']}% ({summary['progress_to_next']:.1f}% away)")

    # Handle history
    if args.history:
        ph = ProgressHistory()
        ph.display_trend()

    # Handle exports
    if args.export:
        pb = ProgressBar()
        if args.export == 'json':
            path = pb.export_json()
            print(f"✅ Exported to: {path}")
        elif args.export == 'csv':
            path = pb.export_csv()
            print(f"✅ Exported to: {path}")
        elif args.export == 'all':
            json_path = pb.export_json()
            csv_path = pb.export_csv()
            print(f"✅ JSON exported to: {json_path}")
            print(f"✅ CSV exported to: {csv_path}")

    # Handle summary
    if args.summary:
        pb = ProgressBar()
        print(pb.get_summary())
        widget = ProgressWidget()
        print(widget.compact_bar(show_details=True))

    # Handle record
    if args.record:
        ph = ProgressHistory()
        count = ph.record_current()
        print(f"✅ Recorded progress snapshot #{count}")

def show_default_dashboard():
    """Show default progress dashboard."""
    pb = ProgressBar()
    widget = ProgressWidget()

    print("\n" + "=" * 80)
    print(" " * 25 + "📊 PROGRESS DASHBOARD" + " " * 25)
    print("=" * 80 + "\n")

    # Overall progress
    overall = pb.get_overall_progress()
    counts = pb.get_status_counts()

    print("Overall Progress:")
    print(f"  {widget.sparkline(width=50)}")
    print()

    print("Status:")
    print(f"  ✅ Complete: {counts['complete']:2d}  ⚠️  In Progress: {counts['in_progress']:2d}  ❌ Not Started: {counts['not_started']:2d}")
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

    for i, (name, cat) in enumerate(sorted_cats[:5], 1):
        status_emoji = {
            'complete': '✅',
            'in_progress': '⚠️',
            'templates_ready': '📝',
            'not_started': '❌'
        }.get(cat['status'], '❓')

        bar = pb.draw_bar(cat['progress'], width=30, style='simple')
        print(f"  {i}. {status_emoji} {name:<30s} {bar}")

    print()
    print("=" * 80)
    print("\n💡 Use --help to see all available options")

def show_all_features():
    """Show all progress bar features."""
    print("\n" + "=" * 80)
    print(" " * 15 + "🎨 COMPLETE PROGRESS BAR SYSTEM - ALL FEATURES" + " " * 15)
    print("=" * 80 + "\n")

    # Widget formats
    print("1. WIDGET FORMATS:")
    print("-" * 80)
    widget = ProgressWidget()
    widget.display_all_formats()

    # Notifications
    print("\n2. NOTIFICATIONS:")
    print("-" * 80)
    notifier = ProgressNotifier()
    notifier.display_notifications()

    # History
    print("\n3. HISTORY & TRENDS:")
    print("-" * 80)
    ph = ProgressHistory()
    ph.display_trend()

    # Summary
    print("\n4. SUMMARY:")
    print("-" * 80)
    pb = ProgressBar()
    print(pb.get_summary())

    print("\n" + "=" * 80)
    print("✅ All features displayed above")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
