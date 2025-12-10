#!/usr/bin/env python3
"""
Collect Employee Role Documentation

Script to help document employee roles and organizational structure.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
EMPLOYEES_DIR = PROJECT_ROOT / 'research/employees'

# 15 employees identified
EMPLOYEES = {
    'robert_kettler': {
        'name': 'Robert Kettler',
        'title': 'CEO/Founder',
        'category': 'Executive Leadership',
        'performs_licensed_activities': True,
    },
    'cindy_fisher': {
        'name': 'Cindy Fisher',
        'title': 'President',
        'category': 'Executive Leadership',
        'performs_licensed_activities': True,
    },
    'luke_davis': {
        'name': 'Luke Davis',
        'title': 'Chief Information Officer',
        'category': 'Executive Leadership',
        'performs_licensed_activities': False,
    },
    'pat_cassada': {
        'name': 'Pat Cassada',
        'title': 'Chief Financial Officer',
        'category': 'Executive Leadership',
        'performs_licensed_activities': False,
    },
    'sean_curtin': {
        'name': 'Sean Curtin',
        'title': 'General Counsel',
        'category': 'Executive Leadership',
        'performs_licensed_activities': False,
    },
    'edward_hyland': {
        'name': 'Edward Hyland',
        'title': 'Senior Regional Manager',
        'category': 'Operations Management',
        'performs_licensed_activities': True,
    },
    'amy_groff': {
        'name': 'Amy Groff',
        'title': 'VP Operations',
        'category': 'Operations Management',
        'performs_licensed_activities': True,
    },
    'robert_grealy': {
        'name': 'Robert Grealy',
        'title': 'SVP Operations',
        'category': 'Operations Management',
        'performs_licensed_activities': True,
    },
    'todd_bowen': {
        'name': 'Todd Bowen',
        'title': 'SVP Strategic Services',
        'category': 'Operations Management',
        'performs_licensed_activities': True,
    },
    'djene_moyer': {
        'name': 'Djene Moyer',
        'title': 'Community Manager',
        'category': 'Property Management Staff',
        'performs_licensed_activities': True,
    },
    'henry_ramos': {
        'name': 'Henry Ramos',
        'title': 'Property Manager',
        'category': 'Property Management Staff',
        'performs_licensed_activities': True,
    },
    'kristina_thoummarath': {
        'name': 'Kristina Thoummarath',
        'title': 'Chief of Staff',
        'category': 'Other Key Personnel',
        'performs_licensed_activities': False,
    },
    'christina_chang': {
        'name': 'Christina Chang',
        'title': 'Head of Asset Management',
        'category': 'Other Key Personnel',
        'performs_licensed_activities': True,
    },
    'liddy_bisanz': {
        'name': 'Liddy Bisanz',
        'title': 'Operations Connection',
        'category': 'Other Key Personnel',
        'performs_licensed_activities': False,
    },
    'caitlin_skidmore': {
        'name': 'Caitlin Skidmore',
        'title': 'Principal Broker',
        'category': 'Licensed Employee',
        'performs_licensed_activities': True,
        'licensed': True,
        'license_states': ['District of Columbia'],
    },
}


def create_employee_roles_file():
    """Create employee roles JSON file."""
    EMPLOYEES_DIR.mkdir(parents=True, exist_ok=True)
    
    output = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'total_employees': len(EMPLOYEES),
            'source': 'License search investigation',
        },
        'employees': EMPLOYEES,
        'summary': {
            'executive_leadership': len([e for e in EMPLOYEES.values() if e['category'] == 'Executive Leadership']),
            'operations_management': len([e for e in EMPLOYEES.values() if e['category'] == 'Operations Management']),
            'property_management': len([e for e in EMPLOYEES.values() if e['category'] == 'Property Management Staff']),
            'licensed': len([e for e in EMPLOYEES.values() if e.get('licensed', False)]),
            'performs_licensed_activities': len([e for e in EMPLOYEES.values() if e['performs_licensed_activities']]),
        },
    }
    
    filepath = EMPLOYEES_DIR / 'employee_roles.json'
    filepath.write_text(json.dumps(output, indent=2) + '\n')
    print(f"Created {filepath}")
    return filepath


def create_organizational_chart():
    """Create organizational chart structure."""
    chart = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'company': 'Kettler Management Inc.',
        },
        'structure': {
            'ceo': {
                'name': 'Robert Kettler',
                'reports_to': None,
                'direct_reports': ['President', 'CIO', 'CFO', 'General Counsel'],
            },
            'president': {
                'name': 'Cindy Fisher',
                'reports_to': 'CEO',
                'direct_reports': ['VP Operations', 'SVP Operations', 'SVP Strategic Services'],
            },
            'principal_broker': {
                'name': 'Caitlin Skidmore',
                'reports_to': 'President',
                'direct_reports': ['Property Management Staff'],
                'note': 'Only licensed employee',
            },
        },
    }
    
    filepath = EMPLOYEES_DIR / 'organizational_chart.json'
    filepath.write_text(json.dumps(chart, indent=2) + '\n')
    print(f"Created {filepath}")
    return filepath


if __name__ == '__main__':
    create_employee_roles_file()
    create_organizational_chart()
    print("\n✅ Employee role documentation files created")
