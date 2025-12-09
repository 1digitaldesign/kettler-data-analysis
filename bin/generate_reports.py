#!/usr/bin/env python3
"""
Generate All Outputs and Reports (Python)
Master script to generate all analysis outputs
"""

import sys
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from scripts.utils.paths import RESEARCH_CONNECTIONS_DIR, RESEARCH_VERIFICATION_DIR, PROJECT_ROOT
from bin.analyze_connections import main_analysis
from bin.validate_data import main_validation

def generate_summary_csvs():
    """
    Generate summary CSV files from analysis results.

    Creates:
    - State summary (connections by state)
    - Connection type summary
    - High-quality records CSV
    """
    print("Generating summary CSV files...")

    # Load data
    connections_file = RESEARCH_CONNECTIONS_DIR / "dpor_skidmore_connections.csv"
    validated_file = RESEARCH_VERIFICATION_DIR / "dpor_validated.csv"

    if connections_file.exists():
        connections = pd.read_csv(connections_file)

        if not connections.empty and 'state' in connections.columns and 'firm_name' in connections.columns:
            # Summary by state
            summary_by_state = connections.groupby('state').agg(
                firm_count=('firm_name', 'nunique'),
                connection_count=('firm_name', 'count')
            ).reset_index().sort_values('connection_count', ascending=False)

            output_file = PROJECT_ROOT / "dpor_multi_state_summary.csv"
            summary_by_state.to_csv(output_file, index=False)
            print(f"Saved state summary to: {output_file}")

        if not connections.empty and 'connection_type' in connections.columns and 'firm_name' in connections.columns:
            # Summary by connection type
            summary_by_type = connections.groupby('connection_type').agg(
                firm_count=('firm_name', 'nunique'),
                connection_count=('firm_name', 'count')
            ).reset_index().sort_values('connection_count', ascending=False)

            output_file = PROJECT_ROOT / "dpor_connection_type_summary.csv"
            summary_by_type.to_csv(output_file, index=False)
            print(f"Saved connection type summary to: {output_file}")

    if validated_file.exists():
        validated = pd.read_csv(validated_file)

        # High-quality records only
        if not validated.empty and all(col in validated.columns for col in ['license_valid', 'address_valid', 'is_duplicate']):
            high_quality = validated[
                ((validated['license_valid'] == True) | validated['license_valid'].isna()) &
                ((validated['address_valid'] == True) | validated['address_valid'].isna()) &
                ((validated['is_duplicate'] == False) | validated['is_duplicate'].isna())
            ]

            output_file = PROJECT_ROOT / "dpor_high_quality_records.csv"
            high_quality.to_csv(output_file, index=False)
            print(f"Saved high-quality records to: {output_file}")

def main_outputs():
    """
    Main output generation function.

    Runs connection analysis, data validation, and generates
    all summary CSV files.
    """
    print("=== Generating All Outputs ===\n")

    print("Step 1: Running connection analysis...")
    main_analysis()

    print("\nStep 2: Running data quality validation...")
    main_validation()

    print("\nStep 3: Generating summary CSV files...")
    generate_summary_csvs()

    print("\n=== All Outputs Generated ===")
    print("\nOutput files:")
    print("  - research/connections/dpor_skidmore_connections.csv")
    print("  - research/verification/dpor_validated.csv")
    print("  - research/summaries/analysis_summary.json")
    print("  - research/summaries/data_quality_report.json")
    print("  - dpor_multi_state_summary.csv")
    print("  - dpor_connection_type_summary.csv")
    print("  - dpor_high_quality_records.csv")

if __name__ == "__main__":
    main_outputs()
