#!/usr/bin/env python3
"""
Extract Evidence from Excel Documents (Python)
Extracts data from Excel files with vector embeddings
"""

import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.utils.paths import PROJECT_ROOT, EVIDENCE_DIR, RESEARCH_DIR
from scripts.etl.vector_embeddings import VectorEmbeddingSystem

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Error: pandas not available. Install with: pip install pandas openpyxl")

def extract_excel_data(excel_path: Path, embedding_system: Optional[VectorEmbeddingSystem] = None) -> Optional[Dict[str, Any]]:
    """Extract data from Excel file"""
    try:
        # Read all sheets
        excel_file = pd.ExcelFile(excel_path)

        extracted = {
            'file': excel_path.name,
            'file_path': str(excel_path),
            'sheets': []
        }

        # Extract data from each sheet
        for sheet_name in excel_file.sheet_names:
            try:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)

                # Extract key information
                sheet_data = {
                    'sheet_name': sheet_name,
                    'row_count': len(df),
                    'col_count': len(df.columns),
                    'column_names': list(df.columns),
                    'sample_data': df.head(min(5, len(df))).to_dict('records') if len(df) > 0 else None
                }

                # Extract entities from all text in the sheet
                if len(df) > 0:
                    all_text = " ".join([str(val) for val in df.values.flatten() if pd.notna(val)])

                    # Extract emails
                    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                    emails = list(set(re.findall(email_pattern, all_text, re.IGNORECASE)))

                    # Extract phone numbers
                    phone_pattern = r'\b(\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
                    phones = list(set(re.findall(phone_pattern, all_text)))

                    # Extract dates
                    date_pattern = r'(?i)\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[-]\d{2}[-]\d{2}|(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b'
                    dates = list(set(re.findall(date_pattern, all_text)))

                    # Extract addresses
                    address_pattern = r'(?i)\d+\s+[A-Za-z0-9\s,.-]+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Court|Ct|Way|Place|Pl)[^,]*,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}'
                    addresses = list(set(re.findall(address_pattern, all_text)))

                    sheet_data['entities'] = {
                        'emails': emails,
                        'phones': phones,
                        'dates': dates,
                        'addresses': addresses
                    }

                    # Create embeddings for this sheet
                    if embedding_system:
                        try:
                            source = f"excel:{excel_path.relative_to(PROJECT_ROOT)}:sheet_{sheet_name}"
                            embedding_system.embed_dataframe(df, source)
                        except Exception as e:
                            print(f"  Warning: Could not create embeddings for sheet {sheet_name}: {e}")

                extracted['sheets'].append(sheet_data)

            except Exception as e:
                print(f"  Error reading sheet {sheet_name}: {e}")

        return extracted

    except Exception as e:
        print(f"Error extracting from {excel_path}: {e}")
        return None

def process_all_excel(embedding_system: Optional[VectorEmbeddingSystem] = None) -> List[Dict[str, Any]]:
    """Process all Excel files"""
    excel_dir = EVIDENCE_DIR / "excel_files"

    if not excel_dir.exists():
        print(f"No Excel directory found at {excel_dir}")
        return []

    excel_files = list(excel_dir.glob("*.xlsx")) + list(excel_dir.glob("*.xls")) + \
                  list(excel_dir.glob("*.XLSX")) + list(excel_dir.glob("*.XLS"))

    if not excel_files:
        print(f"No Excel files found in {excel_dir}")
        return []

    print(f"Processing {len(excel_files)} Excel file(s)...\n")

    all_extracted = []

    for excel_file in excel_files:
        print(f"Processing: {excel_file.name}")

        extracted = extract_excel_data(excel_file, embedding_system)

        if extracted:
            all_extracted.append(extracted)

            # Print summary
            total_emails = sum(len(s.get('entities', {}).get('emails', [])) for s in extracted['sheets'])
            total_addresses = sum(len(s.get('entities', {}).get('addresses', [])) for s in extracted['sheets'])
            print(f"  Sheets: {len(extracted['sheets'])} | "
                  f"Emails: {total_emails} | "
                  f"Addresses: {total_addresses}")

    # Save extracted data
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESEARCH_DIR / "excel_evidence_extracted.json"
    with open(output_file, 'w') as f:
        json.dump(all_extracted, f, indent=2, default=str)
    print(f"\nSaved extracted data to: {output_file}")

    # Create summary CSV
    if all_extracted:
        summary_data = []
        for extracted in all_extracted:
            total_rows = sum(s.get('row_count', 0) for s in extracted['sheets'])
            total_emails = sum(len(s.get('entities', {}).get('emails', [])) for s in extracted['sheets'])
            total_addresses = sum(len(s.get('entities', {}).get('addresses', [])) for s in extracted['sheets'])

            summary_data.append({
                'file': extracted['file'],
                'sheets': len(extracted['sheets']),
                'total_rows': total_rows,
                'emails': total_emails,
                'addresses': total_addresses
            })

        df = pd.DataFrame(summary_data)
        summary_file = RESEARCH_DIR / "excel_evidence_summary.csv"
        df.to_csv(summary_file, index=False)
        print(f"Saved summary to: {summary_file}")

    # Save embeddings if system was used
    if embedding_system:
        try:
            embedding_system.save()
        except Exception as e:
            print(f"Warning: Could not save embeddings: {e}")

    return all_extracted

def main():
    """Main execution"""
    print("=" * 60)
    print("Excel Evidence Extraction (Python)")
    print("=" * 60)
    print()

    if not PANDAS_AVAILABLE:
        print("Error: pandas not available.")
        print("Install with: pip install pandas openpyxl")
        return

    # Initialize embedding system
    try:
        embedding_system = VectorEmbeddingSystem()
        print("Vector embedding system initialized\n")
    except Exception as e:
        print(f"Warning: Could not initialize embedding system: {e}")
        print("Continuing without embeddings...\n")
        embedding_system = None

    # Process all Excel files
    results = process_all_excel(embedding_system)

    print(f"\n{'=' * 60}")
    print(f"Extraction Complete: {len(results)} Excel files processed")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
