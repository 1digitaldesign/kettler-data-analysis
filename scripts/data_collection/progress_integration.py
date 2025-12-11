#!/usr/bin/env python3
"""
Progress Bar Integration Helper
Provides easy integration functions for use in other scripts.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_widget import ProgressWidget

def get_progress_string(format='compact'):
    """
    Get progress as a string for easy integration.

    Formats:
    - 'compact': Compact bar with details
    - 'sparkline': Sparkline visualization
    - 'badges': Status badges
    - 'inline': Inline progress bar
    - 'percentage': Just percentage
    """
    widget = ProgressWidget()
    pb = ProgressBar()

    if format == 'compact':
        return widget.compact_bar(show_details=True)
    elif format == 'sparkline':
        return widget.sparkline()
    elif format == 'badges':
        return widget.status_badges()
    elif format == 'inline':
        return widget.inline_bar()
    elif format == 'percentage':
        return f"{pb.get_overall_progress():.1f}%"
    else:
        return widget.compact_bar()

def print_progress(format='compact'):
    """Print progress bar (for use in scripts)."""
    print(get_progress_string(format))

def get_progress_dict():
    """Get progress as dictionary for programmatic use."""
    pb = ProgressBar()
    return {
        'overall': pb.get_overall_progress(),
        'status_counts': pb.get_status_counts(),
        'categories': pb.stats
    }

def log_progress(message="Progress update"):
    """Log progress with timestamp and message."""
    from datetime import datetime
    pb = ProgressBar()
    widget = ProgressWidget()

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    progress_str = widget.compact_bar()

    print(f"[{timestamp}] {message}: {progress_str}")

if __name__ == "__main__":
    # Example usage
    print("Progress Integration Examples:")
    print("-" * 80)
    print()

    print("1. Compact format:")
    print_progress('compact')
    print()

    print("2. Sparkline format:")
    print_progress('sparkline')
    print()

    print("3. Badges format:")
    print_progress('badges')
    print()

    print("4. Percentage only:")
    print_progress('percentage')
    print()

    print("5. Dictionary format:")
    import json
    progress_dict = get_progress_dict()
    print(json.dumps({
        'overall': progress_dict['overall'],
        'status_counts': progress_dict['status_counts']
    }, indent=2))
    print()

    print("6. Logged progress:")
    log_progress("Current status")
