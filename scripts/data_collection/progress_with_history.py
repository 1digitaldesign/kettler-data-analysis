#!/usr/bin/env python3
"""
Progress Bar with Historical Tracking
Tracks progress over time and shows trends.
"""

import json
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar

OUTPUT_DIR = Path(__file__).parent.parent.parent / "outputs" / "reports"
HISTORY_FILE = OUTPUT_DIR / "progress_history.json"

class ProgressHistory:
    """Track progress history over time."""

    def __init__(self):
        self.pb = ProgressBar()
        self.history_file = HISTORY_FILE
        self.history = self._load_history()

    def _load_history(self):
        """Load historical progress data."""
        if self.history_file.exists():
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return []

    def _save_history(self):
        """Save current progress to history."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        entry = {
            'timestamp': datetime.now().isoformat(),
            'overall_progress': self.pb.get_overall_progress(),
            'status_counts': self.pb.get_status_counts(),
            'categories': {}
        }

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

        for key, name in category_names.items():
            entry['categories'][name] = {
                'progress': self.pb.stats[key]['progress'],
                'status': self.pb.stats[key]['status']
            }

        self.history.append(entry)

        # Keep only last 100 entries
        if len(self.history) > 100:
            self.history = self.history[-100:]

        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=2)

    def record_current(self):
        """Record current progress snapshot."""
        self.pb = ProgressBar()  # Refresh stats
        self._save_history()
        return len(self.history)

    def get_trend(self, days=7):
        """Get progress trend over specified days."""
        if not self.history:
            return None

        cutoff = datetime.now() - timedelta(days=days)
        recent = [
            h for h in self.history
            if datetime.fromisoformat(h['timestamp']) >= cutoff
        ]

        if len(recent) < 2:
            return None

        first = recent[0]['overall_progress']
        last = recent[-1]['overall_progress']
        change = last - first

        return {
            'period_days': days,
            'first_progress': first,
            'last_progress': last,
            'change': change,
            'change_percent': (change / first * 100) if first > 0 else 0,
            'entries': len(recent)
        }

    def display_trend(self):
        """Display progress trend visualization."""
        trend = self.get_trend(7)
        current = self.pb.get_overall_progress()

        print("\n" + "=" * 80)
        print(" " * 25 + "📈 PROGRESS TREND ANALYSIS" + " " * 25)
        print("=" * 80)
        print()

        if trend:
            print(f"Last 7 Days Trend:")
            print(f"  Starting Progress: {trend['first_progress']:.1f}%")
            print(f"  Current Progress:  {trend['last_progress']:.1f}%")
            print(f"  Change:            {trend['change']:+.1f}% ({trend['change_percent']:+.1f}%)")
            print(f"  Data Points:      {trend['entries']} snapshots")
            print()

            # Visual trend
            if trend['change'] > 0:
                print("  Trend: 📈 Improving")
                bar = self.pb.draw_bar(abs(trend['change_percent']), width=30, style='simple')
                print(f"  Growth: {bar}")
            elif trend['change'] < 0:
                print("  Trend: 📉 Declining")
            else:
                print("  Trend: ➡️  Stable")
        else:
            print("Not enough historical data yet.")
            print("Run this script multiple times to build history.")

        print()
        print(f"Current Overall Progress: {self.pb.draw_bar(current)}")
        print()

        # Show recent history
        if self.history:
            print("Recent History (Last 5 entries):")
            print("-" * 80)
            for entry in self.history[-5:]:
                dt = datetime.fromisoformat(entry['timestamp'])
                print(f"  {dt.strftime('%Y-%m-%d %H:%M:%S')}: {entry['overall_progress']:.1f}%")

        print("=" * 80)
        print()

if __name__ == "__main__":
    ph = ProgressHistory()

    # Record current progress
    count = ph.record_current()
    print(f"✅ Recorded progress snapshot #{count}")

    # Display trend
    ph.display_trend()
