#!/usr/bin/env python3
"""
Extract Evidence from PDF Documents (Python)
Extracts text, metadata, and entities from PDF files with vector embeddings
"""

import sys
import re
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.utils.paths import PROJECT_ROOT, EVIDENCE_DIR, RESEARCH_DIR
from scripts.etl.vector_embeddings import VectorEmbeddingSystem

# Try to import PDF libraries
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False
    print("Warning: PyPDF2 not available. Install with: pip install PyPDF2")

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False

# Evidence subdirectories
EVIDENCE_SUBDIRS = [
    "pdfs",
    "emails",
    "legal_documents",
    "linkedin_profiles",
    "airbnb",
    "accommodation_forms",
    "correspondence"
]

def extract_pdf_text(pdf_path: Path) -> str:
    """Extract text from PDF file"""
    text = ""

    # Try pdfplumber first (best for text extraction)
    if PDFPLUMBER_AVAILABLE:
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pages_text = []
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
                text = "\n".join(pages_text)
                if text:
                    return text
        except Exception as e:
            print(f"  pdfplumber error: {e}")

    # Try PyPDF2
    if PYPDF2_AVAILABLE and not text:
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                pages_text = []
                for page in pdf_reader.pages:
                    pages_text.append(page.extract_text())
                text = "\n".join(pages_text)
                if text:
                    return text
        except Exception as e:
            print(f"  PyPDF2 error: {e}")

    # Try pypdf (newer library)
    if PYPDF_AVAILABLE and not text:
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                pages_text = []
                for page in pdf_reader.pages:
                    pages_text.append(page.extract_text())
                text = "\n".join(pages_text)
                if text:
                    return text
        except Exception as e:
            print(f"  pypdf error: {e}")

    return text

def extract_pdf_metadata(pdf_path: Path) -> Dict[str, Any]:
    """Extract metadata from PDF file"""
    metadata = {}

    try:
        if PDFPLUMBER_AVAILABLE:
            with pdfplumber.open(pdf_path) as pdf:
                metadata = {
                    'pages': len(pdf.pages),
                    'file_size': pdf_path.stat().st_size
                }
                if pdf.metadata:
                    metadata.update({
                        'title': pdf.metadata.get('Title', ''),
                        'author': pdf.metadata.get('Author', ''),
                        'creator': pdf.metadata.get('Creator', ''),
                        'producer': pdf.metadata.get('Producer', ''),
                        'creation_date': str(pdf.metadata.get('CreationDate', '')),
                        'modification_date': str(pdf.metadata.get('ModDate', ''))
                    })
        elif PYPDF2_AVAILABLE:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata = {
                    'pages': len(pdf_reader.pages),
                    'file_size': pdf_path.stat().st_size
                }
                if pdf_reader.metadata:
                    metadata.update({
                        'title': pdf_reader.metadata.get('/Title', ''),
                        'author': pdf_reader.metadata.get('/Author', ''),
                        'creator': pdf_reader.metadata.get('/Creator', ''),
                        'producer': pdf_reader.metadata.get('/Producer', ''),
                        'creation_date': str(pdf_reader.metadata.get('/CreationDate', '')),
                        'modification_date': str(pdf_reader.metadata.get('/ModDate', ''))
                    })
    except Exception as e:
        print(f"  Error extracting metadata: {e}")

    return metadata

def extract_entities(text: str) -> Dict[str, List[str]]:
    """Extract entities from text (emails, phone numbers, addresses, dates, etc.)"""
    entities = {
        'emails': [],
        'phones': [],
        'dates': [],
        'addresses': [],
        'units': [],
        'license_numbers': [],
        'firms': []
    }

    if not text:
        return entities

    # Email addresses
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    entities['emails'] = list(set(re.findall(email_pattern, text, re.IGNORECASE)))

    # Phone numbers
    phone_pattern = r'\b(\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
    entities['phones'] = list(set(re.findall(phone_pattern, text)))

    # Dates
    date_pattern = r'(?i)\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4}|\d{4}[-]\d{2}[-]\d{2}|(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4})\b'
    entities['dates'] = list(set(re.findall(date_pattern, text)))

    # Addresses
    address_pattern = r'(?i)\d+\s+[A-Za-z0-9\s,.-]+(Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Boulevard|Blvd|Lane|Ln|Court|Ct|Way|Place|Pl)[^,]*,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s+\d{5}'
    entities['addresses'] = list(set(re.findall(address_pattern, text)))

    # Unit numbers
    unit_pattern = r'(?i)Unit\s+(\d+[A-Z]?|[A-Z]\d+)'
    entities['units'] = list(set(re.findall(unit_pattern, text)))

    # License numbers (6-12 digits)
    license_pattern = r'\b\d{6,12}\b'
    entities['license_numbers'] = list(set(re.findall(license_pattern, text)))

    # Company/Firm names
    firm_pattern = r'\b([A-Z][a-z]+\s+)+(Inc|LLC|Corporation|Corp|Company|Co|Ltd|Limited|Management|Partners|Properties|Residential|Services)\b'
    entities['firms'] = list(set(re.findall(firm_pattern, text)))

    return entities

def extract_regulatory_info(text: str) -> Dict[str, int]:
    """Extract key information for regulatory filings"""
    info = {}

    # Violation keywords
    violation_keywords = [
        "violation", "violate", "illegal", "unlawful", "fraud", "fraudulent",
        "misrepresentation", "deceptive", "breach", "non-compliance",
        "unauthorized", "improper", "wrongful", "negligent", "negligence"
    ]

    info['violation_mentions'] = {}
    for keyword in violation_keywords:
        pattern = rf'(?i)\b{re.escape(keyword)}\b'
        matches = re.findall(pattern, text)
        info['violation_mentions'][keyword] = len(matches)

    # Regulatory agency mentions
    agency_keywords = [
        "DPOR", "Department of Professional", "Real Estate Commission",
        "HUD", "Housing and Urban Development", "FTC", "Federal Trade Commission",
        "SEC", "Securities and Exchange", "IRS", "Internal Revenue",
        "BBB", "Better Business Bureau", "Attorney General", "Consumer Protection"
    ]

    info['agency_mentions'] = {}
    for keyword in agency_keywords:
        pattern = rf'(?i){re.escape(keyword)}'
        matches = re.findall(pattern, text)
        info['agency_mentions'][keyword] = len(matches)

    # Lease/rental terms
    lease_keywords = [
        "lease", "rental", "tenant", "landlord", "eviction", "termination",
        "security deposit", "rent", "maintenance", "repair"
    ]

    info['lease_mentions'] = {}
    for keyword in lease_keywords:
        pattern = rf'(?i)\b{re.escape(keyword)}\b'
        matches = re.findall(pattern, text)
        info['lease_mentions'][keyword] = len(matches)

    return info

def process_all_pdfs(embedding_system: Optional[VectorEmbeddingSystem] = None) -> List[Dict[str, Any]]:
    """Process all PDFs in evidence directory and subdirectories"""
    # Collect PDFs from all subdirectories
    pdf_files = []
    evidence_base = EVIDENCE_DIR

    for subdir in EVIDENCE_SUBDIRS:
        subdir_path = evidence_base / subdir
        if subdir_path.exists():
            pdf_files.extend(subdir_path.glob("**/*.pdf"))
            pdf_files.extend(subdir_path.glob("**/*.PDF"))

    # Also check root evidence directory
    if evidence_base.exists():
        pdf_files.extend(evidence_base.glob("*.pdf"))
        pdf_files.extend(evidence_base.glob("*.PDF"))

    # Remove duplicates
    pdf_files = list(set(pdf_files))

    if not pdf_files:
        print("No PDF files found in evidence directories")
        return []

    print(f"Processing {len(pdf_files)} PDF file(s)...\n")

    all_extracted = []

    # Initialize embedding system if not provided
    if embedding_system is None:
        try:
            embedding_system = VectorEmbeddingSystem()
        except Exception as e:
            print(f"Warning: Could not initialize embedding system: {e}")
            embedding_system = None

    for pdf_file in pdf_files:
        print(f"Processing: {pdf_file.name}")

        # Extract text
        text = extract_pdf_text(pdf_file)

        if not text:
            print(f"  Warning: No text extracted from {pdf_file.name}")
            continue

        # Extract metadata
        metadata = extract_pdf_metadata(pdf_file)

        # Extract entities
        entities = extract_entities(text)

        # Extract regulatory information
        regulatory_info = extract_regulatory_info(text)

        # Create embedding for the full text
        if embedding_system:
            try:
                source = f"pdf:{pdf_file.relative_to(PROJECT_ROOT)}"
                pdf_metadata = {
                    'file_name': pdf_file.name,
                    'data_type': 'pdf',
                    'pages': metadata.get('pages', 0),
                    'entities_count': {k: len(v) for k, v in entities.items()}
                }
                embedding_system.embed_text(text, source, pdf_metadata)
            except Exception as e:
                print(f"  Warning: Could not create embedding: {e}")

        # Combine all information
        extracted = {
            'file': pdf_file.name,
            'file_path': str(pdf_file),
            'metadata': metadata,
            'text_length': len(text),
            'text_preview': text[:500] if text else "",
            'entities': entities,
            'regulatory_info': regulatory_info
        }

        all_extracted.append(extracted)

        print(f"  Extracted {len(entities['emails'])} emails, "
              f"{len(entities['addresses'])} addresses, "
              f"{len(entities['firms'])} firms")

    # Save extracted data
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    output_file = RESEARCH_DIR / "pdf_evidence_extracted.json"
    with open(output_file, 'w') as f:
        json.dump(all_extracted, f, indent=2, default=str)
    print(f"\nSaved extracted data to: {output_file}")

    # Create summary CSV
    import pandas as pd
    if all_extracted:
        summary_data = []
        for extracted in all_extracted:
            summary_data.append({
                'file': extracted['file'],
                'emails': len(extracted['entities']['emails']),
                'addresses': len(extracted['entities']['addresses']),
                'firms': len(extracted['entities']['firms']),
                'violation_mentions': sum(extracted['regulatory_info'].get('violation_mentions', {}).values()),
                'agency_mentions': sum(extracted['regulatory_info'].get('agency_mentions', {}).values())
            })

        df = pd.DataFrame(summary_data)
        summary_file = RESEARCH_DIR / "pdf_evidence_summary.csv"
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
    print("PDF Evidence Extraction (Python)")
    print("=" * 60)
    print()

    # Check if PDF libraries are available
    if not any([PYPDF2_AVAILABLE, PDFPLUMBER_AVAILABLE, PYPDF_AVAILABLE]):
        print("Error: No PDF library available.")
        print("Install one of: pip install PyPDF2 pdfplumber pypdf")
        return

    # Initialize embedding system
    try:
        embedding_system = VectorEmbeddingSystem()
        print("Vector embedding system initialized\n")
    except Exception as e:
        print(f"Warning: Could not initialize embedding system: {e}")
        print("Continuing without embeddings...\n")
        embedding_system = None

    # Process all PDFs
    results = process_all_pdfs(embedding_system)

    print(f"\n{'=' * 60}")
    print(f"Extraction Complete: {len(results)} PDFs processed")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main()
