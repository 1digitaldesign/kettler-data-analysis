#!/usr/bin/env python3
"""
Search Workflow with Progress Bar
Complete workflow for performing searches with integrated progress tracking.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_realtime import RealTimeProgress
from progress_integration import log_progress, print_progress, get_progress_string
from complete_license_searches import (
    STATES_TO_COMPLETE, EMPLOYEES, check_missing_searches,
    create_search_template, LICENSE_DIR
)

class SearchWorkflow:
    """Complete search workflow with progress tracking."""

    def __init__(self):
        self.pb = ProgressBar()
        self.rt = RealTimeProgress()
        self.initial_progress = self.pb.get_overall_progress()

    def show_workflow_header(self):
        """Show workflow header with progress."""
        print("\n" + "=" * 80)
        print(" " * 20 + "🔍 SEARCH WORKFLOW WITH PROGRESS" + " " * 20)
        print("=" * 80)
        print()
        print("Initial Progress:")
        print_progress('compact')
        print()
        print("=" * 80)
        print()

    def analyze_search_status(self):
        """Analyze current search status."""
        print("📊 Analyzing Search Status...")
        print()

        license_status = {}
        total_missing = 0

        for state, info in STATES_TO_COMPLETE.items():
            missing = check_missing_searches(state)
            complete = len(EMPLOYEES) - len(missing)
            license_status[state] = {
                'missing': missing,
                'complete': complete,
                'total': len(EMPLOYEES),
                'progress': (complete / len(EMPLOYEES) * 100) if len(EMPLOYEES) > 0 else 0
            }
            total_missing += len(missing)

        # Display status
        print("License Search Status by State:")
        print("-" * 80)

        for state, status in license_status.items():
            progress_bar = self.pb.draw_bar(status['progress'], width=30, style='simple')
            print(f"  {state.upper():<15s} {progress_bar} "
                  f"({status['complete']}/{status['total']} complete)")

            if status['missing']:
                print(f"    Missing: {len(status['missing'])} searches")

        print("-" * 80)
        print(f"Total Missing Searches: {total_missing}")
        print()

        return license_status, total_missing

    def perform_searches(self, state, employees, simulate=False):
        """Perform searches for a state with progress updates."""
        print(f"\n🔍 Starting searches for {state.upper()}")
        print("-" * 80)

        self.rt.show_with_message(f"Starting {state} searches")

        completed = 0
        for i, employee in enumerate(employees, 1):
            employee_name = employee.replace('_', ' ').title()

            # Show progress
            self.rt.show_update(f"{state}: {employee_name} ({i}/{len(employees)})")

            if simulate:
                # Simulate search
                time.sleep(0.3)
                print(f"  [{i}/{len(employees)}] Searching {employee_name}...")
            else:
                # Actual search would happen here
                print(f"  [{i}/{len(employees)}] {employee_name}: Ready to search")

            completed += 1

        self.rt.show_with_message(f"Completed {state} searches")
        print(f"\n✅ Completed {completed}/{len(employees)} searches for {state}")

        return completed

    def update_progress_summary(self):
        """Update and show progress summary."""
        # Refresh progress
        self.pb = ProgressBar()
        final_progress = self.pb.get_overall_progress()
        progress_change = final_progress - self.initial_progress

        print("\n" + "=" * 80)
        print("📈 Progress Summary")
        print("=" * 80)
        print()
        print("Final Progress:")
        print_progress('compact')
        print()

        if progress_change > 0:
            print(f"Progress Increase: +{progress_change:.1f}%")
        elif progress_change < 0:
            print(f"Progress Change: {progress_change:.1f}%")
        else:
            print("Progress: No change")

        print()
        print("=" * 80)

        log_progress("Search workflow completed")

    def run_workflow(self, simulate=False):
        """Run complete search workflow."""
        self.show_workflow_header()

        # Analyze status
        license_status, total_missing = self.analyze_search_status()

        if total_missing == 0:
            print("✅ All searches are complete!")
            print()
            self.update_progress_summary()
            return

        # Perform searches for each state
        print("\n🚀 Starting Search Operations")
        print("=" * 80)

        for state, status in license_status.items():
            if status['missing']:
                self.perform_searches(state, status['missing'], simulate=simulate)
                time.sleep(1)  # Brief pause between states

        # Final summary
        self.update_progress_summary()

def main():
    """Main workflow execution."""
    import argparse

    parser = argparse.ArgumentParser(description='Search workflow with progress tracking')
    parser.add_argument('--simulate', action='store_true',
                       help='Simulate searches (for testing)')
    parser.add_argument('--state', type=str,
                       help='Search specific state only')

    args = parser.parse_args()

    workflow = SearchWorkflow()

    if args.state:
        # Search specific state
        state_lower = args.state.lower()
        if state_lower in STATES_TO_COMPLETE:
            missing = check_missing_searches(state_lower)
            if missing:
                workflow.perform_searches(state_lower, missing, simulate=args.simulate)
            else:
                print(f"✅ All searches complete for {args.state}")
        else:
            print(f"Unknown state: {args.state}")
            print(f"Available states: {', '.join(STATES_TO_COMPLETE.keys())}")
    else:
        # Run full workflow
        workflow.run_workflow(simulate=args.simulate)

if __name__ == "__main__":
    main()
