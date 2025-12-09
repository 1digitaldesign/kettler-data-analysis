#!/usr/bin/env python3
"""
Unified Reporting Module
Consolidates multiple R reporting scripts into a single Python module
Replaces: generate_comprehensive_audit_report, update_final_audit_report,
          compile_all_violations, etc.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.utils.paths import (
    RESEARCH_DIR, RESEARCH_VIOLATIONS_DIR, RESEARCH_ANOMALIES_DIR,
    RESEARCH_CONNECTIONS_DIR, OUTPUTS_DIR, FILINGS_DIR
)

class UnifiedReporter:
    """Unified reporter that replaces multiple R reporting scripts"""

    def __init__(self):
        self.reports = {}

    def compile_all_violations(self) -> Dict[str, Any]:
        """Compile all violations (replaces compile_all_violations.R)"""
        violations = {
            'license_violations': [],
            'address_violations': [],
            'timeline_violations': [],
            'connection_violations': []
        }

        # Load anomalies
        anomalies_file = RESEARCH_ANOMALIES_DIR / "all_anomalies_consolidated.json"
        if anomalies_file.exists():
            with open(anomalies_file, 'r') as f:
                anomalies = json.load(f)
                violations['license_violations'] = anomalies.get('license_gaps', [])
                violations['address_violations'] = anomalies.get('address_clusters', [])
                violations['timeline_violations'] = anomalies.get('timeline_issues', [])

        # Load connections
        connections_file = RESEARCH_CONNECTIONS_DIR / "nexus_patterns_analysis.json"
        if connections_file.exists():
            with open(connections_file, 'r') as f:
                nexus = json.load(f)
                if nexus.get('front_person_indicator'):
                    violations['connection_violations'].append({
                        'type': 'Front person pattern',
                        'description': 'All firms use same principal broker',
                        'severity': 'High'
                    })

        return violations

    def generate_audit_report(self) -> Dict[str, Any]:
        """Generate comprehensive audit report (replaces generate_comprehensive_audit_report.R)"""
        report = {
            'metadata': {
                'report_date': datetime.now().isoformat(),
                'report_type': 'Comprehensive Audit',
                'version': '1.0'
            },
            'executive_summary': {},
            'findings': {},
            'recommendations': []
        }

        # Load all data sources
        fraud_file = RESEARCH_DIR / "fraud_indicators.json"
        if fraud_file.exists():
            with open(fraud_file, 'r') as f:
                report['findings']['fraud_indicators'] = json.load(f)

        violations = self.compile_all_violations()
        report['findings']['violations'] = violations

        # Create executive summary
        total_violations = sum(len(v) if isinstance(v, list) else 0 for v in violations.values())
        report['executive_summary'] = {
            'total_violations': total_violations,
            'license_violations': len(violations.get('license_violations', [])),
            'address_violations': len(violations.get('address_violations', [])),
            'timeline_violations': len(violations.get('timeline_violations', [])),
            'connection_violations': len(violations.get('connection_violations', []))
        }

        # Generate recommendations
        if total_violations > 0:
            report['recommendations'] = [
                'File complaints with relevant state DPOR agencies',
                'Submit evidence to federal regulatory agencies',
                'Document all violations for legal proceedings',
                'Continue monitoring for additional violations'
            ]

        return report

    def update_final_audit_report(self) -> Dict[str, Any]:
        """Update final audit report (replaces update_final_audit_report.R)"""
        # Load existing report or create new
        report_file = OUTPUTS_DIR / "reports" / "final_audit_report.json"

        if report_file.exists():
            with open(report_file, 'r') as f:
                report = json.load(f)
        else:
            report = self.generate_audit_report()

        # Update with latest findings
        violations = self.compile_all_violations()
        report['last_updated'] = datetime.now().isoformat()
        report['findings']['violations'] = violations

        # Update summary
        total_violations = sum(len(v) if isinstance(v, list) else 0 for v in violations.values())
        report['executive_summary']['total_violations'] = total_violations

        return report

    def generate_summary_report(self) -> pd.DataFrame:
        """Generate summary report as DataFrame"""
        violations = self.compile_all_violations()

        summary_rows = []
        for violation_type, violation_list in violations.items():
            if isinstance(violation_list, list):
                for violation in violation_list:
                    if isinstance(violation, dict):
                        summary_rows.append({
                            'violation_type': violation_type,
                            'description': violation.get('description', str(violation)),
                            'severity': violation.get('severity', 'Medium')
                        })

        return pd.DataFrame(summary_rows)

    def save_all_reports(self):
        """Save all reports"""
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        (OUTPUTS_DIR / "reports").mkdir(parents=True, exist_ok=True)

        # Generate and save audit report
        audit_report = self.generate_audit_report()
        with open(OUTPUTS_DIR / "reports" / "comprehensive_audit_report.json", 'w') as f:
            json.dump(audit_report, f, indent=2, default=str)

        # Update and save final report
        final_report = self.update_final_audit_report()
        with open(OUTPUTS_DIR / "reports" / "final_audit_report.json", 'w') as f:
            json.dump(final_report, f, indent=2, default=str)

        # Save summary CSV
        summary_df = self.generate_summary_report()
        if not summary_df.empty:
            summary_df.to_csv(OUTPUTS_DIR / "reports" / "violations_summary.csv", index=False)

        print("All reports saved to outputs/reports/")

def main():
    """Main entry point"""
    reporter = UnifiedReporter()
    reporter.save_all_reports()

    print("\n=== Reporting Complete ===")
    violations = reporter.compile_all_violations()
    total = sum(len(v) if isinstance(v, list) else 0 for v in violations.values())
    print(f"Total violations compiled: {total}")

if __name__ == "__main__":
    main()
