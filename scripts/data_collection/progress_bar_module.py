#!/usr/bin/env python3
"""
Progress Bar Module
Reusable progress bar functionality that can be imported into other scripts.
"""

from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(__file__).parent.parent.parent
RESEARCH_DIR = BASE_DIR / "research"
OUTPUT_DIR = BASE_DIR / "outputs" / "reports"

class ProgressBar:
    """Progress bar class for data collection tracking."""

    def __init__(self):
        self.stats = self._get_all_stats()
        self.categories = self._get_category_list()

    def _count_license_searches(self):
        """Count license search files."""
        license_dir = RESEARCH_DIR / "license_searches"
        if not license_dir.exists():
            return 0, 0, 0
        states = [d for d in license_dir.iterdir() if d.is_dir()]
        total_states = 15
        completed_states = len(states)
        total_files = sum(1 for f in license_dir.rglob("*.json") if f.is_file())
        return completed_states, total_states, total_files

    def _count_company_registrations(self):
        """Count company registration files."""
        reg_dir = RESEARCH_DIR / "company_registrations"
        if not reg_dir.exists():
            return 0, 12, 0
        files = list(reg_dir.rglob("*.json"))
        complete = len([f for f in files if f.stat().st_size > 100])
        templates = len([f for f in files if f.stat().st_size <= 100])
        return complete, 12, templates

    def _count_employee_roles(self):
        """Count employee role files."""
        emp_dir = RESEARCH_DIR / "employees"
        if not emp_dir.exists():
            return 0, 2
        files = list(emp_dir.glob("*.json"))
        return len(files), 2

    def _count_template_files(self, category_dir, expected_templates):
        """Count template files for a category."""
        if not category_dir.exists():
            return 0, expected_templates
        files = list(category_dir.rglob("*.json"))
        templates = len([f for f in files if f.stat().st_size <= 500])
        return templates, expected_templates

    def _get_all_stats(self):
        """Get statistics for all categories."""
        stats = {}

        completed_states, total_states, total_files = self._count_license_searches()
        stats['license_searches'] = {
            'completed': completed_states,
            'total': total_states,
            'files': total_files,
            'progress': int((completed_states / total_states) * 100) if total_states > 0 else 0,
            'status': 'complete' if completed_states == total_states else 'in_progress'
        }

        complete, total, templates = self._count_company_registrations()
        stats['company_registrations'] = {
            'completed': complete,
            'total': total,
            'templates': templates,
            'progress': int((complete / total) * 100) if total > 0 else 0,
            'status': 'complete' if complete == total else ('templates_ready' if templates > 0 else 'not_started')
        }

        emp_files, emp_total = self._count_employee_roles()
        stats['employee_roles'] = {
            'completed': emp_files,
            'total': emp_total,
            'progress': int((emp_files / emp_total) * 100) if emp_total > 0 else 0,
            'status': 'complete' if emp_files == emp_total else 'in_progress'
        }

        template_categories = {
            'property_contracts': (RESEARCH_DIR / "contracts", 1),
            'regulatory_complaints': (RESEARCH_DIR / "complaints", 1),
            'financial_records': (RESEARCH_DIR / "financial", 1),
            'news_coverage': (RESEARCH_DIR / "news", 2),
            'fair_housing': (RESEARCH_DIR / "discrimination", 3),
            'professional_memberships': (RESEARCH_DIR / "professional", 2),
            'social_media': (RESEARCH_DIR / "online", 3),
        }

        for key, (dir_path, expected) in template_categories.items():
            templates, total_templates = self._count_template_files(dir_path, expected)
            stats[key] = {
                'templates': templates,
                'total_templates': total_templates,
                'progress': int((templates / total_templates) * 100) if total_templates > 0 else 0,
                'status': 'templates_ready' if templates > 0 else 'not_started'
            }

        return stats

    def _get_category_list(self):
        """Get list of all categories."""
        return [
            self.stats['license_searches'],
            self.stats['company_registrations'],
            self.stats['employee_roles'],
            self.stats['property_contracts'],
            self.stats['regulatory_complaints'],
            self.stats['financial_records'],
            self.stats['news_coverage'],
            self.stats['fair_housing'],
            self.stats['professional_memberships'],
            self.stats['social_media'],
        ]

    def get_overall_progress(self):
        """Get overall progress percentage."""
        return sum(cat['progress'] for cat in self.categories) / len(self.categories)

    def get_status_counts(self):
        """Get counts by status."""
        complete = sum(1 for cat in self.categories if cat['status'] == 'complete')
        in_progress = sum(1 for cat in self.categories if cat['status'] in ['in_progress', 'templates_ready'])
        not_started = sum(1 for cat in self.categories if cat['status'] == 'not_started')
        return {'complete': complete, 'in_progress': in_progress, 'not_started': not_started}

    def draw_bar(self, progress, width=50, style='enhanced'):
        """Draw a progress bar."""
        filled = int((progress / 100) * width)
        empty = width - filled

        if style == 'enhanced':
            if progress == 100:
                bar = '█' * filled
            elif progress >= 75:
                bar = '█' * (filled - 1) + '▉' + '░' * empty
            elif progress >= 50:
                bar = '█' * (filled - 1) + '▊' + '░' * empty
            elif progress >= 25:
                bar = '█' * (filled - 1) + '▋' + '░' * empty
            else:
                bar = '█' * filled + '░' * empty
        else:  # simple
            bar = '█' * filled + '░' * empty

        return f"{bar} {progress:.1f}%"

    def export_json(self, filepath=None):
        """Export progress data to JSON."""
        if filepath is None:
            filepath = OUTPUT_DIR / "progress_data.json"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        data = {
            'timestamp': datetime.now().isoformat(),
            'overall_progress': self.get_overall_progress(),
            'status_counts': self.get_status_counts(),
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
            data['categories'][name] = self.stats[key]

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

        return filepath

    def export_csv(self, filepath=None):
        """Export progress data to CSV."""
        if filepath is None:
            filepath = OUTPUT_DIR / "progress_data.csv"

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

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

        with open(filepath, 'w') as f:
            f.write("Category,Progress,Status,Details\n")
            for key, name in category_names.items():
                cat = self.stats[key]
                if key == 'license_searches':
                    details = f"{cat['completed']}/{cat['total']} states, {cat['files']} files"
                elif key == 'company_registrations':
                    details = f"{cat['completed']}/{cat['total']} complete"
                elif key == 'employee_roles':
                    details = f"{cat['completed']}/{cat['total']} files"
                else:
                    details = f"{cat['templates']}/{cat['total_templates']} templates"

                f.write(f"{name},{cat['progress']},{cat['status']},{details}\n")

        return filepath

    def get_summary(self):
        """Get a text summary of progress."""
        overall = self.get_overall_progress()
        counts = self.get_status_counts()

        return f"""Progress Summary
================
Overall Progress: {overall:.1f}%
Complete: {counts['complete']} categories
In Progress: {counts['in_progress']} categories
Not Started: {counts['not_started']} categories
"""

if __name__ == "__main__":
    # Example usage
    pb = ProgressBar()
    print(pb.get_summary())
    print(f"Overall Progress Bar: {pb.draw_bar(pb.get_overall_progress())}")
    print(f"\nJSON export: {pb.export_json()}")
    print(f"CSV export: {pb.export_csv()}")
