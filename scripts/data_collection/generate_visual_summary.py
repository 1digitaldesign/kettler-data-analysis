#!/usr/bin/env python3
"""
Generate a concise visual progress summary in markdown format.
Creates a clean, readable progress report with visual progress bars.
"""

import json
import os
from pathlib import Path
from datetime import datetime

# Base paths
BASE_DIR = Path(__file__).parent.parent.parent
RESEARCH_DIR = BASE_DIR / "research"
OUTPUT_DIR = BASE_DIR / "outputs" / "reports"
REPORTS_DIR = RESEARCH_DIR / "reports"

def count_license_searches():
    """Count license search files."""
    license_dir = RESEARCH_DIR / "license_searches"
    if not license_dir.exists():
        return 0, 0, 0

    # Count state directories
    states = [d for d in license_dir.iterdir() if d.is_dir()]
    total_states = 15  # Expected states
    completed_states = len(states)

    # Count total files
    total_files = sum(1 for f in license_dir.rglob("*.json") if f.is_file())

    return completed_states, total_states, total_files

def count_company_registrations():
    """Count company registration files."""
    reg_dir = RESEARCH_DIR / "company_registrations"
    if not reg_dir.exists():
        return 0, 12, 0

    # Count JSON files
    files = list(reg_dir.rglob("*.json"))
    complete = len([f for f in files if f.stat().st_size > 100])  # Non-empty files
    templates = len([f for f in files if f.stat().st_size <= 100])  # Template files

    return complete, 12, templates

def count_employee_roles():
    """Count employee role files."""
    emp_dir = RESEARCH_DIR / "employees"
    if not emp_dir.exists():
        return 0, 2

    files = list(emp_dir.glob("*.json"))
    return len(files), 2

def count_template_files(category_dir, expected_templates):
    """Count template files for a category."""
    if not category_dir.exists():
        return 0, expected_templates

    files = list(category_dir.rglob("*.json"))
    templates = len([f for f in files if f.stat().st_size <= 500])  # Template files
    return templates, expected_templates

def get_all_stats():
    """Get statistics for all categories."""
    stats = {}

    # License Searches
    completed_states, total_states, total_files = count_license_searches()
    stats['license_searches'] = {
        'completed': completed_states,
        'total': total_states,
        'files': total_files,
        'progress': int((completed_states / total_states) * 100) if total_states > 0 else 0,
        'status': 'complete' if completed_states == total_states else 'in_progress'
    }

    # Company Registrations
    complete, total, templates = count_company_registrations()
    stats['company_registrations'] = {
        'completed': complete,
        'total': total,
        'templates': templates,
        'progress': int((complete / total) * 100) if total > 0 else 0,
        'status': 'complete' if complete == total else ('templates_ready' if templates > 0 else 'not_started')
    }

    # Employee Roles
    emp_files, emp_total = count_employee_roles()
    stats['employee_roles'] = {
        'completed': emp_files,
        'total': emp_total,
        'progress': int((emp_files / emp_total) * 100) if emp_total > 0 else 0,
        'status': 'complete' if emp_files == emp_total else 'in_progress'
    }

    # Template categories
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
        templates, total_templates = count_template_files(dir_path, expected)
        stats[key] = {
            'templates': templates,
            'total_templates': total_templates,
            'progress': int((templates / total_templates) * 100) if total_templates > 0 else 0,
            'status': 'templates_ready' if templates > 0 else 'not_started'
        }

    return stats

def draw_progress_bar(progress, width=30):
    """Draw a text-based progress bar."""
    filled = int((progress / 100) * width)
    empty = width - filled
    return '█' * filled + '░' * empty

def generate_visual_summary():
    """Generate concise visual progress summary."""
    stats = get_all_stats()

    # Calculate overall progress
    categories = [
        stats['license_searches'],
        stats['company_registrations'],
        stats['employee_roles'],
        stats['property_contracts'],
        stats['regulatory_complaints'],
        stats['financial_records'],
        stats['news_coverage'],
        stats['fair_housing'],
        stats['professional_memberships'],
        stats['social_media'],
    ]

    overall_progress = sum(cat['progress'] for cat in categories) / len(categories)
    complete_count = sum(1 for cat in categories if cat['status'] == 'complete')
    in_progress_count = sum(1 for cat in categories if cat['status'] in ['in_progress', 'templates_ready'])
    not_started_count = sum(1 for cat in categories if cat['status'] == 'not_started')

    # Category names mapping
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

    # Generate markdown
    markdown = f"""# 📊 Visual Progress Summary

**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## 🎯 Overall Progress

```
{draw_progress_bar(overall_progress)} {overall_progress:.1f}%
```

**Status Breakdown:**
- ✅ **Complete:** {complete_count} categories
- ⚠️ **In Progress:** {in_progress_count} categories
- ❌ **Not Started:** {not_started_count} categories

---

## 📋 Category Details

"""

    # Add each category
    for i, (key, name) in enumerate(category_names.items(), 1):
        cat_stats = stats[key]
        progress = cat_stats['progress']
        status = cat_stats['status']

        # Status emoji
        if status == 'complete':
            status_emoji = '✅'
            status_text = 'Complete'
        elif status == 'in_progress':
            status_emoji = '⚠️'
            status_text = 'In Progress'
        elif status == 'templates_ready':
            status_emoji = '⚠️'
            status_text = 'Templates Ready'
        else:
            status_emoji = '❌'
            status_text = 'Not Started'

        # Details
        if key == 'license_searches':
            details = f"{cat_stats['completed']}/{cat_stats['total']} states | {cat_stats['files']} files"
        elif key == 'company_registrations':
            details = f"{cat_stats['completed']}/{cat_stats['total']} complete | {cat_stats['templates']} templates"
        elif key == 'employee_roles':
            details = f"{cat_stats['completed']}/{cat_stats['total']} files"
        else:
            details = f"{cat_stats['templates']}/{cat_stats['total_templates']} templates"

        markdown += f"""### {i}. {name} {status_emoji} {status_text}

```
{draw_progress_bar(progress)} {progress}%
```

**Details:** {details}

"""

    markdown += f"""---

## 📈 Quick Stats

- **Overall Progress:** {overall_progress:.1f}%
- **Categories Complete:** {complete_count}/10
- **Categories In Progress:** {in_progress_count}/10
- **Categories Not Started:** {not_started_count}/10

---

## 🔗 Related Reports

- [Detailed Progress Report](DATA_COLLECTION_PROGRESS.md) - Full task breakdown
- [HTML Dashboard](../../outputs/reports/progress_dashboard.html) - Interactive visual dashboard

---

*Generated automatically by `scripts/data_collection/generate_visual_summary.py`*
"""

    # Ensure reports directory exists
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Write markdown file
    summary_path = REPORTS_DIR / "VISUAL_PROGRESS_SUMMARY.md"
    summary_path.write_text(markdown)

    print(f"✅ Visual progress summary generated: {summary_path}")
    print(f"   Overall progress: {overall_progress:.1f}%")
    print(f"   Complete: {complete_count} | In Progress: {in_progress_count} | Not Started: {not_started_count}")

    return summary_path

if __name__ == "__main__":
    generate_visual_summary()
