#!/usr/bin/env python3
"""
Progress Estimator
Estimates completion time based on historical progress data.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, timedelta

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar

OUTPUT_DIR = Path(__file__).parent.parent.parent / "outputs" / "reports"
HISTORY_FILE = OUTPUT_DIR / "progress_history.json"

class ProgressEstimator:
    """Estimate completion time based on progress rate."""

    def __init__(self):
        self.pb = ProgressBar()
        self.history_file = HISTORY_FILE

    def get_progress_rate(self, days=7):
        """Calculate progress rate per day."""
        if not self.history_file.exists():
            return None

        with open(self.history_file, 'r') as f:
            history = json.load(f)

        if len(history) < 2:
            return None

        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            h for h in history
            if datetime.fromisoformat(h['timestamp']) >= cutoff
        ]

        if len(recent) < 2:
            return None

        first = recent[0]['overall_progress']
        last = recent[-1]['overall_progress']
        first_time = datetime.fromisoformat(recent[0]['timestamp'])
        last_time = datetime.fromisoformat(recent[-1]['timestamp'])

        time_diff = (last_time - first_time).total_seconds() / 86400  # days
        progress_diff = last - first

        if time_diff == 0:
            return None

        rate_per_day = progress_diff / time_diff
        return {
            'rate_per_day': rate_per_day,
            'period_days': time_diff,
            'progress_change': progress_diff,
            'data_points': len(recent)
        }

    def estimate_completion(self):
        """Estimate when 100% will be reached."""
        current = self.pb.get_overall_progress()
        rate_info = self.get_progress_rate()

        if not rate_info or rate_info['rate_per_day'] <= 0:
            return None

        remaining = 100 - current
        days_needed = remaining / rate_info['rate_per_day']
        completion_date = datetime.now() + timedelta(days=days_needed)

        return {
            'current_progress': current,
            'remaining': remaining,
            'rate_per_day': rate_info['rate_per_day'],
            'days_needed': days_needed,
            'completion_date': completion_date,
            'completion_date_str': completion_date.strftime('%Y-%m-%d'),
            'confidence': 'high' if rate_info['data_points'] >= 5 else 'medium'
        }

    def display_estimate(self):
        """Display completion estimate."""
        estimate = self.estimate_completion()
        rate_info = self.get_progress_rate()

        print("\n" + "=" * 80)
        print(" " * 25 + "⏱️  COMPLETION ESTIMATE" + " " * 25)
        print("=" * 80 + "\n")

        if estimate:
            print(f"Current Progress: {estimate['current_progress']:.1f}%")
            print(f"Remaining: {estimate['remaining']:.1f}%")
            print()

            if rate_info:
                print(f"Progress Rate: {rate_info['rate_per_day']:.2f}% per day")
                print(f"Based on: {rate_info['data_points']} data points over {rate_info['period_days']:.1f} days")
                print()

            print(f"Estimated Days Remaining: {estimate['days_needed']:.1f} days")
            print(f"Estimated Completion Date: {estimate['completion_date_str']}")
            print(f"Confidence: {estimate['confidence']}")

            # Visual timeline
            print()
            print("Timeline:")
            today = datetime.now()
            completion = estimate['completion_date']
            days_total = (completion - today).days

            if days_total > 0:
                weeks = days_total / 7
                print(f"  Today: {today.strftime('%Y-%m-%d')}")
                print(f"  → Estimated completion in {days_total:.0f} days ({weeks:.1f} weeks)")
                print(f"  → Target date: {completion.strftime('%Y-%m-%d')}")
        else:
            print("Not enough historical data to estimate completion time.")
            print("Run progress_with_history.py multiple times to build history.")
            print()
            print("Current Progress:", self.pb.get_overall_progress(), "%")
            print("Remaining:", 100 - self.pb.get_overall_progress(), "%")

        print()
        print("=" * 80 + "\n")

if __name__ == "__main__":
    estimator = ProgressEstimator()
    estimator.display_estimate()
