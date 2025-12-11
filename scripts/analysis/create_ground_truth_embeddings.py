#!/usr/bin/env python3
"""
Create Ground Truth Embeddings from Full Law Citations
Generates embeddings from complete law citations to serve as authoritative ground truth
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT, DATA_PROCESSED_DIR, DATA_VECTORS_DIR

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Installing sentence-transformers...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user",
                          "sentence-transformers"],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from sentence_transformers import SentenceTransformer


def create_ground_truth_citation_text(law_data: Dict[str, Any]) -> str:
    """Create comprehensive ground truth text from full law citation"""
    parts = []

    # Full law name
    if "name" in law_data:
        parts.append(f"LAW: {law_data['name']}")

    # Complete description
    if "description" in law_data:
        parts.append(f"DESCRIPTION: {law_data['description']}")

    # Official source URL
    if "url" in law_data:
        parts.append(f"OFFICIAL_SOURCE: {law_data['url']}")

    # Full citations - this is the ground truth
    if "key_sections" in law_data:
        # Create full citation format
        citations = []
        for section in law_data['key_sections']:
            # Ensure proper citation format
            citation = section.strip()
            if not any(marker in citation for marker in ["U.S.C.", "Code", "Stat.", "Penal", "Rev. Stat"]):
                # Try to format if missing
                if "§" in citation:
                    citation = f"{law_data.get('name', '')} {citation}"
            citations.append(citation)

        parts.append(f"FULL_CITATIONS: {' | '.join(citations)}")
        parts.append(f"KEY_SECTIONS: {'; '.join(law_data['key_sections'])}")

    # Reporting forms
    if "reporting_forms" in law_data:
        form_texts = []
        for form in law_data.get("reporting_forms", []):
            form_citation = (
                f"{form.get('form_name', '')} "
                f"({form.get('form_number', '')}) - "
                f"{form.get('agency', '')} - "
                f"{form.get('description', '')} - "
                f"URL: {form.get('url', '')}"
            )
            form_texts.append(form_citation)
        if form_texts:
            parts.append(f"REPORTING_FORMS: {' | '.join(form_texts)}")

    # Relevance
    if "relevance" in law_data:
        parts.append(f"RELEVANCE: {law_data['relevance']}")

    # Ground truth markers
    parts.append("GROUND_TRUTH: TRUE")
    parts.append("AUTHORITATIVE_SOURCE: TRUE")
    parts.append("FULL_CITATION_EMBEDDING: TRUE")

    return " | ".join(parts)


def extract_all_law_citations(law_references: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract all law citations from the reference structure"""
    citations = []

    def extract_recursive(data: Any, path: str = ""):
        if isinstance(data, dict):
            # Check if this is a law entry
            if "name" in data or ("key_sections" in data and len(data.get("key_sections", [])) > 0):
                citation_data = {
                    "path": path,
                    "name": data.get("name", ""),
                    "description": data.get("description", ""),
                    "url": data.get("url", ""),
                    "key_sections": data.get("key_sections", []),
                    "relevance": data.get("relevance", ""),
                    "reporting_forms": data.get("reporting_forms", []),
                    "jurisdiction": "federal" if "federal" in path else
                                   ("state" if "states" in path else "local")
                }
                citations.append(citation_data)

            # Recursively process
            for key, value in data.items():
                if key not in ["embedding", "embedding_text", "metadata"]:
                    new_path = f"{path}.{key}" if path else key
                    extract_recursive(value, new_path)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                extract_recursive(item, new_path)

    extract_recursive(law_references)
    return citations


def create_ground_truth_embeddings(law_references_file: Path, output_file: Path):
    """Create ground truth embeddings from full law citations"""
    print("=" * 80)
    print("Creating Ground Truth Embeddings from Full Law Citations")
    print("=" * 80)

    # Load law references
    print(f"\n📖 Loading law references from {law_references_file}...")
    with open(law_references_file, 'r', encoding='utf-8') as f:
        law_references = json.load(f)
    print("✅ Law references loaded")

    # Extract all citations
    print("\n📋 Extracting all law citations...")
    citations = extract_all_law_citations(law_references)
    print(f"✅ Found {len(citations)} law citations")

    # Load embedding model
    print("\n🤖 Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Model loaded")

    # Create ground truth texts and embeddings
    print("\n🚀 Creating ground truth embeddings from full citations...")
    ground_truth_vectors = []

    for i, citation in enumerate(citations):
        # Create comprehensive ground truth text
        ground_truth_text = create_ground_truth_citation_text(citation)

        # Generate embedding
        embedding = model.encode(ground_truth_text, normalize_embeddings=True)

        ground_truth_vectors.append({
            "id": f"ground_truth_{citation['path']}",
            "path": citation['path'],
            "text": ground_truth_text,
            "embedding": embedding.tolist(),
            "name": citation['name'],
            "url": citation['url'],
            "key_sections": citation['key_sections'],
            "jurisdiction": citation['jurisdiction'],
            "is_ground_truth": True,
            "authoritative": True,
            "created": datetime.now().isoformat()
        })

        if (i + 1) % 10 == 0 or (i + 1) == len(citations):
            print(f"   Progress: {i + 1}/{len(citations)} ({(i+1)/len(citations)*100:.1f}%)")

    # Create output structure
    output_data = {
        "metadata": {
            "created": datetime.now().isoformat(),
            "version": "2.0.0",
            "description": "Ground truth embeddings from full law citations",
            "model": "all-MiniLM-L6-v2",
            "dimension": 384,
            "total_citations": len(ground_truth_vectors),
            "is_ground_truth": True
        },
        "ground_truth_vectors": ground_truth_vectors
    }

    # Save output
    print(f"\n💾 Saving ground truth embeddings to {output_file}...")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("=" * 80)
    print("✅ Ground Truth Embeddings Created")
    print("=" * 80)
    print(f"   File: {output_file}")
    print(f"   Total citations: {len(ground_truth_vectors)}")
    print(f"   Model: all-MiniLM-L6-v2")
    print(f"   Dimensions: 384")
    print(f"   Ground Truth: TRUE")
    print("=" * 80)


def main():
    """Main execution"""
    law_references_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
    output_file = DATA_VECTORS_DIR / "law_ground_truth_embeddings.json"

    if not law_references_file.exists():
        print(f"❌ Error: Law references file not found: {law_references_file}")
        print("   Please run scripts/utils/create_law_references.py first")
        sys.exit(1)

    create_ground_truth_embeddings(law_references_file, output_file)


if __name__ == "__main__":
    main()
