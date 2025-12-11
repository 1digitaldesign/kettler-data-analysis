#!/usr/bin/env python3
"""
Advanced Progress Bar Widget
A sophisticated, embeddable progress bar widget with multiple display modes.
"""

import sys
from pathlib import Path
from datetime import datetime
import time

sys.path.insert(0, str(Path(__file__).parent))
from progress_bar_module import ProgressBar

class ProgressWidget:
    """Advanced progress bar widget with multiple display modes."""

    def __init__(self):
        self.pb = ProgressBar()
        self.width = 80

    def compact_bar(self, show_details=False):
        """Compact single-line progress bar."""
        overall = self.pb.get_overall_progress()
        counts = self.pb.get_status_counts()
        bar = self.pb.draw_bar(overall, width=40, style='enhanced')

        line = f"📊 Progress: {bar} | ✅{counts['complete']} ⚠️{counts['in_progress']} ❌{counts['not_started']}"

        if show_details:
            top_category = max(
                [(k, v) for k, v in self.pb.stats.items()],
                key=lambda x: x[1]['progress']
            )
            line += f" | Top: {top_category[1]['progress']:.0f}%"

        return line

    def mini_dashboard(self):
        """Mini dashboard format."""
        overall = self.pb.get_overall_progress()
        counts = self.pb.get_status_counts()

        lines = [
            "┌" + "─" * 78 + "┐",
            "│ " + "📊 PROGRESS WIDGET".center(75) + "│",
            "├" + "─" * 78 + "┤",
            f"│ Overall: {self.pb.draw_bar(overall, width=55, style='enhanced'):65s} │",
            "├" + "─" * 78 + "┤",
            f"│ Status: ✅ Complete: {counts['complete']:2d}  ⚠️  In Progress: {counts['in_progress']:2d}  ❌ Not Started: {counts['not_started']:2d}" + " " * 35 + "│",
            "└" + "─" * 78 + "┘"
        ]
        return "\n".join(lines)

    def inline_bar(self, label="Progress", width=50):
        """Inline progress bar for embedding in text."""
        overall = self.pb.get_overall_progress()
        bar = self.pb.draw_bar(overall, width=width, style='simple')
        return f"{label}: {bar}"

    def sparkline(self, width=20):
        """Create a sparkline-style progress visualization."""
        overall = self.pb.get_overall_progress()
        filled = int((overall / 100) * width)
        empty = width - filled

        # Use different characters for sparkline effect
        chars = ['▁', '▂', '▃', '▄', '▅', '▆', '▇', '█']
        bar_parts = []

        for i in range(width):
            if i < filled:
                # Use full block for filled portion
                bar_parts.append('█')
            else:
                # Use lighter character for empty
                bar_parts.append('░')

        return ''.join(bar_parts) + f" {overall:.1f}%"

    def category_grid(self, cols=2):
        """Display categories in a grid format."""
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

        items = []
        for key, name in category_names.items():
            cat = self.pb.stats[key]
            status_emoji = {
                'complete': '✅',
                'in_progress': '⚠️',
                'templates_ready': '📝',
                'not_started': '❌'
            }.get(cat['status'], '❓')

            bar = self.pb.draw_bar(cat['progress'], width=20, style='simple')
            items.append(f"{status_emoji} {name:<25s} {bar}")

        # Arrange in grid
        lines = []
        for i in range(0, len(items), cols):
            row_items = items[i:i+cols]
            # Pad row if needed
            while len(row_items) < cols:
                row_items.append("")
            lines.append("  ".join(row_items))

        return "\n".join(lines)

    def percentage_circle(self, size="medium"):
        """ASCII art percentage circle."""
        overall = self.pb.get_overall_progress()

        if size == "small":
            return f"⭕ {overall:.1f}%"
        elif size == "large":
            # Create a larger visual representation
            filled = int(overall / 10)
            empty = 10 - filled
            circle = "●" * filled + "○" * empty
            return f"Progress: [{circle}] {overall:.1f}%"
        else:  # medium
            filled = int(overall / 5)
            empty = 20 - filled
            circle = "●" * filled + "○" * empty
            return f"[{circle}] {overall:.1f}%"

    def status_badges(self):
        """Create status badges."""
        counts = self.pb.get_status_counts()
        overall = self.pb.get_overall_progress()

        badges = [
            f"Overall: {overall:.1f}%",
            f"✅ {counts['complete']}",
            f"⚠️  {counts['in_progress']}",
            f"❌ {counts['not_started']}"
        ]

        return " | ".join(badges)

    def display_all_formats(self):
        """Display all widget formats for demonstration."""
        print("\n" + "=" * 80)
        print(" " * 20 + "🎨 PROGRESS BAR WIDGET - ALL FORMATS" + " " * 20)
        print("=" * 80 + "\n")

        print("1. COMPACT BAR:")
        print("   " + self.compact_bar(show_details=True))
        print()

        print("2. MINI DASHBOARD:")
        print(self.mini_dashboard())
        print()

        print("3. INLINE BAR:")
        print("   " + self.inline_bar("Data Collection", width=40))
        print()

        print("4. SPARKLINE:")
        print("   " + self.sparkline(width=30))
        print()

        print("5. PERCENTAGE CIRCLE:")
        print("   " + self.percentage_circle("large"))
        print()

        print("6. STATUS BADGES:")
        print("   " + self.status_badges())
        print()

        print("7. CATEGORY GRID:")
        print(self.category_grid(cols=2))
        print()

        print("=" * 80)
        print("\n💡 Use these widgets in your scripts by importing ProgressWidget")
        print("   Example: widget = ProgressWidget(); print(widget.compact_bar())")

if __name__ == "__main__":
    widget = ProgressWidget()
    widget.display_all_formats()
