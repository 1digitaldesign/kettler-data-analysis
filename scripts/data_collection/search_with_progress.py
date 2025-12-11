#!/usr/bin/env python3
"""
Search with Progress Bar Integration
Performs searches and updates progress bar in real-time.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_realtime import RealTimeProgress
from progress_integration import log_progress, get_progress_string

PROJECT_ROOT = Path(__file__).parent.parent.parent
LICENSE_DIR = PROJECT_ROOT / 'research/license_searches/data'

class SearchWithProgress:
    """Search operations with integrated progress tracking."""

    def __init__(self):
        self.pb = ProgressBar()
        self.rt = RealTimeProgress()
        self.initial_progress = self.pb.get_overall_progress()

    def show_search_start(self, search_type, total_items):
        """Show search start message."""
        print("\n" + "=" * 80)
        print(f"🔍 Starting {search_type}")
        print("=" * 80)
        print(f"Total items to search: {total_items}")
        print(f"Initial progress: {self.initial_progress:.1f}%")
        print()
        log_progress(f"Starting {search_type}")

    def show_search_progress(self, current, total, item_name=""):
        """Show progress during search."""
        progress_pct = (current / total * 100) if total > 0 else 0

        # Update progress bar
        message = f"Searching {item_name}" if item_name else f"Item {current}/{total}"
        self.rt.show_update(message)

        # Show detailed progress every 5 items
        if current % 5 == 0 or current == total:
            print(f"\n  Progress: {current}/{total} ({progress_pct:.1f}%)")

    def show_search_complete(self, search_type, items_searched):
        """Show search completion."""
        final_progress = self.pb.get_overall_progress()
        progress_change = final_progress - self.initial_progress

        print("\n" + "=" * 80)
        print(f"✅ {search_type} Complete")
        print("=" * 80)
        print(f"Items searched: {items_searched}")
        print(f"Final progress: {final_progress:.1f}%")
        if progress_change > 0:
            print(f"Progress increase: +{progress_change:.1f}%")
        print()

        # Show updated progress bar
        print("Updated Progress:")
        print(get_progress_string('compact'))
        print()

        log_progress(f"Completed {search_type}")

    def simulate_search(self, search_type, items, delay=0.5):
        """Simulate a search operation with progress updates."""
        self.show_search_start(search_type, len(items))

        for i, item in enumerate(items, 1):
            # Simulate search work
            time.sleep(delay)

            # Show progress
            self.show_search_progress(i, len(items), item)

            # Refresh progress bar (in real scenario, this would update files)
            self.pb = ProgressBar()  # Refresh stats

        self.show_search_complete(search_type, len(items))

    def check_license_searches_status(self):
        """Check status of license searches."""
        if not LICENSE_DIR.exists():
            return {'total': 0, 'complete': 0, 'missing': []}

        total_states = 15
        complete_states = 0
        missing_searches = []

        for state_dir in LICENSE_DIR.iterdir():
            if state_dir.is_dir():
                finding_files = list(state_dir.glob('*_finding.json'))
                if len(finding_files) >= 15:
                    complete_states += 1
                else:
                    missing_count = 15 - len(finding_files)
                    missing_searches.append({
                        'state': state_dir.name,
                        'missing': missing_count,
                        'complete': len(finding_files)
                    })

        return {
            'total': total_states,
            'complete': complete_states,
            'missing': missing_searches,
            'progress': (complete_states / total_states * 100) if total_states > 0 else 0
        }

def main():
    """Main search with progress."""
    swp = SearchWithProgress()

    print("\n" + "=" * 80)
    print(" " * 20 + "🔍 SEARCH WITH PROGRESS BAR" + " " * 20)
    print("=" * 80)
    print()

    # Show current status
    print("Current Status:")
    print(get_progress_string('compact'))
    print()

    # Check license search status
    license_status = swp.check_license_searches_status()

    print("License Search Status:")
    print(f"  Complete states: {license_status['complete']}/{license_status['total']}")
    print(f"  Progress: {license_status['progress']:.1f}%")

    if license_status['missing']:
        print("\n  Missing searches:")
        for state_info in license_status['missing']:
            print(f"    - {state_info['state']}: {state_info['complete']}/15 complete "
                  f"({state_info['missing']} missing)")

    print()
    print("=" * 80)
    print("\n💡 This script demonstrates search operations with progress tracking.")
    print("   In actual use, searches would update files and progress would update automatically.")
    print()

if __name__ == "__main__":
    main()
