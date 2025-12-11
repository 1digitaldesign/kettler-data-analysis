#!/usr/bin/env python3
"""
Data Cleaning and Population System

Identifies and fixes:
1. Missing data due to technical errors
2. Incomplete records
3. Data requiring manual verification
4. Populates missing fields where possible
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from collections import defaultdict
import re

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_DIR, DATA_CLEANED_DIR, DATA_PROCESSED_DIR
from scripts.utils.state_normalizer import normalize_dict_recursive, normalize_state
from scripts.utils.normalize_data_parallel import get_optimal_worker_count


class DataCleaningAndPopulation:
    """Comprehensive data cleaning and population system."""

    def __init__(self):
        self.issues_found = {
            "missing_data": [],
            "incomplete_records": [],
            "technical_errors": [],
            "needs_manual_verification": [],
            "populated_data": []
        }
        self.stats = {
            "files_analyzed": 0,
            "issues_found": 0,
            "issues_fixed": 0,
            "needs_manual_review": 0
        }

    def analyze_data_quality(self) -> Dict[str, Any]:
        """Analyze all cleaned data for quality issues."""
        print("=" * 80)
        print("DATA QUALITY ANALYSIS")
        print("=" * 80)

        # Get all cleaned files
        cleaned_files = list(DATA_CLEANED_DIR.rglob('*.json'))
        self.stats["files_analyzed"] = len(cleaned_files)

        print(f"\nAnalyzing {len(cleaned_files)} cleaned files...")

        # Analyze files in parallel
        worker_count = get_optimal_worker_count()

        with ProcessPoolExecutor(max_workers=worker_count) as executor:
            futures = {
                executor.submit(self._analyze_file_quality, file_path): file_path
                for file_path in cleaned_files
            }

            for future in as_completed(futures):
                file_path = futures[future]
                try:
                    issues = future.result()
                    if issues:
                        self._categorize_issues(file_path, issues)
                        self.stats["issues_found"] += len(issues)
                except Exception as e:
                    self.issues_found["technical_errors"].append({
                        "file": str(file_path),
                        "error": str(e),
                        "type": "analysis_error"
                    })

        print(f"\n  Issues found: {self.stats['issues_found']}")
        print(f"    - Missing data: {len(self.issues_found['missing_data'])}")
        print(f"    - Incomplete records: {len(self.issues_found['incomplete_records'])}")
        print(f"    - Technical errors: {len(self.issues_found['technical_errors'])}")
        print(f"    - Needs manual verification: {len(self.issues_found['needs_manual_verification'])}")

        return self.issues_found

    def _analyze_file_quality(self, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze quality of a single file."""
        issues = []

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Check for common issues
            issues.extend(self._check_missing_fields(data, file_path))
            issues.extend(self._check_incomplete_records(data, file_path))
            issues.extend(self._check_data_consistency(data, file_path))
            issues.extend(self._check_technical_errors(data, file_path))

        except json.JSONDecodeError as e:
            issues.append({
                "type": "technical_error",
                "error": f"JSON decode error: {str(e)}",
                "severity": "high"
            })
        except Exception as e:
            issues.append({
                "type": "technical_error",
                "error": str(e),
                "severity": "medium"
            })

        return issues

    def _check_missing_fields(self, data: Any, file_path: Path) -> List[Dict[str, Any]]:
        """Check for missing critical fields."""
        issues = []

        if isinstance(data, dict):
            # Check for common missing fields
            critical_fields = ['name', 'id', 'state', 'status', 'date', 'license']

            for field in critical_fields:
                if field not in data and self._is_expected_field(data, field):
                    issues.append({
                        "type": "missing_data",
                        "field": field,
                        "severity": "medium",
                        "can_populate": self._can_populate_field(data, field)
                    })

        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    item_issues = self._check_missing_fields(item, file_path)
                    for issue in item_issues:
                        issue["index"] = i
                        issues.append(issue)

        return issues

    def _check_incomplete_records(self, data: Any, file_path: Path) -> List[Dict[str, Any]]:
        """Check for incomplete records."""
        issues = []

        if isinstance(data, dict):
            # Check if record seems incomplete
            if len(data) < 2:  # Very sparse record
                issues.append({
                    "type": "incomplete_record",
                    "field_count": len(data),
                    "severity": "medium"
                })

            # Check for empty string values
            for key, value in data.items():
                if value == "" or value is None:
                    issues.append({
                        "type": "incomplete_record",
                        "field": key,
                        "value": value,
                        "severity": "low"
                    })

        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, dict):
                    item_issues = self._check_incomplete_records(item, file_path)
                    for issue in item_issues:
                        issue["index"] = i
                        issues.append(issue)

        return issues

    def _check_data_consistency(self, data: Any, file_path: Path) -> List[Dict[str, Any]]:
        """Check for data consistency issues."""
        issues = []

        if isinstance(data, dict):
            # Check state/jurisdiction consistency
            if 'state' in data and 'jurisdiction' in data:
                state_norm = normalize_state(data.get('state', ''))
                juris_norm = normalize_state(data.get('jurisdiction', ''))
                if state_norm != juris_norm and state_norm and juris_norm:
                    issues.append({
                        "type": "consistency_issue",
                        "field1": "state",
                        "field2": "jurisdiction",
                        "values": [data.get('state'), data.get('jurisdiction')],
                        "severity": "medium"
                    })

            # Check date consistency
            date_fields = [k for k in data.keys() if 'date' in k.lower()]
            for date_field in date_fields:
                date_value = data.get(date_field)
                if date_value and not self._is_valid_date_format(date_value):
                    issues.append({
                        "type": "consistency_issue",
                        "field": date_field,
                        "value": date_value,
                        "severity": "low"
                    })

        return issues

    def _check_technical_errors(self, data: Any, file_path: Path) -> List[Dict[str, Any]]:
        """Check for technical errors."""
        issues = []

        if isinstance(data, dict):
            # Check for malformed data
            for key, value in data.items():
                # Check for encoding issues
                if isinstance(value, str):
                    try:
                        value.encode('utf-8')
                    except UnicodeEncodeError:
                        issues.append({
                            "type": "technical_error",
                            "field": key,
                            "error": "encoding_issue",
                            "severity": "high"
                        })

                # Check for unexpected types
                if key in ['date', 'timestamp'] and not isinstance(value, (str, int, float)):
                    issues.append({
                        "type": "technical_error",
                        "field": key,
                        "error": "unexpected_type",
                        "severity": "medium"
                    })

        return issues

    def _is_expected_field(self, data: Dict, field: str) -> bool:
        """Check if field is expected for this data type."""
        # Heuristic: if similar fields exist, this field might be expected
        similar_fields = {
            'name': ['title', 'company', 'person', 'entity'],
            'id': ['identifier', 'number', 'code'],
            'state': ['jurisdiction', 'location', 'region'],
            'status': ['state', 'condition', 'result'],
            'date': ['timestamp', 'time', 'created', 'updated'],
            'license': ['licensure', 'permit', 'registration']
        }

        if field in similar_fields:
            return any(similar in data for similar in similar_fields[field])
        return False

    def _can_populate_field(self, data: Dict, field: str) -> bool:
        """Check if field can be populated from existing data."""
        # Try to infer from context - be more aggressive
        if field == 'state':
            # Check multiple possible sources
            return any(key in data for key in ['jurisdiction', 'location', 'region', 'state_code', 'state_abbrev'])
        if field == 'jurisdiction':
            return any(key in data for key in ['state', 'location', 'region'])
        if field == 'date':
            return any(key in data for key in ['timestamp', 'created', 'updated', 'date_created', 'date_updated', 'search_date'])
        if field == 'name':
            return any(key in data for key in ['title', 'company', 'person', 'entity', 'firm', 'organization'])
        if field == 'id':
            return any(key in data for key in ['identifier', 'number', 'code', 'license_number', 'registration_number'])
        if field == 'status':
            return any(key in data for key in ['result', 'outcome', 'condition', 'state'])
        if field == 'license':
            return any(key in data for key in ['license_number', 'licensure', 'permit', 'registration'])
        return False

    def _is_valid_date_format(self, value: Any) -> bool:
        """Check if value is a valid date format."""
        if isinstance(value, (int, float)):
            return True  # Unix timestamp
        if isinstance(value, str):
            # Check common date formats
            date_patterns = [
                r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
                r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
                r'\d{4}_\d{2}_\d{2}',  # YYYY_MM_DD
            ]
            return any(re.match(pattern, value) for pattern in date_patterns)
        return False

    def _categorize_issues(self, file_path: Path, issues: List[Dict[str, Any]]):
        """Categorize issues by type."""
        for issue in issues:
            issue["file"] = str(file_path)

            if issue["type"] == "missing_data":
                self.issues_found["missing_data"].append(issue)
            elif issue["type"] == "incomplete_record":
                self.issues_found["incomplete_records"].append(issue)
            elif issue["type"] == "technical_error":
                self.issues_found["technical_errors"].append(issue)
            elif issue["type"] == "consistency_issue":
                if issue.get("severity") == "high":
                    self.issues_found["needs_manual_verification"].append(issue)

    def populate_missing_data(self) -> Dict[str, Any]:
        """Populate missing data where possible."""
        print("\n" + "=" * 80)
        print("POPULATING MISSING DATA")
        print("=" * 80)

        populated = {
            "files_updated": 0,
            "fields_populated": 0,
            "populations": []
        }

        # Group issues by file
        files_to_fix = defaultdict(list)
        for issue in self.issues_found["missing_data"]:
            if issue.get("can_populate"):
                files_to_fix[issue["file"]].append(issue)

        print(f"\nPopulating data in {len(files_to_fix)} files...")

        for file_path_str, issues in files_to_fix.items():
            file_path = Path(file_path_str)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                original_data = json.dumps(data, sort_keys=True)
                updated = False

                for issue in issues:
                    field = issue.get("field")
                    if self._populate_field(data, field):
                        populated["fields_populated"] += 1
                        populated["populations"].append({
                            "file": str(file_path),
                            "field": field,
                            "method": "inferred"
                        })
                        updated = True

                if updated:
                    # Write updated data
                    normalized_data = normalize_dict_recursive(data)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(normalized_data, f, indent=2, ensure_ascii=False)

                    populated["files_updated"] += 1
                    self.stats["issues_fixed"] += len(issues)

            except Exception as e:
                self.issues_found["technical_errors"].append({
                    "file": str(file_path),
                    "error": f"Population error: {str(e)}",
                    "type": "population_error"
                })

        print(f"\n  Files updated: {populated['files_updated']}")
        print(f"  Fields populated: {populated['fields_populated']}")

        self.issues_found["populated_data"] = populated["populations"]
        return populated

    def _populate_field(self, data: Any, field: str) -> bool:
        """Populate a missing field in data structure."""
        if isinstance(data, dict):
            if field not in data or data.get(field) in [None, "", "null"]:
                # Try to populate from related fields - be more aggressive
                populated = False

                if field == 'state':
                    for source in ['jurisdiction', 'location', 'region', 'state_code', 'state_abbrev']:
                        if source in data and data[source]:
                            data[field] = normalize_state(data[source])
                            populated = True
                            break

                elif field == 'jurisdiction':
                    for source in ['state', 'location', 'region']:
                        if source in data and data[source]:
                            data[field] = normalize_state(data[source])
                            populated = True
                            break

                elif field == 'date':
                    for source in ['timestamp', 'created', 'updated', 'date_created', 'date_updated', 'search_date']:
                        if source in data:
                            value = data[source]
                            if isinstance(value, (int, float)) and value > 0:
                                from datetime import datetime
                                data[field] = datetime.fromtimestamp(value).isoformat()
                                populated = True
                                break
                            elif isinstance(value, str) and value:
                                data[field] = value
                                populated = True
                                break

                elif field == 'name':
                    for source in ['title', 'company', 'person', 'entity', 'firm', 'organization', 'business_name']:
                        if source in data and data[source]:
                            data[field] = data[source]
                            populated = True
                            break

                elif field == 'id':
                    for source in ['identifier', 'number', 'code', 'license_number', 'registration_number', 'file_number']:
                        if source in data and data[source]:
                            data[field] = str(data[source])
                            populated = True
                            break

                elif field == 'status':
                    for source in ['result', 'outcome', 'condition', 'state', 'verification_status']:
                        if source in data and data[source]:
                            data[field] = data[source]
                            populated = True
                            break

                elif field == 'license':
                    for source in ['license_number', 'licensure', 'permit', 'registration', 'license_id']:
                        if source in data and data[source]:
                            data[field] = data[source]
                            populated = True
                            break

                return populated

        elif isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    if self._populate_field(item, field):
                        return True

        return False

    def generate_manual_verification_report(self) -> Path:
        """Generate report for items needing manual verification."""
        print("\n" + "=" * 80)
        print("GENERATING MANUAL VERIFICATION REPORT")
        print("=" * 80)

        report = {
            "generated_date": datetime.now().isoformat(),
            "summary": {
                "total_items": len(self.issues_found["needs_manual_verification"]),
                "high_priority": len([i for i in self.issues_found["needs_manual_verification"]
                                     if i.get("severity") == "high"]),
                "medium_priority": len([i for i in self.issues_found["needs_manual_verification"]
                                       if i.get("severity") == "medium"])
            },
            "items": self.issues_found["needs_manual_verification"],
            "technical_errors": self.issues_found["technical_errors"],
            "incomplete_records": self.issues_found["incomplete_records"][:100]  # First 100
        }

        report_path = DATA_PROCESSED_DIR / "manual_verification_report.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"\n  Report generated: {report_path}")
        print(f"  Items needing verification: {report['summary']['total_items']}")
        print(f"  High priority: {report['summary']['high_priority']}")
        print(f"  Technical errors: {len(report['technical_errors'])}")

        return report_path

    def run_full_cleaning(self) -> Dict[str, Any]:
        """Run complete cleaning and population process."""
        print("=" * 80)
        print("DATA CLEANING AND POPULATION SYSTEM")
        print("=" * 80)

        results = {
            "analysis": {},
            "population": {},
            "report_path": None,
            "stats": {}
        }

        # Step 1: Analyze data quality
        results["analysis"] = self.analyze_data_quality()

        # Step 2: Populate missing data
        results["population"] = self.populate_missing_data()

        # Step 3: Generate manual verification report
        results["report_path"] = str(self.generate_manual_verification_report())

        # Step 4: Final stats
        results["stats"] = {
            "files_analyzed": self.stats["files_analyzed"],
            "issues_found": self.stats["issues_found"],
            "issues_fixed": self.stats["issues_fixed"],
            "needs_manual_review": len(self.issues_found["needs_manual_verification"])
        }

        print("\n" + "=" * 80)
        print("CLEANING COMPLETE")
        print("=" * 80)
        print(f"  Files analyzed: {results['stats']['files_analyzed']}")
        print(f"  Issues found: {results['stats']['issues_found']}")
        print(f"  Issues fixed: {results['stats']['issues_fixed']}")
        print(f"  Needs manual review: {results['stats']['needs_manual_review']}")
        print(f"  Report: {results['report_path']}")
        print("=" * 80)

        return results


def main():
    """Main execution."""
    cleaner = DataCleaningAndPopulation()
    results = cleaner.run_full_cleaning()

    # Save results
    results_path = DATA_PROCESSED_DIR / "data_cleaning_results.json"
    with open(results_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {results_path}")
    return results


if __name__ == "__main__":
    main()
