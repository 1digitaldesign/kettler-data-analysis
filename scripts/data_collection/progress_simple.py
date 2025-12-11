#!/usr/bin/env python3
"""
Simple Progress Bar
One-line progress bar for quick checks and script integration.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_widget import ProgressWidget

def show_simple():
    """Show simple one-line progress."""
    pb = ProgressBar()
    widget = ProgressWidget()

    overall = pb.get_overall_progress()
    counts = pb.get_status_counts()

    # Compact format
    bar = widget.sparkline(width=30)
    print(f"{bar} | ✅{counts['complete']} ⚠️{counts['in_progress']} ❌{counts['not_started']}")

def show_compact():
    """Show compact progress bar."""
    widget = ProgressWidget()
    print(widget.compact_bar(show_details=True))

def show_sparkline():
    """Show sparkline only."""
    widget = ProgressWidget()
    print(widget.sparkline())

def show_badges():
    """Show status badges only."""
    widget = ProgressWidget()
    print(widget.status_badges())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == 'compact':
            show_compact()
        elif mode == 'sparkline':
            show_sparkline()
        elif mode == 'badges':
            show_badges()
        else:
            show_simple()
    else:
        show_simple()
