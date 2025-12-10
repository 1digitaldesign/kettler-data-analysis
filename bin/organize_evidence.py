#!/usr/bin/env python3
"""
Master Evidence Organization Script (Python)
Organizes all evidence and cross-references with license data for administrative filings
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from scripts.utils.paths import (
    PROJECT_ROOT, DATA_SOURCE_DIR, RESEARCH_DIR,
    FILINGS_DIR, EVIDENCE_DIR, RESEARCH_EVIDENCE_DIR, RESEARCH_CONNECTIONS_DIR
)

def load_all_data() -> Dict[str, Any]:
    """Load all data sources"""
    data = {}

    # Load Skidmore firm data
    firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
    if not firms_file.exists():
        firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"

    if firms_file.exists():
        if firms_file.suffix == '.json':
            data['firms'] = pd.read_json(firms_file)
        else:
            data['firms'] = pd.read_csv(firms_file)

    # Load connections
    connections_file = RESEARCH_CONNECTIONS_DIR / "dpor_skidmore_connections.csv"
    if connections_file.exists():
        data['connections'] = pd.read_csv(connections_file)

    # Load PDF evidence
    pdf_file = RESEARCH_EVIDENCE_DIR / "pdf_evidence_extracted.json"
    if not pdf_file.exists():
        pdf_file = RESEARCH_DIR / "pdf_evidence_extracted.json"
    if pdf_file.exists():
        with open(pdf_file, 'r') as f:
            data['pdf_evidence'] = json.load(f)

    return data

def cross_reference_evidence(data: Dict[str, Any]) -> Dict[str, Any]:
    """Cross-reference evidence with license data"""
    cross_ref = {}

    pdf_evidence = data.get('pdf_evidence', [])
    if pdf_evidence and isinstance(pdf_evidence, list) and len(pdf_evidence) > 0:
        pdf_data = pdf_evidence[0]
        entities = pdf_data.get('entities', {})

        # Extract addresses and match with firms
        pdf_addresses = entities.get('addresses', [])
        if pdf_addresses and 'firms' in data and not data['firms'].empty:
            # Extract street number from first address
            if pdf_addresses:
                first_addr = pdf_addresses[0] if isinstance(pdf_addresses, list) else str(pdf_addresses)
                street_num = re.search(r'^\d+', first_addr)
                if street_num:
                    street_num = street_num.group()
                    matched = data['firms'][
                        data['firms']['Address'].str.contains(street_num, na=False, regex=False) &
                        data['firms']['Address'].str.contains('MCLEAN.*VA|VA.*MCLEAN', na=False, regex=True, case=False)
                    ]
                    if not matched.empty:
                        cross_ref['address_matches'] = matched

        # Extract Kettler emails
        emails = entities.get('emails', [])
        if emails:
            kettler_emails = [e for e in emails if 'kettler' in str(e).lower()]
            if kettler_emails:
                cross_ref['kettler_emails'] = kettler_emails

        # Extract violations
        reg_info = pdf_data.get('regulatory_info', {})
        violations = reg_info.get('violation_mentions', {})
        if violations:
            violations_found = {k: v for k, v in violations.items() if v > 0}
            if violations_found:
                cross_ref['violations_mentioned'] = len(violations_found)
                cross_ref['violation_details'] = violations_found

    return cross_ref

def create_filing_evidence_summary(data: Dict[str, Any], cross_ref: Dict[str, Any]) -> Dict[str, Any]:
    """Create evidence summary for filings"""
    summary = {}

    firms = data.get('firms', pd.DataFrame())

    # Key findings
    summary['key_findings'] = {
        'total_firms_connected': len(firms) if not firms.empty else 0,
        'firms_same_address_as_pdf': len(cross_ref.get('address_matches', pd.DataFrame())) if isinstance(cross_ref.get('address_matches'), pd.DataFrame) else 0,
        'kettler_emails_in_pdf': len(cross_ref.get('kettler_emails', [])),
        'violations_mentioned': cross_ref.get('violations_mentioned', 0)
    }

    # Address analysis
    if not firms.empty and 'Address' in firms.columns and 'Firm.Name' in firms.columns:
        address_analysis = firms.groupby('Address').agg({
            'Firm.Name': ['count', lambda x: '; '.join(x.unique())]
        }).reset_index()
        address_analysis.columns = ['Address', 'firm_count', 'firms']
        summary['address_analysis'] = address_analysis[address_analysis['firm_count'] > 1].sort_values('firm_count', ascending=False).to_dict('records')

    # Timeline issues
    if not firms.empty and all(col in firms.columns for col in ['Firm.Name', 'Gap.Years', 'Initial.Cert.Date', 'Skidmore.License.Date']):
        timeline_issues = firms[firms['Gap.Years'] > 0][['Firm.Name', 'Initial.Cert.Date', 'Skidmore.License.Date', 'Gap.Years']].sort_values('Gap.Years', ascending=False)
        summary['timeline_issues'] = timeline_issues.to_dict('records')

    return summary

def generate_filing_package(data: Dict[str, Any], cross_ref: Dict[str, Any], summary: Dict[str, Any]) -> Dict[str, Any]:
    """Generate filing-ready evidence package"""
    package = {}

    # Executive summary
    package['executive_summary'] = {
        'date_prepared': datetime.now().date().isoformat(),
        'case_summary': 'Investigation into multiple real estate firms listing Caitlin Skidmore as Principal Broker, with evidence of potential license violations and fraudulent practices',
        'key_evidence': summary['key_findings'],
        'recommended_filings': [
            'Virginia DPOR - License violation complaint',
            'FTC - Consumer fraud complaint',
            'CFPB - Financial services complaint',
            'HUD - Fair housing complaint (if applicable)'
        ]
    }

    # Evidence documents
    pdf_dir = EVIDENCE_DIR / "pdfs"
    pdf_files = list(pdf_dir.glob("*.pdf")) if pdf_dir.exists() else []

    package['evidence_documents'] = {
        'pdf_files': [f.name for f in pdf_files],
        'license_data': str(DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"),
        'connections_data': str(RESEARCH_CONNECTIONS_DIR / "dpor_skidmore_connections.csv")
    }

    # Key entities from PDF
    pdf_evidence = data.get('pdf_evidence', [])
    if pdf_evidence and isinstance(pdf_evidence, list) and len(pdf_evidence) > 0:
        entities = pdf_evidence[0].get('entities', {})
        package['key_entities'] = {
            'emails': entities.get('emails', []),
            'addresses': entities.get('addresses', []),
            'phone_numbers': entities.get('phones', []),
            'units_mentioned': entities.get('units', []),
            'license_numbers': entities.get('license_numbers', [])
        }

        # Kettler emails
        kettler_emails = [e for e in entities.get('emails', []) if 'kettler' in str(e).lower()]
        if kettler_emails:
            package['key_entities']['kettler_emails'] = kettler_emails
            package['executive_summary']['key_evidence']['kettler_emails_in_pdf'] = len(kettler_emails)

        # Violations
        reg_info = pdf_evidence[0].get('regulatory_info', {})
        violations = reg_info.get('violation_mentions', {})
        if violations:
            violations_count = sum(1 for v in violations.values() if v > 0)
            package['executive_summary']['key_evidence']['violations_mentioned'] = violations_count

    # Violations identified
    connections = data.get('connections', pd.DataFrame())
    if not connections.empty and 'connection_type' in connections.columns:
        principal_broker = connections[connections['connection_type'] == 'Principal Broker']
        if not principal_broker.empty and 'state' in principal_broker.columns:
            pb_pattern = principal_broker.groupby('state').size().reset_index(name='firm_count')
            package['violations'] = {'principal_broker_pattern': pb_pattern.to_dict('records')}

    package['violations'] = package.get('violations', {})
    package['violations'].update({
        'license_violations': summary.get('timeline_issues', []),
        'address_clustering': summary.get('address_analysis', [])
    })

    return package

def write_executive_summary(filepath: Path, package: Dict[str, Any]):
    """Write executive summary markdown"""
    exec_sum = package['executive_summary']
    key_ev = exec_sum['key_evidence']

    content = f"""# Executive Summary - Administrative Filing Evidence Package

**Date Prepared:** {exec_sum['date_prepared']}

## Case Summary

{exec_sum['case_summary']}

## Key Evidence

- Total Firms Connected: {key_ev['total_firms_connected']}
- Firms at Same Address as PDF Evidence: {key_ev['firms_same_address_as_pdf']}
- Kettler Emails Found in PDF: {key_ev['kettler_emails_in_pdf']}
- Violation Types Mentioned: {key_ev['violations_mentioned']}

## Recommended Filings

{chr(10).join('- ' + f for f in exec_sum['recommended_filings'])}

## Evidence Documents

### PDF Files
{chr(10).join('- ' + f for f in package['evidence_documents']['pdf_files'])}

### Data Files
- {package['evidence_documents']['license_data']}
- {package['evidence_documents']['connections_data']}
"""

    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w') as f:
        f.write(content)

def main_organize():
    """Main organization function"""
    print("=== Evidence Organization for Administrative Filings ===\n")

    print("Step 1: Loading all data sources...")
    data = load_all_data()
    firms_count = len(data.get('firms', pd.DataFrame())) if isinstance(data.get('firms'), pd.DataFrame) else 0
    connections_count = len(data.get('connections', pd.DataFrame())) if isinstance(data.get('connections'), pd.DataFrame) else 0
    pdf_count = len(data.get('pdf_evidence', [])) if isinstance(data.get('pdf_evidence'), list) else 0
    print(f"  Loaded firm data: {firms_count} firms")
    print(f"  Loaded connections: {connections_count} connections")
    print(f"  Loaded PDF evidence: {pdf_count} file(s)\n")

    print("Step 2: Cross-referencing evidence...")
    cross_ref = cross_reference_evidence(data)

    if isinstance(cross_ref.get('address_matches'), pd.DataFrame) and not cross_ref['address_matches'].empty:
        print(f"  Found {len(cross_ref['address_matches'])} firms matching PDF address")
        print(f"    - {', '.join(cross_ref['address_matches']['Firm.Name'].tolist())}")
    else:
        print("  No firms matched PDF address")

    if cross_ref.get('kettler_emails'):
        print(f"  Found {len(cross_ref['kettler_emails'])} Kettler email addresses in PDF")

    if cross_ref.get('violations_mentioned', 0) > 0:
        print(f"  Found {cross_ref['violations_mentioned']} violation types mentioned")
    print()

    print("Step 3: Creating evidence summary...")
    summary = create_filing_evidence_summary(data, cross_ref)
    print("  Key findings documented")
    print(f"  Address clusters: {len(summary.get('address_analysis', []))}")
    print(f"  Timeline issues: {len(summary.get('timeline_issues', []))}\n")

    print("Step 4: Generating filing package...")
    package = generate_filing_package(data, cross_ref, summary)

    # Save filing package
    package_file = FILINGS_DIR / "filing_evidence_package.json"
    package_file.parent.mkdir(parents=True, exist_ok=True)
    with open(package_file, 'w') as f:
        json.dump(package, f, indent=2, default=str)
    print(f"  Saved filing package to: {package_file}")

    # Create executive summary
    exec_summary_file = FILINGS_DIR / "executive_summary.md"
    write_executive_summary(exec_summary_file, package)
    print(f"  Saved executive summary to: {exec_summary_file}")

    print("\n=== Organization Complete ===")
    print("\nKey Evidence Points:")
    key_ev = package['executive_summary']['key_evidence']
    print(f"  - {key_ev['total_firms_connected']} firms connected to Skidmore")
    print(f"  - {key_ev['firms_same_address_as_pdf']} firms at same address as PDF")
    print(f"  - {key_ev['violations_mentioned']} violation types mentioned in PDF")

if __name__ == "__main__":
    main_organize()
