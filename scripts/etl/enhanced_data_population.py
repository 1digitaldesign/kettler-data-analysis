#!/usr/bin/env python3
"""
Enhanced Data Population System

Cross-references data sources to populate missing fields and identifies
records needing manual verification with specific guidance.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
from datetime import datetime
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_DIR, DATA_CLEANED_DIR, DATA_PROCESSED_DIR, DATA_SOURCE_DIR
from scripts.utils.state_normalizer import normalize_state


class EnhancedDataPopulation:
    """Enhanced system for populating missing data through cross-referencing."""

    def __init__(self):
        self.reference_data = {}
        self.population_log = []
        self.manual_verification_items = []

    def load_reference_data(self):
        """Load reference data from source files for cross-referencing."""
        print("Loading reference data for cross-referencing...")

        # Load source firm data
        source_firms = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"
        if source_firms.exists():
            try:
                with open(source_firms, 'r', encoding='utf-8') as f:
                    self.reference_data['firms'] = json.load(f)
                print(f"  Loaded {len(self.reference_data.get('firms', []))} firms from source")
            except:
                pass

        # Load individual licenses
        source_licenses = DATA_SOURCE_DIR / "skidmore_individual_licenses.json"
        if source_licenses.exists():
            try:
                with open(source_licenses, 'r', encoding='utf-8') as f:
                    self.reference_data['licenses'] = json.load(f)
                print(f"  Loaded {len(self.reference_data.get('licenses', []))} licenses from source")
            except:
                pass

        # Load aggregated research data
        for agg_file in DATA_PROCESSED_DIR.glob("research_*_aggregated.json"):
            try:
                with open(agg_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    category = agg_file.stem.replace('research_', '').replace('_aggregated', '')
                    self.reference_data[category] = data.get('data', [])
                print(f"  Loaded {len(self.reference_data.get(category, []))} items from {category}")
            except:
                pass

    def cross_reference_and_populate(self, file_path: Path) -> Dict[str, Any]:
        """Cross-reference data and populate missing fields."""
        result = {
            "file": str(file_path),
            "fields_populated": 0,
            "populations": [],
            "needs_manual_verification": []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            original_data = json.dumps(data, sort_keys=True)

            # Populate based on data type
            if isinstance(data, list):
                for i, item in enumerate(data):
                    if isinstance(item, dict):
                        populated = self._populate_record(item, file_path)
                        result["fields_populated"] += populated["count"]
                        result["populations"].extend(populated["fields"])
                        if populated["needs_verification"]:
                            result["needs_manual_verification"].append({
                                "index": i,
                                "record": item,
                                "reason": populated["verification_reason"]
                            })
            elif isinstance(data, dict):
                populated = self._populate_record(data, file_path)
                result["fields_populated"] += populated["count"]
                result["populations"].extend(populated["fields"])
                if populated["needs_verification"]:
                    result["needs_manual_verification"].append({
                        "record": data,
                        "reason": populated["verification_reason"]
                    })

            # Write updated data if changes were made
            updated_data = json.dumps(data, sort_keys=True)
            if original_data != updated_data:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            result["error"] = str(e)

        return result

    def _populate_record(self, record: Dict, file_path: Path) -> Dict[str, Any]:
        """Populate a single record with missing data."""
        result = {
            "count": 0,
            "fields": [],
            "needs_verification": False,
            "verification_reason": None
        }

        # Try to populate missing critical fields
        missing_fields = []

        # Check and populate name
        if not record.get('name') and not record.get('title'):
            name = self._find_name(record)
            if name:
                record['name'] = name
                result["count"] += 1
                result["fields"].append({"field": "name", "value": name, "source": "cross_reference"})
            else:
                missing_fields.append("name")

        # Check and populate state/jurisdiction
        if not record.get('state') and not record.get('jurisdiction'):
            state = self._find_state(record)
            if state:
                record['state'] = state
                record['jurisdiction'] = state
                result["count"] += 1
                result["fields"].append({"field": "state", "value": state, "source": "cross_reference"})
            else:
                missing_fields.append("state")

        # Check and populate license information
        if 'license' in str(file_path).lower() or 'license' in record:
            if not record.get('license_number') and not record.get('license'):
                license_info = self._find_license(record)
                if license_info:
                    record.update(license_info)
                    result["count"] += len(license_info)
                    result["fields"].extend([{"field": k, "value": v, "source": "cross_reference"}
                                           for k, v in license_info.items()])

        # Check and populate dates
        if not record.get('date') and not record.get('created_date'):
            date = self._find_date(record)
            if date:
                record['date'] = date
                result["count"] += 1
                result["fields"].append({"field": "date", "value": date, "source": "inferred"})

        # Flag for manual verification if critical fields still missing
        if missing_fields:
            result["needs_verification"] = True
            result["verification_reason"] = f"Missing critical fields: {', '.join(missing_fields)}"

        return result

    def _find_name(self, record: Dict) -> Optional[str]:
        """Find name from record or cross-reference."""
        # Check record itself
        for key in ['title', 'company', 'person', 'entity', 'firm', 'organization', 'business_name']:
            if key in record and record[key]:
                return str(record[key])

        # Cross-reference with source data
        if 'id' in record or 'identifier' in record:
            identifier = record.get('id') or record.get('identifier')
            # Search in reference firms
            for firm in self.reference_data.get('firms', []):
                if (firm.get('id') == identifier or
                    firm.get('identifier') == identifier or
                    firm.get('name', '').lower() in str(record).lower()):
                    return firm.get('name')

        return None

    def _find_state(self, record: Dict) -> Optional[str]:
        """Find state from record or cross-reference."""
        # Check record itself
        for key in ['jurisdiction', 'location', 'region', 'state_code', 'state_abbrev']:
            if key in record and record[key]:
                return normalize_state(record[key])

        # Try to infer from file path
        # This would be set by the caller if needed

        # Cross-reference
        if 'name' in record:
            name = record['name']
            # Search in reference data
            for firm in self.reference_data.get('firms', []):
                if name.lower() in firm.get('name', '').lower():
                    # Check firm's states
                    if 'states' in firm:
                        states = firm['states']
                        if isinstance(states, list) and states:
                            return normalize_state(states[0])
                        elif isinstance(states, dict):
                            return normalize_state(list(states.keys())[0])

        return None

    def _find_license(self, record: Dict) -> Dict[str, Any]:
        """Find license information from cross-reference."""
        license_info = {}

        # Check record itself
        for key in ['license_number', 'licensure', 'permit', 'registration', 'license_id']:
            if key in record and record[key]:
                license_info['license_number'] = record[key]
                return license_info

        # Cross-reference with license data
        name = record.get('name') or record.get('person') or record.get('entity')
        if name:
            for license_data in self.reference_data.get('licenses', []):
                if name.lower() in str(license_data.get('name', '')).lower():
                    if 'license_number' in license_data:
                        license_info['license_number'] = license_data['license_number']
                    if 'state' in license_data:
                        license_info['state'] = license_data['state']
                    if license_info:
                        return license_info

        return license_info

    def _find_date(self, record: Dict) -> Optional[str]:
        """Find date from record."""
        for key in ['timestamp', 'created', 'updated', 'date_created', 'date_updated', 'search_date', 'verified_date']:
            if key in record:
                value = record[key]
                if isinstance(value, (int, float)) and value > 0:
                    from datetime import datetime
                    return datetime.fromtimestamp(value).isoformat()
                elif isinstance(value, str) and value:
                    return value
        return None

    def process_all_files(self) -> Dict[str, Any]:
        """Process all cleaned files."""
        print("\n" + "=" * 80)
        print("ENHANCED DATA POPULATION")
        print("=" * 80)

        # Load reference data
        self.load_reference_data()

        # Get all cleaned files
        cleaned_files = list(DATA_CLEANED_DIR.rglob('*.json'))

        print(f"\nProcessing {len(cleaned_files)} files...")

        results = {
            "files_processed": 0,
            "files_updated": 0,
            "total_fields_populated": 0,
            "manual_verification_needed": 0
        }

        for file_path in cleaned_files:
            try:
                result = self.cross_reference_and_populate(file_path)
                results["files_processed"] += 1

                if result.get("fields_populated", 0) > 0:
                    results["files_updated"] += 1
                    results["total_fields_populated"] += result["fields_populated"]
                    self.population_log.append(result)

                if result.get("needs_manual_verification"):
                    results["manual_verification_needed"] += len(result["needs_manual_verification"])
                    self.manual_verification_items.extend(result["needs_manual_verification"])

                if results["files_processed"] % 100 == 0:
                    print(f"  Processed {results['files_processed']}/{len(cleaned_files)} files...")

            except Exception as e:
                print(f"  Error processing {file_path.name}: {str(e)}")

        print(f"\n  Files processed: {results['files_processed']}")
        print(f"  Files updated: {results['files_updated']}")
        print(f"  Fields populated: {results['total_fields_populated']}")
        print(f"  Manual verification needed: {results['manual_verification_needed']}")

        return results

    def generate_verification_guide(self) -> Path:
        """Generate detailed manual verification guide."""
        print("\n" + "=" * 80)
        print("GENERATING MANUAL VERIFICATION GUIDE")
        print("=" * 80)

        guide = {
            "generated_date": datetime.now().isoformat(),
            "summary": {
                "total_items": len(self.manual_verification_items),
                "by_reason": defaultdict(int)
            },
            "verification_items": [],
            "population_log": self.population_log[:100]  # First 100
        }

        # Categorize by reason
        for item in self.manual_verification_items:
            reason = item.get("reason", "unknown")
            guide["summary"]["by_reason"][reason] += 1

        # Add ALL items with guidance - no limits with 128GB RAM
        print(f"  Processing {len(self.manual_verification_items)} items for guide...")
        for i, item in enumerate(self.manual_verification_items):
            verification_item = {
                "reason": item.get("reason"),
                "record_preview": {k: v for k, v in item.get("record", {}).items()
                                 if k not in ['embedding', 'vectors', 'large_data']},
                "guidance": self._generate_guidance(item)
            }
            guide["verification_items"].append(verification_item)

            if (i + 1) % 1000 == 0:
                print(f"    Processed {i + 1}/{len(self.manual_verification_items)} items...")

        guide_path = DATA_PROCESSED_DIR / "manual_verification_guide.json"
        with open(guide_path, 'w', encoding='utf-8') as f:
            json.dump(guide, f, indent=2, ensure_ascii=False)

        print(f"\n  Guide generated: {guide_path}")
        print(f"  Items needing verification: {guide['summary']['total_items']}")
        for reason, count in guide["summary"]["by_reason"].items():
            print(f"    - {reason}: {count}")

        return guide_path

    def _generate_guidance(self, item: Dict) -> str:
        """Generate specific guidance for manual verification."""
        reason = item.get("reason", "")
        record = item.get("record", {})

        if "Missing critical fields" in reason:
            missing = reason.split(": ")[-1] if ": " in reason else ""
            guidance = f"Please verify and populate the following fields: {missing}. "
            guidance += "Check source documents, cross-reference with other data files, or mark as 'not available' if confirmed missing."
            return guidance

        return "Please review this record for data completeness and accuracy."

    def run_full_population(self) -> Dict[str, Any]:
        """Run complete enhanced population process."""
        print("=" * 80)
        print("ENHANCED DATA POPULATION SYSTEM")
        print("=" * 80)

        # Process all files
        results = self.process_all_files()

        # Generate verification guide
        guide_path = self.generate_verification_guide()
        results["verification_guide"] = str(guide_path)

        # Save results
        results_path = DATA_PROCESSED_DIR / "enhanced_population_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        print("\n" + "=" * 80)
        print("POPULATION COMPLETE")
        print("=" * 80)
        print(f"  Results saved to: {results_path}")
        print(f"  Verification guide: {guide_path}")
        print("=" * 80)

        return results


def main():
    """Main execution."""
    populator = EnhancedDataPopulation()
    results = populator.run_full_population()
    return results


if __name__ == "__main__":
    main()
