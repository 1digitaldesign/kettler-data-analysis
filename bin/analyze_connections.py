#!/usr/bin/env python3
"""
Analyze Skidmore Connections (Python)
Identifies connections between firms and Caitlin Skidmore from DPOR data
"""

import sys
import re
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import pandas as pd

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from scripts.utils.paths import (
    PROJECT_ROOT, DATA_SOURCE_DIR, DATA_CLEANED_DIR, DATA_ANALYSIS_DIR,
    DATA_DIR
)

def normalize_name(name: str) -> str:
    """Normalize names for matching"""
    if pd.isna(name) or name == "":
        return ""
    name = str(name).upper()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name

def load_skidmore_data() -> Dict[str, pd.DataFrame]:
    """Load existing Skidmore data"""
    # Try CSV first, then JSON
    firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.csv"
    if not firms_file.exists():
        firms_file = DATA_SOURCE_DIR / "skidmore_all_firms_complete.json"
        if firms_file.exists():
            firms_complete = pd.read_json(firms_file)
        else:
            raise FileNotFoundError(f"Cannot find skidmore_all_firms_complete.csv/json in {DATA_SOURCE_DIR}")
    else:
        firms_complete = pd.read_csv(firms_file)

    firms_db_file = DATA_SOURCE_DIR / "skidmore_firms_database.csv"
    if not firms_db_file.exists():
        raise FileNotFoundError(f"Cannot find skidmore_firms_database.csv in {DATA_SOURCE_DIR}")
    firms_db = pd.read_csv(firms_db_file)

    licenses_file = DATA_SOURCE_DIR / "skidmore_individual_licenses.csv"
    if not licenses_file.exists():
        licenses_file = DATA_SOURCE_DIR / "skidmore_individual_licenses.json"
        if licenses_file.exists():
            individual_licenses = pd.read_json(licenses_file)
        else:
            raise FileNotFoundError(f"Cannot find skidmore_individual_licenses.csv/json in {DATA_SOURCE_DIR}")
    else:
        individual_licenses = pd.read_csv(licenses_file)

    return {
        'firms_complete': firms_complete,
        'firms_db': firms_db,
        'individual_licenses': individual_licenses
    }

def load_dpor_results() -> pd.DataFrame:
    """Load cleaned DPOR search results"""
    cleaned_file = DATA_CLEANED_DIR / "dpor_all_cleaned.csv"

    if cleaned_file.exists():
        return pd.read_csv(cleaned_file)

    # Fallback to raw files
    raw_dir = DATA_DIR / "raw"
    if raw_dir.exists():
        raw_files = list(raw_dir.glob("*.csv"))
        if raw_files:
            dfs = []
            for file in raw_files:
                try:
                    df = pd.read_csv(file)
                    dfs.append(df)
                except Exception as e:
                    print(f"Warning: Could not read {file}: {e}")
            if dfs:
                return pd.concat(dfs, ignore_index=True)

    return pd.DataFrame()

def find_skidmore_connections(dpor_results: pd.DataFrame, skidmore_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Find firms connected to Skidmore"""
    connections = []

    if len(dpor_results) == 0:
        return pd.DataFrame(columns=['firm_name', 'license_number', 'state', 'connection_type', 'connection_detail', 'skidmore_license'])

    # Extract Skidmore name variations
    skidmore_names = [
        "SKIDMORE",
        "CAITLIN SKIDMORE",
        "CAITLIN MARIE SKIDMORE",
        "SKIDMORE CAITLIN",
        "SKIDMORE CAITLIN MARIE"
    ]
    skidmore_normalized = [normalize_name(name) for name in skidmore_names]

    # Extract Skidmore addresses from individual licenses
    individual_licenses = skidmore_data.get('individual_licenses', pd.DataFrame())
    if 'address' in individual_licenses.columns:
        skidmore_addresses = individual_licenses['address'].dropna().unique().tolist()
        skidmore_addresses = [addr for addr in skidmore_addresses if addr != ""]
    else:
        skidmore_addresses = []

    # Extract known firm addresses from Skidmore data
    firms_complete = skidmore_data.get('firms_complete', pd.DataFrame())
    if 'Address' in firms_complete.columns:
        known_firm_addresses = firms_complete['Address'].dropna().unique().tolist()
        known_firm_addresses = [addr for addr in known_firm_addresses if addr != ""]
    else:
        known_firm_addresses = []

    # Extract known firm names
    if 'Firm.Name' in firms_complete.columns:
        known_firms = firms_complete['Firm.Name'].dropna().unique().tolist()
    else:
        known_firms = []

    # Check each DPOR result
    for idx, row in dpor_results.iterrows():
        firm_name = row.get('name', '')
        firm_name_cleaned = row.get('name_cleaned', firm_name)
        license_number = row.get('license_number', '')
        address = row.get('address', '')
        address_norm = row.get('address_normalized', address)
        principal_broker = row.get('principal_broker', '')
        state = row.get('state', '')

        connection_found = False
        connection_type = ""
        connection_detail = ""
        skidmore_license = ""

        # Check 1: Principal broker is Skidmore
        if principal_broker and principal_broker != "":
            principal_normalized = normalize_name(principal_broker)
            for skidmore_norm in skidmore_normalized:
                if skidmore_norm in principal_normalized or principal_normalized in skidmore_norm:
                    connection_found = True
                    connection_type = "Principal Broker"
                    connection_detail = f"Listed as Principal Broker: {principal_broker}"
                    break

        # Check 2: Same address as Skidmore licenses
        if not connection_found and address_norm and address_norm != "":
            address_normalized = normalize_name(address_norm)
            for skidmore_addr in skidmore_addresses:
                skidmore_addr_norm = normalize_name(skidmore_addr)
                if address_normalized == skidmore_addr_norm or skidmore_addr_norm in address_normalized:
                    connection_found = True
                    connection_type = "Same Address"
                    connection_detail = f"Same address as Skidmore license: {skidmore_addr}"
                    break

        # Check 3: Same address as known firms
        if not connection_found and address_norm and address_norm != "":
            address_normalized = normalize_name(address_norm)
            for firm_addr in known_firm_addresses:
                firm_addr_norm = normalize_name(firm_addr)
                if address_normalized == firm_addr_norm or firm_addr_norm in address_normalized:
                    connection_found = True
                    connection_type = "Same Address as Known Firm"
                    connection_detail = f"Same address as known firm: {firm_addr}"
                    break

        # Check 4: Firm name matches known firms
        if not connection_found and firm_name_cleaned and firm_name_cleaned != "":
            firm_normalized = normalize_name(firm_name_cleaned)
            for known_firm in known_firms:
                known_firm_norm = normalize_name(known_firm)
                if firm_normalized == known_firm_norm or known_firm_norm in firm_normalized:
                    connection_found = True
                    connection_type = "Known Firm Match"
                    connection_detail = f"Matches known firm: {known_firm}"
                    break

        if connection_found:
            connections.append({
                'firm_name': firm_name_cleaned,
                'license_number': license_number,
                'state': state,
                'connection_type': connection_type,
                'connection_detail': connection_detail,
                'skidmore_license': skidmore_license
            })

    return pd.DataFrame(connections)

def generate_network_analysis(connections: pd.DataFrame, skidmore_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Generate connection network analysis"""
    network = {}

    if len(connections) == 0:
        return {
            'connections_by_type': pd.DataFrame(),
            'connections_by_state': pd.DataFrame(),
            'unique_firms': 0,
            'address_clusters': pd.DataFrame()
        }

    # Count connections by type
    if 'connection_type' in connections.columns:
        network['connections_by_type'] = connections.groupby('connection_type').size().reset_index(name='count')
    else:
        network['connections_by_type'] = pd.DataFrame()

    # Count connections by state
    if 'state' in connections.columns:
        network['connections_by_state'] = connections.groupby('state').size().reset_index(name='count')
    else:
        network['connections_by_state'] = pd.DataFrame()

    # Unique firms connected
    if 'firm_name' in connections.columns:
        network['unique_firms'] = connections['firm_name'].nunique()
    else:
        network['unique_firms'] = 0

    # Address clusters
    if 'address' in connections.columns and 'firm_name' in connections.columns:
        network['address_clusters'] = connections.groupby('address')['firm_name'].nunique().reset_index(name='firm_count')
        network['address_clusters'] = network['address_clusters'].sort_values('firm_count', ascending=False)
    else:
        network['address_clusters'] = pd.DataFrame()

    return network

def create_summary_stats(connections: pd.DataFrame, dpor_results: pd.DataFrame, skidmore_data: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    """Create summary statistics"""
    stats = {}

    stats['total_dpor_results'] = len(dpor_results)
    stats['total_connections'] = len(connections)

    if len(connections) > 0 and 'firm_name' in connections.columns:
        stats['unique_connected_firms'] = connections['firm_name'].nunique()
    else:
        stats['unique_connected_firms'] = 0

    if len(connections) > 0 and 'state' in connections.columns:
        stats['states_with_connections'] = connections['state'].nunique()
    else:
        stats['states_with_connections'] = 0

    # Connection types breakdown
    if len(connections) > 0 and 'connection_type' in connections.columns:
        stats['connection_types'] = connections.groupby('connection_type').size().reset_index(name='count').to_dict('records')
    else:
        stats['connection_types'] = []

    # States breakdown
    if len(connections) > 0 and 'state' in connections.columns:
        stats['states'] = connections.groupby('state').size().reset_index(name='count').to_dict('records')
    else:
        stats['states'] = []

    # Known firms from original data
    firms_complete = skidmore_data.get('firms_complete', pd.DataFrame())
    if len(firms_complete) > 0 and 'Firm.Name' in firms_complete.columns:
        stats['known_firms_count'] = len(firms_complete)
        stats['known_firms'] = firms_complete['Firm.Name'].tolist()
    else:
        stats['known_firms_count'] = 0
        stats['known_firms'] = []

    return stats

def main_analysis():
    """Main analysis function"""
    print("Loading data...")

    # Load existing Skidmore data
    skidmore_data = load_skidmore_data()
    firms_count = len(skidmore_data.get('firms_complete', pd.DataFrame()))
    licenses_count = len(skidmore_data.get('individual_licenses', pd.DataFrame()))
    print(f"Loaded {firms_count} known firms")
    print(f"Loaded {licenses_count} Skidmore individual licenses")

    # Load DPOR search results
    dpor_results = load_dpor_results()
    print(f"Loaded {len(dpor_results)} DPOR search results")

    if len(dpor_results) == 0:
        print("No DPOR results found. Run search scripts first.")
        return

    # Find connections
    print("\nAnalyzing connections...")
    connections = find_skidmore_connections(dpor_results, skidmore_data)
    print(f"Found {len(connections)} connections")

    # Save connections
    DATA_ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    connections_file = DATA_ANALYSIS_DIR / "dpor_skidmore_connections.csv"
    connections.to_csv(connections_file, index=False)
    print(f"Saved connections to: {connections_file}")

    # Generate network analysis
    print("\nGenerating network analysis...")
    network = generate_network_analysis(connections, skidmore_data)

    # Create summary statistics
    stats = create_summary_stats(connections, dpor_results, skidmore_data)

    # Save summary
    summary_file = DATA_ANALYSIS_DIR / "analysis_summary.json"
    summary_json = {
        'statistics': stats,
        'network': {
            'connections_by_type': network['connections_by_type'].to_dict('records') if len(network['connections_by_type']) > 0 else [],
            'connections_by_state': network['connections_by_state'].to_dict('records') if len(network['connections_by_state']) > 0 else [],
            'unique_firms': network['unique_firms'],
            'address_clusters': network['address_clusters'].to_dict('records') if len(network['address_clusters']) > 0 else []
        },
        'timestamp': datetime.now().isoformat()
    }
    with open(summary_file, 'w') as f:
        json.dump(summary_json, f, indent=2, default=str)
    print(f"Saved summary to: {summary_file}")

    # Print summary
    print("\n=== Analysis Summary ===")
    print(f"Total DPOR Results: {stats['total_dpor_results']}")
    print(f"Total Connections Found: {stats['total_connections']}")
    print(f"Unique Connected Firms: {stats['unique_connected_firms']}")
    print(f"States with Connections: {stats['states_with_connections']}")

    print("\nConnection Types:")
    for ct in stats['connection_types']:
        print(f"  {ct['connection_type']}: {ct['count']}")

    print("\nTop States:")
    for state_info in stats['states'][:10]:
        print(f"  {state_info['state']}: {state_info['count']}")

    print("\n=== Analysis Complete ===")

if __name__ == "__main__":
    main_analysis()
