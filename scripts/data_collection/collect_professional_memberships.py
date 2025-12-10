#!/usr/bin/env python3
"""
Collect Professional Association Memberships

Script to help search professional associations and certifications.
"""

from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent.parent
PROFESSIONAL_DIR = PROJECT_ROOT / 'research/professional'

# Real estate associations
REAL_ESTATE_ASSOCIATIONS = {
    'National': {
        'name': 'National Association of Realtors (NAR)',
        'url': 'https://www.nar.realtor/',
        'search_method': 'Member directory search',
    },
    'DC': {
        'name': 'DC Association of Realtors',
        'url': 'https://www.dcrealtors.org/',
    },
    'Maryland': {
        'name': 'Maryland Association of Realtors',
        'url': 'https://www.mdrealtor.org/',
    },
    'Virginia': {
        'name': 'Virginia Association of Realtors',
        'url': 'https://www.varealtor.com/',
    },
    'New Jersey': {
        'name': 'New Jersey Association of Realtors',
        'url': 'https://www.njar.com/',
    },
    'New York': {
        'name': 'New York State Association of Realtors',
        'url': 'https://www.nysar.com/',
    },
    'Connecticut': {
        'name': 'Connecticut Association of Realtors',
        'url': 'https://www.ctrealtors.com/',
    },
}

# Property management associations
PROPERTY_MANAGEMENT_ASSOCIATIONS = {
    'IREM': {
        'name': 'Institute of Real Estate Management',
        'url': 'https://www.irem.org/',
        'certifications': ['CPM - Certified Property Manager'],
    },
    'NAA': {
        'name': 'National Apartment Association',
        'url': 'https://www.naahq.org/',
        'certifications': ['CAM - Certified Apartment Manager', 'CAPS - Certified Apartment Property Supervisor'],
    },
}


def create_memberships_template():
    """Create template for professional memberships."""
    PROFESSIONAL_DIR.mkdir(parents=True, exist_ok=True)

    template = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Professional association memberships and certifications',
        },
        'real_estate_associations': {},
        'property_management_associations': {},
        'certifications': {
            'cpm': [],
            'arm': [],
            'other': [],
        },
        'continuing_education': {
            'records': [],
            'note': 'CE records if publicly available',
        },
    }

    for key, assoc in REAL_ESTATE_ASSOCIATIONS.items():
        template['real_estate_associations'][key] = {
            'name': assoc['name'],
            'url': assoc.get('url', ''),
            'members': [],
            'search_status': 'pending',
        }

    for key, assoc in PROPERTY_MANAGEMENT_ASSOCIATIONS.items():
        template['property_management_associations'][key] = {
            'name': assoc['name'],
            'url': assoc['url'],
            'members': [],
            'certifications': assoc.get('certifications', []),
            'search_status': 'pending',
        }

    filepath = PROFESSIONAL_DIR / 'memberships.json'
    filepath.write_text(json.dumps(template, indent=2) + '\n')
    print(f"Created {filepath}")

    # Certifications template
    cert_file = PROFESSIONAL_DIR / 'certifications.json'
    cert_data = {
        'metadata': {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'purpose': 'Professional certifications',
        },
        'cpm_certifications': [],
        'arm_certifications': [],
        'other_certifications': [],
    }
    cert_file.write_text(json.dumps(cert_data, indent=2) + '\n')
    print(f"Created {cert_file}")

    return filepath


def print_search_instructions():
    """Print search instructions."""
    print("=== Professional Memberships Search Instructions ===\n")

    print("Real Estate Associations:")
    for key, assoc in REAL_ESTATE_ASSOCIATIONS.items():
        print(f"  {assoc['name']}: {assoc.get('url', 'N/A')}")
    print()

    print("Property Management Associations:")
    for key, assoc in PROPERTY_MANAGEMENT_ASSOCIATIONS.items():
        print(f"  {assoc['name']}: {assoc['url']}")
        if 'certifications' in assoc:
            print(f"    Certifications: {', '.join(assoc['certifications'])}")
    print()

    print("Search Terms:")
    print("  - Kettler Management")
    print("  - Caitlin Skidmore")
    print("  - Robert Kettler")
    print("  - Individual employee names")
    print()


if __name__ == '__main__':
    create_memberships_template()
    print_search_instructions()
