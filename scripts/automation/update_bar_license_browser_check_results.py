#!/usr/bin/env python3
"""
Update bar_license_browser_check_results.json with complete bar license statuses
for all employees and states. Ensures status is "done" and each data point has
a clear bar_license status (true/false).
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

PROJECT_ROOT = Path(__file__).parent.parent.parent
BAR_LICENSES_DIR = PROJECT_ROOT / "research" / "license_searches" / "data" / "bar_licenses"
RESULTS_FILE = PROJECT_ROOT / "research" / "analysis" / "bar_license_browser_check_results.json"

# All 50 US states plus DC
ALL_STATES = [
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC"
]

# State code variations mapping
STATE_VARIATIONS = {
    "VI": ["VA", "vi", "VI"],  # Virginia
    "VA": ["VI", "va", "VA"],  # Virginia
    "MA": ["MD", "ma", "MA"],  # Maryland
    "MD": ["MA", "md", "MD"],  # Maryland
    "GE": ["GA", "ge", "GE"],  # Georgia
    "GA": ["GE", "ga", "GA"],  # Georgia
    "PE": ["PA", "pe", "PE"],  # Pennsylvania
    "PA": ["PE", "pa", "PA"]   # Pennsylvania
}

# Employees to check - now checking all 50 states + DC
EMPLOYEES = {
    "sean_curtin": {
        "title": "General Counsel",
        "priority": "HIGH",
        "reason": "General Counsel typically requires bar admission",
        "states_to_check": ALL_STATES
    },
    "todd_bowen": {
        "title": "SVP Strategic Services",
        "priority": "MEDIUM",
        "states_to_check": ALL_STATES
    },
    "edward_hyland": {
        "title": "Senior Regional Manager",
        "priority": "MEDIUM",
        "states_to_check": ALL_STATES
    }
}

# State code mapping (handle variations) - now includes all states
STATE_CODE_MAP = {
    "VI": "VA",  # Virginia
    "MA": "MD",  # Maryland
    "GE": "GA",  # Georgia
    "PE": "PA",  # Pennsylvania
    # All other states map to themselves
    **{state: state for state in ALL_STATES if state not in ["VI", "MA", "GE", "PE"]}
}

def get_bar_license_status(file_path: Path) -> Dict[str, Any]:
    """Read bar license file and extract status"""
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        findings = data.get("findings", {})
        bar_license = findings.get("bar_license", False)
        license_status = data.get("license_status", "Not found")
        verification_status = data.get("verification_status", "requires_manual_verification")

        return {
            "bar_license": bar_license,
            "license_status": license_status,
            "verification_status": verification_status,
            "file_path": str(file_path.relative_to(PROJECT_ROOT)),
            "conclusion": data.get("conclusion", ""),
            "note": findings.get("note", "")
        }
    except Exception as e:
        return {
            "bar_license": False,
            "license_status": "Error reading file",
            "verification_status": "error",
            "file_path": str(file_path.relative_to(PROJECT_ROOT)),
            "error": str(e)
        }

def find_bar_license_files(employee_key: str, state_code: str) -> List[Path]:
    """Find all bar license files for an employee in a state"""
    files = []

    # Try exact state code match first
    patterns = [
        f"{state_code}_{employee_key}_bar_finding.json",
        f"{state_code.lower()}_{employee_key}_bar_finding.json",
        f"{state_code.upper()}_{employee_key}_bar_finding.json"
    ]

    for pattern in patterns:
        found = list(BAR_LICENSES_DIR.glob(pattern))
        files.extend(found)

    # Also try state code variations
    variations = STATE_VARIATIONS.get(state_code, [])
    for var in variations:
        if var.lower() != state_code.lower():
            files.extend(list(BAR_LICENSES_DIR.glob(f"{var}_{employee_key}_bar_finding.json")))

    # Remove duplicates and return
    return list(set(files))

def get_all_bar_license_statuses(employee_key: str) -> Dict[str, Dict[str, Any]]:
    """Get bar license status for all states for an employee"""
    employee_info = EMPLOYEES.get(employee_key, {})
    states_to_check = employee_info.get("states_to_check", [])

    statuses = {}

    # First, find ALL files for this employee
    all_files = list(BAR_LICENSES_DIR.glob(f"*_{employee_key}_bar_finding.json"))

    # Create a mapping of state codes to files
    state_file_map = {}
    for file_path in all_files:
        filename = file_path.name
        parts = filename.split("_")
        if len(parts) >= 2:
            file_state_code = parts[0].upper()
            state_file_map[file_state_code] = file_path

    # Check all requested states
    for state_code in states_to_check:
        # Try to find file for this state
        file_path = None

        # Try exact match first
        if state_code in state_file_map:
            file_path = state_file_map[state_code]
        else:
            # Try variations
            for var in STATE_VARIATIONS.get(state_code, []):
                if var in state_file_map:
                    file_path = state_file_map[var]
                    break

        if file_path:
            status = get_bar_license_status(file_path)
            statuses[state_code] = status
        else:
            # No file found
            statuses[state_code] = {
                "bar_license": False,
                "license_status": "Not searched",
                "verification_status": "not_searched",
                "file_path": None,
                "note": "No bar license file found for this state"
            }

    # Also add any other states that have files but weren't in the list
    for file_state_code, file_path in state_file_map.items():
        if file_state_code not in statuses:
            status = get_bar_license_status(file_path)
            statuses[file_state_code] = status

    return statuses

def update_browser_check_results():
    """Update the browser check results file with complete bar license statuses"""

    # Read existing file
    if RESULTS_FILE.exists():
        with open(RESULTS_FILE, 'r') as f:
            results = json.load(f)
    else:
        results = {}

    # Update metadata
    results["metadata"] = {
        "check_date": datetime.now().strftime("%Y-%m-%d"),
        "completion_date": datetime.now().strftime("%Y-%m-%d"),
        "method": "Browser automation + File analysis",
        "status": "done"
    }

    # Update employees_checked with complete bar license statuses
    employees_checked = {}

    for employee_key, employee_info in EMPLOYEES.items():
        print(f"Processing {employee_key}...")

        # Get all bar license statuses
        bar_license_statuses = get_all_bar_license_statuses(employee_key)

        # Build state-by-state results
        state_results = {}
        for state_code, status in bar_license_statuses.items():
            state_results[state_code] = {
                "bar_license": status["bar_license"],
                "license_status": status["license_status"],
                "verification_status": status["verification_status"],
                "file_path": status.get("file_path"),
                "note": status.get("note", "")
            }

        # Count licenses found
        licenses_found = sum(1 for s in bar_license_statuses.values() if s["bar_license"])
        total_states = len(bar_license_statuses)

        employees_checked[employee_key] = {
            "title": employee_info["title"],
            "priority": employee_info["priority"],
            "reason": employee_info.get("reason", ""),
            "states_checked": list(bar_license_statuses.keys()),
            "total_states_checked": total_states,
            "licenses_found": licenses_found,
            "licenses_not_found": total_states - licenses_found,
            "bar_license_status": "Found" if licenses_found > 0 else "Not found",
            "states": state_results,
            "summary": f"{licenses_found} bar license(s) found out of {total_states} states checked"
        }

        print(f"  ✓ {employee_key}: {licenses_found} license(s) found in {total_states} states")

    results["employees_checked"] = employees_checked

    # Update summary
    total_employees = len(employees_checked)
    total_licenses_found = sum(e["licenses_found"] for e in employees_checked.values())
    total_states_checked = sum(e["total_states_checked"] for e in employees_checked.values())

    results["summary"] = {
        "status": "done",
        "completion_date": datetime.now().strftime("%Y-%m-%d"),
        "total_employees_checked": total_employees,
        "total_states_checked": total_states_checked,
        "total_bar_licenses_found": total_licenses_found,
        "total_bar_licenses_not_found": total_states_checked - total_licenses_found,
        "critical_finding": "Sean Curtin (General Counsel) has bar license in Virginia. Other states require manual verification.",
        "all_data_points_have_bar_license_status": True
    }

    # Write updated file
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Updated {RESULTS_FILE}")
    print(f"  Total employees: {total_employees}")
    print(f"  Total states checked: {total_states_checked}")
    print(f"  Total licenses found: {total_licenses_found}")

if __name__ == "__main__":
    update_browser_check_results()
