#!/usr/bin/env python3
"""
Run All with Progress
Master script that runs all operations with integrated progress tracking.
"""

import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_integration import print_progress, log_progress
from search_dashboard import display_search_dashboard
from automated_search_workflow import AutomatedSearchWorkflow

def main():
    """Run all operations with progress tracking."""
    print("\n" + "=" * 80)
    print(" " * 20 + "🚀 RUN ALL WITH PROGRESS TRACKING" + " " * 20)
    print("=" * 80)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Show initial progress
    print("📊 Initial Progress:")
    print_progress('compact')
    print()

    # Show search dashboard
    print("=" * 80)
    display_search_dashboard()

    # Run automated workflow
    print("=" * 80)
    print("Running Automated Workflow...")
    print("=" * 80)
    workflow = AutomatedSearchWorkflow()
    workflow.run_automated_workflow()

    # Final summary
    print("\n" + "=" * 80)
    print(" " * 25 + "✅ ALL OPERATIONS COMPLETE" + " " * 25)
    print("=" * 80)
    print()
    print("Final Progress:")
    print_progress('compact')
    print()
    print("=" * 80)
    print()

    log_progress("All operations completed")

if __name__ == "__main__":
    main()
