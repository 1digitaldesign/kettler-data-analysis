#!/usr/bin/env python3
"""
Update Progress from Completed Task Files

Scans for completed task files and updates progress tracking.
"""

import json
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
PROGRESS_FILE = PROJECT_ROOT / 'outputs' / 'reports' / 'progress_data.json'

# Task definitions matching data_collection_automation.py
TASKS = {
    'license_searches': {
        'name': 'License Searches',
        'tasks': [
            {'id': 'md_complete', 'name': 'Maryland searches', 'file_pattern': 'research/license_searches/data/maryland/*_finding.json'},
            {'id': 'ct_complete', 'name': 'Connecticut searches', 'file_pattern': 'research/license_searches/data/connecticut/*_finding.json'},
        ]
    },
    'company_registrations': {
        'name': 'Company Registrations',
        'tasks': [
            {'id': 'kettler_dc', 'name': 'Kettler Management Inc - DC', 'file_pattern': 'research/company_registrations/dc/*_registration.json'},
            {'id': 'kettler_md', 'name': 'Kettler Management Inc - MD', 'file_pattern': 'research/company_registrations/md/*_registration.json'},
            {'id': 'kettler_va', 'name': 'Kettler Management Inc - VA', 'file_pattern': 'research/company_registrations/va/*_registration.json'},
            {'id': 'kettler_nj', 'name': 'Kettler Management Inc - NJ', 'file_pattern': 'research/company_registrations/nj/*_registration.json'},
            {'id': 'kettler_ny', 'name': 'Kettler Management Inc - NY', 'file_pattern': 'research/company_registrations/ny/*_registration.json'},
            {'id': 'skidmore_companies', 'name': 'Skidmore-affiliated companies', 'file_pattern': 'research/company_registrations/**/*_registration.json'},
        ]
    },
    'property_contracts': {
        'name': 'Property Management Contracts',
        'tasks': [
            {'id': 'collect_contracts', 'name': 'Collect sample contracts', 'file_pattern': 'research/contracts/property_management_contracts.json'},
            {'id': 'service_scope', 'name': 'Document service scope', 'file_pattern': 'research/contracts/service_scope.json'},
            {'id': 'geographic_scope', 'name': 'Properties by state', 'file_pattern': 'research/contracts/property_lists_by_state.json'},
            {'id': 'contract_terms', 'name': 'Licensing requirements in contracts', 'file_pattern': 'research/contracts/property_management_contracts.json'},
        ]
    },
    'employee_roles': {
        'name': 'Employee Role Documentation',
        'tasks': [
            {'id': 'identify_employees', 'name': 'Identify key employees', 'file_pattern': 'research/employees/employee_roles.json'},
            {'id': 'categorize_roles', 'name': 'Categorize by role', 'file_pattern': 'research/employees/employee_roles.json'},
            {'id': 'job_descriptions', 'name': 'Job descriptions', 'file_pattern': 'research/employees/job_descriptions.json'},
            {'id': 'org_chart', 'name': 'Organizational charts', 'file_pattern': 'research/employees/organizational_chart.json'},
            {'id': 'role_verification', 'name': 'Role verification', 'file_pattern': 'research/employees/employee_roles.json'},
        ]
    },
    'regulatory_complaints': {
        'name': 'Regulatory Complaint History',
        'tasks': [
            {'id': 'state_complaints', 'name': 'State regulatory complaints', 'file_pattern': 'research/complaints/**/regulatory_complaints.json'},
            {'id': 'consumer_complaints', 'name': 'Consumer complaints (BBB)', 'file_pattern': 'research/complaints/bbb_complaints.json'},
            {'id': 'enforcement_actions', 'name': 'Enforcement actions', 'file_pattern': 'research/complaints/**/regulatory_complaints.json'},
        ]
    },
    'financial_records': {
        'name': 'Financial Records',
        'tasks': [
            {'id': 'sec_filings', 'name': 'SEC filings', 'file_pattern': 'research/financial/sec_filings.json'},
            {'id': 'state_filings', 'name': 'State business filings', 'file_pattern': 'research/financial/*_business_filings.json'},
            {'id': 'property_values', 'name': 'Property value assessments', 'file_pattern': 'research/financial/property_value_assessments.json'},
        ]
    },
    'news_coverage': {
        'name': 'News and Media Coverage',
        'tasks': [
            {'id': 'search_framework', 'name': 'Search framework created', 'file_pattern': 'research/news/violation_coverage.json'},
            {'id': 'violation_coverage', 'name': 'Violation coverage articles', 'file_pattern': 'research/news/violation_coverage.json'},
            {'id': 'legal_proceedings', 'name': 'Legal proceedings', 'file_pattern': 'research/news/legal_proceedings.json'},
        ]
    },
    'fair_housing': {
        'name': 'Fair Housing Records',
        'tasks': [
            {'id': 'hud_complaints', 'name': 'HUD complaints', 'file_pattern': 'research/discrimination/hud_complaints.json'},
            {'id': 'eeoc_records', 'name': 'EEOC records', 'file_pattern': 'research/discrimination/eeoc_records.json'},
            {'id': 'state_discrimination', 'name': 'State discrimination complaints', 'file_pattern': 'research/discrimination/*_discrimination_complaints.json'},
        ]
    },
    'professional_memberships': {
        'name': 'Professional Memberships',
        'tasks': [
            {'id': 'real_estate_assoc', 'name': 'Real estate associations', 'file_pattern': 'research/memberships/association_memberships.json'},
            {'id': 'property_mgmt_assoc', 'name': 'Property management associations', 'file_pattern': 'research/memberships/association_memberships.json'},
        ]
    },
    'social_media': {
        'name': 'Social Media and Online Presence',
        'tasks': [
            {'id': 'company_website', 'name': 'Company websites', 'file_pattern': 'research/social_media/company_websites.json'},
            {'id': 'linkedin_profiles', 'name': 'LinkedIn profiles', 'file_pattern': 'research/social_media/linkedin_profiles.json'},
            {'id': 'online_reviews', 'name': 'Online reviews', 'file_pattern': 'research/social_media/online_reviews.json'},
        ]
    },
}

def check_task_completion(cat_id: str, task: dict) -> bool:
    """Check if a task is completed by looking for files."""
    pattern = task.get('file_pattern', '')
    if not pattern:
        return False

    # Handle glob patterns
    if '**' in pattern:
        # Recursive glob
        parts = pattern.split('**')
        base = PROJECT_ROOT / parts[0].rstrip('/')
        if base.exists():
            matches = list(base.rglob(parts[1].lstrip('/')))
            return len(matches) > 0
    elif '*' in pattern:
        # Simple glob
        file_path = PROJECT_ROOT / pattern
        parent_dir = file_path.parent
        if parent_dir.exists():
            matches = list(parent_dir.glob(file_path.name))
            return len(matches) > 0
    else:
        # Exact file
        file_path = PROJECT_ROOT / pattern
        return file_path.exists()

    return False

def calculate_category_progress(cat_id: str) -> dict:
    """Calculate progress for a category."""
    cat_data = TASKS[cat_id]
    total_tasks = len(cat_data['tasks'])
    completed_tasks = sum(1 for task in cat_data['tasks'] if check_task_completion(cat_id, task))
    percent = round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0.0

    return {
        'name': cat_data['name'],
        'completed': completed_tasks,
        'total': total_tasks,
        'percent': percent,
        'status': 'complete' if completed_tasks >= total_tasks else 'in_progress' if completed_tasks > 0 else 'not_started'
    }

def calculate_overall_progress() -> dict:
    """Calculate overall progress across all categories."""
    categories = {}
    total_completed = 0
    total_tasks = 0

    for cat_id, cat_data in TASKS.items():
        progress = calculate_category_progress(cat_id)
        categories[cat_id] = progress
        total_completed += progress['completed']
        total_tasks += progress['total']

    overall_percent = round(total_completed / total_tasks * 100, 1) if total_tasks > 0 else 0.0

    return {
        'timestamp': datetime.now().isoformat(),
        'overall': {
            'completed': total_completed,
            'total': total_tasks,
            'percent': overall_percent
        },
        'categories': categories
    }

def update_progress():
    """Update progress file."""
    progress = calculate_overall_progress()
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2) + '\n')
    return progress

def main():
    """Main function."""
    print("Updating progress from completed task files...")
    progress = update_progress()

    print(f"\nOverall Progress: {progress['overall']['completed']}/{progress['overall']['total']} tasks ({progress['overall']['percent']}%)")
    print("\nCategory Progress:")
    for cat_id, cat_data in sorted(progress['categories'].items(), key=lambda x: x[1]['percent'], reverse=True):
        status_icon = '✅' if cat_data['status'] == 'complete' else '⚠️' if cat_data['status'] == 'in_progress' else '❌'
        print(f"  {status_icon} {cat_data['name']}: {cat_data['completed']}/{cat_data['total']} ({cat_data['percent']}%)")

    print(f"\n✓ Progress updated: {PROGRESS_FILE}")

if __name__ == '__main__':
    main()
