#!/usr/bin/env python3
"""
Cross-reference violations with research data and identify violation networks
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, RESEARCH_DIR, DATA_PROCESSED_DIR


def load_texas_lariat_data() -> Dict[str, Any]:
    """Load structured Texas lariat data"""
    print("Loading Texas lariat data...")

    lariat_dir = RESEARCH_DIR / "texas" / "lariat"
    data = {
        'entities': {},
        'management': defaultdict(list),
        'associated_entities': defaultdict(list),
        'filing_history': defaultdict(list),
        'registered_agents': {},
        'names': defaultdict(list),
        'assumed_names': defaultdict(list)
    }

    # Load entities
    entities_dir = lariat_dir / "entities"
    if entities_dir.exists():
        for entity_file in entities_dir.glob("*.json"):
            try:
                with open(entity_file, 'r') as f:
                    entity_data = json.load(f)
                    filing_num = entity_data.get('filing_number')
                    if filing_num:
                        data['entities'][filing_num] = entity_data
            except Exception as e:
                print(f"  Warning: Could not load {entity_file}: {e}")

    # Load management
    management_dir = lariat_dir / "management"
    if management_dir.exists():
        for mgmt_file in management_dir.glob("*.json"):
            try:
                with open(mgmt_file, 'r') as f:
                    mgmt_data = json.load(f)
                    filing_num = mgmt_data.get('filing_number')
                    if filing_num:
                        data['management'][filing_num].append(mgmt_data)
            except Exception as e:
                print(f"  Warning: Could not load {mgmt_file}: {e}")

    # Load associated entities
    assoc_dir = lariat_dir / "associated_entities"
    if assoc_dir.exists():
        for assoc_file in assoc_dir.glob("*.json"):
            try:
                with open(assoc_file, 'r') as f:
                    assoc_data = json.load(f)
                    filing_num = assoc_data.get('filing_number')
                    if filing_num:
                        data['associated_entities'][filing_num].append(assoc_data)
            except Exception as e:
                print(f"  Warning: Could not load {assoc_file}: {e}")

    # Load filing history
    history_dir = lariat_dir / "filing_history"
    if history_dir.exists():
        for hist_file in history_dir.glob("*.json"):
            try:
                with open(hist_file, 'r') as f:
                    hist_data = json.load(f)
                    filing_num = hist_data.get('filing_number')
                    if filing_num:
                        data['filing_history'][filing_num].append(hist_data)
            except Exception as e:
                print(f"  Warning: Could not load {hist_file}: {e}")

    # Load registered agents
    agents_dir = lariat_dir / "registered_agents"
    if agents_dir.exists():
        for agent_file in agents_dir.glob("*.json"):
            try:
                with open(agent_file, 'r') as f:
                    agent_data = json.load(f)
                    filing_num = agent_data.get('filing_number')
                    if filing_num:
                        data['registered_agents'][filing_num] = agent_data
            except Exception as e:
                print(f"  Warning: Could not load {agent_file}: {e}")

    print(f"  Loaded: {len(data['entities'])} entities, "
          f"{sum(len(v) for v in data['management'].values())} management records, "
          f"{sum(len(v) for v in data['associated_entities'].values())} associated entities")

    return data


def load_research_intersections() -> Dict[str, Any]:
    """Load research directory intersections"""
    print("Loading research intersections...")

    intersections = {
        'license_searches': {},
        'employees': {},
        'connections': [],
        'company_registrations': [],
        'financial': [],
        'fraud_indicators': {}
    }

    # Load fraud indicators
    fraud_file = RESEARCH_DIR / "fraud_indicators.json"
    if fraud_file.exists():
        try:
            with open(fraud_file, 'r') as f:
                intersections['fraud_indicators'] = json.load(f)
        except Exception as e:
            print(f"  Warning: Could not load fraud indicators: {e}")

    # Load connections
    connections_dir = RESEARCH_DIR / "connections"
    if connections_dir.exists():
        for conn_file in connections_dir.glob("*.json"):
            try:
                with open(conn_file, 'r') as f:
                    intersections['connections'].append(json.load(f))
            except Exception as e:
                print(f"  Warning: Could not load {conn_file}: {e}")

    # Load all entities
    entities_file = RESEARCH_DIR / "all_entities_extracted.json"
    if entities_file.exists():
        try:
            with open(entities_file, 'r') as f:
                data = json.load(f)
                intersections['all_entities'] = data if isinstance(data, dict) else {}
        except Exception as e:
            print(f"  Warning: Could not load all entities: {e}")

    print(f"  Loaded: {len(intersections['fraud_indicators'])} fraud indicators, "
          f"{len(intersections['connections'])} connections")

    return intersections


def correlate_violations_with_management(violations: Dict[str, Any],
                                        lariat_data: Dict[str, Any]) -> Dict[str, Any]:
    """Correlate violations with management changes"""
    correlations = []

    for violation_type, violation_list in violations.items():
        for violation in violation_list:
            filing_num = violation.get('filing_number')
            if not filing_num:
                continue

            management_records = lariat_data['management'].get(filing_num, [])

            violation_date_str = violation.get('filing_date') or violation.get('effective_date')
            if not violation_date_str:
                continue

            try:
                violation_date = datetime.fromisoformat(violation_date_str)
            except:
                continue

            # Find management changes around violation date
            for mgmt in management_records:
                mgmt_date_str = mgmt.get('last_update') or mgmt.get('date')
                if not mgmt_date_str:
                    continue

                try:
                    mgmt_date = datetime.fromisoformat(mgmt_date_str)
                    days_diff = abs((mgmt_date - violation_date).days)

                    if days_diff <= 90:  # Within 90 days
                        correlations.append({
                            'violation': violation,
                            'management_change': mgmt,
                            'days_difference': days_diff,
                            'correlation_type': 'management_change_during_violation'
                        })
                except:
                    pass

    return correlations


def identify_violation_networks(violations: Dict[str, Any],
                                lariat_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Identify violation networks through entity relationships"""
    networks = []

    # Group violations by entity
    entity_violations = defaultdict(list)
    for violation_type, violation_list in violations.items():
        for violation in violation_list:
            filing_num = violation.get('filing_number')
            if filing_num:
                entity_violations[filing_num].append(violation)

    # Find connected entities through associated entities
    for filing_num, violations_list in entity_violations.items():
        associated = lariat_data['associated_entities'].get(filing_num, [])

        if associated:
            network = {
                'central_entity': filing_num,
                'violations': violations_list,
                'connected_entities': [],
                'network_size': 1
            }

            for assoc in associated:
                assoc_filing = assoc.get('associated_filing_number')
                if assoc_filing and assoc_filing in entity_violations:
                    network['connected_entities'].append({
                        'filing_number': assoc_filing,
                        'violations': entity_violations[assoc_filing]
                    })
                    network['network_size'] += 1

            if network['network_size'] > 1:
                networks.append(network)

    return networks


def match_with_fraud_indicators(violations: Dict[str, Any],
                               fraud_indicators: Dict[str, Any],
                               lariat_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Match violations with known fraud indicators"""
    matches = []

    # Check address clustering
    address_clusters = fraud_indicators.get('address_clusters', [])
    for cluster in address_clusters:
        cluster_address = cluster.get('Address', '').upper()

        for violation_type, violation_list in violations.items():
            for violation in violation_list:
                entity_filing = violation.get('filing_number')
                entity = lariat_data['entities'].get(entity_filing)

                if entity:
                    entity_address = entity.get('address', '').upper()
                    if cluster_address in entity_address or entity_address in cluster_address:
                        matches.append({
                            'violation': violation,
                            'fraud_indicator': cluster,
                            'match_type': 'address_cluster'
                        })

    return matches


def main():
    """Main cross-reference function"""
    print("=" * 60)
    print("Cross-Reference Violations with Research Data")
    print("=" * 60)

    # Load violations
    violations_file = DATA_PROCESSED_DIR / "extracted_violations.json"
    if not violations_file.exists():
        print(f"Error: {violations_file} not found. Run enhanced_violation_extraction.py first.")
        return

    print(f"\n1. Loading violations from: {violations_file}")
    with open(violations_file, 'r') as f:
        violations_data = json.load(f)

    violations = violations_data.get('violations', {})
    print(f"   Loaded {sum(len(v) for v in violations.values())} violations")

    # Load Texas lariat data
    print("\n2. Loading Texas lariat data...")
    lariat_data = load_texas_lariat_data()

    # Load research intersections
    print("\n3. Loading research intersections...")
    research_data = load_research_intersections()

    # Correlate violations with management
    print("\n4. Correlating violations with management changes...")
    management_correlations = correlate_violations_with_management(violations, lariat_data)
    print(f"   Found {len(management_correlations)} management correlations")

    # Identify violation networks
    print("\n5. Identifying violation networks...")
    violation_networks = identify_violation_networks(violations, lariat_data)
    print(f"   Found {len(violation_networks)} violation networks")

    # Match with fraud indicators
    print("\n6. Matching with fraud indicators...")
    fraud_matches = match_with_fraud_indicators(
        violations, research_data.get('fraud_indicators', {}), lariat_data
    )
    print(f"   Found {len(fraud_matches)} fraud indicator matches")

    # Create violation propagation map
    print("\n7. Creating violation propagation map...")
    propagation_map = {}

    for network in violation_networks:
        central = network['central_entity']
        if central not in propagation_map:
            propagation_map[central] = {
                'central_entity': central,
                'violations': network['violations'],
                'connected_entities': network['connected_entities'],
                'propagation_paths': []
            }

    # Save results
    output_file = DATA_PROCESSED_DIR / "cross_referenced_violations.json"
    results = {
        'management_correlations': management_correlations,
        'violation_networks': violation_networks,
        'fraud_indicator_matches': fraud_matches,
        'violation_propagation_map': propagation_map,
        'summary': {
            'total_violations': sum(len(v) for v in violations.values()),
            'management_correlations': len(management_correlations),
            'violation_networks': len(violation_networks),
            'fraud_matches': len(fraud_matches),
            'entities_in_networks': len(propagation_map)
        },
        'metadata': {
            'generated': datetime.now().isoformat(),
            'source': 'cross_reference_violations.py'
        }
    }

    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)

    print(f"\n✓ Cross-reference analysis complete!")
    print(f"  Results saved to: {output_file}")
    print(f"\nSummary:")
    print(f"  - Management correlations: {len(management_correlations)}")
    print(f"  - Violation networks: {len(violation_networks)}")
    print(f"  - Fraud indicator matches: {len(fraud_matches)}")
    print(f"  - Entities in networks: {len(propagation_map)}")


if __name__ == '__main__':
    main()
