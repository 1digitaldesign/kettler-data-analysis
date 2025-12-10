#!/usr/bin/env python3
"""
Unified Analysis Module

Consolidates multiple R analysis scripts into a single, efficient Python module.
Uses Python 3.14 features: match expressions, except expressions, modern type hints, efficient patterns.

Replaces: analyze_fraud_patterns, analyze_nexus_patterns, find_real_nexus,
          analyze_shared_resources, consolidate_all_anomalies, find_new_anomalies,
          analyze_lease_abnormalities, create_timeline_analysis, etc.
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Optional
import pandas as pd
import re

from scripts.utils.paths import (
    DATA_SOURCE_DIR, RESEARCH_DIR, FILINGS_DIR,
    RESEARCH_CONNECTIONS_DIR, RESEARCH_ANOMALIES_DIR, RESEARCH_TIMELINES_DIR
)


class UnifiedAnalyzer:
    """Unified analyzer that replaces multiple R analysis scripts."""

    def __init__(self):
        self.data: dict[str, Any] = {}
        self.results: dict[str, Any] = {}

    def load_all_data(self) -> dict[str, Any]:
        """Load all relevant data sources using Python 3.14 features."""
        data: dict[str, Any] = {}

        # Load firms - use match expression for file type
        firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
        if not firms_file.exists():
            firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"

        if firms_file.exists():
            match firms_file.suffix:
                case '.csv':
                    data['firms'] = pd.read_csv(firms_file)
                case '.json':
                    json_data = json.loads(firms_file.read_text(encoding='utf-8'))
                    match json_data:
                        case list():
                            data['firms'] = pd.DataFrame(json_data)
                        case dict() as d:
                            # Find first list value
                            list_value = next((v for v in d.values() if isinstance(v, list) and len(v) > 0), None)
                            data['firms'] = pd.DataFrame(list_value) if list_value else pd.read_json(firms_file, orient='records')
                        case _:
                            data['firms'] = pd.read_json(firms_file, orient='records')

        # Load connections
        conn_file = RESEARCH_CONNECTIONS_DIR / "dpor_skidmore_connections.csv"
        if conn_file.exists():
            data['connections'] = pd.read_csv(conn_file)

        # Load JSON files efficiently using Path.read_text
        json_files = {
            'pdf_evidence': RESEARCH_DIR / "pdf_evidence_extracted.json",
            'connection_matrix': RESEARCH_DIR / "connection_matrix.json",
            'shared_resources': RESEARCH_DIR / "shared_resources_analysis.json"
        }

        for key, file_path in json_files.items():
            if file_path.exists():
                try:
                    data[key] = json.loads(file_path.read_text(encoding='utf-8'))
                except Exception:
                    continue

        self.data = data
        return data

    def analyze_fraud_patterns(self) -> dict[str, Any]:
        """Analyze fraud patterns using efficient pandas operations."""
        indicators: dict[str, Any] = {}
        firms = self.data.get('firms', pd.DataFrame())
        connections = self.data.get('connections', pd.DataFrame())

        if not firms.empty:
            # License gaps using boolean indexing
            if 'Gap.Years' in firms.columns:
                gaps = firms[firms['Gap.Years'] > 0]
                if not gaps.empty:
                    indicators['license_gaps'] = gaps[
                        ['Firm.Name', 'License.Number', 'Gap.Years', 'Notes']
                    ].to_dict('records')

            # Address clusters using groupby
            if 'Address' in firms.columns:
                address_counts = firms.groupby('Address').size().reset_index(name='firm_count')
                clustered = address_counts[address_counts['firm_count'] > 1].sort_values('firm_count', ascending=False)
                if not clustered.empty:
                    indicators['address_clusters'] = clustered.to_dict('records')

        # Principal broker patterns
        if not connections.empty and 'connection_type' in connections.columns:
            pb_pattern = connections[connections['connection_type'] == 'Principal Broker']
            if not pb_pattern.empty:
                indicators['principal_broker_pattern'] = (
                    pb_pattern.groupby('state')['firm_name']
                    .nunique()
                    .reset_index(name='firm_count')
                    .sort_values('firm_count', ascending=False)
                    .to_dict('records')
                )

        return indicators

    def analyze_nexus_patterns(self) -> dict[str, Any]:
        """Analyze nexus patterns using efficient operations."""
        patterns: dict[str, Any] = {}
        firms = self.data.get('firms', pd.DataFrame())

        if firms.empty:
            return patterns

        # Single principal broker pattern
        if 'Principal.Broker' in firms.columns:
            unique_brokers = firms['Principal.Broker'].dropna().unique()
            patterns.update({
                'single_principal_broker': len(unique_brokers) == 1,
                'broker_name': unique_brokers[0] if len(unique_brokers) == 1 else None,
                'front_person_indicator': len(unique_brokers) == 1
            })

        # Address clustering
        if 'Address' in firms.columns:
            address_counts = firms['Address'].value_counts()
            if len(address_counts) > 0:
                patterns.update({
                    'largest_cluster_size': int(address_counts.max()),
                    'centralized_control_indicator': address_counts.max() > 3
                })

        # License gaps
        if 'Gap.Years' in firms.columns:
            gaps = pd.to_numeric(firms['Gap.Years'], errors='coerce').dropna()
            if len(gaps) > 0:
                patterns.update({
                    'average_license_gap': float(gaps.mean()),
                    'retroactive_assignment_indicator': gaps.mean() > 5
                })

        # Geographic distribution
        if 'Address' in firms.columns:
            states = firms['Address'].str.extract(r',\s*([A-Z]{2})\s*\d')[0].dropna().unique()
            patterns.update({
                'state_count': len(states),
                'interstate_operation': len(states) > 1
            })

        return patterns

    def analyze_timeline(self) -> dict[str, Any]:
        """Create timeline analysis."""
        timeline: dict[str, Any] = {}
        firms = self.data.get('firms', pd.DataFrame())

        if firms.empty:
            return timeline

        date_cols = ['Initial.Cert.Date', 'Skidmore.License.Date']
        if all(col in firms.columns for col in date_cols):
            firms_with_dates = firms[firms[date_cols].notna().all(axis=1)].copy()
            if not firms_with_dates.empty:
                firms_with_dates['cert_date'] = pd.to_datetime(firms_with_dates['Initial.Cert.Date'], errors='coerce')
                firms_with_dates['skidmore_date'] = pd.to_datetime(firms_with_dates['Skidmore.License.Date'], errors='coerce')
                firms_with_dates['days_between'] = (firms_with_dates['cert_date'] - firms_with_dates['skidmore_date']).dt.days

                timeline['events'] = firms_with_dates[[
                    'Firm.Name', 'Initial.Cert.Date', 'Skidmore.License.Date', 'days_between'
                ]].to_dict('records')

                anomalies = firms_with_dates[firms_with_dates['days_between'] < 0]
                if not anomalies.empty:
                    timeline['anomalies'] = anomalies.to_dict('records')

        return timeline

    def consolidate_anomalies(self) -> dict[str, Any]:
        """Consolidate all anomalies using efficient operations."""
        anomalies: dict[str, Any] = {
            'license_gaps': [],
            'address_clusters': [],
            'timeline_issues': [],
            'connection_patterns': []
        }

        firms = self.data.get('firms', pd.DataFrame())
        connections = self.data.get('connections', pd.DataFrame())

        # License gaps
        if not firms.empty and 'Gap.Years' in firms.columns:
            gaps = firms[firms['Gap.Years'] > 0]
            if not gaps.empty:
                anomalies['license_gaps'] = gaps.to_dict('records')

        # Address clusters
        if not firms.empty and 'Address' in firms.columns:
            address_counts = firms.groupby('Address').size()
            clustered = address_counts[address_counts > 1]
            if len(clustered) > 0:
                anomalies['address_clusters'] = firms[firms['Address'].isin(clustered.index)].to_dict('records')

        # Timeline issues
        timeline = self.analyze_timeline()
        if timeline.get('anomalies'):
            anomalies['timeline_issues'] = timeline['anomalies']

        # Connection patterns
        if not connections.empty:
            anomalies['connection_patterns'] = (
                connections.groupby(['connection_type', 'state'])
                .size()
                .reset_index(name='count')
                .to_dict('records')
            )

        return anomalies

    def analyze_lease_abnormalities(self) -> dict[str, Any]:
        """Analyze lease abnormalities."""
        abnormalities: dict[str, Any] = {}
        pdf_evidence = self.data.get('pdf_evidence', [])

        if isinstance(pdf_evidence, list):
            for pdf in pdf_evidence:
                if isinstance(pdf, dict):
                    reg_info = pdf.get('regulatory_info', {})
                    lease_mentions = reg_info.get('lease_mentions', {})
                    if lease_mentions:
                        abnormalities['lease_keywords'] = {
                            k: v for k, v in lease_mentions.items() if v > 0
                        }

        return abnormalities

    def analyze_all_evidence(self) -> dict[str, Any]:
        """Analyze all evidence using efficient list comprehensions."""
        evidence_summary: dict[str, Any] = {
            'extraction_date': datetime.now().date().isoformat(),
            'total_pdfs': 0,
            'total_excel_files': 0,
            'entities_found': {},
            'key_findings': {}
        }

        pdf_evidence = self.data.get('pdf_evidence', [])
        if isinstance(pdf_evidence, list):
            evidence_summary['total_pdfs'] = len(pdf_evidence)

            # Extract all entities using list comprehensions
            all_entities = {
                'emails': [email for pdf in pdf_evidence if isinstance(pdf, dict)
                          for email in pdf.get('entities', {}).get('emails', [])],
                'addresses': [addr for pdf in pdf_evidence if isinstance(pdf, dict)
                             for addr in pdf.get('entities', {}).get('addresses', [])],
                'phone_numbers': [phone for pdf in pdf_evidence if isinstance(pdf, dict)
                                 for phone in pdf.get('entities', {}).get('phones', [])],
                'dates': [date for pdf in pdf_evidence if isinstance(pdf, dict)
                         for date in pdf.get('entities', {}).get('dates', [])],
                'license_numbers': [lic for pdf in pdf_evidence if isinstance(pdf, dict)
                                   for lic in pdf.get('entities', {}).get('license_numbers', [])]
            }

            # Remove duplicates efficiently
            all_entities = {k: list(set(str(e) for e in v if e)) for k, v in all_entities.items()}

            evidence_summary['entities_found'] = {
                'total_emails': len(all_entities['emails']),
                'total_addresses': len(all_entities['addresses']),
                'total_phones': len(all_entities['phone_numbers']),
                'total_dates': len(all_entities['dates']),
                'kettler_emails': [e for e in all_entities['emails'] if 'kettler' in str(e).lower()]
            }

        return evidence_summary

    def create_connection_matrix(self) -> dict[str, Any]:
        """Create connection matrix."""
        matrix: dict[str, Any] = {
            'creation_date': datetime.now().date().isoformat(),
            'hyland_firm_connections': {},
            'firm_firm_connections': {},
            'kettler_firm_connections': {},
            'violation_entity_connections': {}
        }

        firms = self.data.get('firms', pd.DataFrame())
        shared_resources = self.data.get('shared_resources', {})

        # Firm-Firm connections (shared addresses)
        if shared_resources.get('shared_addresses'):
            matrix['firm_firm_connections'] = {
                'shared_addresses': shared_resources['shared_addresses'],
                'cluster_count': shared_resources.get('shared_address_count', 0)
            }

        # Kettler-Firm connections
        if not firms.empty and 'Firm.Name' in firms.columns:
            kettler_firm = firms[firms['Firm.Name'] == 'KETTLER MANAGEMENT INC']
            if not kettler_firm.empty:
                first_row = kettler_firm.iloc[0]
                matrix['kettler_firm_connections'] = {
                    'kettler_license_number': first_row.get('License.Number', ''),
                    'kettler_address': first_row.get('Address', ''),
                    'principal_broker': first_row.get('Principal.Broker', ''),
                    'connection_type': 'direct_license_match'
                }

        # Summary
        matrix['summary'] = {
            'total_firms': len(firms) if not firms.empty else 0,
            'hyland_connections': len(matrix.get('hyland_firm_connections', {})),
            'firm_firm_clusters': matrix.get('firm_firm_connections', {}).get('cluster_count', 0),
            'kettler_connected': len(matrix.get('kettler_firm_connections', {})) > 0
        }

        return matrix

    def analyze_shared_resources(self) -> dict[str, Any]:
        """Analyze shared resources using efficient operations."""
        results: dict[str, Any] = {
            'analysis_date': datetime.now().date().isoformat(),
            'shared_addresses': [],
            'shared_address_count': 0,
            'email_domains_found': [],
            'summary': {}
        }

        firms = self.data.get('firms', pd.DataFrame())
        if firms.empty or 'Address' not in firms.columns:
            return results

        # Normalize addresses
        def normalize_address(addr):
            if pd.isna(addr) or addr == "":
                return ""
            addr = str(addr).upper().replace('#', 'STE')
            addr = re.sub(r'(STREET|DRIVE|ROAD|SUITE)', lambda m: {'STREET': 'ST', 'DRIVE': 'DR', 'ROAD': 'RD', 'SUITE': 'STE'}[m.group()], addr)
            addr = re.sub(r'[^\w\s]', ' ', addr)
            return re.sub(r'\s+', ' ', addr).strip()

        firms_copy = firms.copy()
        firms_copy['Address.Normalized'] = firms_copy['Address'].apply(normalize_address)

        # Find shared addresses
        address_counts = firms_copy['Address.Normalized'].value_counts()
        shared_addresses_list = address_counts[address_counts > 1]

        results['shared_addresses'] = [
            {
                'address': addr,
                'firm_count': int(count),
                'firms': firms_copy[firms_copy['Address.Normalized'] == addr]['Firm.Name'].tolist()
            }
            for addr, count in shared_addresses_list.items()
        ]

        results['shared_address_count'] = len(results['shared_addresses'])

        # Extract email domains
        pdf_evidence = self.data.get('pdf_evidence', [])
        email_domains = {
            str(email).split('@')[-1]
            for pdf in pdf_evidence if isinstance(pdf, dict)
            for email in pdf.get('entities', {}).get('emails', [])
            if '@' in str(email)
        }

        results['email_domains_found'] = list(email_domains)

        # Summary
        results['summary'] = {
            'firms_sharing_addresses': results['shared_address_count'],
            'largest_address_cluster': max([s['firm_count'] for s in results['shared_addresses']], default=0)
        }

        return results

    def generate_filing_recommendations(self, indicators: dict[str, Any]) -> dict[str, Any]:
        """Generate filing recommendations."""
        recommendations: dict[str, Any] = {'federal': {}, 'state': {}, 'local': {}}

        # Federal filings
        if indicators.get('license_gaps'):
            recommendations['federal']['ftc'] = {
                'reason': 'Multiple firms with significant license gaps',
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
                recommendations['state'][state] = {
                    'reason': f"Multiple firms ({pattern['firm_count']}) listing same principal broker",
                    'evidence_count': pattern['firm_count'],
                    'priority': 'High',
                    'filing_type': 'License violation complaint'
                }

        return recommendations

    def run_all_analyses(self) -> dict[str, Any]:
        """Run all analyses and consolidate results."""
        print("Loading data...")
        self.load_all_data()

        analyses = {
            'fraud_patterns': ('Running fraud pattern analysis...', self.analyze_fraud_patterns),
            'nexus_patterns': ('Running nexus pattern analysis...', self.analyze_nexus_patterns),
            'timeline': ('Creating timeline analysis...', self.analyze_timeline),
            'anomalies': ('Consolidating anomalies...', self.consolidate_anomalies),
            'lease_abnormalities': ('Analyzing lease abnormalities...', self.analyze_lease_abnormalities),
            'all_evidence': ('Analyzing all evidence...', self.analyze_all_evidence),
            'connection_matrix': ('Creating connection matrix...', self.create_connection_matrix),
            'shared_resources': ('Analyzing shared resources...', self.analyze_shared_resources),
        }

        results_dict = {}
        for key, (message, func) in analyses.items():
            print(message)
            results_dict[key] = func()

        print("Generating filing recommendations...")
        recommendations = self.generate_filing_recommendations(results_dict['fraud_patterns'])

        results = {
            'metadata': {
                'date': datetime.now().isoformat(),
                'analyses_run': list(analyses.keys())
            },
            **results_dict,
            'filing_recommendations': recommendations
        }

        self.results = results
        return results

    def save_results(self) -> None:
        """Save all analysis results using Path.write_text."""
        RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
        FILINGS_DIR.mkdir(parents=True, exist_ok=True)

        # Save files using dict mapping
        save_mapping = {
            RESEARCH_DIR / "fraud_indicators.json": self.results.get('fraud_indicators'),
            RESEARCH_CONNECTIONS_DIR / "nexus_patterns_analysis.json": self.results.get('nexus_patterns'),
            RESEARCH_TIMELINES_DIR / "timeline_analysis.json": self.results.get('timeline'),
            RESEARCH_ANOMALIES_DIR / "all_anomalies_consolidated.json": self.results.get('anomalies'),
            RESEARCH_DIR / "all_evidence_summary.json": self.results.get('all_evidence'),
            RESEARCH_CONNECTIONS_DIR / "connection_matrix.json": self.results.get('connection_matrix'),
            RESEARCH_CONNECTIONS_DIR / "shared_resources_analysis.json": self.results.get('shared_resources'),
            RESEARCH_DIR / "filing_recommendations.json": self.results.get('filing_recommendations'),
        }

        for file_path, data in save_mapping.items():
            if data:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.write_text(
                    json.dumps(data, indent=2, default=str),
                    encoding='utf-8'
                )

        # Create checklist
        if self.results.get('filing_recommendations'):
            checklist_rows = [
                {
                    'agency': agency.upper(),
                    'filing_type': 'Federal complaint',
                    'priority': rec['priority'],
                    'evidence_available': f"{rec.get('evidence_count', 'N/A')} items",
                    'status': 'Pending',
                    'notes': rec['reason']
                }
                for agency, rec in self.results['filing_recommendations'].get('federal', {}).items()
            ] + [
                {
                    'agency': f'State: {state}',
                    'filing_type': rec.get('filing_type', 'License violation complaint'),
                    'priority': rec['priority'],
                    'evidence_available': f"{rec.get('evidence_count', 'N/A')} firms",
                    'status': 'Pending',
                    'notes': rec['reason']
                }
                for state, rec in self.results['filing_recommendations'].get('state', {}).items()
            ]

            if checklist_rows:
                checklist_df = pd.DataFrame(checklist_rows)
                checklist_df.to_csv(FILINGS_DIR / "filing_checklist.csv", index=False)


def main() -> None:
    """Main entry point."""
    analyzer = UnifiedAnalyzer()
    results = analyzer.run_all_analyses()
    analyzer.save_results()

    print("\n=== Analysis Complete ===")
    print(f"Fraud indicators: {len(results.get('fraud_indicators', {}))}")
    print(f"Nexus patterns identified: {len(results.get('nexus_patterns', {}))}")
    print(f"Anomalies found: {sum(len(v) if isinstance(v, list) else 0 for v in results.get('anomalies', {}).values())}")
    print(f"Filing recommendations: {len(results.get('filing_recommendations', {}).get('federal', {})) + len(results.get('filing_recommendations', {}).get('state', {}))}")


if __name__ == "__main__":
    main()
