#!/usr/bin/env python3
"""
Data Cleaning and Deduplication Script

Refines data by:
1. Removing duplicates
2. Normalizing structure (flattening nested data)
3. Cleaning FK/PK relationships
4. Removing redundant fields
5. Standardizing formats
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Any, Set
from datetime import datetime

class DataCleaner:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.source_dir = data_dir / "source"
        self.cleaned_dir = data_dir / "cleaned"
        self.cleaned_dir.mkdir(exist_ok=True)

        self.stats = {
            "firms": {"original": 0, "deduplicated": 0, "cleaned": 0},
            "individual_licenses": {"original": 0, "deduplicated": 0, "cleaned": 0},
            "duplicates_removed": 0,
            "fields_normalized": 0
        }

    def normalize_address(self, address: str) -> str:
        """Normalize address format."""
        if not address:
            return address
        # Standardize common variations
        address = address.replace("STE #", "STE ").replace("STE#", "STE ")
        address = address.replace("SUITE #", "SUITE ").replace("SUITE#", "SUITE ")
        address = address.replace("  ", " ").strip()
        return address

    def normalize_firm_type(self, firm_type: str) -> str:
        """Normalize firm type to standard values."""
        if not firm_type:
            return firm_type
        # Map variations to standard values
        type_map = {
            "LLC": "LLC - Limited Liability Company",
            "Limited Partnership": "LP - Limited Partnership",
            "LP": "LP - Limited Partnership",
            "LLP": "LLP - Limited Liability Partnership"
        }
        return type_map.get(firm_type, firm_type)

    def clean_firms(self):
        """Clean and deduplicate firms data."""
        print("=" * 70)
        print("CLEANING FIRMS DATA")
        print("=" * 70)

        # Load original data
        firms_file = self.source_dir / "skidmore_all_firms_complete.json"
        with open(firms_file, 'r') as f:
            data = json.load(f)

        # Extract companies array (flatten nested structure)
        if isinstance(data, dict) and 'companies' in data:
            firms = data['companies']
            metadata = {k: v for k, v in data.items() if k != 'companies'}
        else:
            firms = data if isinstance(data, list) else [data]
            metadata = {}

        self.stats["firms"]["original"] = len(firms)
        print(f"Loaded {len(firms)} firms")

        # Check for duplicate primary keys
        seen_licenses: Set[str] = set()
        duplicates: List[int] = []

        for i, firm in enumerate(firms):
            license_num = firm.get('firm_license', '')
            if license_num in seen_licenses:
                duplicates.append(i)
                print(f"  ⚠️  Duplicate license found: {license_num} at index {i}")
            else:
                seen_licenses.add(license_num)

        # Remove duplicates (keep first occurrence)
        if duplicates:
            for idx in reversed(duplicates):
                firms.pop(idx)
            self.stats["duplicates_removed"] += len(duplicates)
            print(f"  Removed {len(duplicates)} duplicate firms")

        # Clean and normalize each firm
        cleaned_firms = []
        for firm in firms:
            cleaned = self.clean_firm_record(firm)
            cleaned_firms.append(cleaned)

        self.stats["firms"]["cleaned"] = len(cleaned_firms)
        self.stats["firms"]["deduplicated"] = len(cleaned_firms)

        # Save cleaned data (as array, not nested)
        output_file = self.cleaned_dir / "firms.json"
        with open(output_file, 'w') as f:
            json.dump(cleaned_firms, f, indent=2)

        print(f"✅ Saved {len(cleaned_firms)} cleaned firms to {output_file}")
        return cleaned_firms

    def clean_firm_record(self, firm: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a single firm record."""
        cleaned = {}

        # Required fields (keep as-is)
        for field in ['firm_license', 'firm_name', 'license_type', 'firm_type',
                     'address', 'expiration_date', 'principal_broker', 'state']:
            if field in firm:
                value = firm[field]
                # Normalize specific fields
                if field == 'address':
                    value = self.normalize_address(value)
                elif field == 'firm_type':
                    value = self.normalize_firm_type(value)
                cleaned[field] = value

        # Optional fields
        if firm.get('individual_license'):
            cleaned['individual_license'] = firm['individual_license']
        else:
            cleaned['individual_license'] = None

        if firm.get('dba_name'):
            cleaned['dba_name'] = firm['dba_name']

        if firm.get('initial_cert_date'):
            cleaned['initial_cert_date'] = firm['initial_cert_date']
        else:
            cleaned['initial_cert_date'] = None

        # Computed/derived fields (keep for reference but mark as computed)
        if firm.get('gap_years') is not None:
            cleaned['gap_years'] = firm['gap_years']

        # Notes field - keep only if it adds value beyond what can be computed
        if firm.get('notes') and firm['notes'].strip():
            # Only keep notes that provide unique information
            notes = firm['notes']
            # Remove redundant notes that just repeat address or gap info
            if not any(redundant in notes.lower() for redundant in
                      ['same tx address', 'licensed', 'gap', 'address']):
                cleaned['notes'] = notes

        # Verification fields
        if firm.get('verification_date'):
            cleaned['verification_date'] = firm['verification_date']

        # Remove needs_verification if false (default)
        if firm.get('needs_verification', False):
            cleaned['needs_verification'] = True

        return cleaned

    def clean_individual_licenses(self):
        """Clean and deduplicate individual licenses."""
        print("\n" + "=" * 70)
        print("CLEANING INDIVIDUAL LICENSES DATA")
        print("=" * 70)

        # Load original data
        licenses_file = self.source_dir / "skidmore_individual_licenses.json"
        with open(licenses_file, 'r') as f:
            licenses = json.load(f)

        if not isinstance(licenses, list):
            licenses = [licenses]

        self.stats["individual_licenses"]["original"] = len(licenses)
        print(f"Loaded {len(licenses)} individual licenses")

        # Check for duplicate primary keys
        seen_licenses: Set[str] = set()
        duplicates: List[int] = []

        for i, license in enumerate(licenses):
            license_num = license.get('license_number', '')
            if license_num in seen_licenses:
                duplicates.append(i)
                print(f"  ⚠️  Duplicate license found: {license_num} at index {i}")
            else:
                seen_licenses.add(license_num)

        # Remove duplicates
        if duplicates:
            for idx in reversed(duplicates):
                licenses.pop(idx)
            self.stats["duplicates_removed"] += len(duplicates)
            print(f"  Removed {len(duplicates)} duplicate licenses")

        # Clean and normalize each license
        cleaned_licenses = []
        for license in licenses:
            cleaned = self.clean_license_record(license)
            cleaned_licenses.append(cleaned)

        self.stats["individual_licenses"]["cleaned"] = len(cleaned_licenses)
        self.stats["individual_licenses"]["deduplicated"] = len(cleaned_licenses)

        # Save cleaned data
        output_file = self.cleaned_dir / "individual_licenses.json"
        with open(output_file, 'w') as f:
            json.dump(cleaned_licenses, f, indent=2)

        print(f"✅ Saved {len(cleaned_licenses)} cleaned licenses to {output_file}")
        return cleaned_licenses

    def clean_license_record(self, license: Dict[str, Any]) -> Dict[str, Any]:
        """Clean a single license record."""
        cleaned = {
            'license_number': license.get('license_number', ''),
            'name': license.get('name', ''),
            'address': self.normalize_address(license.get('address', '')),
            'license_type': license.get('license_type', ''),
            'board': license.get('board', '')
        }

        # Derive state from address if not present
        if 'state' not in license or not license.get('state'):
            address = cleaned['address']
            # Extract state from address (e.g., "FRISCO, TX 75034" -> "TX")
            if ', ' in address:
                parts = address.split(', ')
                if len(parts) >= 2:
                    state_part = parts[1].split()[0]
                    if len(state_part) == 2:
                        cleaned['state'] = state_part

        return cleaned

    def validate_fk_relationships(self, firms: List[Dict], licenses: List[Dict]):
        """Validate and clean FK relationships."""
        print("\n" + "=" * 70)
        print("VALIDATING FK RELATIONSHIPS")
        print("=" * 70)

        # Build index of valid license numbers
        valid_license_numbers = {lic['license_number'] for lic in licenses}
        print(f"Valid license numbers: {len(valid_license_numbers)}")

        # Check firm.individual_license references
        invalid_refs = []
        for firm in firms:
            ind_license = firm.get('individual_license')
            if ind_license and ind_license not in valid_license_numbers:
                invalid_refs.append({
                    'firm': firm.get('firm_name'),
                    'license': firm.get('firm_license'),
                    'invalid_fk': ind_license
                })
                # Set to null if invalid
                firm['individual_license'] = None

        if invalid_refs:
            print(f"  ⚠️  Found {len(invalid_refs)} invalid FK references:")
            for ref in invalid_refs[:5]:
                print(f"    - {ref['firm']}: invalid individual_license={ref['invalid_fk']}")
            if len(invalid_refs) > 5:
                print(f"    ... and {len(invalid_refs) - 5} more")
        else:
            print("  ✅ All FK references are valid")

        return firms

    def update_schema_references(self):
        """Update schema.json to point to cleaned files."""
        print("\n" + "=" * 70)
        print("UPDATING SCHEMA REFERENCES")
        print("=" * 70)

        schema_file = self.data_dir / "schema.json"
        with open(schema_file, 'r') as f:
            schema = json.load(f)

        # Update file references to cleaned versions
        if 'firms' in schema['tables']:
            schema['tables']['firms']['file'] = "cleaned/firms.json"
            print("  Updated firms.file to cleaned/firms.json")

        if 'individual_licenses' in schema['tables']:
            schema['tables']['individual_licenses']['file'] = "cleaned/individual_licenses.json"
            print("  Updated individual_licenses.file to cleaned/individual_licenses.json")

        # Save updated schema
        with open(schema_file, 'w') as f:
            json.dump(schema, f, indent=2)

        print("✅ Schema updated")

    def print_summary(self):
        """Print cleaning summary."""
        print("\n" + "=" * 70)
        print("CLEANING SUMMARY")
        print("=" * 70)
        print(f"Firms:")
        print(f"  Original: {self.stats['firms']['original']}")
        print(f"  After deduplication: {self.stats['firms']['deduplicated']}")
        print(f"  Final cleaned: {self.stats['firms']['cleaned']}")
        print(f"\nIndividual Licenses:")
        print(f"  Original: {self.stats['individual_licenses']['original']}")
        print(f"  After deduplication: {self.stats['individual_licenses']['deduplicated']}")
        print(f"  Final cleaned: {self.stats['individual_licenses']['cleaned']}")
        print(f"\nTotal duplicates removed: {self.stats['duplicates_removed']}")
        print(f"Fields normalized: {self.stats['fields_normalized']}")
        print("\n✅ Data cleaning complete!")

    def run(self):
        """Run complete cleaning process."""
        print("\n" + "=" * 70)
        print("DATA CLEANING AND DEDUPLICATION")
        print("=" * 70)
        print(f"Data directory: {self.data_dir}")
        print(f"Source directory: {self.source_dir}")
        print(f"Cleaned directory: {self.cleaned_dir}\n")

        # Clean firms
        firms = self.clean_firms()

        # Clean individual licenses
        licenses = self.clean_individual_licenses()

        # Validate FK relationships
        firms = self.validate_fk_relationships(firms, licenses)

        # Save updated firms
        output_file = self.cleaned_dir / "firms.json"
        with open(output_file, 'w') as f:
            json.dump(firms, f, indent=2)

        # Update schema references
        self.update_schema_references()

        # Print summary
        self.print_summary()


def main():
    """Run data cleaning."""
    data_dir = Path(__file__).parent
    cleaner = DataCleaner(data_dir)
    cleaner.run()


if __name__ == "__main__":
    main()
