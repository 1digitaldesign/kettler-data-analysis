#!/usr/bin/env python3
"""
Unified Investigation Module

Consolidates multiple R investigation scripts into a single Python module.
Uses Python 3.14 features: match expressions, except expressions, modern type hints.

Replaces: investigate_hyland_upl, extract_pdf_text_for_upl, research_str_regulations,
          check_alexandria_zoning, audit_management_chain_licenses, etc.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any
import pandas as pd
import re

from scripts.utils.paths import (
    RESEARCH_DIR, RESEARCH_VIOLATIONS_DIR, EVIDENCE_DIR,
    DATA_SOURCE_DIR, RESEARCH_CONNECTIONS_DIR
)


class UnifiedInvestigator:
    """Unified investigator that replaces multiple R investigation scripts."""

    def __init__(self):
        self.results: dict[str, Any] = {}

    def investigate_upl(self, target: str = "hyland") -> dict[str, Any]:
        """Investigate unauthorized practice of law."""
        investigation: dict[str, Any] = {
            'target': target,
            'investigation_date': datetime.now().isoformat(),
            'findings': [],
            'evidence': [],
            'violations': []
        }

        # Load PDF evidence using Path.read_text
        pdf_file = RESEARCH_DIR / "pdf_evidence_extracted.json"
        if pdf_file.exists():
            try:
                pdf_evidence = json.loads(pdf_file.read_text(encoding='utf-8'))
            except Exception:
                return investigation

            # Search for UPL indicators using list comprehension
            upl_keywords = ['legal advice', 'attorney', 'lawyer', 'legal counsel', 'legal representation']

            investigation['findings'] = [
                {
                    'type': 'UPL Indicator',
                    'keyword': keyword,
                    'source': pdf.get('file', ''),
                    'severity': 'High'
                }
                for pdf in pdf_evidence if isinstance(pdf, dict)
                for keyword in upl_keywords
                if keyword.lower() in (pdf.get('text_preview', '') + pdf.get('text', '')).lower()
            ]

        return investigation

    def extract_pdf_text_for_upl(self, pdf_path: Path) -> dict[str, Any]:
        """Extract PDF text for UPL investigation."""
        # This would use the existing PDF extraction module
        try:
            from scripts.extraction.extract_pdf_evidence import extract_pdf_text, extract_entities
            text = extract_pdf_text(pdf_path)
            entities = extract_entities(text) if text else {}
        except ImportError:
            text = None
            entities = {}

        return {
            'file': pdf_path.name,
            'text': text[:1000] if text else '',
            'entities': entities,
            'upl_indicators': self._check_upl_indicators(text) if text else []
        }

    def _check_upl_indicators(self, text: str) -> list[str]:
        """Check for UPL indicators in text using list comprehension."""
        upl_patterns = [
            r'legal\s+advice',
            r'attorney[-\s]client',
            r'legal\s+representation',
            r'practice\s+of\s+law'
        ]

        return [
            pattern for pattern in upl_patterns
            if re.search(pattern, text, re.IGNORECASE)
        ]

    def research_str_regulations(self, location: str = "Alexandria, VA") -> dict[str, Any]:
        """Research STR regulations using match expression."""
        regulations: dict[str, Any] = {
            'location': location,
            'research_date': datetime.now().isoformat(),
            'regulations': [],
            'requirements': [],
            'status': 'framework'
        }

        # Use match expression for location-specific rules
        match location:
            case loc if 'Alexandria' in loc:
                regulations.update({
                    'regulations': [
                        'Short-term rental registration required',
                        'Business license required for STR operations',
                        'Zoning compliance required'
                    ],
                    'requirements': [
                        'Register with City of Alexandria',
                        'Obtain business license',
                        'Comply with zoning regulations'
                    ]
                })
            case _:
                pass

        return regulations

    def check_zoning(self, address: str, location: str = "Alexandria") -> dict[str, Any]:
        """Check zoning compliance."""
        zoning_check: dict[str, Any] = {
            'address': address,
            'location': location,
            'check_date': datetime.now().isoformat(),
            'zoning_status': 'unknown',
            'compliance': 'unknown',
            'status': 'framework'
        }

        # Use match expression for location-specific checks
        match location:
            case loc if 'Alexandria' in loc:
                if re.search(r'\d{3,4}\s+John\s+Carlyle', address, re.IGNORECASE):
                    zoning_check.update({
                        'zoning_status': 'Commercial/Residential Mixed',
                        'compliance': 'Requires verification'
                    })
            case _:
                pass

        return zoning_check

    def audit_management_chain(self) -> dict[str, Any]:
        """Audit management chain licenses."""
        audit: dict[str, Any] = {
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
                if not issues.empty:
                    audit['license_issues'] = issues[['Firm.Name', 'License.Number', 'Gap.Years']].to_dict('records')

        return audit

    def run_all_investigations(self) -> dict[str, Any]:
        """Run all investigations."""
        results: dict[str, Any] = {
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
                results['zoning_checks'] = [
                    self.check_zoning(addr)
                    for addr in firms_df['Address'].dropna().unique()[:5]
                ]

        self.results = results
        return results

    def save_results(self) -> None:
        """Save investigation results using Path.write_text."""
        RESEARCH_VIOLATIONS_DIR.mkdir(parents=True, exist_ok=True)

        # Save files using dict mapping
        save_mapping = {
            RESEARCH_VIOLATIONS_DIR / "upl_investigation.json": self.results.get('upl_investigation'),
            RESEARCH_DIR / "management_chain_license_audit.json": self.results.get('management_audit'),
            RESEARCH_DIR / "all_investigations.json": self.results
        }

        for file_path, data in save_mapping.items():
            if data:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(
                    json.dumps(data, indent=2, default=str),
                    encoding='utf-8'
                )


def main() -> None:
    """Main entry point."""
    investigator = UnifiedInvestigator()
    results = investigator.run_all_investigations()
    investigator.save_results()

    print("\n=== Investigation Complete ===")
    print(f"UPL findings: {len(results.get('upl_investigation', {}).get('findings', []))}")
    print(f"Management chain firms: {len(results.get('management_audit', {}).get('firms_audited', []))}")


if __name__ == "__main__":
    main()
