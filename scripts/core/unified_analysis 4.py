#!/usr/bin/env python3
"""
Unified Analysis Module
Consolidates multiple R analysis scripts into a single, efficient Python module
Replaces: analyze_fraud_patterns, analyze_nexus_patterns, find_real_nexus,
          analyze_shared_resources, consolidate_all_anomalies, find_new_anomalies,
          analyze_lease_abnormalities, create_timeline_analysis, etc.
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
    DATA_SOURCE_DIR, DATA_ANALYSIS_DIR, RESEARCH_DIR, FILINGS_DIR,
    RESEARCH_CONNECTIONS_DIR, RESEARCH_ANOMALIES_DIR, RESEARCH_TIMELINES_DIR
)

class UnifiedAnalyzer:
    """Unified analyzer that replaces multiple R analysis scripts"""

    def __init__(self):
        self.data = {}
        self.results = {}

    def load_all_data(self) -> Dict[str, Any]:
        """Load all relevant data sources"""
        data = {}

        # Load firms
        firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
        if not firms_file.exists():
            firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"
        if firms_file.exists():
            if firms_file.suffix == '.csv':
                data['firms'] = pd.read_csv(firms_file)
            else:
                # For JSON, try reading as JSON first, then convert to DataFrame
                with open(firms_file, 'r') as f:
                    json_data = json.load(f)
                    if isinstance(json_data, list):
                        data['firms'] = pd.DataFrame(json_data)
                    elif isinstance(json_data, dict):
                        # Try to find a list/array in the dict
                        for key, value in json_data.items():
                            if isinstance(value, list) and len(value) > 0:
                                data['firms'] = pd.DataFrame(value)
                                break
                        if 'firms' not in data:
                            # Fallback: try pd.read_json
                            data['firms'] = pd.read_json(firms_file, orient='records')
                    else:
                        data['firms'] = pd.read_json(firms_file, orient='records')

        # Load connections
        conn_file = DATA_ANALYSIS_DIR / "dpor_skidmore_connections.csv"
        if conn_file.exists():
            data['connections'] = pd.read_csv(conn_file)

        # Load PDF evidence
        pdf_file = RESEARCH_DIR / "pdf_evidence_extracted.json"
        if pdf_file.exists():
            with open(pdf_file, 'r') as f:
                data['pdf_evidence'] = json.load(f)

        # Load connection matrix
        matrix_file = RESEARCH_DIR / "connection_matrix.json"
        if matrix_file.exists():
            with open(matrix_file, 'r') as f:
                data['connection_matrix'] = json.load(f)

        # Load shared resources
        shared_file = RESEARCH_DIR / "shared_resources_analysis.json"
        if shared_file.exists():
            with open(shared_file, 'r') as f:
                data['shared_resources'] = json.load(f)

        self.data = data
        return data

    def analyze_fraud_patterns(self) -> Dict[str, Any]:
        """Analyze fraud patterns (replaces analyze_fraud_patterns.R)"""
        indicators = {}
        firms = self.data.get('firms', pd.DataFrame())
        connections = self.data.get('connections', pd.DataFrame())

        if not firms.empty:
            # License gaps
            if 'Gap.Years' in firms.columns:
                indicators['license_gaps'] = firms[firms['Gap.Years'] > 0][
                    ['Firm.Name', 'License.Number', 'Gap.Years', 'Notes']
                ].to_dict('records')

            # Address clusters
            if 'Address' in firms.columns:
                address_counts = firms.groupby('Address').size().reset_index(name='firm_count')
                indicators['address_clusters'] = address_counts[address_counts['firm_count'] > 1].sort_values('firm_count', ascending=False).to_dict('records')

        # Principal broker patterns
        if not connections.empty and 'connection_type' in connections.columns:
            pb_pattern = connections[connections['connection_type'] == 'Principal Broker']
            if not pb_pattern.empty:
                indicators['principal_broker_pattern'] = pb_pattern.groupby('state')['firm_name'].nunique().reset_index(name='firm_count').sort_values('firm_count', ascending=False).to_dict('records')

        return indicators

    def analyze_nexus_patterns(self) -> Dict[str, Any]:
        """Analyze nexus patterns (replaces analyze_nexus_patterns.R, find_real_nexus.R)"""
        patterns = {}
        firms = self.data.get('firms', pd.DataFrame())

        if firms.empty:
            return patterns

        # Single principal broker pattern
        if 'Principal.Broker' in firms.columns:
            unique_brokers = firms['Principal.Broker'].dropna().unique()
            patterns['single_principal_broker'] = len(unique_brokers) == 1
            patterns['broker_name'] = unique_brokers[0] if len(unique_brokers) == 1 else None
            patterns['front_person_indicator'] = len(unique_brokers) == 1

        # Address clustering
        if 'Address' in firms.columns:
            address_counts = firms['Address'].value_counts()
            if len(address_counts) > 0:
                patterns['largest_cluster_size'] = int(address_counts.max())
                patterns['centralized_control_indicator'] = address_counts.max() > 3

        # License gaps
        if 'Gap.Years' in firms.columns:
            gaps = pd.to_numeric(firms['Gap.Years'], errors='coerce').dropna()
            if len(gaps) > 0:
                patterns['average_license_gap'] = float(gaps.mean())
                patterns['retroactive_assignment_indicator'] = gaps.mean() > 5

        # Geographic distribution
        if 'Address' in firms.columns:
            states = firms['Address'].str.extract(r',\s*([A-Z]{2})\s*\d')[0].dropna().unique()
            patterns['state_count'] = len(states)
            patterns['interstate_operation'] = len(states) > 1

        return patterns

    def analyze_timeline(self) -> Dict[str, Any]:
        """Create timeline analysis (replaces create_timeline_analysis.R)"""
        timeline = {}
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

                timeline['anomalies'] = firms_with_dates[firms_with_dates['days_between'] < 0].to_dict('records')

        return timeline

    def consolidate_anomalies(self) -> Dict[str, Any]:
        """Consolidate all anomalies (replaces consolidate_all_anomalies.R, find_new_anomalies.R)"""
        anomalies = {
            'license_gaps': [],
            'address_clusters': [],
            'timeline_issues': [],
            'connection_patterns': []
        }

        firms = self.data.get('firms', pd.DataFrame())
        connections = self.data.get('connections', pd.DataFrame())

        # License gaps
        if not firms.empty and 'Gap.Years' in firms.columns:
            anomalies['license_gaps'] = firms[firms['Gap.Years'] > 0].to_dict('records')

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
            anomalies['connection_patterns'] = connections.groupby(['connection_type', 'state']).size().reset_index(name='count').to_dict('records')

        return anomalies

    def analyze_lease_abnormalities(self) -> Dict[str, Any]:
        """Analyze lease abnormalities (replaces analyze_lease_abnormalities.R)"""
        abnormalities = {}
        pdf_evidence = self.data.get('pdf_evidence', [])

        if pdf_evidence and isinstance(pdf_evidence, list):
            for pdf in pdf_evidence:
                reg_info = pdf.get('regulatory_info', {})
                lease_mentions = reg_info.get('lease_mentions', {})
                if lease_mentions:
                    abnormalities['lease_keywords'] = {k: v for k, v in lease_mentions.items() if v > 0}

        return abnormalities

    def analyze_all_evidence(self) -> Dict[str, Any]:
        """Analyze all evidence (replaces analyze_all_evidence.R)"""
        evidence_summary = {
            'extraction_date': datetime.now().date().isoformat(),
            'total_pdfs': 0,
            'total_excel_files': 0,
            'entities_found': {},
            'key_findings': {}
        }

        pdf_evidence = self.data.get('pdf_evidence', [])
        if isinstance(pdf_evidence, list):
            evidence_summary['total_pdfs'] = len(pdf_evidence)

        # Extract all entities
        all_entities = {
            'emails': [],
            'addresses': [],
            'phone_numbers': [],
            'dates': [],
            'license_numbers': []
        }

        if isinstance(pdf_evidence, list):
            for pdf in pdf_evidence:
                if isinstance(pdf, dict):
                    entities = pdf.get('entities', {})
                    all_entities['emails'].extend(entities.get('emails', []))
                    all_entities['addresses'].extend(entities.get('addresses', []))
                    all_entities['phone_numbers'].extend(entities.get('phones', []))
                    all_entities['dates'].extend(entities.get('dates', []))
                    all_entities['license_numbers'].extend(entities.get('license_numbers', []))

        # Remove duplicates
        for key in all_entities:
            all_entities[key] = list(set([str(e) for e in all_entities[key] if e]))

        evidence_summary['entities_found'] = {
            'total_emails': len(all_entities['emails']),
            'total_addresses': len(all_entities['addresses']),
            'total_phones': len(all_entities['phone_numbers']),
            'total_dates': len(all_entities['dates']),
            'kettler_emails': [e for e in all_entities['emails'] if 'kettler' in str(e).lower()]
        }

        return evidence_summary

    def create_connection_matrix(self) -> Dict[str, Any]:
        """Create connection matrix (replaces create_connection_matrix.R)"""
        matrix = {
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
                matrix['kettler_firm_connections'] = {
                    'kettler_license_number': kettler_firm.iloc[0].get('License.Number', ''),
                    'kettler_address': kettler_firm.iloc[0].get('Address', ''),
                    'principal_broker': kettler_firm.iloc[0].get('Principal.Broker', ''),
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

    def analyze_shared_resources(self) -> Dict[str, Any]:
        """Analyze shared resources (replaces analyze_shared_resources.R)"""
        results = {
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
            addr = str(addr).upper()
            addr = addr.replace('#', 'STE')
            addr = addr.replace('STREET', 'ST').replace('DRIVE', 'DR').replace('ROAD', 'RD').replace('SUITE', 'STE')
            import re
            addr = re.sub(r'[^\w\s]', ' ', addr)
            addr = re.sub(r'\s+', ' ', addr).strip()
            return addr

        firms_copy = firms.copy()
        firms_copy['Address.Normalized'] = firms_copy['Address'].apply(normalize_address)

        # Find shared addresses
        address_counts = firms_copy['Address.Normalized'].value_counts()
        shared_addresses_list = address_counts[address_counts > 1]

        for addr, count in shared_addresses_list.items():
            firms_at_addr = firms_copy[firms_copy['Address.Normalized'] == addr]
            results['shared_addresses'].append({
                'address': addr,
                'firm_count': int(count),
                'firms': firms_at_addr['Firm.Name'].tolist()
            })

        results['shared_address_count'] = len(results['shared_addresses'])

        # Extract email domains from PDF evidence
        pdf_evidence = self.data.get('pdf_evidence', [])
        email_domains = set()
        if isinstance(pdf_evidence, list):
            for pdf in pdf_evidence:
                if isinstance(pdf, dict):
                    entities = pdf.get('entities', {})
                    emails = entities.get('emails', [])
                    for email in emails:
                        if '@' in str(email):
                            domain = str(email).split('@')[-1]
                            email_domains.add(domain)

        results['email_domains_found'] = list(email_domains)

        # Summary
        results['summary'] = {
            'firms_sharing_addresses': results['shared_address_count'],
            'largest_address_cluster': max([s['firm_count'] for s in results['shared_addresses']], default=0)
        }

        return results

    def generate_filing_recommendations(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Generate filing recommendations"""
        recommendations = {'federal': {}, 'state': {}, 'local': {}}

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

    def run_all_analyses(self) -> Dict[str, Any]:
        """Run all analyses and consolidate results"""
        print("Loading data...")
        self.load_all_data()

        print("Running fraud pattern analysis...")
        fraud_indicators = self.analyze_fraud_patterns()

        print("Running nexus pattern analysis...")
        nexus_patterns = self.analyze_nexus_patterns()

        print("Creating timeline analysis...")
        timeline = self.analyze_timeline()

        print("Consolidating anomalies...")
        anomalies = self.consolidate_anomalies()

        print("Analyzing lease abnormalities...")
        lease_abnormalities = self.analyze_lease_abnormalities()

        print("Analyzing all evidence...")
        evidence_summary = self.analyze_all_evidence()

        print("Creating connection matrix...")
        connection_matrix = self.create_connection_matrix()

        print("Analyzing shared resources...")
        shared_resources = self.analyze_shared_resources()

        print("Generating filing recommendations...")
        recommendations = self.generate_filing_recommendations(fraud_indicators)

        results = {
            'metadata': {
                'date': datetime.now().isoformat(),
                'analyses_run': ['fraud_patterns', 'nexus_patterns', 'timeline', 'anomalies',
                               'lease_abnormalities', 'all_evidence', 'connection_matrix', 'shared_resources']
            },
            'fraud_indicators': fraud_indicators,
            'nexus_patterns': nexus_patterns,
            'timeline': timeline,
            'anomalies': anomalies,
            'lease_abnormalities': lease_abnormalities,
            'evidence_summary': evidence_summary,
            'connection_matrix': connection_matrix,
            'shared_resources': shared_resources,
            'filing_recommendations': recommendations
        }

        self.results = results
        return results

    def save_results(self):
        """Save all analysis results"""
        RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
        FILINGS_DIR.mkdir(parents=True, exist_ok=True)

        # Save fraud indicators
        if self.results.get('fraud_indicators'):
            with open(RESEARCH_DIR / "fraud_indicators.json", 'w') as f:
                json.dump(self.results['fraud_indicators'], f, indent=2, default=str)

        # Save nexus patterns
        if self.results.get('nexus_patterns'):
            with open(RESEARCH_CONNECTIONS_DIR / "nexus_patterns_analysis.json", 'w') as f:
                json.dump(self.results['nexus_patterns'], f, indent=2, default=str)

        # Save timeline
        if self.results.get('timeline'):
            with open(RESEARCH_TIMELINES_DIR / "timeline_analysis.json", 'w') as f:
                json.dump(self.results['timeline'], f, indent=2, default=str)

        # Save anomalies
        if self.results.get('anomalies'):
            with open(RESEARCH_ANOMALIES_DIR / "all_anomalies_consolidated.json", 'w') as f:
                json.dump(self.results['anomalies'], f, indent=2, default=str)

        # Save evidence summary
        if self.results.get('evidence_summary'):
            with open(RESEARCH_DIR / "all_evidence_summary.json", 'w') as f:
                json.dump(self.results['evidence_summary'], f, indent=2, default=str)

        # Save connection matrix
        if self.results.get('connection_matrix'):
            with open(RESEARCH_CONNECTIONS_DIR / "connection_matrix.json", 'w') as f:
                json.dump(self.results['connection_matrix'], f, indent=2, default=str)

        # Save shared resources
        if self.results.get('shared_resources'):
            with open(RESEARCH_CONNECTIONS_DIR / "shared_resources_analysis.json", 'w') as f:
                json.dump(self.results['shared_resources'], f, indent=2, default=str)

        # Save filing recommendations
        if self.results.get('filing_recommendations'):
            with open(RESEARCH_DIR / "filing_recommendations.json", 'w') as f:
                json.dump(self.results['filing_recommendations'], f, indent=2, default=str)

            # Create checklist
            checklist_rows = []
            for agency, rec in self.results['filing_recommendations'].get('federal', {}).items():
                checklist_rows.append({
                    'agency': agency.upper(),
                    'filing_type': 'Federal complaint',
                    'priority': rec['priority'],
                    'evidence_available': f"{rec.get('evidence_count', 'N/A')} items",
                    'status': 'Pending',
                    'notes': rec['reason']
                })
            for state, rec in self.results['filing_recommendations'].get('state', {}).items():
                checklist_rows.append({
                    'agency': f'State: {state}',
                    'filing_type': rec.get('filing_type', 'License violation complaint'),
                    'priority': rec['priority'],
                    'evidence_available': f"{rec.get('evidence_count', 'N/A')} firms",
                    'status': 'Pending',
                    'notes': rec['reason']
                })

            if checklist_rows:
                checklist_df = pd.DataFrame(checklist_rows)
                checklist_df.to_csv(FILINGS_DIR / "filing_checklist.csv", index=False)

def main():
    """Main entry point"""
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
