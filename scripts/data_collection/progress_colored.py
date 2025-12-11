#!/usr/bin/env python3
"""
Colored Progress Bar
Progress bar with ANSI color support for better visual distinction.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar

class ColoredProgressBar:
    """Progress bar with color support."""

    # ANSI color codes
    COLORS = {
        'reset': '\033[0m',
        'bold': '\033[1m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
    }

    def __init__(self):
        self.pb = ProgressBar()

    def colorize(self, text, color):
        """Add color to text."""
        if color in self.COLORS:
            return f"{self.COLORS[color]}{text}{self.COLORS['reset']}"
        return text

    def draw_colored_bar(self, progress, width=50):
        """Draw a colored progress bar."""
        filled = int((progress / 100) * width)
        empty = width - filled

        # Choose color based on progress
        if progress == 100:
            color = 'green'
            char = '█'
        elif progress >= 75:
            color = 'cyan'
            char = '█'
        elif progress >= 50:
            color = 'blue'
            char = '█'
        elif progress >= 25:
            color = 'yellow'
            char = '█'
        else:
            color = 'red'
            char = '█'

        filled_bar = self.colorize(char * filled, color)
        empty_bar = '░' * empty

        return f"{filled_bar}{empty_bar} {self.colorize(f'{progress:.1f}%', color)}"

    def display_colored_dashboard(self):
        """Display colored progress dashboard."""
        overall = self.pb.get_overall_progress()
        counts = self.pb.get_status_counts()

        print("\n" + self.colorize("=" * 80, 'bold'))
        print(self.colorize(" " * 25 + "🎨 COLORED PROGRESS DASHBOARD" + " " * 25, 'bold'))
        print(self.colorize("=" * 80, 'bold') + "\n")

        # Overall progress
        print("Overall Progress:")
        print(f"  {self.draw_colored_bar(overall, width=60)}")
        print()

        # Status counts with colors
        print("Status Breakdown:")
        print(f"  {self.colorize('✅ Complete:', 'green')} {counts['complete']:2d}  "
              f"{self.colorize('⚠️  In Progress:', 'yellow')} {counts['in_progress']:2d}  "
              f"{self.colorize('❌ Not Started:', 'red')} {counts['not_started']:2d}")
        print()

        # Categories with colors
        print("Category Progress:")
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
            progress = cat['progress']
            status = cat['status']

            # Status emoji and color
            if status == 'complete':
                emoji = '✅'
                status_color = 'green'
            elif status == 'in_progress':
                emoji = '⚠️'
                status_color = 'yellow'
            elif status == 'templates_ready':
                emoji = '📝'
                status_color = 'blue'
            else:
                emoji = '❌'
                status_color = 'red'

            bar = self.draw_colored_bar(progress, width=40)
            status_text = self.colorize(status.replace('_', ' ').title(), status_color)

            print(f"  {emoji} {self.colorize(name, 'bold'):<30s} {bar}  {status_text}")

        print()
        print(self.colorize("=" * 80, 'bold') + "\n")

    def get_colored_summary(self):
        """Get colored summary line."""
        overall = self.pb.get_overall_progress()
        counts = self.pb.get_status_counts()

        bar = self.draw_colored_bar(overall, width=40)

        complete_str = "✅" + str(counts['complete'])
        in_progress_str = "⚠️" + str(counts['in_progress'])
        not_started_str = "❌" + str(counts['not_started'])

        summary = (
            self.colorize('📊 Progress:', 'bold') + " " + bar + " | " +
            self.colorize(complete_str, 'green') + " " +
            self.colorize(in_progress_str, 'yellow') + " " +
            self.colorize(not_started_str, 'red')
        )

        return summary

if __name__ == "__main__":
    cpb = ColoredProgressBar()
    cpb.display_colored_dashboard()
    print("\nColored Summary:")
    print(cpb.get_colored_summary())
