#!/usr/bin/env python3
"""
Extract All Evidence - Master Script (Python)
Extracts data from all PDFs and Excel files with integrated vector embeddings
"""

import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from scripts.utils.paths import PROJECT_ROOT, RESEARCH_DIR
from scripts.etl.vector_embeddings import VectorEmbeddingSystem
from scripts.extraction.extract_pdf_evidence import process_all_pdfs
from scripts.extraction.extract_excel_evidence import process_all_excel
import json
from datetime import datetime

def main_extract_all():
    """Main function to extract all evidence"""
    print("=" * 60)
    print("Extracting All Evidence (Python)")
    print("=" * 60)
    print()

    # Initialize embedding system
    try:
        embedding_system = VectorEmbeddingSystem()
        print("Vector embedding system initialized\n")
    except Exception as e:
        print(f"Warning: Could not initialize embedding system: {e}")
        print("Continuing without embeddings...\n")
        embedding_system = None

    # Step 1: Extract PDFs from all subdirectories
    print("Step 1: Extracting PDF evidence...")
    pdf_results = process_all_pdfs(embedding_system)

    # Step 2: Extract Excel files
    print("\nStep 2: Extracting Excel evidence...")
    excel_results = process_all_excel(embedding_system)

    # Step 3: Combine all results
    print("\nStep 3: Combining all evidence...")
    combined_evidence = {
        'pdfs': pdf_results,
        'excel': excel_results,
        'extraction_date': datetime.now().isoformat(),
        'pdf_count': len(pdf_results),
        'excel_count': len(excel_results)
    }

    # Save combined evidence
    RESEARCH_DIR.mkdir(parents=True, exist_ok=True)
    combined_file = RESEARCH_DIR / "all_evidence_extracted.json"
    with open(combined_file, 'w') as f:
        json.dump(combined_evidence, f, indent=2, default=str)
    print(f"Saved combined evidence to: {combined_file}")

    # Save embeddings if system was used
    if embedding_system:
        try:
            embedding_system.save()
            print(f"\nSaved vector embeddings: {embedding_system.get_stats()['total_embeddings']} embeddings")
        except Exception as e:
            print(f"Warning: Could not save embeddings: {e}")

    print(f"\n{'=' * 60}")
    print(f"Extraction Complete:")
    print(f"  PDFs processed: {len(pdf_results)}")
    print(f"  Excel files processed: {len(excel_results)}")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    main_extract_all()
