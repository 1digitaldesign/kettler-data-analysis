#!/usr/bin/env python3
"""
Data Collection Workflow with Progress Bars

Interactive workflow that shows progress bars while working through tasks.
"""

from pathlib import Path
import json
import time
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent


def draw_progress_bar(progress: int, width: int = 20, label: str = "") -> str:
    """Draw a progress bar."""
    filled = int((progress / 100) * width)
    empty = width - filled
    bar = '█' * filled + '░' * empty
    return f"{label:<30} {bar} {progress}%"


def update_progress_display(category: str, current: int, total: int, status: str = ""):
    """Update and display progress for a category."""
    progress = round((current / total) * 100) if total > 0 else 0
    bar = draw_progress_bar(progress, label=category)
    print(f"  {bar} {status}")
    return progress


def check_license_searches():
    """Check license search completion status."""
    license_dir = PROJECT_ROOT / 'research/license_searches/data'
    
    if not license_dir.exists():
        return {'complete': 0, 'total': 15, 'progress': 0}
    
    states_complete = 0
    states_partial = {}
    
    for state_dir in license_dir.iterdir():
        if state_dir.is_dir():
            finding_files = list(state_dir.glob('*_finding.json'))
            if len(finding_files) >= 15:
                states_complete += 1
            elif len(finding_files) > 0:
                states_partial[state_dir.name] = len(finding_files)
    
    return {
        'complete': states_complete,
        'partial': states_partial,
        'total': 15,
        'progress': round((states_complete / 15) * 100),
    }


def check_company_registrations():
    """Check company registration search status."""
    reg_dir = PROJECT_ROOT / 'research/company_registrations'
    
    if not reg_dir.exists():
        return {'complete': 0, 'total': 12, 'progress': 0}
    
    total = 12  # 6 states × 2 companies
    complete = 0
    
    for state_dir in reg_dir.iterdir():
        if state_dir.is_dir():
            for reg_file in state_dir.glob('*_registration.json'):
                try:
                    data = json.loads(reg_file.read_text())
                    if data.get('findings', {}).get('registered') is not None:
                        complete += 1
                except:
                    pass
    
    return {
        'complete': complete,
        'total': total,
        'progress': round((complete / total) * 100) if total > 0 else 0,
    }


def check_employee_roles():
    """Check employee roles completion."""
    emp_dir = PROJECT_ROOT / 'research/employees'
    
    required_files = ['employee_roles.json', 'organizational_chart.json']
    found = sum(1 for f in required_files if (emp_dir / f).exists())
    
    return {
        'complete': found,
        'total': len(required_files),
        'progress': round((found / len(required_files)) * 100),
    }


def display_workflow_progress():
    """Display progress for all workflow categories."""
    print("\n" + "=" * 70)
    print(" DATA COLLECTION WORKFLOW - LIVE PROGRESS".center(70))
    print("=" * 70 + "\n")
    
    # License Searches
    license_stats = check_license_searches()
    update_progress_display(
        "License Searches",
        license_stats['complete'],
        license_stats['total'],
        f"({license_stats['complete']}/{license_stats['total']} states)"
    )
    
    # Company Registrations
    reg_stats = check_company_registrations()
    update_progress_display(
        "Company Registrations",
        reg_stats['complete'],
        reg_stats['total'],
        f"({reg_stats['complete']}/{reg_stats['total']} searches)"
    )
    
    # Employee Roles
    emp_stats = check_employee_roles()
    update_progress_display(
        "Employee Roles",
        emp_stats['complete'],
        emp_stats['total'],
        f"({emp_stats['complete']}/{emp_stats['total']} files)"
    )
    
    # Calculate overall
    overall = round((license_stats['progress'] + reg_stats['progress'] + emp_stats['progress']) / 3)
    print("\n" + "-" * 70)
    print(f"Overall Progress: {draw_progress_bar(overall, width=30)}")
    print("-" * 70 + "\n")
    
    return {
        'license': license_stats,
        'registrations': reg_stats,
        'employees': emp_stats,
        'overall': overall,
    }


def identify_next_tasks():
    """Identify next high-priority tasks."""
    print("=" * 70)
    print(" NEXT PRIORITY TASKS".center(70))
    print("=" * 70 + "\n")
    
    license_stats = check_license_searches()
    reg_stats = check_company_registrations()
    
    tasks = []
    
    # License searches
    if license_stats['progress'] < 100:
        if license_stats['partial']:
            print("1. Complete License Searches:")
            for state, count in license_stats['partial'].items():
                remaining = 15 - count
                print(f"   • {state.title()}: {remaining} searches remaining ({count}/15 complete)")
                tasks.append(f"Complete {state} license searches")
        else:
            print("1. License Searches: All states need completion")
            tasks.append("Complete license searches for all states")
    
    # Company registrations
    if reg_stats['progress'] < 100:
        remaining = reg_stats['total'] - reg_stats['complete']
        print(f"\n2. Company Registrations: {remaining} searches remaining")
        print(f"   • Use: python3.14 scripts/data_collection/start_company_searches.py")
        tasks.append(f"Complete {remaining} company registration searches")
    
    # Property contracts
    contracts_dir = PROJECT_ROOT / 'research/contracts'
    if contracts_dir.exists():
        contract_file = contracts_dir / 'property_management_contracts.json'
        if contract_file.exists():
            data = json.loads(contract_file.read_text())
            total_properties = sum(
                len(state_data.get('properties', []))
                for state_data in data.get('properties_by_state', {}).values()
            )
            if total_properties == 0:
                print(f"\n3. Property Contracts: Identify properties under management")
                tasks.append("Identify properties for each state")
    
    print("\n" + "=" * 70 + "\n")
    
    return tasks


if __name__ == '__main__':
    stats = display_workflow_progress()
    tasks = identify_next_tasks()
    
    print(f"📋 Identified {len(tasks)} priority tasks")
    print(f"📊 Overall Progress: {stats['overall']}%\n")
