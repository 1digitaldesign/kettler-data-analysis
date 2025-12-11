#!/usr/bin/env python3
"""
Audit Whistleblower and Private Citizen Reporting Forms
Identifies all available forms for reporting wrongdoing to government agencies
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Set
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR

print("🔍 Auditing Whistleblower and Private Citizen Reporting Forms")


class WhistleblowerFormAuditor:
    """Audit whistleblower and citizen reporting forms"""

    def __init__(self):
        self.all_forms = []
        self.whistleblower_forms = []
        self.citizen_forms = []
        self.complaint_forms = []
        self.tip_forms = []
        self.missing_forms = []

    def load_law_references(self):
        """Load law references and extract all forms"""
        print("\n📂 Loading law references...")

        law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
        if not law_file.exists():
            print(f"❌ Law references file not found: {law_file}")
            return

        with open(law_file, 'r', encoding='utf-8') as f:
            self.laws = json.load(f)

        # Extract all forms
        self._extract_all_forms(self.laws)

        print(f"   Found {len(self.all_forms)} total forms")
        print(f"   Whistleblower forms: {len(self.whistleblower_forms)}")
        print(f"   Citizen complaint forms: {len(self.citizen_forms)}")
        print(f"   Tip forms: {len(self.tip_forms)}")

    def _extract_all_forms(self, data: Any, path: str = ""):
        """Recursively extract all reporting forms"""
        if isinstance(data, dict):
            # Check for reporting_forms
            if "reporting_forms" in data:
                for form in data["reporting_forms"]:
                    form_info = {
                        "form_name": form.get("form_name", ""),
                        "form_number": form.get("form_number", ""),
                        "agency": form.get("agency", ""),
                        "url": form.get("url", ""),
                        "description": form.get("description", ""),
                        "form_type": form.get("form_type", ""),
                        "law": data.get("name", ""),
                        "path": path
                    }
                    self.all_forms.append(form_info)

                    # Categorize
                    desc_lower = form_info["description"].lower()
                    name_lower = form_info["form_name"].lower()
                    combined = f"{desc_lower} {name_lower}"

                    if any(term in combined for term in ["whistleblower", "whistle-blower", "whistle blower"]):
                        self.whistleblower_forms.append(form_info)

                    if any(term in combined for term in ["citizen", "private", "public", "individual"]):
                        self.citizen_forms.append(form_info)

                    if "complaint" in combined:
                        self.complaint_forms.append(form_info)

                    if any(term in combined for term in ["tip", "tips", "tip line", "hotline"]):
                        self.tip_forms.append(form_info)

            # Recursively process
            for key, value in data.items():
                if key not in ["embedding", "embedding_text", "ground_truth_embedding", "ground_truth_text"]:
                    sub_path = f"{path}.{key}" if path else key
                    self._extract_all_forms(value, sub_path)

        elif isinstance(data, list):
            for i, item in enumerate(data):
                self._extract_all_forms(item, f"{path}[{i}]")

    def identify_missing_forms(self):
        """Identify common whistleblower/citizen forms that may be missing"""
        print("\n🔍 Identifying potentially missing forms...")

        # Known whistleblower/citizen reporting mechanisms
        known_forms = {
            # Federal
            "FBI Tip Line": {"agency": "FBI", "type": "tip"},
            "IRS Whistleblower (Form 211)": {"agency": "IRS", "type": "whistleblower"},
            "SEC Whistleblower (TCR Form)": {"agency": "SEC", "type": "whistleblower"},
            "FTC Consumer Complaint": {"agency": "FTC", "type": "complaint"},
            "HUD Fair Housing Complaint": {"agency": "HUD", "type": "complaint"},
            "DOJ Civil Rights Complaint": {"agency": "DOJ", "type": "complaint"},
            "USPIS Mail Fraud Report": {"agency": "USPIS", "type": "report"},
            "IC3 Internet Crime Complaint": {"agency": "FBI/IC3", "type": "complaint"},
            "CFPB Consumer Complaint": {"agency": "CFPB", "type": "complaint"},
            "OSHA Whistleblower Complaint": {"agency": "OSHA", "type": "whistleblower"},
            "DOL Whistleblower Complaint": {"agency": "DOL", "type": "whistleblower"},
            "FDA MedWatch": {"agency": "FDA", "type": "report"},
            "EPA Environmental Violation Report": {"agency": "EPA", "type": "report"},
            "FAA Aviation Safety Reporting": {"agency": "FAA", "type": "report"},
            "NHTSA Vehicle Safety Complaint": {"agency": "NHTSA", "type": "complaint"},
            "SSA Fraud Report": {"agency": "SSA", "type": "report"},
            "Medicare Fraud Report": {"agency": "CMS", "type": "report"},
            "Medicaid Fraud Report": {"agency": "CMS", "type": "report"},
            "Treasury Financial Crimes": {"agency": "Treasury/FinCEN", "type": "report"},
            "State Department Fraud": {"agency": "State Department", "type": "report"},

            # State (Virginia)
            "Virginia DPOR Complaint": {"agency": "DPOR", "type": "complaint"},
            "Virginia Attorney General Complaint": {"agency": "VA AG", "type": "complaint"},
            "Virginia Consumer Affairs": {"agency": "VA Consumer Affairs", "type": "complaint"},

            # State (Maryland)
            "Maryland Real Estate Commission Complaint": {"agency": "MD REC", "type": "complaint"},
            "Maryland Attorney General Complaint": {"agency": "MD AG", "type": "complaint"},

            # State (Texas)
            "Texas Real Estate Commission Complaint": {"agency": "TREC", "type": "complaint"},
            "Texas Attorney General Complaint": {"agency": "TX AG", "type": "complaint"},

            # Local
            "Local Law Enforcement": {"agency": "Local", "type": "report"},
            "Local Consumer Protection": {"agency": "Local", "type": "complaint"},
        }

        # Check which are present
        found_forms = set()
        for form in self.all_forms:
            form_name = form.get("form_name", "").lower()
            agency = form.get("agency", "").lower()
            for known_name, known_info in known_forms.items():
                if (known_info["agency"].lower() in agency or
                    any(word in form_name for word in known_name.lower().split())):
                    found_forms.add(known_name)

        # Identify missing
        self.missing_forms = [
            {"name": name, **info}
            for name, info in known_forms.items()
            if name not in found_forms
        ]

        print(f"   Known forms checked: {len(known_forms)}")
        print(f"   Forms found: {len(found_forms)}")
        print(f"   Potentially missing: {len(self.missing_forms)}")

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report"""
        print("\n📊 Generating audit report...")

        # Organize by agency
        by_agency = defaultdict(list)
        for form in self.all_forms:
            agency = form.get("agency", "Unknown")
            by_agency[agency].append(form)

        report = {
            "metadata": {
                "total_forms": len(self.all_forms),
                "whistleblower_forms": len(self.whistleblower_forms),
                "citizen_forms": len(self.citizen_forms),
                "complaint_forms": len(self.complaint_forms),
                "tip_forms": len(self.tip_forms),
                "unique_agencies": len(by_agency)
            },
            "forms_by_category": {
                "whistleblower": self.whistleblower_forms,
                "citizen_complaints": self.citizen_forms,
                "complaints": self.complaint_forms,
                "tips": self.tip_forms
            },
            "forms_by_agency": dict(by_agency),
            "all_forms": self.all_forms,
            "potentially_missing": self.missing_forms
        }

        return report


def main():
    """Main function"""
    print("=" * 80)
    print("🔍 Whistleblower & Private Citizen Form Audit")
    print("=" * 80)
    print()

    auditor = WhistleblowerFormAuditor()
    auditor.load_law_references()
    auditor.identify_missing_forms()

    report = auditor.generate_report()

    # Save report
    output_file = DATA_PROCESSED_DIR / "whistleblower_forms_audit.json"
    print(f"\n💾 Saving audit report to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    # Print summary
    print("\n" + "=" * 80)
    print("📊 AUDIT SUMMARY")
    print("=" * 80)
    print(f"Total Forms: {report['metadata']['total_forms']}")
    print(f"Whistleblower Forms: {report['metadata']['whistleblower_forms']}")
    print(f"Citizen Complaint Forms: {report['metadata']['citizen_forms']}")
    print(f"Complaint Forms: {report['metadata']['complaint_forms']}")
    print(f"Tip Forms: {report['metadata']['tip_forms']}")
    print(f"Unique Agencies: {report['metadata']['unique_agencies']}")
    print(f"\nPotentially Missing Forms: {len(report['potentially_missing'])}")

    if report['potentially_missing']:
        print("\n⚠️  Potentially Missing Forms:")
        for missing in report['potentially_missing'][:20]:
            print(f"  • {missing['name']} ({missing['agency']})")

    print("\n" + "=" * 80)
    print("✅ Audit Complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
