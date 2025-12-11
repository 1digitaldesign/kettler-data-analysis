#!/usr/bin/env python3
"""
Progress Notifier
Sends progress updates and notifications when milestones are reached.
"""

import sys
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar

OUTPUT_DIR = Path(__file__).parent.parent.parent / "outputs" / "reports"
NOTIFICATIONS_FILE = OUTPUT_DIR / "progress_notifications.json"

class ProgressNotifier:
    """Notify about progress milestones and changes."""

    def __init__(self):
        self.pb = ProgressBar()
        self.notifications_file = NOTIFICATIONS_FILE
        self.milestones = [10, 25, 50, 75, 90, 100]

    def check_milestones(self):
        """Check if any milestones have been reached."""
        overall = self.pb.get_overall_progress()
        notifications = []

        for milestone in self.milestones:
            if overall >= milestone:
                # Check if we've already notified for this milestone
                if not self._already_notified(milestone):
                    notifications.append({
                        'type': 'milestone',
                        'milestone': milestone,
                        'progress': overall,
                        'timestamp': datetime.now().isoformat(),
                        'message': f"🎉 Milestone reached: {milestone}% complete!"
                    })
                    self._save_notification(milestone)

        return notifications

    def check_category_completions(self):
        """Check if any categories have been completed."""
        notifications = []
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
            cat = self.pb.stats[key]
            if cat['status'] == 'complete':
                if not self._category_notified(key):
                    notifications.append({
                        'type': 'category_complete',
                        'category': name,
                        'timestamp': datetime.now().isoformat(),
                        'message': f"✅ Category complete: {name}"
                    })
                    self._save_category_notification(key)

        return notifications

    def _already_notified(self, milestone):
        """Check if milestone was already notified."""
        if not self.notifications_file.exists():
            return False

        with open(self.notifications_file, 'r') as f:
            data = json.load(f)
            return milestone in data.get('milestones', [])

    def _category_notified(self, category_key):
        """Check if category completion was already notified."""
        if not self.notifications_file.exists():
            return False

        with open(self.notifications_file, 'r') as f:
            data = json.load(f)
            return category_key in data.get('categories_complete', [])

    def _save_notification(self, milestone):
        """Save milestone notification."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        if self.notifications_file.exists():
            with open(self.notifications_file, 'r') as f:
                data = json.load(f)
        else:
            data = {'milestones': [], 'categories_complete': []}

        if milestone not in data['milestones']:
            data['milestones'].append(milestone)

        with open(self.notifications_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _save_category_notification(self, category_key):
        """Save category completion notification."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        if self.notifications_file.exists():
            with open(self.notifications_file, 'r') as f:
                data = json.load(f)
        else:
            data = {'milestones': [], 'categories_complete': []}

        if category_key not in data['categories_complete']:
            data['categories_complete'].append(category_key)

        with open(self.notifications_file, 'w') as f:
            json.dump(data, f, indent=2)

    def display_notifications(self):
        """Display all current notifications."""
        milestone_notifs = self.check_milestones()
        category_notifs = self.check_category_completions()

        all_notifs = milestone_notifs + category_notifs

        if all_notifs:
            print("\n" + "=" * 80)
            print(" " * 25 + "🔔 PROGRESS NOTIFICATIONS" + " " * 25)
            print("=" * 80 + "\n")

            for notif in all_notifs:
                print(f"  {notif['message']}")
                print(f"    Time: {datetime.fromisoformat(notif['timestamp']).strftime('%Y-%m-%d %H:%M:%S')}")
                if 'progress' in notif:
                    print(f"    Progress: {notif['progress']:.1f}%")
                print()

            print("=" * 80 + "\n")
        else:
            print("\n✅ No new notifications - all milestones and completions already notified.\n")

        return all_notifs

    def get_progress_summary(self):
        """Get a summary of current progress."""
        overall = self.pb.get_overall_progress()
        counts = self.pb.get_status_counts()

        # Find next milestone
        next_milestone = None
        for milestone in self.milestones:
            if overall < milestone:
                next_milestone = milestone
                break

        summary = {
            'current_progress': overall,
            'status_counts': counts,
            'next_milestone': next_milestone,
            'progress_to_next': next_milestone - overall if next_milestone else None
        }

        return summary

if __name__ == "__main__":
    notifier = ProgressNotifier()

    # Display notifications
    notifications = notifier.display_notifications()

    # Show summary
    summary = notifier.get_progress_summary()
    print("📊 Progress Summary:")
    print(f"   Current: {summary['current_progress']:.1f}%")
    if summary['next_milestone']:
        print(f"   Next Milestone: {summary['next_milestone']}% ({summary['progress_to_next']:.1f}% away)")
    print(f"   Complete: {summary['status_counts']['complete']} | "
          f"In Progress: {summary['status_counts']['in_progress']} | "
          f"Not Started: {summary['status_counts']['not_started']}")
