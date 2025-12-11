#!/usr/bin/env python3
"""
Process PDFs and lariat.txt recursively with abnormal pattern analysis
Creates JSON files and embeddings for each recursive structure
Analyzes for abnormal patterns especially in US context
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Installing sentence-transformers...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "sentence-transformers"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Warning: Could not install sentence-transformers automatically.")
        sys.exit(1)
    from sentence_transformers import SentenceTransformer

try:
    import pdfplumber
except ImportError:
    print("Installing pdfplumber...")
    import subprocess
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "--break-system-packages", "pdfplumber"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        print("Warning: Could not install pdfplumber automatically.")
        sys.exit(1)
    import pdfplumber

# US state abbreviations for pattern detection
US_STATES = {
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY', 'DC'
}

def extract_text_from_pdf(pdf_path: Path) -> List[Dict[str, Any]]:
    """Extract text from PDF by pages"""
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    pages.append({
                        'page_number': i + 1,
                        'text': text,
                        'char_count': len(text),
                        'word_count': len(text.split())
                    })
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
    return pages

def detect_us_addresses(text: str) -> List[Dict[str, Any]]:
    """Detect US addresses in text"""
    addresses = []
    # Pattern for US addresses (street, city, state zip)
    patterns = [
        r'(\d+\s+[\w\s]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|Court|Ct|Place|Pl|Way|Circle|Cir|Parkway|Pkwy))[,\s]+([A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)[,\s]+([A-Z]{2})[,\s]+(\d{5}(?:-\d{4})?)',
        r'([A-Z][a-z]+(?:[\s-][A-Z][a-z]+)*)[,\s]+([A-Z]{2})[,\s]+(\d{5}(?:-\d{4})?)',  # City, State ZIP
    ]

    for pattern in patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            addresses.append({
                'full_match': match.group(0),
                'groups': match.groups(),
                'start': match.start(),
                'end': match.end()
            })

    return addresses

def detect_us_entities(text: str) -> List[Dict[str, Any]]:
    """Detect US business entities in text"""
    entities = []
    # Patterns for common US business entity types
    entity_patterns = [
        r'([A-Z][A-Za-z0-9\s&,\.-]+?)\s+(Inc\.|LLC|L\.L\.C\.|Corp\.|Corporation|LP|L\.P\.|LLP|L\.L\.P\.|PC|P\.C\.)',
        r'([A-Z][A-Za-z0-9\s&,\.-]+?)\s+(Management|Services|Group|Holdings|Properties|Realty|Advisors)',
    ]

    for pattern in entity_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            entities.append({
                'name': match.group(0),
                'entity_type': match.group(2) if len(match.groups()) > 1 else None,
                'start': match.start(),
                'end': match.end()
            })

    return entities

def detect_dates(text: str) -> List[Dict[str, Any]]:
    """Detect dates in text"""
    dates = []
    # Various date patterns
    date_patterns = [
        r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
        r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
        r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
    ]

    for pattern in date_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            dates.append({
                'date': match.group(0),
                'start': match.start(),
                'end': match.end()
            })

    return dates

def analyze_abnormal_patterns(text: str, page_num: int, source: str) -> Dict[str, Any]:
    """Analyze text for abnormal patterns in US context"""
    anomalies = {
        'page_number': page_num,
        'source': source,
        'address_clusters': [],
        'entity_variations': [],
        'date_sequences': [],
        'suspicious_patterns': []
    }

    # Detect addresses
    addresses = detect_us_addresses(text)
    if len(addresses) > 5:  # Multiple addresses on one page
        anomalies['address_clusters'].append({
            'count': len(addresses),
            'addresses': addresses[:10],  # Limit to first 10
            'pattern': 'Multiple addresses clustered',
            'severity': 'medium'
        })

    # Detect entities
    entities = detect_us_entities(text)
    entity_names = {}
    for entity in entities:
        name = entity['name'].upper()
        if name not in entity_names:
            entity_names[name] = []
        entity_names[name].append(entity)

    # Check for entity name variations
    for name, occurrences in entity_names.items():
        if len(occurrences) > 3:
            anomalies['entity_variations'].append({
                'entity_name': name,
                'occurrences': len(occurrences),
                'pattern': 'Repeated entity name',
                'severity': 'low'
            })

    # Detect dates
    dates = detect_dates(text)
    if len(dates) > 10:
        anomalies['date_sequences'].append({
            'count': len(dates),
            'pattern': 'High density of dates',
            'severity': 'low'
        })

    # Check for suspicious patterns
    # Multiple state abbreviations in close proximity
    state_pattern = r'\b(' + '|'.join(US_STATES) + r')\b'
    states = re.findall(state_pattern, text)
    if len(states) > 5:
        unique_states = set(states)
        if len(unique_states) > 3:
            anomalies['suspicious_patterns'].append({
                'pattern': 'Multiple states mentioned',
                'states': list(unique_states),
                'count': len(states),
                'severity': 'medium'
            })

    # Check for shell company indicators
    shell_indicators = ['registered agent', 'c/o', 'suite', 'ste', 'mail forwarding', 'virtual office']
    shell_count = sum(1 for indicator in shell_indicators if indicator.lower() in text.lower())
    if shell_count > 2:
        anomalies['suspicious_patterns'].append({
            'pattern': 'Possible shell company indicators',
            'indicators_found': shell_count,
            'severity': 'high'
        })

    return anomalies

def create_text_representation(data: Dict[str, Any], prefix: str = "") -> str:
    """Create text representation for embedding"""
    text_parts = []

    if isinstance(data, dict):
        for key, value in data.items():
            if value is not None:
                if isinstance(value, (dict, list)):
                    if isinstance(value, list) and len(value) > 0:
                        text_parts.append(f"{key}: {len(value)} items")
                    elif isinstance(value, dict):
                        text_parts.append(f"{key}: {json.dumps(value, separators=(',', ':'))}")
                else:
                    text_parts.append(f"{key}: {value}")
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, dict):
                text_parts.append(f"Item {i}: {json.dumps(item, separators=(',', ':'))}")
            else:
                text_parts.append(f"Item {i}: {item}")
    else:
        text_parts.append(str(data))

    return " | ".join(text_parts)

def generate_embedding(text: str, model: SentenceTransformer) -> Optional[List[float]]:
    """Generate embedding for text"""
    if not text or not text.strip():
        return None
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()

def save_json_with_embedding(data: Dict[str, Any], file_path: Path, model: SentenceTransformer,
                            text_representation: Optional[str] = None):
    """Save JSON file and generate embedding"""
    file_path.parent.mkdir(parents=True, exist_ok=True)

    if text_representation is None:
        text_representation = create_text_representation(data)

    embedding = generate_embedding(text_representation, model)

    output = {
        'metadata': {
            'source': 'pdf_analysis',
            'created': datetime.now().isoformat(),
            'file_path': str(file_path),
            'has_embedding': embedding is not None
        },
        'data': data,
        'text_representation': text_representation,
        'embedding': embedding
    }

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    return output

def process_pdf(pdf_path: Path, base_dir: Path, model: SentenceTransformer, index: Dict[str, Any]):
    """Process a PDF file recursively"""
    pdf_name = pdf_path.stem
    print(f"   Processing PDF: {pdf_name}")

    # Extract pages
    pages = extract_text_from_pdf(pdf_path)
    print(f"     Extracted {len(pages)} pages")

    pdf_index = {
        'source_file': str(pdf_path),
        'total_pages': len(pages),
        'pages': []
    }

    # Process each page
    for page in pages:
        page_num = page['page_number']

        # Analyze for abnormal patterns
        anomalies = analyze_abnormal_patterns(page['text'], page_num, pdf_name)

        # Save page JSON
        page_dir = base_dir / pdf_name / 'pages'
        page_file = page_dir / f"page_{page_num:04d}.json"
        page_data = {
            'page_number': page_num,
            'text': page['text'],
            'char_count': page['char_count'],
            'word_count': page['word_count'],
            'anomalies': anomalies
        }
        save_json_with_embedding(page_data, page_file, model)

        pdf_index['pages'].append({
            'page_number': page_num,
            'file': str(page_file.relative_to(PROJECT_ROOT)),
            'anomalies_count': sum(len(v) if isinstance(v, list) else 1 for v in anomalies.values() if v)
        })

        # Save anomalies separately if found
        if any(anomalies.values()):
            anomalies_dir = base_dir / pdf_name / 'anomalies'
            anomalies_file = anomalies_dir / f"anomalies_page_{page_num:04d}.json"
            save_json_with_embedding(anomalies, anomalies_file, model)

    # Save PDF index
    pdf_index_file = base_dir / pdf_name / 'index.json'
    with open(pdf_index_file, 'w', encoding='utf-8') as f:
        json.dump(pdf_index, f, indent=2, ensure_ascii=False)

    index['pdfs'].append({
        'pdf_name': pdf_name,
        'source_file': str(pdf_path),
        'index_file': str(pdf_index_file.relative_to(PROJECT_ROOT)),
        'total_pages': len(pages)
    })

def process_lariat_txt(txt_path: Path, base_dir: Path, model: SentenceTransformer, index: Dict[str, Any]):
    """Process lariat.txt file recursively"""
    print(f"   Processing lariat.txt")

    # Use existing recursive breakdown script logic
    # For now, we'll reference the existing processed files
    existing_file = PROJECT_ROOT / "research" / "company_registrations" / "data" / "texas" / "lariat_tx_filings.json"

    if existing_file.exists():
        with open(existing_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Create reference in index
        index['lariat_txt'] = {
            'source_file': str(txt_path),
            'processed_file': str(existing_file.relative_to(PROJECT_ROOT)),
            'total_entities': len(data.get('entities', []))
        }

        # Link to existing recursive breakdown
        recursive_index = PROJECT_ROOT / "research" / "texas" / "lariat" / "index.json"
        if recursive_index.exists():
            index['lariat_txt']['recursive_index'] = str(recursive_index.relative_to(PROJECT_ROOT))

def main():
    """Main function"""
    print("=" * 70)
    print("Recursive PDF and TXT Processing with Abnormal Pattern Analysis")
    print("=" * 70)

    # Initialize embedding model
    print("\n1. Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print(f"   ✓ Model loaded (dimension: {model.get_sentence_embedding_dimension()})")

    # Define source files
    base_raw_dir = PROJECT_ROOT / "data" / "raw"
    lariat_txt = base_raw_dir / "lariat.txt"
    lariat_pdf = base_raw_dir / "tx" / "lariat-merged.pdf"
    kettler_pdf = base_raw_dir / "tx" / "MERGED-Kettler.pdf"

    # Create base directory
    base_dir = PROJECT_ROOT / "research" / "texas" / "pdf_analysis"
    base_dir.mkdir(parents=True, exist_ok=True)

    # Initialize index
    index = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'embedding_model': 'all-MiniLM-L6-v2',
            'embedding_dimension': model.get_sentence_embedding_dimension()
        },
        'pdfs': [],
        'lariat_txt': None
    }

    # Process files
    print("\n2. Processing files...")

    # Process lariat.txt
    if lariat_txt.exists():
        process_lariat_txt(lariat_txt, base_dir, model, index)
    else:
        print(f"   Warning: {lariat_txt} not found")

    # Process lariat-merged.pdf
    if lariat_pdf.exists():
        process_pdf(lariat_pdf, base_dir, model, index)
    else:
        print(f"   Warning: {lariat_pdf} not found")

    # Process MERGED-Kettler.pdf
    if kettler_pdf.exists():
        process_pdf(kettler_pdf, base_dir, model, index)
    else:
        print(f"   Warning: {kettler_pdf} not found")

    # Save master index
    index_file = base_dir / "master_index.json"
    print(f"\n3. Saving master index to {index_file}")
    with open(index_file, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    print(f"   ✓ Index saved")

    # Print summary
    print("\n" + "=" * 70)
    print("PROCESSING SUMMARY")
    print("=" * 70)
    print(f"PDFs processed: {len(index['pdfs'])}")
    if index['lariat_txt']:
        print(f"Lariat.txt entities: {index['lariat_txt'].get('total_entities', 0)}")
    print(f"\nBase directory: {base_dir}")
    print(f"Index file: {index_file}")
    print("\n" + "=" * 70)
    print("Processing complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()
