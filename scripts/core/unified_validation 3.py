#!/usr/bin/env python3
"""
Unified Validation Module
Consolidates multiple R validation scripts into a single Python module
Replaces: validate_kettler_claims, validate_hyland_claims, validate_skidmore_firms,
          verify_business_licenses, verify_property_management_licenses, etc.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.utils.paths import DATA_SOURCE_DIR, RESEARCH_DIR, RESEARCH_VERIFICATION_DIR

class UnifiedValidator:
    """Unified validator that replaces multiple R validation scripts"""

    def __init__(self):
        self.results = {}

    def validate_license_format(self, license_number: str, state: str = None) -> Dict[str, Any]:
        """Validate license number format"""
        result = {
            'license': license_number,
            'valid': True,
            'issues': []
        }

        if not license_number or pd.isna(license_number):
            result['valid'] = False
            result['issues'].append('Missing license number')
            return result

        license_str = str(license_number).strip()

        # Basic format checks
        if len(license_str) < 6 or len(license_str) > 15:
            result['valid'] = False
            result['issues'].append(f'Invalid length: {len(license_str)}')

        if not re.match(r'^[A-Za-z0-9\s\-]+$', license_str):
            result['valid'] = False
            result['issues'].append('Contains invalid characters')

        return result

    def validate_address(self, address: str) -> Dict[str, Any]:
        """Validate address format"""
        result = {
            'address': address,
            'valid': True,
            'issues': []
        }

        if not address or pd.isna(address):
            result['valid'] = False
            result['issues'].append('Missing address')
            return result

        addr_str = str(address).strip()

        if len(addr_str) < 10:
            result['valid'] = False
            result['issues'].append('Address too short')

        has_street = bool(re.search(r'(Street|St|Avenue|Ave|Road|Rd|Drive|Dr)', addr_str, re.IGNORECASE))
        has_city = bool(re.search(r'[A-Z]{2}\s+\d{5}', addr_str))

        if not has_street and not has_city:
            result['valid'] = False
            result['issues'].append('Missing street or city/state/zip')

        return result

    def validate_firm_claims(self, firms_df: pd.DataFrame, claim_type: str = "kettler") -> Dict[str, Any]:
        """Validate firm claims (replaces validate_kettler_claims.R, validate_hyland_claims.R)"""
        validation_results = {
            'claim_type': claim_type,
            'total_firms': len(firms_df),
            'validated': [],
            'issues': []
        }

        if firms_df.empty:
            return validation_results

        for idx, firm in firms_df.iterrows():
            firm_result = {
                'firm_name': firm.get('Firm.Name', ''),
                'license_number': firm.get('License.Number', ''),
                'address': firm.get('Address', ''),
                'valid': True,
                'issues': []
            }

            # Validate license
            if 'License.Number' in firm:
                license_validation = self.validate_license_format(firm['License.Number'])
                if not license_validation['valid']:
                    firm_result['valid'] = False
                    firm_result['issues'].extend(license_validation['issues'])

            # Validate address
            if 'Address' in firm:
                address_validation = self.validate_address(firm['Address'])
                if not address_validation['valid']:
                    firm_result['valid'] = False
                    firm_result['issues'].extend(address_validation['issues'])

            if firm_result['valid']:
                validation_results['validated'].append(firm_result)
            else:
                validation_results['issues'].append(firm_result)

        return validation_results

    def verify_business_licenses(self, firms_df: pd.DataFrame) -> Dict[str, Any]:
        """Verify business licenses (replaces verify_business_licenses.R)"""
        verification = {
            'total_firms': len(firms_df),
            'verified': [],
            'unverified': [],
            'status': 'framework'
        }

        if firms_df.empty:
            return verification

        # Framework - actual implementation would query business license databases
        for idx, firm in firms_df.iterrows():
            result = {
                'firm_name': firm.get('Firm.Name', ''),
                'license_number': firm.get('License.Number', ''),
                'status': 'framework',
                'note': 'Requires business license database API'
            }
            verification['unverified'].append(result)

        return verification

    def verify_property_management_licenses(self, firms_df: pd.DataFrame) -> Dict[str, Any]:
        """Verify property management licenses (replaces verify_property_management_licenses.R)"""
        verification = {
            'total_firms': len(firms_df),
            'verified': [],
            'unverified': [],
            'status': 'framework'
        }

        if firms_df.empty:
            return verification

        # Framework - would query DPOR databases
        for idx, firm in firms_df.iterrows():
            result = {
                'firm_name': firm.get('Firm.Name', ''),
                'license_number': firm.get('License.Number', ''),
                'state': firm.get('State', ''),
                'status': 'framework',
                'note': 'Requires DPOR database API'
            }
            verification['unverified'].append(result)

        return verification

    def validate_all(self, validation_type: str = "all") -> Dict[str, Any]:
        """Run all validations"""
        results = {}

        # Load firms data
        firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
        if not firms_file.exists():
            firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"

        if not firms_file.exists():
            print("No firms data found")
            return results

        if firms_file.suffix == '.csv':
            firms_df = pd.read_csv(firms_file)
        else:
            # Handle JSON files carefully
            with open(firms_file, 'r') as f:
                json_data = json.load(f)
                if isinstance(json_data, list):
                    firms_df = pd.DataFrame(json_data)
                elif isinstance(json_data, dict):
                    # Try to find a list/array in the dict
                    for key, value in json_data.items():
                        if isinstance(value, list) and len(value) > 0:
                            firms_df = pd.DataFrame(value)
                            break
                    if 'firms_df' not in locals():
                        # Fallback: try pd.read_json with orient
                        try:
                            firms_df = pd.read_json(firms_file, orient='records')
                        except:
                            firms_df = pd.DataFrame()
                else:
                    firms_df = pd.DataFrame()

        if validation_type in ['all', 'claims']:
            print("Validating firm claims...")
            results['kettler_claims'] = self.validate_firm_claims(firms_df, 'kettler')
            results['hyland_claims'] = self.validate_firm_claims(firms_df, 'hyland')

        if validation_type in ['all', 'licenses']:
            print("Verifying business licenses...")
            results['business_licenses'] = self.verify_business_licenses(firms_df)

            print("Verifying property management licenses...")
            results['property_management_licenses'] = self.verify_property_management_licenses(firms_df)

        self.results = results
        return results

    def save_results(self):
        """Save validation results"""
        RESEARCH_VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)

        for key, value in self.results.items():
            output_file = RESEARCH_VERIFICATION_DIR / f"{key}_verification.json"
            with open(output_file, 'w') as f:
                json.dump(value, f, indent=2, default=str)
            print(f"Saved {key} validation to: {output_file}")

def main():
    """Main entry point"""
    validator = UnifiedValidator()
    results = validator.validate_all()
    validator.save_results()

    print("\n=== Validation Complete ===")
    for key, value in results.items():
        if isinstance(value, dict):
            total = value.get('total_firms', 0)
            validated = len(value.get('validated', []))
            issues = len(value.get('issues', []))
            print(f"{key}: {validated}/{total} validated, {issues} issues")

if __name__ == "__main__":
    main()
