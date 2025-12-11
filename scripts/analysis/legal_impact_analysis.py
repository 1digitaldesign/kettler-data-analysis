#!/usr/bin/env python3
"""
Legal Impact Analysis
Analyzes legal consequences, penalties, enforcement mechanisms, and compliance requirements
for discovered violations
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR

print("🔍 Legal Impact Analysis - Analyzing Legal Consequences")


class LegalImpactAnalyzer:
    """Analyze legal impacts and consequences of violations"""

    def __init__(self):
        self.violations = {}
        self.laws = {}
        self.forms = {}
        self.legal_impacts = defaultdict(list)
        self.penalties = defaultdict(list)
        self.enforcement_mechanisms = defaultdict(list)
        self.compliance_requirements = defaultdict(list)

    def load_data(self):
        """Load violations, laws, and connections"""
        print("\n📂 Loading data...")

        # Load violations with law matches
        violations_file = DATA_PROCESSED_DIR / "integrated_violations_with_laws.json"
        if violations_file.exists():
            with open(violations_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.violations = data.get("matched_violations", [])

        # Load law references
        law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
        if law_file.exists():
            with open(law_file, 'r', encoding='utf-8') as f:
                self.laws = json.load(f)

        # Load graph analysis for pathways
        graph_file = DATA_PROCESSED_DIR / "graph_theory_analysis.json"
        if graph_file.exists():
            with open(graph_file, 'r', encoding='utf-8') as f:
                self.graph_data = json.load(f)

        print(f"   Loaded {len(self.violations)} violations with law matches")
        print(f"   Loaded law references")

    def extract_legal_penalties(self, law_data: Dict[str, Any], path: str = "") -> List[Dict[str, Any]]:
        """Extract penalty information from law data"""
        penalties = []

        if isinstance(law_data, dict):
            # Check for penalty-related fields
            description = law_data.get("description", "").lower()
            relevance = law_data.get("relevance", "").lower()
            name = law_data.get("name", "").lower()

            # Look for penalty indicators
            penalty_keywords = [
                "fine", "penalty", "imprisonment", "misdemeanor", "felony",
                "criminal", "civil penalty", "monetary", "sentence", "jail",
                "prison", "restitution", "damages", "punitive", "sanction"
            ]

            text_to_search = f"{name} {description} {relevance}"

            for keyword in penalty_keywords:
                if keyword in text_to_search:
                    # Extract context around keyword
                    penalty_info = {
                        "law": law_data.get("name", ""),
                        "path": path,
                        "keyword": keyword,
                        "description": description[:200] if description else "",
                        "url": law_data.get("url", ""),
                        "key_sections": law_data.get("key_sections", [])
                    }
                    penalties.append(penalty_info)
                    break

            # Recursively search nested structures
            for key, value in law_data.items():
                if key not in ["embedding", "embedding_text", "ground_truth_embedding", "ground_truth_text"]:
                    sub_path = f"{path}.{key}" if path else key
                    penalties.extend(self.extract_legal_penalties(value, sub_path))

        elif isinstance(law_data, list):
            for i, item in enumerate(law_data):
                sub_path = f"{path}[{i}]"
                penalties.extend(self.extract_legal_penalties(item, sub_path))

        return penalties

    def categorize_penalties(self, penalties: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Categorize penalties by type"""
        categorized = {
            "criminal": [],
            "civil": [],
            "administrative": [],
            "monetary": [],
            "imprisonment": [],
            "license_revocation": [],
            "other": []
        }

        for penalty in penalties:
            description = penalty.get("description", "").lower()
            keyword = penalty.get("keyword", "").lower()
            law_name = penalty.get("law", "").lower()

            # Categorize based on keywords and context
            if any(term in description or term in law_name for term in ["criminal", "felony", "misdemeanor", "imprisonment", "jail", "prison"]):
                categorized["criminal"].append(penalty)
            elif any(term in description or term in law_name for term in ["civil", "damages", "lawsuit", "tort"]):
                categorized["civil"].append(penalty)
            elif any(term in description or term in law_name for term in ["administrative", "license", "revocation", "suspension"]):
                categorized["administrative"].append(penalty)

            if keyword in ["fine", "penalty", "monetary", "restitution", "damages"]:
                categorized["monetary"].append(penalty)

            if keyword in ["imprisonment", "jail", "prison", "sentence"]:
                categorized["imprisonment"].append(penalty)

            if any(term in description or term in law_name for term in ["license", "revocation", "suspension", "disciplinary"]):
                categorized["license_revocation"].append(penalty)

            if not any(penalty in cat for cat in categorized.values() if cat != categorized["other"]):
                categorized["other"].append(penalty)

        return categorized

    def analyze_violation_severity(self) -> Dict[str, Any]:
        """Analyze severity of violations and their legal impacts"""
        print("\n⚠️  Analyzing violation severity and legal impacts...")

        severity_analysis = {
            "high_severity": [],
            "medium_severity": [],
            "low_severity": [],
            "criminal_violations": [],
            "civil_violations": [],
            "administrative_violations": []
        }

        for violation in self.violations:
            severity = violation.get("violation", {}).get("severity", "UNKNOWN").upper()
            violation_type = violation.get("violation", {}).get("violation_type", "").lower()

            # Categorize by severity
            if severity == "HIGH":
                severity_analysis["high_severity"].append(violation)
            elif severity == "MEDIUM":
                severity_analysis["medium_severity"].append(violation)
            else:
                severity_analysis["low_severity"].append(violation)

            # Categorize by violation type
            if any(term in violation_type for term in ["criminal", "fraud", "theft", "embezzlement"]):
                severity_analysis["criminal_violations"].append(violation)
            elif any(term in violation_type for term in ["civil", "breach", "contract", "tort"]):
                severity_analysis["civil_violations"].append(violation)
            elif any(term in violation_type for term in ["license", "administrative", "regulatory"]):
                severity_analysis["administrative_violations"].append(violation)

        print(f"   High Severity: {len(severity_analysis['high_severity'])}")
        print(f"   Medium Severity: {len(severity_analysis['medium_severity'])}")
        print(f"   Low Severity: {len(severity_analysis['low_severity'])}")
        print(f"   Criminal: {len(severity_analysis['criminal_violations'])}")
        print(f"   Civil: {len(severity_analysis['civil_violations'])}")
        print(f"   Administrative: {len(severity_analysis['administrative_violations'])}")

        return severity_analysis

    def identify_enforcement_mechanisms(self) -> Dict[str, Any]:
        """Identify enforcement mechanisms and reporting requirements"""
        print("\n⚖️  Identifying enforcement mechanisms...")

        enforcement = {
            "reporting_forms": [],
            "enforcement_agencies": [],
            "statutory_authorities": [],
            "compliance_deadlines": []
        }

        # Extract from law references
        def extract_enforcement(data, path=""):
            if isinstance(data, dict):
                # Check for reporting forms
                if "reporting_forms" in data:
                    for form in data["reporting_forms"]:
                        enforcement["reporting_forms"].append({
                            "form_name": form.get("form_name", ""),
                            "form_number": form.get("form_number", ""),
                            "agency": form.get("agency", ""),
                            "url": form.get("url", ""),
                            "description": form.get("description", ""),
                            "law": data.get("name", ""),
                            "path": path
                        })

                # Extract agency information
                if "agency" in data:
                    enforcement["enforcement_agencies"].append({
                        "agency": data["agency"],
                        "law": data.get("name", ""),
                        "path": path
                    })

                # Recursively process
                for key, value in data.items():
                    if key not in ["embedding", "embedding_text", "ground_truth_embedding", "ground_truth_text"]:
                        sub_path = f"{path}.{key}" if path else key
                        extract_enforcement(value, sub_path)

            elif isinstance(data, list):
                for i, item in enumerate(data):
                    extract_enforcement(item, f"{path}[{i}]")

        extract_enforcement(self.laws)

        print(f"   Reporting Forms: {len(enforcement['reporting_forms'])}")
        print(f"   Enforcement Agencies: {len(set(f['agency'] for f in enforcement['reporting_forms'] if f.get('agency')))}")

        return enforcement

    def analyze_compliance_requirements(self) -> Dict[str, Any]:
        """Analyze compliance requirements and obligations"""
        print("\n📋 Analyzing compliance requirements...")

        compliance = {
            "immediate_reporting": [],
            "regulatory_filings": [],
            "license_requirements": [],
            "documentation_requirements": []
        }

        # Analyze violations for compliance requirements
        for violation in self.violations:
            violation_data = violation.get("violation", {})
            violation_type = violation_data.get("violation_type", "").lower()

            # Identify compliance requirements based on violation type
            if any(term in violation_type for term in ["unlicensed", "license"]):
                compliance["license_requirements"].append({
                    "violation": violation_data,
                    "requirements": ["License verification", "License application", "Continuing education"]
                })

            if any(term in violation_type for term in ["fraud", "misrepresentation", "deceptive"]):
                compliance["immediate_reporting"].append({
                    "violation": violation_data,
                    "requirements": ["Immediate law enforcement notification", "Regulatory agency reporting"]
                })

            if any(term in violation_type for term in ["tax", "filing", "disclosure"]):
                compliance["regulatory_filings"].append({
                    "violation": violation_data,
                    "requirements": ["Tax filing", "Regulatory disclosure", "Financial reporting"]
                })

        print(f"   Immediate Reporting Required: {len(compliance['immediate_reporting'])}")
        print(f"   Regulatory Filings: {len(compliance['regulatory_filings'])}")
        print(f"   License Requirements: {len(compliance['license_requirements'])}")

        return compliance

    def generate_legal_impact_report(self) -> Dict[str, Any]:
        """Generate comprehensive legal impact report"""
        print("\n📊 Generating legal impact report...")

        # Extract penalties from laws
        penalties = self.extract_legal_penalties(self.laws)
        categorized_penalties = self.categorize_penalties(penalties)

        # Analyze severity
        severity_analysis = self.analyze_violation_severity()

        # Identify enforcement
        enforcement = self.identify_enforcement_mechanisms()

        # Analyze compliance
        compliance = self.analyze_compliance_requirements()

        report = {
            "metadata": {
                "generated": datetime.now().isoformat(),
                "total_violations": len(self.violations),
                "total_penalties_identified": len(penalties)
            },
            "penalties": {
                "summary": {
                    "total": len(penalties),
                    "criminal": len(categorized_penalties["criminal"]),
                    "civil": len(categorized_penalties["civil"]),
                    "administrative": len(categorized_penalties["administrative"]),
                    "monetary": len(categorized_penalties["monetary"]),
                    "imprisonment": len(categorized_penalties["imprisonment"]),
                    "license_revocation": len(categorized_penalties["license_revocation"])
                },
                "by_category": categorized_penalties
            },
            "severity_analysis": {
                "high_severity_count": len(severity_analysis["high_severity"]),
                "medium_severity_count": len(severity_analysis["medium_severity"]),
                "low_severity_count": len(severity_analysis["low_severity"]),
                "criminal_violations_count": len(severity_analysis["criminal_violations"]),
                "civil_violations_count": len(severity_analysis["civil_violations"]),
                "administrative_violations_count": len(severity_analysis["administrative_violations"])
            },
            "enforcement_mechanisms": enforcement,
            "compliance_requirements": compliance,
            "legal_risks": {
                "criminal_liability": len(severity_analysis["criminal_violations"]),
                "civil_liability": len(severity_analysis["civil_violations"]),
                "administrative_sanctions": len(severity_analysis["administrative_violations"]),
                "license_risks": len(compliance["license_requirements"]),
                "reporting_obligations": len(compliance["immediate_reporting"])
            }
        }

        return report


def main():
    """Main function to run legal impact analysis"""
    import time
    start_time = time.time()

    print("=" * 80)
    print("⚖️  Legal Impact Analysis")
    print("=" * 80)
    print()

    analyzer = LegalImpactAnalyzer()
    analyzer.load_data()

    # Generate report
    report = analyzer.generate_legal_impact_report()

    # Save results
    output_file = DATA_PROCESSED_DIR / "legal_impact_analysis.json"
    print(f"\n💾 Saving legal impact analysis to {output_file}...")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    total_time = time.time() - start_time

    print("\n" + "=" * 80)
    print("✅ Legal Impact Analysis Complete!")
    print("=" * 80)
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Penalties identified: {report['metadata']['total_penalties_identified']}")
    print(f"High severity violations: {report['severity_analysis']['high_severity_count']}")
    print(f"Criminal violations: {report['severity_analysis']['criminal_violations_count']}")
    print(f"Reporting forms: {len(report['enforcement_mechanisms']['reporting_forms'])}")
    print("=" * 80)


if __name__ == "__main__":
    main()
