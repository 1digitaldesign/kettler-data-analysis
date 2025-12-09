#!/usr/bin/env python3
"""
Unified Investigation Module
Consolidates multiple R investigation scripts into a single Python module
Replaces: investigate_hyland_upl, extract_pdf_text_for_upl, research_str_regulations,
          check_alexandria_zoning, audit_management_chain_licenses, etc.
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd
import re

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.utils.paths import (
    RESEARCH_DIR, RESEARCH_VIOLATIONS_DIR, EVIDENCE_DIR,
    DATA_SOURCE_DIR, DATA_ANALYSIS_DIR
)

class UnifiedInvestigator:
    """Unified investigator that replaces multiple R investigation scripts"""

    def __init__(self):
        self.results = {}

    def investigate_upl(self, target: str = "hyland") -> Dict[str, Any]:
        """Investigate unauthorized practice of law (replaces investigate_hyland_upl.R)"""
        investigation = {
            'target': target,
            'investigation_date': datetime.now().isoformat(),
            'findings': [],
            'evidence': [],
            'violations': []
        }

        # Load PDF evidence
        pdf_file = RESEARCH_DIR / "pdf_evidence_extracted.json"
        if pdf_file.exists():
            with open(pdf_file, 'r') as f:
                pdf_evidence = json.load(f)

                # Search for UPL indicators
                upl_keywords = ['legal advice', 'attorney', 'lawyer', 'legal counsel', 'legal representation']

                for pdf in pdf_evidence:
                    if isinstance(pdf, dict):
                        text = pdf.get('text_preview', '') + pdf.get('text', '')
                        reg_info = pdf.get('regulatory_info', {})

                        # Check for UPL mentions
                        for keyword in upl_keywords:
                            if keyword.lower() in text.lower():
                                investigation['findings'].append({
                                    'type': 'UPL Indicator',
                                    'keyword': keyword,
                                    'source': pdf.get('file', ''),
                                    'severity': 'High'
                                })

        return investigation

    def extract_pdf_text_for_upl(self, pdf_path: Path) -> Dict[str, Any]:
        """Extract PDF text for UPL investigation (replaces extract_pdf_text_for_upl.R)"""
        # This would use the existing PDF extraction module
        from scripts.extraction.extract_pdf_evidence import extract_pdf_text, extract_entities

        text = extract_pdf_text(pdf_path)
        entities = extract_entities(text) if text else {}

        return {
            'file': pdf_path.name,
            'text': text[:1000] if text else '',  # First 1000 chars
            'entities': entities,
            'upl_indicators': self._check_upl_indicators(text) if text else []
        }

    def _check_upl_indicators(self, text: str) -> List[str]:
        """Check for UPL indicators in text"""
        indicators = []
        upl_patterns = [
            r'legal\s+advice',
            r'attorney[-\s]client',
            r'legal\s+representation',
            r'practice\s+of\s+law'
        ]

        for pattern in upl_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                indicators.append(pattern)

        return indicators

    def research_str_regulations(self, location: str = "Alexandria, VA") -> Dict[str, Any]:
        """Research STR regulations (replaces research_str_regulations.R)"""
        regulations = {
            'location': location,
            'research_date': datetime.now().isoformat(),
            'regulations': [],
            'requirements': [],
            'status': 'framework'
        }

        # Framework - would query local government databases
        if 'Alexandria' in location:
            regulations['regulations'] = [
                'Short-term rental registration required',
                'Business license required for STR operations',
                'Zoning compliance required'
            ]
            regulations['requirements'] = [
                'Register with City of Alexandria',
                'Obtain business license',
                'Comply with zoning regulations'
            ]

        return regulations

    def check_zoning(self, address: str, location: str = "Alexandria") -> Dict[str, Any]:
        """Check zoning compliance (replaces check_alexandria_zoning.R)"""
        zoning_check = {
            'address': address,
            'location': location,
            'check_date': datetime.now().isoformat(),
            'zoning_status': 'unknown',
            'compliance': 'unknown',
            'status': 'framework'
        }

        # Framework - would query zoning database
        if 'Alexandria' in location:
            # Check if address matches known zones
            if re.search(r'\d{3,4}\s+John\s+Carlyle', address, re.IGNORECASE):
                zoning_check['zoning_status'] = 'Commercial/Residential Mixed'
                zoning_check['compliance'] = 'Requires verification'

        return zoning_check

    def audit_management_chain(self) -> Dict[str, Any]:
        """Audit management chain licenses (replaces audit_management_chain_licenses.R)"""
        audit = {
            'audit_date': datetime.now().isoformat(),
            'firms_audited': [],
            'license_issues': [],
            'chain_analysis': {}
        }

        # Load firms data
        firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
        if firms_file.exists():
            firms_df = pd.read_csv(firms_file)

            # Analyze management chain
            if 'Principal.Broker' in firms_df.columns:
                broker_counts = firms_df['Principal.Broker'].value_counts()
                audit['chain_analysis'] = {
                    'unique_brokers': len(broker_counts),
                    'most_common_broker': broker_counts.index[0] if len(broker_counts) > 0 else None,
                    'firms_per_broker': broker_counts.to_dict()
                }

            # Check for license issues
            if 'Gap.Years' in firms_df.columns:
                issues = firms_df[firms_df['Gap.Years'] > 0]
                audit['license_issues'] = issues[['Firm.Name', 'License.Number', 'Gap.Years']].to_dict('records')

        return audit

    def run_all_investigations(self) -> Dict[str, Any]:
        """Run all investigations"""
        results = {
            'upl_investigation': self.investigate_upl(),
            'str_regulations': self.research_str_regulations(),
            'zoning_checks': [],
            'management_audit': self.audit_management_chain()
        }

        # Check zoning for known addresses
        firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
        if firms_file.exists():
            firms_df = pd.read_csv(firms_file)
            if 'Address' in firms_df.columns:
                for addr in firms_df['Address'].dropna().unique()[:5]:  # Check first 5
                    results['zoning_checks'].append(self.check_zoning(addr))

        self.results = results
        return results

    def save_results(self):
        """Save investigation results"""
        RESEARCH_VIOLATIONS_DIR.mkdir(parents=True, exist_ok=True)

        # Save UPL investigation
        if self.results.get('upl_investigation'):
            with open(RESEARCH_VIOLATIONS_DIR / "upl_investigation.json", 'w') as f:
                json.dump(self.results['upl_investigation'], f, indent=2, default=str)

        # Save management audit
        if self.results.get('management_audit'):
            with open(RESEARCH_DIR / "management_chain_license_audit.json", 'w') as f:
                json.dump(self.results['management_audit'], f, indent=2, default=str)

        # Save all results
        with open(RESEARCH_DIR / "all_investigations.json", 'w') as f:
            json.dump(self.results, f, indent=2, default=str)

def main():
    """Main entry point"""
    investigator = UnifiedInvestigator()
    results = investigator.run_all_investigations()
    investigator.save_results()

    print("\n=== Investigation Complete ===")
    print(f"UPL findings: {len(results.get('upl_investigation', {}).get('findings', []))}")
    print(f"Management chain firms: {len(results.get('management_audit', {}).get('firms_audited', []))}")

if __name__ == "__main__":
    main()
