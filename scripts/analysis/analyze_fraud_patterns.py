#!/usr/bin/env python3
"""
Analyze Fraud Patterns (Python)
Identifies patterns and connections for administrative filings
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from scripts.utils.paths import DATA_DIR, DATA_SOURCE_DIR, RESEARCH_DIR, FILINGS_DIR, RESEARCH_CONNECTIONS_DIR

def load_all_evidence() -> Dict[str, Any]:
    """Load all relevant data"""
    evidence = {}

    # Load Skidmore firm data
    firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
    if firms_file.exists():
        evidence['firms'] = pd.read_csv(firms_file)

    # Load DPOR connections
    connections_file = RESEARCH_CONNECTIONS_DIR / "dpor_skidmore_connections.csv"
    if connections_file.exists():
        evidence['connections'] = pd.read_csv(connections_file)

    # Load extracted PDF evidence
    pdf_evidence_file = RESEARCH_DIR / "pdf_evidence_extracted.json"
    if pdf_evidence_file.exists():
        with open(pdf_evidence_file, 'r') as f:
            evidence['pdf_data'] = json.load(f)

    return evidence

def identify_fraud_indicators(evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Identify fraud indicators"""
    indicators = {}

    firms = evidence.get('firms', pd.DataFrame())
    if not firms.empty:
        # License gaps
        if 'Gap.Years' in firms.columns:
            indicators['license_gaps'] = firms[firms['Gap.Years'] > 0][
                ['Firm.Name', 'License.Number', 'Gap.Years', 'Notes']
            ].to_dict('records')

        # Address clusters (potential shell companies)
        if 'Address' in firms.columns:
            address_counts = firms.groupby('Address').size().reset_index(name='firm_count')
            indicators['address_clusters'] = address_counts[address_counts['firm_count'] > 1].sort_values('firm_count', ascending=False).to_dict('records')

    # Connection patterns
    connections = evidence.get('connections', pd.DataFrame())
    if not connections.empty and 'connection_type' in connections.columns:
        pb_pattern = connections[connections['connection_type'] == 'Principal Broker']
        if not pb_pattern.empty and 'state' in pb_pattern.columns:
            indicators['principal_broker_pattern'] = pb_pattern.groupby('state')['firm_name'].nunique().reset_index(name='firm_count').sort_values('firm_count', ascending=False).to_dict('records')

    # Timeline issues
    if not firms.empty and 'Initial.Cert.Date' in firms.columns:
        firms_with_dates = firms[firms['Initial.Cert.Date'].notna() & (firms['Initial.Cert.Date'] != '')]
        if not firms_with_dates.empty:
            firms_with_dates = firms_with_dates.copy()
            firms_with_dates['cert_date'] = pd.to_datetime(firms_with_dates['Initial.Cert.Date'], errors='coerce')
            firms_with_dates['skidmore_date'] = pd.Timestamp('2025-05-30')
            firms_with_dates['licensed_after'] = firms_with_dates['cert_date'] > firms_with_dates['skidmore_date']
            indicators['timeline_issues'] = firms_with_dates[firms_with_dates['licensed_after']][
                ['Firm.Name', 'Initial.Cert.Date', 'Skidmore.License.Date']
            ].to_dict('records')

    return indicators

def generate_filing_recommendations(indicators: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
    """Generate filing recommendations"""
    recommendations = {'federal': {}, 'state': {}, 'local': {}}

    # Federal filings
    if indicators.get('license_gaps'):
        recommendations['federal']['ftc'] = {
            'reason': 'Multiple firms with significant license gaps and same principal broker',
            'evidence_count': len(indicators['license_gaps']),
            'priority': 'High'
        }

    if indicators.get('address_clusters'):
        recommendations['federal']['cfpb'] = {
            'reason': 'Address clustering suggests potential shell company scheme',
            'evidence_count': len(indicators['address_clusters']),
            'priority': 'High'
        }

    # State filings
    if indicators.get('principal_broker_pattern'):
        for pattern in indicators['principal_broker_pattern']:
            state = pattern['state']
            firm_count = pattern['firm_count']
            recommendations['state'][state] = {
                'reason': f'Multiple firms ({firm_count}) listing same principal broker',
                'evidence_count': firm_count,
                'priority': 'High',
                'filing_type': 'License violation complaint'
            }

    # Local filings
    recommendations['local']['consumer_protection'] = {
        'reason': 'Potential consumer fraud and deceptive business practices',
        'priority': 'Medium'
    }

    return recommendations

def create_filing_checklist(recommendations: Dict[str, Any], evidence: Dict[str, Any]) -> pd.DataFrame:
    """Create filing checklist"""
    checklist_rows = []

    # Federal filings
    for agency, rec in recommendations.get('federal', {}).items():
        checklist_rows.append({
            'agency': agency.upper(),
            'filing_type': 'Federal complaint',
            'priority': rec['priority'],
            'evidence_available': f"{rec.get('evidence_count', 'N/A')} items",
            'status': 'Pending',
            'notes': rec['reason']
        })

    # State filings
    for state, rec in recommendations.get('state', {}).items():
        checklist_rows.append({
            'agency': f'State: {state}',
            'filing_type': rec.get('filing_type', 'License violation complaint'),
            'priority': rec['priority'],
            'evidence_available': f"{rec.get('evidence_count', 'N/A')} firms",
            'status': 'Pending',
            'notes': rec['reason']
        })

    return pd.DataFrame(checklist_rows)

def main_analysis():
    """Main analysis"""
    print("Loading evidence...")
    evidence = load_all_evidence()

    print("Identifying fraud indicators...")
    indicators = identify_fraud_indicators(evidence)

    print("Generating filing recommendations...")
    recommendations = generate_filing_recommendations(indicators, evidence)

    print("Creating filing checklist...")
    checklist = create_filing_checklist(recommendations, evidence)

    # Save results
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    FILINGS_DIR.mkdir(parents=True, exist_ok=True)

    indicators_file = RESEARCH_DIR / "fraud_indicators.json"
    with open(indicators_file, 'w') as f:
        json.dump(indicators, f, indent=2, default=str)
    print(f"Saved fraud indicators to: {indicators_file}")

    recommendations_file = RESEARCH_DIR / "filing_recommendations.json"
    with open(recommendations_file, 'w') as f:
        json.dump(recommendations, f, indent=2, default=str)
    print(f"Saved filing recommendations to: {recommendations_file}")

    checklist_file = FILINGS_DIR / "filing_checklist.csv"
    checklist.to_csv(checklist_file, index=False)
    print(f"Saved filing checklist to: {checklist_file}")

    # Print summary
    print("\n=== Fraud Pattern Analysis Summary ===")
    print(f"License Gaps Found: {len(indicators.get('license_gaps', []))}")
    print(f"Address Clusters Found: {len(indicators.get('address_clusters', []))}")
    print(f"Federal Filings Recommended: {len(recommendations.get('federal', {}))}")
    print(f"State Filings Recommended: {len(recommendations.get('state', {}))}")
    print("\nFiling Checklist:")
    print(checklist.to_string(index=False))

if __name__ == "__main__":
    main_analysis()
