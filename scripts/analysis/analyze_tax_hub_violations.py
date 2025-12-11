#!/usr/bin/env python3
"""
Analyze anomalies relative to tax hub of Texas violations
Correlates tax forfeitures from lariat.txt with PDF anomalies and business violations
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict
import re

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

def parse_lariat_txt(file_path: Path) -> Dict[str, Any]:
    """Parse lariat.txt and extract tax forfeitures and violations"""

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    violations = {
        'tax_forfeitures': [],
        'forfeited_entities': [],
        'entities': {}
    }

    current_entity = None
    current_filing_number = None

    lines = content.split('\n')

    for i, line in enumerate(lines):
        # Detect new entity
        if 'Filing Number:' in line:
            match = re.search(r'Filing Number:\s+(\d+)', line)
            if match:
                filing_num = match.group(1)
                current_filing_number = filing_num

                # Extract entity name
                name_match = re.search(r'Name:\s+([^\t\n]+)', line)
                if not name_match and i + 1 < len(lines):
                    # Check next lines for name
                    for j in range(i+1, min(i+10, len(lines))):
                        if 'Name:' in lines[j]:
                            name_match = re.search(r'Name:\s+([^\t\n]+)', lines[j])
                            break

                if name_match:
                    entity_name = name_match.group(1).strip()
                    if filing_num not in violations['entities']:
                        violations['entities'][filing_num] = {
                            'filing_number': filing_num,
                            'name': entity_name,
                            'status': None,
                            'tax_forfeitures': [],
                            'filing_history': []
                        }
                    current_entity = violations['entities'][filing_num]

        # Extract entity status
        if current_entity and 'Entity Status:' in line:
            status_match = re.search(r'Entity Status:\s+([^\t\n]+)', line)
            if status_match:
                status = status_match.group(1).strip()
                current_entity['status'] = status
                if 'Forfeited' in status:
                    violations['forfeited_entities'].append({
                        'filing_number': current_filing_number,
                        'name': current_entity.get('name', 'Unknown'),
                        'status': status
                    })

        # Extract tax forfeitures from filing history
        if current_entity and 'Tax Forfeiture' in line:
            parts = [p.strip() for p in line.split('\t') if p.strip()]
            if len(parts) >= 3:
                forfeiture = {
                    'document_number': parts[0] if parts[0] else None,
                    'filing_type': 'Tax Forfeiture',
                    'filing_date': parts[2] if len(parts) > 2 else None,
                    'effective_date': parts[3] if len(parts) > 3 else None,
                    'entity_name': current_entity.get('name', 'Unknown'),
                    'filing_number': current_filing_number
                }
                violations['tax_forfeitures'].append(forfeiture)
                if current_entity:
                    current_entity['tax_forfeitures'].append(forfeiture)

    return violations

def analyze_anomalies(anomalies_dir: Path) -> Dict[str, Any]:
    """Analyze all anomaly files for suspicious patterns"""

    anomaly_files = sorted(anomalies_dir.glob('anomalies_page_*.json'))

    analysis = {
        'total_pages': len(anomaly_files),
        'pages_with_suspicious_patterns': 0,
        'shell_company_indicators': 0,
        'suspicious_patterns_by_severity': defaultdict(int),
        'pages_by_pattern': defaultdict(list),
        'all_suspicious_pages': []
    }

    for anomaly_file in anomaly_files:
        try:
            with open(anomaly_file, 'r') as f:
                data = json.load(f)

            page_data = data.get('data', {})
            page_num = page_data.get('page_number', 0)
            suspicious_patterns = page_data.get('suspicious_patterns', [])

            if suspicious_patterns:
                analysis['pages_with_suspicious_patterns'] += 1
                page_info = {
                    'page_number': page_num,
                    'patterns': suspicious_patterns
                }

                for pattern in suspicious_patterns:
                    pattern_type = pattern.get('pattern', 'Unknown')
                    severity = pattern.get('severity', 'unknown')

                    analysis['suspicious_patterns_by_severity'][severity] += 1
                    analysis['pages_by_pattern'][pattern_type].append(page_num)

                    if 'shell' in pattern_type.lower():
                        analysis['shell_company_indicators'] += 1

                analysis['all_suspicious_pages'].append(page_info)

        except Exception as e:
            print(f"Error processing {anomaly_file}: {e}", file=sys.stderr)
            continue

    return analysis

def load_ml_findings() -> Optional[Dict[str, Any]]:
    """Load ML analysis findings if available"""
    ml_file = PROJECT_ROOT / 'data' / 'processed' / 'ml_tax_structure_analysis.json'
    embedding_file = PROJECT_ROOT / 'data' / 'processed' / 'embedding_similarity_analysis.json'

    ml_data = {}

    if ml_file.exists():
        try:
            with open(ml_file, 'r') as f:
                ml_data['ml_analysis'] = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load ML analysis: {e}", file=sys.stderr)

    if embedding_file.exists():
        try:
            with open(embedding_file, 'r') as f:
                ml_data['embedding'] = json.load(f)
        except Exception as e:
            print(f"Warning: Could not load embedding analysis: {e}", file=sys.stderr)

    return ml_data if ml_data else None


def correlate_violations_and_anomalies(
    violations: Dict[str, Any],
    anomalies: Dict[str, Any],
    ml_findings: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Correlate tax forfeitures with anomalies and ML findings"""

    correlation = {
        'summary': {
            'total_tax_forfeitures': len(violations['tax_forfeitures']),
            'total_forfeited_entities': len(violations['forfeited_entities']),
            'total_suspicious_pages': anomalies['pages_with_suspicious_patterns'],
            'shell_company_indicators': anomalies['shell_company_indicators']
        },
        'tax_forfeitures': violations['tax_forfeitures'],
        'forfeited_entities': violations['forfeited_entities'],
        'suspicious_patterns': {
            'by_severity': dict(anomalies['suspicious_patterns_by_severity']),
            'by_pattern_type': {
                k: len(v) for k, v in anomalies['pages_by_pattern'].items()
            },
            'high_severity_pages': [
                p for p in anomalies['all_suspicious_pages']
                if any(pat.get('severity') == 'high' for pat in p.get('patterns', []))
            ]
        },
        'key_findings': []
    }

    # Integrate ML findings if available
    if ml_findings:
        ml_analysis = ml_findings.get('ml_analysis', {})
        embedding = ml_findings.get('embedding', {})

        correlation['ml_integration'] = {
            'clustering_results': ml_analysis.get('clustering_results', {}),
            'anomaly_detection': ml_analysis.get('anomaly_detection', {}),
            'risk_scores': ml_analysis.get('risk_scores', {}),
            'embedding_clusters': embedding.get('violation_clusters', [])
        }

        # Add ML anomalies to summary
        iso_anomalies = ml_analysis.get('anomaly_detection', {}).get('isolation_forest', {})
        if iso_anomalies:
            correlation['summary']['ml_anomalies_detected'] = iso_anomalies.get('n_anomalies', 0)

        # Add risk scores
        risk_scores = ml_analysis.get('risk_scores', {})
        if risk_scores:
            risk_values = list(risk_scores.values())
            correlation['summary']['ml_risk_score_mean'] = sum(risk_values) / len(risk_values) if risk_values else 0.0
            correlation['summary']['high_risk_entities_ml'] = len([v for v in risk_values if v > 0.7])

    # Key findings
    if violations['tax_forfeitures']:
        correlation['key_findings'].append({
            'finding': 'Tax Forfeiture Events',
            'count': len(violations['tax_forfeitures']),
            'details': violations['tax_forfeitures']
        })

    if anomalies['shell_company_indicators'] > 0:
        correlation['key_findings'].append({
            'finding': 'Shell Company Indicators',
            'count': anomalies['shell_company_indicators'],
            'severity': 'high',
            'details': f"Found {anomalies['shell_company_indicators']} pages with shell company indicators"
        })

    if violations['forfeited_entities']:
        correlation['key_findings'].append({
            'finding': 'Forfeited Entities',
            'count': len(violations['forfeited_entities']),
            'details': violations['forfeited_entities']
        })

    return correlation

def generate_report(correlation: Dict[str, Any], output_path: Path):
    """Generate comprehensive analysis report"""

    report = {
        'metadata': {
            'generated': datetime.now().isoformat(),
            'analysis_type': 'Tax Hub Violations and Anomalies Analysis',
            'scope': 'Texas business filings and PDF anomalies'
        },
        'executive_summary': {
            'total_tax_forfeitures': correlation['summary']['total_tax_forfeitures'],
            'total_forfeited_entities': correlation['summary']['total_forfeited_entities'],
            'suspicious_pages_detected': correlation['summary']['total_suspicious_pages'],
            'shell_company_indicators': correlation['summary']['shell_company_indicators'],
            'risk_level': 'HIGH' if correlation['summary']['shell_company_indicators'] > 0 or
                          correlation['summary']['total_tax_forfeitures'] > 0 else 'MODERATE'
        },
        'detailed_findings': correlation,
        'recommendations': []
    }

    # Add recommendations based on findings
    if correlation['summary']['total_tax_forfeitures'] > 0:
        report['recommendations'].append({
            'priority': 'HIGH',
            'recommendation': 'Investigate tax forfeiture events for potential tax evasion or non-compliance',
            'details': f"{correlation['summary']['total_tax_forfeitures']} tax forfeiture events identified"
        })

    if correlation['summary']['shell_company_indicators'] > 0:
        report['recommendations'].append({
            'priority': 'HIGH',
            'recommendation': 'Review shell company indicators for potential fraud or money laundering',
            'details': f"{correlation['summary']['shell_company_indicators']} pages contain shell company indicators"
        })

    if correlation['summary']['total_forfeited_entities'] > 0:
        report['recommendations'].append({
            'priority': 'MEDIUM',
            'recommendation': 'Examine forfeited entities for patterns of business violations',
            'details': f"{correlation['summary']['total_forfeited_entities']} entities with forfeited status"
        })

    # Write report
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)

    return report

def main():
    """Main analysis function"""

    # Paths
    lariat_txt = PROJECT_ROOT / 'data' / 'raw' / 'lariat.txt'
    anomalies_dir = PROJECT_ROOT / 'research' / 'texas' / 'pdf_analysis' / 'MERGED-Kettler' / 'anomalies'
    output_dir = PROJECT_ROOT / 'research' / 'texas' / 'analysis'
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / 'tax_hub_violations_analysis.json'

    print("Analyzing tax hub violations and anomalies...")
    print(f"Reading lariat.txt from: {lariat_txt}")
    print(f"Reading anomalies from: {anomalies_dir}")

    # Parse violations from lariat.txt
    print("\n1. Parsing tax forfeitures from lariat.txt...")
    violations = parse_lariat_txt(lariat_txt)
    print(f"   Found {len(violations['tax_forfeitures'])} tax forfeiture events")
    print(f"   Found {len(violations['forfeited_entities'])} forfeited entities")

    # Analyze anomalies
    print("\n2. Analyzing anomaly files...")
    anomalies = analyze_anomalies(anomalies_dir)
    print(f"   Analyzed {anomalies['total_pages']} pages")
    print(f"   Found {anomalies['pages_with_suspicious_patterns']} pages with suspicious patterns")
    print(f"   Found {anomalies['shell_company_indicators']} shell company indicators")

    # Load ML findings if available
    print("\n3. Loading ML findings...")
    ml_findings = load_ml_findings()
    if ml_findings:
        print("   ML findings loaded")
    else:
        print("   No ML findings found (run ml_tax_structure_analysis.py first)")

    # Correlate
    print("\n4. Correlating violations with anomalies...")
    correlation = correlate_violations_and_anomalies(violations, anomalies, ml_findings)

    # Generate report
    print("\n5. Generating comprehensive report...")
    report = generate_report(correlation, output_file)

    print(f"\n✓ Analysis complete!")
    print(f"  Report saved to: {output_file}")
    print(f"\nExecutive Summary:")
    print(f"  - Tax Forfeitures: {report['executive_summary']['total_tax_forfeitures']}")
    print(f"  - Forfeited Entities: {report['executive_summary']['total_forfeited_entities']}")
    print(f"  - Suspicious Pages: {report['executive_summary']['suspicious_pages_detected']}")
    print(f"  - Shell Company Indicators: {report['executive_summary']['shell_company_indicators']}")
    print(f"  - Risk Level: {report['executive_summary']['risk_level']}")

    # Print key findings
    if report['detailed_findings']['key_findings']:
        print(f"\nKey Findings:")
        for finding in report['detailed_findings']['key_findings']:
            print(f"  - {finding['finding']}: {finding.get('count', 'N/A')}")

if __name__ == '__main__':
    main()
