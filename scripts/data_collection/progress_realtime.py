#!/usr/bin/env python3
"""
Real-time Progress Bar
Shows progress updates during long-running operations.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar
from progress_widget import ProgressWidget

class RealTimeProgress:
    """Real-time progress bar for operations."""

    def __init__(self):
        self.pb = ProgressBar()
        self.widget = ProgressWidget()
        self.last_progress = None

    def show_update(self, message="", clear_line=True):
        """Show progress update."""
        current = self.pb.get_overall_progress()

        if clear_line:
            print("\r", end="", flush=True)

        progress_bar = self.widget.sparkline(width=40)
        timestamp = datetime.now().strftime('%H:%M:%S')

        if message:
            output = f"[{timestamp}] {message} | {progress_bar}"
        else:
            output = f"[{timestamp}] {progress_bar}"

        print(output, end="", flush=True)

        # Check if progress changed
        if self.last_progress is not None and current != self.last_progress:
            change = current - self.last_progress
            if change > 0:
                print(f" (+{change:.1f}%)", end="", flush=True)

        self.last_progress = current

    def monitor(self, interval=2, duration=None):
        """Monitor progress with updates."""
        start_time = time.time()

        print("Monitoring progress... (Press Ctrl+C to stop)")
        print()

        try:
            while True:
                self.show_update("Progress")
                time.sleep(interval)

                if duration and (time.time() - start_time) >= duration:
                    break
        except KeyboardInterrupt:
            print("\n\nMonitoring stopped.")

        print()  # New line after monitoring

    def show_with_message(self, message):
        """Show progress with custom message."""
        self.show_update(message, clear_line=False)
        print()  # New line

if __name__ == "__main__":
    rt = RealTimeProgress()

    print("Real-time Progress Monitor")
    print("=" * 80)
    print()

    # Show initial progress
    rt.show_with_message("Initial status")

    # Monitor for 10 seconds as demo
    print("Monitoring for 10 seconds...")
    rt.monitor(interval=2, duration=10)

    # Final status
    pb = ProgressBar()
    counts = pb.get_status_counts()
    print(f"Final: {pb.get_overall_progress():.1f}% | "
          f"✅{counts['complete']} ⚠️{counts['in_progress']} ❌{counts['not_started']}")
