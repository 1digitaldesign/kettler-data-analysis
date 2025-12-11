#!/usr/bin/env python3
"""
Add comprehensive reporting forms to all law references
This script enhances the law references with government reporting forms
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT

# Standard reporting forms by violation type
REPORTING_FORMS_TEMPLATE = {
    "real_estate_licensing": [
        {
            "form_name": "State Real Estate Commission Complaint",
            "form_number": "Varies by state",
            "agency": "State Real Estate Commission",
            "url": "Contact state commission",
            "description": "File complaint against unlicensed real estate activity",
            "form_type": "Online or written complaint"
        }
    ],
    "tax_violations": [
        {
            "form_name": "IRS Form 3949-A",
            "form_number": "3949-A",
            "agency": "Internal Revenue Service",
            "url": "https://www.irs.gov/pub/irs-pdf/f3949a.pdf",
            "description": "Report suspected tax fraud or evasion",
            "form_type": "PDF form"
        }
    ],
    "criminal_fraud": [
        {
            "form_name": "FBI Tip Form",
            "form_number": "Online Tip",
            "agency": "Federal Bureau of Investigation",
            "url": "https://tips.fbi.gov/",
            "description": "Report federal crimes including fraud",
            "form_type": "Online submission"
        }
    ],
    "consumer_protection": [
        {
            "form_name": "FTC Consumer Complaint",
            "form_number": "Online Complaint",
            "agency": "Federal Trade Commission",
            "url": "https://www.ftccomplaintassistant.gov/",
            "description": "Report unfair or deceptive business practices",
            "form_type": "Online complaint"
        }
    ],
    "fair_housing": [
        {
            "form_name": "HUD Fair Housing Complaint",
            "form_number": "HUD-903.1",
            "agency": "Department of Housing and Urban Development",
            "url": "https://www.hud.gov/program_offices/fair_housing_equal_opp/online-complaint",
            "description": "Report housing discrimination",
            "form_type": "Online complaint"
        }
    ]
}


def add_forms_to_law_references(law_file: Path):
    """Add reporting forms to law references that don't have them"""
    print(f"Loading law references from {law_file}...")

    with open(law_file, 'r', encoding='utf-8') as f:
        laws = json.load(f)

    def add_forms_recursive(data: Any, path: str = ""):
        """Recursively add forms to law entries"""
        if isinstance(data, dict):
            # Check if this is a law entry (has name and relevance)
            if "name" in data and "relevance" in data and "reporting_forms" not in data:
                # Determine form type based on relevance
                relevance = data.get("relevance", "").lower()
                forms = []

                if "real estate" in relevance or "licensing" in relevance:
                    forms.extend(REPORTING_FORMS_TEMPLATE["real_estate_licensing"])
                if "tax" in relevance:
                    forms.extend(REPORTING_FORMS_TEMPLATE["tax_violations"])
                if "fraud" in relevance or "criminal" in relevance:
                    forms.extend(REPORTING_FORMS_TEMPLATE["criminal_fraud"])
                if "consumer" in relevance or "trade" in relevance:
                    forms.extend(REPORTING_FORMS_TEMPLATE["consumer_protection"])
                if "housing" in relevance or "discrimination" in relevance:
                    forms.extend(REPORTING_FORMS_TEMPLATE["fair_housing"])

                if forms:
                    data["reporting_forms"] = forms
                    print(f"  Added {len(forms)} forms to {path}")

            # Recursively process nested dictionaries
            for key, value in data.items():
                if key != "reporting_forms":  # Skip already processed
                    new_path = f"{path}.{key}" if path else key
                    add_forms_recursive(value, new_path)

        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                add_forms_recursive(item, new_path)

    print("Adding reporting forms to law references...")
    add_forms_recursive(laws)

    # Save updated file
    print(f"Saving updated law references to {law_file}...")
    with open(law_file, 'w', encoding='utf-8') as f:
        json.dump(laws, f, indent=2, ensure_ascii=False)

    print("✅ Completed adding reporting forms")


if __name__ == "__main__":
    law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
    if not law_file.exists():
        print(f"❌ Law references file not found: {law_file}")
        print("Please run create_law_references.py first")
        sys.exit(1)

    add_forms_to_law_references(law_file)
