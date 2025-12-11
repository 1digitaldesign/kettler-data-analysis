#!/usr/bin/env python3
"""
Process PDFs and lariat.txt recursively with abnormal pattern analysis
Creates JSON files and embeddings for each recursive structure
Analyzes for abnormal patterns especially in US context
"""

import json
import sys
import re
import warnings
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import os

# CRITICAL: Suppress warnings BEFORE any other imports that might trigger them
warnings.filterwarnings('ignore')
os.environ['PYTHONWARNINGS'] = 'ignore'

# Suppress pdfplumber FontBBox warnings - must be done before importing pdfplumber
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*FontBBox.*')
warnings.filterwarnings('ignore', message='.*font.*', flags=re.IGNORECASE)
import logging
logging.getLogger('pdfplumber').setLevel(logging.CRITICAL)
logging.getLogger('pdfminer').setLevel(logging.CRITICAL)
# Suppress pdfplumber's internal warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
# Suppress stderr for pdfplumber warnings
os.environ['PDFPLUMBER_SUPPRESS_WARNINGS'] = '1'

# Optimize for ARM M4 MAX - use all available cores
CPU_COUNT = os.cpu_count() or 8
# M4 MAX has many performance cores - use 85% for parallel processing
PARALLEL_WORKERS = max(1, int(CPU_COUNT * 0.85))
# Set environment for optimal ARM performance
os.environ['OMP_NUM_THREADS'] = str(PARALLEL_WORKERS)
os.environ['MKL_NUM_THREADS'] = str(PARALLEL_WORKERS)
print(f"ARM M4 MAX optimization: Using {PARALLEL_WORKERS} workers out of {CPU_COUNT} CPU cores")

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

class NullWriter:
    """A file-like object that discards all output"""
    def write(self, s: str) -> int:
        return len(s)

    def flush(self) -> None:
        pass

def extract_text_from_pdf(pdf_path: Path) -> List[Dict[str, Any]]:
    """Extract text from PDF by pages with stderr suppression"""
    pages = []
    try:
        # Suppress warnings and stderr during PDF processing
        import sys

        # Create a null device for stderr that discards all output
        null_stderr = NullWriter()

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            warnings.filterwarnings('ignore', message='.*FontBBox.*')
            warnings.filterwarnings('ignore', category=UserWarning)
            warnings.filterwarnings('ignore', message='.*font.*', flags=re.IGNORECASE)
            # Redirect stderr to suppress FontBBox warnings completely
            old_stderr = sys.stderr
            try:
                sys.stderr = null_stderr
                with pdfplumber.open(pdf_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        text = page.extract_text()
                        if text:
                            # Ensure page_number is integer type
                            pages.append({
                                'page_number': int(i + 1),
                                'text': str(text),
                                'char_count': int(len(text)),
                                'word_count': int(len(text.split()))
                            })
            finally:
                sys.stderr = old_stderr
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

def generate_embeddings_batch(texts: List[str], model: SentenceTransformer) -> List[Optional[List[float]]]:
    """Generate embeddings for multiple texts in batch (optimized for ARM)"""
    if not texts:
        return []
    # Filter empty texts
    valid_texts = [(i, text) for i, text in enumerate(texts) if text and text.strip()]
    if not valid_texts:
        return [None] * len(texts)

    # Extract valid texts
    valid_text_list = [text for _, text in valid_texts]
    # Batch encode (much faster than individual encodes)
    embeddings = model.encode(valid_text_list, normalize_embeddings=True, batch_size=32, show_progress_bar=False)

    # Map back to original positions
    result = [None] * len(texts)
    for idx, (orig_idx, _) in enumerate(valid_texts):
        result[orig_idx] = embeddings[idx].tolist()

    return result

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

# Global model variable for thread-safe access
import threading
_model_lock = threading.Lock()
_shared_model = None

def get_model():
    """Get or initialize the shared model (thread-safe)"""
    global _shared_model
    if _shared_model is None:
        with _model_lock:
            if _shared_model is None:
                _shared_model = SentenceTransformer('all-MiniLM-L6-v2')
    return _shared_model

def process_page_worker(args: Tuple) -> Dict[str, Any]:
    """Worker function for processing a single page in parallel"""
    page_data, pdf_name, base_dir_str, page_num = args

    # Convert string paths back to Path objects
    base_dir = Path(base_dir_str)

    # Ensure page_num is an integer for proper padding
    page_num = int(page_num) if not isinstance(page_num, int) else page_num

    # Get shared model (thread-safe)
    model = get_model()

    # Analyze for abnormal patterns
    anomalies = analyze_abnormal_patterns(page_data['text'], page_num, pdf_name)

    # Save page JSON with zero-padded page number (4 digits)
    page_dir = base_dir / pdf_name / 'pages'
    page_file = page_dir / f"page_{page_num:04d}.json"
    page_output = {
        'page_number': page_num,
        'text': page_data['text'],
        'char_count': page_data['char_count'],
        'word_count': page_data['word_count'],
        'anomalies': anomalies
    }
    save_json_with_embedding(page_output, page_file, model)

    result = {
        'page_number': page_num,
        'file': str(page_file.relative_to(PROJECT_ROOT)),
        'anomalies_count': sum(len(v) if isinstance(v, list) else 1 for v in anomalies.values() if v),
        'has_anomalies': any(anomalies.values()),
        'anomalies': anomalies if any(anomalies.values()) else None
    }

    # Save anomalies separately if found (with zero-padded page number)
    if result['has_anomalies']:
        anomalies_dir = base_dir / pdf_name / 'anomalies'
        anomalies_file = anomalies_dir / f"anomalies_page_{page_num:04d}.json"
        save_json_with_embedding(anomalies, anomalies_file, model)
        result['anomalies_file'] = str(anomalies_file.relative_to(PROJECT_ROOT))

    return result

def process_pdf(pdf_path: Path, base_dir: Path, model: SentenceTransformer, index: Dict[str, Any]):
    """Process a PDF file recursively with parallel page processing"""
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

    # Prepare arguments for parallel processing (convert Path to string for pickling)
    page_args = [
        (page, pdf_name, str(base_dir), page['page_number'])
        for page in pages
    ]

    # Process pages in parallel
    print(f"     Processing {len(pages)} pages in parallel using {PARALLEL_WORKERS} workers...")
    # Use ThreadPoolExecutor for I/O-bound tasks (file writing) instead of ProcessPoolExecutor
    # This avoids model serialization issues and is faster for this use case
    with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as executor:
        results = list(executor.map(process_page_worker, page_args))

    # Collect results
    for result in results:
        pdf_index['pages'].append({
            'page_number': result['page_number'],
            'file': result['file'],
            'anomalies_count': result['anomalies_count']
        })

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

    # Process files in parallel
    print("\n2. Processing files in parallel...")

    # Collect all PDFs to process
    pdfs_to_process = []
    if lariat_pdf.exists():
        pdfs_to_process.append(lariat_pdf)
    if kettler_pdf.exists():
        pdfs_to_process.append(kettler_pdf)

    # Process PDFs sequentially (each PDF processes its pages in parallel internally)
    # This avoids memory issues with multiple large PDFs
    for pdf_path in pdfs_to_process:
        try:
            process_pdf(pdf_path, base_dir, model, index)
            print(f"   ✓ Completed: {pdf_path.name}")
        except Exception as e:
            print(f"   ✗ Error processing {pdf_path.name}: {e}")

    if not pdfs_to_process:
        print("   No PDFs found to process")

    # Process lariat.txt (separate, as it references existing files)
    if lariat_txt.exists():
        process_lariat_txt(lariat_txt, base_dir, model, index)
    else:
        print(f"   Warning: {lariat_txt} not found")

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
