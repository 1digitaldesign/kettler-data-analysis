#!/usr/bin/env python3
"""
Data Quality Validation Script (Python)
Validates license data, flags duplicates, and creates quality reports
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
    PROJECT_ROOT, DATA_CLEANED_DIR, RESEARCH_VERIFICATION_DIR, RESEARCH_SUMMARIES_DIR
)

def normalize_text(text: str) -> str:
    """Normalize text for matching"""
    if pd.isna(text) or text == "":
        return ""
    return re.sub(r'[^\w\s]', '', str(text).upper()).strip()

def validate_license_numbers(df: pd.DataFrame) -> pd.DataFrame:
    """Validate license number formats"""
    if len(df) == 0:
        return df

    if 'license_number' not in df.columns:
        df['license_valid'] = None
        df['license_format_issue'] = "License number column not found"
        return df

    df['license_valid'] = True
    df['license_format_issue'] = ""

    for idx, row in df.iterrows():
        license = row.get('license_number', '')

        if pd.isna(license) or license == "":
            df.at[idx, 'license_valid'] = False
            df.at[idx, 'license_format_issue'] = "Missing license number"
            continue

        license = str(license).strip()

        # Check for common valid formats (6-15 characters, alphanumeric)
        if len(license) < 6 or len(license) > 15:
            df.at[idx, 'license_valid'] = False
            df.at[idx, 'license_format_issue'] = f"Invalid length: {len(license)}"

        # Check for invalid characters
        if not re.match(r'^[A-Za-z0-9\s\-]+$', license):
            df.at[idx, 'license_valid'] = False
            df.at[idx, 'license_format_issue'] = "Contains invalid characters"

    return df

def flag_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Flag potential duplicates"""
    if len(df) == 0:
        return df

    df['is_duplicate'] = False
    df['duplicate_group'] = None
    df['duplicate_reason'] = ""

    # Create matching keys
    has_license = 'license_number' in df.columns
    has_name = 'name' in df.columns
    has_address = 'address' in df.columns
    has_state = 'state' in df.columns

    license_part = df['license_number'].apply(lambda x: normalize_text(str(x))) if has_license else pd.Series([''] * len(df))
    name_part = df['name'].apply(lambda x: normalize_text(str(x))) if has_name else pd.Series([''] * len(df))
    address_part = df['address'].apply(lambda x: normalize_text(str(x))) if has_address else pd.Series([''] * len(df))
    state_part = df['state'].apply(lambda x: normalize_text(str(x))) if has_state else pd.Series([''] * len(df))

    df['match_key1'] = license_part + "|" + name_part + "|" + state_part
    df['match_key2'] = name_part + "|" + address_part + "|" + state_part

    # Find duplicates by license number + name + state
    dup_groups1 = df[df.groupby('match_key1')['match_key1'].transform('size') > 1].copy()
    if len(dup_groups1) > 0:
        dup_groups1['duplicate_group'] = dup_groups1.groupby('match_key1').ngroup() + 1
        df.loc[dup_groups1.index, 'is_duplicate'] = True
        df.loc[dup_groups1.index, 'duplicate_group'] = dup_groups1['duplicate_group']
        df.loc[dup_groups1.index, 'duplicate_reason'] = "Same license number, name, and state"

    # Find duplicates by name + address + state
    max_dup_group = df['duplicate_group'].max() if 'duplicate_group' in df.columns else 0
    if pd.isna(max_dup_group):
        max_dup_group = 0

    dup_groups2 = df[~df['is_duplicate'] & (df.groupby('match_key2')['match_key2'].transform('size') > 1)].copy()
    if len(dup_groups2) > 0:
        dup_groups2['duplicate_group'] = max_dup_group + dup_groups2.groupby('match_key2').ngroup() + 1
        df.loc[dup_groups2.index, 'is_duplicate'] = True
        df.loc[dup_groups2.index, 'duplicate_group'] = dup_groups2['duplicate_group']
        df.loc[dup_groups2.index, 'duplicate_reason'] = "Same name, address, and state (different license)"

    # Remove temporary columns
    df = df.drop(columns=['match_key1', 'match_key2'])

    return df

def validate_addresses(df: pd.DataFrame) -> pd.DataFrame:
    """Validate addresses"""
    if len(df) == 0 or 'address' not in df.columns:
        return df

    df['address_valid'] = True
    df['address_issue'] = ""

    for idx, row in df.iterrows():
        addr = row.get('address', '')

        if pd.isna(addr) or addr == "":
            df.at[idx, 'address_valid'] = False
            df.at[idx, 'address_issue'] = "Missing address"
            continue

        addr = str(addr).strip()

        # Check for minimum length
        if len(addr) < 10:
            df.at[idx, 'address_valid'] = False
            df.at[idx, 'address_issue'] = "Address too short"

        # Check for common address components
        has_street = bool(re.search(r'(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln)', addr, re.IGNORECASE))
        has_city = bool(re.search(r'[A-Z]{2}\s+\d{5}', addr))  # State + ZIP pattern

        if not has_street and not has_city:
            df.at[idx, 'address_valid'] = False
            df.at[idx, 'address_issue'] = "Missing street or city/state/zip"

    return df

def validate_dates(df: pd.DataFrame) -> pd.DataFrame:
    """Validate dates"""
    if len(df) == 0:
        return df

    date_columns = ['expiration_date', 'initial_cert_date', 'expiration_date_parsed', 'initial_cert_date_parsed']

    for col in date_columns:
        if col not in df.columns:
            continue

        df[f'{col}_valid'] = True
        df[f'{col}_issue'] = ""

        for idx, row in df.iterrows():
            date_val = row.get(col)

            if pd.isna(date_val) or date_val == "":
                df.at[idx, f'{col}_valid'] = False
                df.at[idx, f'{col}_issue'] = "Missing date"
                continue

            # Try to parse date
            try:
                parsed_date = pd.to_datetime(date_val)

                # Check if date is reasonable
                if parsed_date < pd.Timestamp('1900-01-01') or parsed_date > pd.Timestamp('2100-01-01'):
                    df.at[idx, f'{col}_valid'] = False
                    df.at[idx, f'{col}_issue'] = "Date out of reasonable range"
            except:
                df.at[idx, f'{col}_valid'] = False
                df.at[idx, f'{col}_issue'] = "Invalid date format"

    return df

def cross_reference_addresses(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-reference addresses"""
    if len(df) == 0 or 'address' not in df.columns:
        return df

    df['address_cluster'] = None

    # Normalize addresses for clustering
    df['address_normalized_cluster'] = df['address'].apply(
        lambda x: normalize_text(str(x)) if pd.notna(x) and x != "" else ""
    )

    # Group by normalized address
    address_groups = df.groupby('address_normalized_cluster').ngroup() + 1
    df['address_cluster'] = df['address_normalized_cluster'].map(
        dict(zip(df['address_normalized_cluster'].unique(), range(1, len(df['address_normalized_cluster'].unique()) + 1)))
    )

    df = df.drop(columns=['address_normalized_cluster'])

    return df

def generate_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
    """Generate data quality report"""
    report = {}

    if len(df) == 0:
        return {
            'total_records': 0,
            'overall_completeness': 0,
            'note': "No data to generate report"
        }

    report['total_records'] = len(df)

    # License number validation
    if 'license_valid' in df.columns:
        report['license_validation'] = {
            'valid': int(df['license_valid'].sum()) if 'license_valid' in df.columns else 0,
            'invalid': int((~df['license_valid']).sum()) if 'license_valid' in df.columns else 0,
            'missing': int(df['license_number'].isna().sum() | (df['license_number'] == "").sum()) if 'license_number' in df.columns else 0
        }

    # Duplicate analysis
    if 'is_duplicate' in df.columns:
        duplicate_groups = df[df['is_duplicate']]['duplicate_group'].dropna().unique()
        report['duplicates'] = {
            'total_duplicates': int(df['is_duplicate'].sum()),
            'duplicate_groups': len(duplicate_groups),
            'unique_records': int((~df['is_duplicate']).sum())
        }

    # Address validation
    if 'address_valid' in df.columns:
        report['address_validation'] = {
            'valid': int(df['address_valid'].sum()),
            'invalid': int((~df['address_valid']).sum()),
            'missing': int(df['address'].isna().sum() | (df['address'] == "").sum()) if 'address' in df.columns else 0
        }

    # Date validation
    date_cols = [col for col in df.columns if col.endswith('_valid') and 'date' in col]
    report['date_validation'] = {}
    for col in date_cols:
        report['date_validation'][col] = {
            'valid': int(df[col].sum()),
            'invalid': int((~df[col]).sum())
        }

    # Completeness score
    required_fields = ['license_number', 'name', 'state', 'address']
    completeness_scores = {}
    for field in required_fields:
        if field in df.columns:
            completeness_scores[field] = float((df[field].notna() & (df[field] != "")).sum() / len(df) * 100)
        else:
            completeness_scores[field] = 0.0

    report['completeness'] = completeness_scores
    report['overall_completeness'] = sum(completeness_scores.values()) / len(completeness_scores) if completeness_scores else 0.0

    # State distribution
    if 'state' in df.columns:
        state_dist = df['state'].value_counts().reset_index()
        state_dist.columns = ['state', 'count']
        report['state_distribution'] = state_dist.to_dict('records')

    return report

def main_validation():
    """Main validation function"""
    print("Starting data quality validation...")

    # Load cleaned data
    cleaned_file = DATA_CLEANED_DIR / "dpor_all_cleaned.csv"

    if not cleaned_file.exists():
        print("Cleaned data file not found. Running cleaning script first...")
        return

    df = pd.read_csv(cleaned_file)
    print(f"Loaded {len(df)} records for validation")

    if len(df) == 0:
        print("No data to validate")
        return

    # Run validations
    print("\nValidating license numbers...")
    df = validate_license_numbers(df)

    print("Flagging duplicates...")
    df = flag_duplicates(df)

    print("Validating addresses...")
    df = validate_addresses(df)

    print("Validating dates...")
    df = validate_dates(df)

    print("Cross-referencing addresses...")
    df = cross_reference_addresses(df)

    # Generate quality report
    print("\nGenerating quality report...")
    report = generate_quality_report(df)

    # Save validated data
    RESEARCH_VERIFICATION_DIR.mkdir(parents=True, exist_ok=True)
    RESEARCH_SUMMARIES_DIR.mkdir(parents=True, exist_ok=True)

    validated_file = RESEARCH_VERIFICATION_DIR / "dpor_validated.csv"
    df.to_csv(validated_file, index=False)
    print(f"Saved validated data to: {validated_file}")

    # Save quality report
    report_file = RESEARCH_SUMMARIES_DIR / "data_quality_report.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"Saved quality report to: {report_file}")

    # Save flagged issues
    if 'license_valid' in df.columns and 'is_duplicate' in df.columns and 'address_valid' in df.columns:
        issues = df[
            (df['license_valid'] == False) |
            (df['is_duplicate'] == True) |
            (df['address_valid'] == False)
        ]

        if len(issues) > 0:
            issues_file = RESEARCH_VERIFICATION_DIR / "data_quality_issues.csv"
            issues.to_csv(issues_file, index=False)
            print(f"Saved {len(issues)} flagged issues to: {issues_file}")

    # Print summary
    print("\n=== Data Quality Summary ===")
    print(f"Total Records: {report['total_records']}")
    print(f"Overall Completeness: {report['overall_completeness']:.2f}%")

    if 'license_validation' in report:
        print("\nLicense Validation:")
        print(f"  Valid: {report['license_validation']['valid']}")
        print(f"  Invalid: {report['license_validation']['invalid']}")
        print(f"  Missing: {report['license_validation']['missing']}")

    if 'duplicates' in report:
        print("\nDuplicates:")
        print(f"  Total Duplicate Records: {report['duplicates']['total_duplicates']}")
        print(f"  Duplicate Groups: {report['duplicates']['duplicate_groups']}")
        print(f"  Unique Records: {report['duplicates']['unique_records']}")

    print("\n=== Validation Complete ===")

if __name__ == "__main__":
    main_validation()
