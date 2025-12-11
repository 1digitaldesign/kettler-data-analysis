#!/usr/bin/env python3
"""
Populate analysis JSON files with actual data from company registration files
and other data sources. Ensures all fields are populated with real data.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent
ANALYSIS_DIR = PROJECT_ROOT / "research" / "analysis"
COMPANY_REG_DIR = PROJECT_ROOT / "research" / "company_registrations" / "data"

def load_company_registration_data(state_code: str) -> Dict[str, Any]:
    """Load company registration data for a state"""
    state_map = {
        "maryland": "md",
        "dc": "dc",
        "connecticut": "ct",
        "new_jersey": "nj",
        "new_york": "ny"
    }

    state_lower = state_code.lower()
    file_state = state_map.get(state_lower, state_lower)

    # Try multiple file patterns
    patterns = [
        f"{file_state}/kettler_management_inc_registration.json",
        f"{state_lower}/kettler_management_inc_registration.json",
        f"maryland/maryland_kettler_management_inc_registration.json" if state_lower == "maryland" else None,
        f"dc/dc_kettler_management_inc_registration.json" if state_lower == "dc" else None,
        f"connecticut/connecticut_kettler_management_inc_registration.json" if state_lower == "connecticut" else None,
        f"new_jersey/new_jersey_kettler_management_inc_registration.json" if state_lower == "new_jersey" else None,
        f"new_york/new_york_kettler_management_inc_registration.json" if state_lower == "new_york" else None
    ]

    for pattern in patterns:
        if pattern:
            file_path = COMPANY_REG_DIR / pattern
            if file_path.exists():
                try:
                    with open(file_path, 'r') as f:
                        return json.load(f)
                except:
                    pass

    return None

def populate_cross_reference_analysis():
    """Populate cross-reference analysis with actual company registration data"""
    file_path = ANALYSIS_DIR / "virginia_scc_cross_reference_analysis.json"

    if not file_path.exists():
        return False

    with open(file_path, 'r') as f:
        data = json.load(f)

    # Update cross-state analysis with actual registration data
    if "cross_state_analysis" in data:
        state_map = {
            "maryland": "Maryland",
            "dc": "dc",
            "connecticut": "Connecticut",
            "new_jersey": "New Jersey",
            "new_york": "New York"
        }

        for state_key, state_name in state_map.items():
            if state_key in data["cross_state_analysis"]:
                reg_data = load_company_registration_data(state_key)

                if reg_data and "findings" in reg_data:
                    findings = reg_data["findings"]
                    state_data = data["cross_state_analysis"][state_key]

                    # Update with actual data
                    if "registered" in findings:
                        state_data["registered"] = findings["registered"]
                        if findings["registered"] == False:
                            state_data["status"] = "NOT REGISTERED"
                            state_data["status_detail"] = "not_registered"
                            # Update abnormality to reflect verified status
                            if "abnormality" in state_data:
                                state_data["abnormality"] = state_data["abnormality"].replace("status unknown", "NOT REGISTERED - verified via state database search")
                        else:
                            state_data["status"] = "REGISTERED"
                            state_data["status_detail"] = "registered"

                    if "entity_type" in findings and findings["entity_type"] is not None:
                        state_data["entity_type"] = findings["entity_type"]

                    if "formation_date" in findings:
                        if findings["formation_date"] is not None:
                            state_data["formation_date"] = findings["formation_date"]
                        else:
                            state_data["formation_date"] = None

                    if "registered_agent" in findings and findings["registered_agent"] is not None:
                        state_data["registered_agent"] = findings["registered_agent"]

                    if "business_address" in findings and findings["business_address"] is not None:
                        state_data["business_address"] = findings["business_address"]

                    if "status" in findings and findings["status"] is not None:
                        state_data["status_detail"] = findings["status"]

                    # Update search info from metadata
                    if "metadata" in reg_data:
                        meta = reg_data["metadata"]
                        if "search_url" in meta:
                            state_data["search_url"] = meta["search_url"]
                        if "search_method" in meta:
                            state_data["search_method"] = meta["search_method"]
                        if "date" in meta:
                            state_data["search_date"] = meta["date"]

    # Write updated file
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return True

def populate_all_analysis_files():
    """Populate all analysis files with actual data"""
    print("Populating analysis files with actual data...")

    updated = populate_cross_reference_analysis()

    if updated:
        print("  ✓ Updated virginia_scc_cross_reference_analysis.json with actual registration data")
    else:
        print("  - No updates needed")

    print("\n✓ Population complete")

if __name__ == "__main__":
    populate_all_analysis_files()
