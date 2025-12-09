#!/usr/bin/env python3
"""
DPOR Data Cleaning Script using Hugging Face Transformers
Cleans and standardizes license data from multiple state DPOR searches
"""

import pandas as pd
import numpy as np
import re
import json
from pathlib import Path
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import warnings
warnings.filterwarnings('ignore')

# Configuration
# Get project root (parent of bin directory)
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

DATA_DIR = Path(project_root) / "data" / "raw"
CLEANED_DIR = Path(project_root) / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

# Initialize Hugging Face models for NER and text processing
print("Loading Hugging Face models...")
try:
    # Named Entity Recognition for extracting entities
    ner_pipeline = pipeline("ner",
                          model="dbmdz/bert-large-cased-finetuned-conll03-english",
                          aggregation_strategy="simple")
    print("NER model loaded successfully")
except Exception as e:
    print(f"Warning: Could not load NER model: {e}")
    ner_pipeline = None

def clean_firm_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize firm names using pattern matching and Hugging Face NER.

    Args:
        df: DataFrame with 'name' column

    Returns:
        DataFrame with 'name_cleaned' and 'name_ner' columns added
    """
    if 'name' not in df.columns:
        return df

    def standardize_name(name):
        if pd.isna(name) or name == "":
            return name

        # Remove common suffixes and standardize
        name = str(name).strip()

        # Remove trailing punctuation
        name = re.sub(r'[.,;:]+$', '', name)

        # Standardize common suffixes
        name = re.sub(r'\s+(Inc|LLC|Corporation|Corp|Company|Co|Ltd|Limited)\.?$', '', name, flags=re.IGNORECASE)

        # Remove extra whitespace
        name = re.sub(r'\s+', ' ', name).strip()

        # Capitalize properly
        name = name.title()

        return name

    df['name_cleaned'] = df['name'].apply(standardize_name)

    # Use NER to extract organization names if available
    if ner_pipeline:
        try:
            org_names = []
            for name in df['name'].fillna(''):
                if name:
                    entities = ner_pipeline(name)
                    org_entities = [e['word'] for e in entities if e['entity_group'] == 'ORG']
                    if org_entities:
                        org_names.append(' '.join(org_entities))
                    else:
                        org_names.append(name)
                else:
                    org_names.append('')
            df['name_ner'] = org_names
        except Exception as e:
            print(f"Warning: NER processing failed: {e}")
            df['name_ner'] = df['name_cleaned']
    else:
        df['name_ner'] = df['name_cleaned']

    return df

def normalize_addresses(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize addresses to standard format.

    Standardizes common abbreviations (St -> Street, Ave -> Avenue, etc.)
    and normalizes whitespace and comma usage.

    Args:
        df: DataFrame with 'address' column

    Returns:
        DataFrame with 'address_normalized' column added
    """
    if 'address' not in df.columns:
        return df

    def normalize_address(addr):
        if pd.isna(addr) or addr == "":
            return addr

        addr = str(addr).strip()

        # Standardize common abbreviations
        replacements = {
            r'\bSt\b': 'Street',
            r'\bAve\b': 'Avenue',
            r'\bRd\b': 'Road',
            r'\bBlvd\b': 'Boulevard',
            r'\bDr\b': 'Drive',
            r'\bLn\b': 'Lane',
            r'\bPkwy\b': 'Parkway',
            r'\bSte\b': 'Suite',
            r'\bSte\.\b': 'Suite',
            r'\b#\s*': 'Suite ',
            r'\bApt\b': 'Apartment',
            r'\bApt\.\b': 'Apartment',
        }

        for pattern, replacement in replacements.items():
            addr = re.sub(pattern, replacement, addr, flags=re.IGNORECASE)

        # Remove extra whitespace
        addr = re.sub(r'\s+', ' ', addr).strip()

        # Standardize comma usage
        addr = re.sub(r',\s*,', ',', addr)  # Remove double commas
        addr = re.sub(r'\s*,\s*', ', ', addr)  # Standardize comma spacing

        return addr

    df['address_normalized'] = df['address'].apply(normalize_address)

    return df

def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse and standardize date formats.

    Attempts multiple date formats and standardizes to YYYY-MM-DD.

    Args:
        df: DataFrame with date columns ('expiration_date', 'initial_cert_date')

    Returns:
        DataFrame with '_parsed' columns added for each date column
    """
    date_columns = ['expiration_date', 'initial_cert_date']

    for col in date_columns:
        if col not in df.columns:
            continue

        def parse_date(date_str):
            if pd.isna(date_str) or date_str == "":
                return None

            date_str = str(date_str).strip()

            # Try pandas date parsing
            try:
                parsed = pd.to_datetime(date_str, errors='coerce', infer_datetime_format=True)
                if pd.notna(parsed):
                    return parsed.strftime('%Y-%m-%d')
            except:
                pass

            # Try common formats
            formats = [
                '%Y-%m-%d',
                '%m/%d/%Y',
                '%d/%m/%Y',
                '%Y/%m/%d',
                '%m-%d-%Y',
                '%d-%m-%Y',
            ]

            for fmt in formats:
                try:
                    parsed = pd.to_datetime(date_str, format=fmt)
                    return parsed.strftime('%Y-%m-%d')
                except:
                    continue

            return date_str  # Return original if can't parse

        df[f'{col}_parsed'] = df[col].apply(parse_date)

    return df

def extract_entities(text):
    """
    Extract entities from text using Hugging Face NER
    """
    if not text or pd.isna(text):
        return {}

    if not ner_pipeline:
        return {}

    try:
        entities = ner_pipeline(str(text))
        result = {
            'organizations': [],
            'locations': [],
            'persons': []
        }

        for entity in entities:
            entity_group = entity.get('entity_group', '')
            word = entity.get('word', '')

            if entity_group == 'ORG':
                result['organizations'].append(word)
            elif entity_group == 'LOC':
                result['locations'].append(word)
            elif entity_group == 'PER':
                result['persons'].append(word)

        return result
    except Exception as e:
        print(f"Error extracting entities: {e}")
        return {}

def deduplicate_results(df: pd.DataFrame) -> pd.DataFrame:
    """
    Intelligent deduplication based on license number, name, and address.

    Creates deduplication keys from normalized fields and removes exact duplicates.

    Args:
        df: DataFrame to deduplicate

    Returns:
        DataFrame with duplicates removed
    """
    if df.empty:
        return df

    # Create deduplication key
    # Use conditional column access - pandas DataFrames don't have .get() method
    # Important: Use df.index to ensure proper alignment when creating fallback Series
    license_col = df['license_number'] if 'license_number' in df.columns else pd.Series([''] * len(df), index=df.index)
    name_col = df['name_cleaned'] if 'name_cleaned' in df.columns else (df['name'] if 'name' in df.columns else pd.Series([''] * len(df), index=df.index))
    address_col = df['address_normalized'] if 'address_normalized' in df.columns else (df['address'] if 'address' in df.columns else pd.Series([''] * len(df), index=df.index))
    state_col = df['state'] if 'state' in df.columns else pd.Series([''] * len(df), index=df.index)

    df['dedup_key'] = (
        license_col.fillna('').astype(str) + '|' +
        name_col.fillna('').astype(str) + '|' +
        address_col.fillna('').astype(str) + '|' +
        state_col.fillna('').astype(str)
    )

    # Remove exact duplicates
    df = df.drop_duplicates(subset=['dedup_key'], keep='first')

    # Remove dedup_key column
    df = df.drop(columns=['dedup_key'], errors='ignore')

    return df

def clean_all_files():
    """
    Process all CSV files in the raw data directory
    """
    csv_files = list(DATA_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {DATA_DIR}")
        return

    print(f"Found {len(csv_files)} CSV files to process")

    all_cleaned = []

    for csv_file in csv_files:
        print(f"\nProcessing: {csv_file.name}")

        try:
            # Read CSV
            df = pd.read_csv(csv_file)

            if df.empty:
                print(f"  Skipping empty file: {csv_file.name}")
                continue

            print(f"  Original rows: {len(df)}")

            # Clean firm names
            df = clean_firm_names(df)

            # Normalize addresses
            df = normalize_addresses(df)

            # Parse dates
            df = parse_dates(df)

            # Deduplicate
            df = deduplicate_results(df)

            print(f"  Cleaned rows: {len(df)}")

            # Save cleaned file
            output_file = CLEANED_DIR / csv_file.name
            df.to_csv(output_file, index=False)
            print(f"  Saved to: {output_file}")

            all_cleaned.append(df)

        except Exception as e:
            print(f"  Error processing {csv_file.name}: {e}")
            continue

    # Combine all cleaned data
    if all_cleaned:
        combined = pd.concat(all_cleaned, ignore_index=True)

        # Final deduplication across all files
        combined = deduplicate_results(combined)

        # Save combined file
        combined_file = CLEANED_DIR / "dpor_all_cleaned.csv"
        combined.to_csv(combined_file, index=False)
        print(f"\nCombined cleaned data saved to: {combined_file}")
        print(f"Total unique records: {len(combined)}")

        return combined

    return None

def create_summary_report(df: pd.DataFrame) -> None:
    """
    Create summary statistics report.

    Generates JSON report with total records, unique firms, states covered,
    and distribution statistics.

    Args:
        df: Cleaned DataFrame to summarize
    """
    if df is None or df.empty:
        return

    summary = {
        'total_records': len(df),
        'unique_firms': df['name_cleaned'].nunique() if 'name_cleaned' in df.columns else 0,
        'states_covered': df['state'].nunique() if 'state' in df.columns else 0,
        'records_by_state': df['state'].value_counts().to_dict() if 'state' in df.columns else {},
        'license_types': df['license_type'].value_counts().to_dict() if 'license_type' in df.columns else {}
    }

    summary_file = CLEANED_DIR / "cleaning_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nSummary report saved to: {summary_file}")
    print(json.dumps(summary, indent=2))

def main() -> None:
    """
    Main execution function for data cleaning pipeline.

    Processes all raw CSV files, cleans data, and generates summary report.
    """
    print("Starting DPOR data cleaning process...")
    print("=" * 60)

    # Clean all files
    cleaned_df = clean_all_files()

    # Create summary report
    if cleaned_df is not None:
        create_summary_report(cleaned_df)

    print("\n" + "=" * 60)
    print("Data cleaning complete!")

if __name__ == "__main__":
    main()
