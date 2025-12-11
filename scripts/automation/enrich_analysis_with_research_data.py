#!/usr/bin/env python3
"""
Enrich analysis JSON files with data from other research sources.
Cross-references employee data, license data, and violation data.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent
ANALYSIS_DIR = PROJECT_ROOT / "research" / "analysis"
EMPLOYEES_DIR = PROJECT_ROOT / "research" / "employees" / "data"
LICENSE_DIR = PROJECT_ROOT / "research" / "license_searches" / "data"
VA_DPOR_DIR = PROJECT_ROOT / "research" / "va_dpor_complaint"
COMPANY_REG_DIR = PROJECT_ROOT / "research" / "company_registrations" / "data"

def load_employee_data() -> Dict[str, Any]:
    """Load employee data"""
    employee_files = [
        EMPLOYEES_DIR / "employee_roles.json",
        EMPLOYEES_DIR / "job_descriptions.json",
        EMPLOYEES_DIR / "organizational_chart.json"
    ]

    data = {}
    for file_path in employee_files:
        if file_path.exists():
            with open(file_path, 'r') as f:
                file_data = json.load(f)
                filename = file_path.stem
                data[filename] = file_data

    return data

def load_license_data() -> Dict[str, Any]:
    """Load key license verification data"""
    license_file = VA_DPOR_DIR / "personnel_license_verification.json"

    if license_file.exists():
        with open(license_file, 'r') as f:
            return json.load(f)

    return {}

def load_violation_data() -> Dict[str, Any]:
    """Load violation data"""
    violation_files = [
        VA_DPOR_DIR / "additional_regulatory_violations.json",
        VA_DPOR_DIR / "unlicensed_activities_documentation.json",
        VA_DPOR_DIR / "50_mile_rule_violations.json"
    ]

    data = {}
    for file_path in violation_files:
        if file_path.exists():
            with open(file_path, 'r') as f:
                file_data = json.load(f)
                filename = file_path.stem
                data[filename] = file_data

    return data

def enrich_connection_matrix(data: Dict[str, Any], employee_data: Dict[str, Any], license_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich connection matrix with employee and license data"""
    if "violation_entity_connections" in data and isinstance(data["violation_entity_connections"], list) and len(data["violation_entity_connections"]) == 0:
        # Add violation connections from unlicensed activities
        violations = []

        if "unlicensed_activities_documentation" in license_data:
            activities = license_data.get("unlicensed_activities_documentation", {}).get("activities_documented", [])
            for activity in activities:
                violations.append({
                    "personnel": activity.get("personnel", ""),
                    "activity_type": activity.get("activity_type", ""),
                    "date": activity.get("date", ""),
                    "violation": activity.get("violation", ""),
                    "connection_type": "unlicensed_activity"
                })

        if violations:
            data["violation_entity_connections"] = violations

    # Add employee count from employee data
    if "employee_data" not in data:
        if "employee_roles" in employee_data:
            roles = employee_data["employee_roles"].get("employees", {})
            data["employee_count"] = len(roles)
            data["unlicensed_employee_count"] = sum(1 for emp in roles.values() if emp.get("performs_licensed_activities") and not emp.get("licensed", False))

    return data

def enrich_hyland_upl_investigation(data: Dict[str, Any], license_data: Dict[str, Any], violation_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich Hyland UPL investigation with actual data"""
    if "upl_indicators" in data and isinstance(data["upl_indicators"], list) and len(data["upl_indicators"]) == 0:
        # Add UPL indicators from unlicensed activities
        indicators = []

        if "unlicensed_activities_documentation" in violation_data:
            activities = violation_data["unlicensed_activities_documentation"].get("activities_documented", [])
            for activity in activities:
                if activity.get("personnel") == "Edward Hyland":
                    indicators.append({
                        "date": activity.get("date", ""),
                        "activity": activity.get("activity_type", ""),
                        "description": activity.get("description", ""),
                        "violation": activity.get("violation", ""),
                        "legal_basis": activity.get("legal_basis", "")
                    })

        if indicators:
            data["upl_indicators"] = indicators

    if "ra_denial_analysis" in data and isinstance(data["ra_denial_analysis"], list) and len(data["ra_denial_analysis"]) == 0:
        # Add RA denial analysis
        if "unlicensed_activities_documentation" in violation_data:
            activities = violation_data["unlicensed_activities_documentation"].get("activities_documented", [])
            for activity in activities:
                if "reasonable accommodation" in activity.get("activity_type", "").lower():
                    data["ra_denial_analysis"] = [{
                        "date": activity.get("date", ""),
                        "personnel": activity.get("personnel", ""),
                        "description": activity.get("description", ""),
                        "violation": activity.get("violation", ""),
                        "evidence": activity.get("evidence", [])
                    }]
                    break

    return data

def enrich_hyland_verification(data: Dict[str, Any], license_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich Hyland verification with license search results"""
    if "claims_to_verify" in data:
        licensing = data["claims_to_verify"].get("licensing_status", {})

        if "all_states" in licensing:
            all_states = licensing["all_states"]
            if "states_searched" in all_states and isinstance(all_states["states_searched"], list) and len(all_states["states_searched"]) == 0:
                # Add states searched from license verification
                if "personnel_list" in license_data:
                    for personnel in license_data["personnel_list"]:
                        if personnel.get("name") == "Edward Hyland":
                            license_verification = personnel.get("license_verification", {})
                            states_searched = list(license_verification.keys())
                            all_states["states_searched"] = states_searched
                            all_states["status"] = "verified_unlicensed" if all(st.get("status") == "not_found" for st in license_verification.values()) else "partial"
                            break

    return data

def enrich_news_violations_search(data: Dict[str, Any], violation_data: Dict[str, Any]) -> Dict[str, Any]:
    """Enrich news violations search with known violations"""
    if "violations_found" in data and isinstance(data["violations_found"], list) and len(data["violations_found"]) == 0:
        # Add known violations from additional_regulatory_violations
        if "additional_regulatory_violations" in violation_data:
            violations = violation_data["additional_regulatory_violations"].get("known_violations", [])
            data["violations_found"] = violations

    return data

def enrich_all_analysis_files():
    """Enrich all analysis files with cross-referenced data"""
    print("Loading research data...")
    employee_data = load_employee_data()
    license_data = load_license_data()
    violation_data = load_violation_data()

    print(f"Loaded: {len(employee_data)} employee files, license data, {len(violation_data)} violation files")
    print()

    json_files = list(ANALYSIS_DIR.glob("*.json"))
    print(f"Found {len(json_files)} JSON files to enrich")
    print()

    updated_count = 0

    for file_path in sorted(json_files):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)

            original = json.dumps(data, sort_keys=True)
            filename = file_path.name

            # File-specific enrichment
            if filename == "connection_matrix.json":
                data = enrich_connection_matrix(data, employee_data, violation_data)
            elif filename == "hyland_upl_investigation.json":
                data = enrich_hyland_upl_investigation(data, license_data, violation_data)
            elif filename == "hyland_verification.json":
                data = enrich_hyland_verification(data, license_data)
            elif filename == "news_violations_search.json":
                data = enrich_news_violations_search(data, violation_data)

            # Check if changed
            new_data = json.dumps(data, sort_keys=True)
            if original != new_data:
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                updated_count += 1
                print(f"  ✓ Enriched {filename}")
            else:
                print(f"  - {filename}")

        except Exception as e:
            print(f"  ✗ Error enriching {file_path.name}: {e}")

    print()
    print(f"{'='*60}")
    print(f"Enrichment complete:")
    print(f"  ✓ {updated_count} files enriched with cross-referenced data")
    print(f"  - {len(json_files) - updated_count} files already complete")

if __name__ == "__main__":
    enrich_all_analysis_files()
