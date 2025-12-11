#!/usr/bin/env python3
"""
Enhance Law References with Full Citation Text and Ground Truth Embeddings
Creates embeddings for complete law citations to use as ground truth
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import threading

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import PROJECT_ROOT

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("Installing sentence-transformers...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", "sentence-transformers"],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    from sentence_transformers import SentenceTransformer

MAX_WORKERS = os.cpu_count() or 16
print(f"🚀 Optimized for ARM M4 MAX: Using {MAX_WORKERS} parallel workers")


def create_full_citation_text(law_entry: Dict[str, Any], path: str = "") -> str:
    """Create full citation text from law entry for ground truth embedding"""
    parts = []

    # Add jurisdiction and law name
    if "name" in law_entry:
        parts.append(f"LAW: {law_entry['name']}")

    # Add full description
    if "description" in law_entry:
        parts.append(f"DESCRIPTION: {law_entry['description']}")

    # Add URL for reference
    if "url" in law_entry:
        parts.append(f"OFFICIAL_SOURCE: {law_entry['url']}")

    # Add ALL key sections with full citations
    if "key_sections" in law_entry:
        parts.append("STATUTORY_SECTIONS:")
        for section in law_entry["key_sections"]:
            parts.append(f"  - {section}")

    # Add relevance
    if "relevance" in law_entry:
        parts.append(f"RELEVANCE: {law_entry['relevance']}")

    # Add reporting forms if available
    if "reporting_forms" in law_entry:
        parts.append("REPORTING_MECHANISMS:")
        for form in law_entry["reporting_forms"]:
            form_text = f"  - {form.get('form_name', 'Unknown Form')}"
            if form.get('form_number'):
                form_text += f" (Form {form['form_number']})"
            if form.get('agency'):
                form_text += f" - {form['agency']}"
            if form.get('url'):
                form_text += f" - {form['url']}"
            if form.get('description'):
                form_text += f": {form['description']}"
            parts.append(form_text)

    # Add path for context
    if path:
        parts.append(f"JURISDICTION_PATH: {path}")

    return "\n".join(parts)


def collect_law_entries(data: Any, path: str = "", entries: List[Tuple[str, Dict[str, Any]]] = None) -> List[Tuple[str, Dict[str, Any]]]:
    """Collect all law entries that need full citation embeddings"""
    if entries is None:
        entries = []

    if isinstance(data, dict):
        # Check if this is a law entry (has name and key_sections or description)
        if ("name" in data and ("key_sections" in data or "description" in data)) and \
           data.get("name") not in ["metadata"]:
            entries.append((path, data))

        # Recursively collect from nested dictionaries
        for key, value in data.items():
            if key not in ["ground_truth_embedding", "ground_truth_text", "embedding", "embedding_text"]:
                new_path = f"{path}.{key}" if path else key
                collect_law_entries(value, new_path, entries)

    elif isinstance(data, list):
        for i, item in enumerate(data):
            new_path = f"{path}[{i}]"
            collect_law_entries(item, new_path, entries)

    return entries


def generate_ground_truth_embeddings_batch(texts_and_paths: List[Tuple[str, str]], model: SentenceTransformer) -> Dict[str, Tuple[List[float], str]]:
    """Generate ground truth embeddings for a batch of full law citations"""
    paths = [p for p, _ in texts_and_paths]
    texts = [t for _, t in texts_and_paths]

    # Batch encode all full citation texts at once
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=False, batch_size=32)

    # Return as dictionary mapping path to (embedding, text)
    results = {}
    for i, path in enumerate(paths):
        results[path] = (embeddings[i].tolist(), texts_and_paths[i][1])

    return results


def add_ground_truth_embeddings(data: Dict[str, Any], model: SentenceTransformer, max_workers: int = MAX_WORKERS) -> None:
    """Add ground truth embeddings for full law citations using parallel batch processing"""
    print(f"📊 Collecting law entries for ground truth embeddings...")
    entries = collect_law_entries(data)
    total_entries = len(entries)
    print(f"   Found {total_entries} law entries requiring ground truth embeddings")

    if total_entries == 0:
        print("⚠️  No law entries found requiring ground truth embeddings")
        return

    # Prepare full citation texts for batch processing
    texts_and_paths = []
    path_to_entry = {}
    for path, entry in entries:
        full_citation_text = create_full_citation_text(entry, path)
        texts_and_paths.append((path, full_citation_text))
        path_to_entry[path] = entry

    print(f"🚀 Generating ground truth embeddings using batch processing with {max_workers} parallel batches...")
    print(f"   Processing {total_entries} full law citations in optimized batches...")

    # Split into batches for parallel processing
    batch_size = max(1, total_entries // max_workers)
    batches = []
    for i in range(0, len(texts_and_paths), batch_size):
        batches.append(texts_and_paths[i:i + batch_size])

    print(f"   Created {len(batches)} batches (avg {len(batches[0]) if batches else 0} citations per batch)")

    # Process batches in parallel
    all_results = {}
    completed_batches = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all batches
        future_to_batch = {executor.submit(generate_ground_truth_embeddings_batch, batch, model): batch
                          for batch in batches}

        # Process completed batches
        for future in as_completed(future_to_batch):
            try:
                batch_results = future.result()
                all_results.update(batch_results)
                completed_batches += 1
                completed_items = len(all_results)
                if completed_batches % max(1, len(batches) // 10) == 0 or completed_batches == len(batches):
                    progress = (completed_items / total_entries) * 100
                    print(f"   Progress: {completed_items}/{total_entries} ({progress:.1f}%) - {completed_batches}/{len(batches)} batches")
            except Exception as e:
                batch = future_to_batch[future]
                print(f"   ⚠️  Error processing batch: {e}")
                import traceback
                traceback.print_exc()

    print(f"✅ Generated {len(all_results)} ground truth embeddings")
    print(f"📝 Applying ground truth embeddings to data structure...")

    # Apply ground truth embeddings back to data structure
    def apply_ground_truth_embeddings_recursive(data: Any, path: str = "") -> None:
        if isinstance(data, dict):
            # Check if this is a law entry
            if ("name" in data and ("key_sections" in data or "description" in data)) and \
               data.get("name") not in ["metadata"]:
                if path in all_results:
                    embedding, text = all_results[path]
                    data["ground_truth_embedding"] = embedding
                    data["ground_truth_text"] = text
                    data["is_ground_truth"] = True

            for key, value in data.items():
                if key not in ["ground_truth_embedding", "ground_truth_text", "embedding", "embedding_text", "is_ground_truth"]:
                    new_path = f"{path}.{key}" if path else key
                    apply_ground_truth_embeddings_recursive(value, new_path)

        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_path = f"{path}[{i}]"
                apply_ground_truth_embeddings_recursive(item, new_path)

    apply_ground_truth_embeddings_recursive(data)
    print(f"✅ Applied all ground truth embeddings to data structure")


def main():
    """Main function to enhance law references with ground truth embeddings"""
    import time
    start_time = time.time()

    print("=" * 80)
    print("🔍 Law Citation Ground Truth Enhancement - ARM M4 MAX Optimized")
    print("=" * 80)
    print(f"Using {MAX_WORKERS} parallel workers for maximum throughput\n")

    # Load existing law references
    law_file = PROJECT_ROOT / "ref" / "law" / "jurisdiction_references.json"
    if not law_file.exists():
        print(f"❌ Law references file not found: {law_file}")
        print("   Please run create_law_references.py first")
        sys.exit(1)

    print(f"📂 Loading law references from {law_file}...")
    with open(law_file, 'r', encoding='utf-8') as f:
        references = json.load(f)
    print(f"✅ Loaded law references\n")

    print("🤖 Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("✅ Model loaded\n")

    print("🚀 Generating ground truth embeddings for full law citations...")
    embedding_start = time.time()
    add_ground_truth_embeddings(references, model, MAX_WORKERS)
    embedding_time = time.time() - embedding_start
    print(f"⏱️  Ground truth embedding generation took {embedding_time:.2f} seconds\n")

    # Update metadata
    if "metadata" in references:
        references["metadata"]["ground_truth_embeddings_created"] = datetime.now().isoformat()
        references["metadata"]["ground_truth_version"] = "1.0.0"
        references["metadata"]["ground_truth_description"] = "Full law citation embeddings for use as ground truth in violation matching"

    # Save enhanced law references
    print(f"💾 Saving enhanced law references to {law_file}...")
    save_start = time.time()
    with open(law_file, 'w', encoding='utf-8') as f:
        json.dump(references, f, indent=2, ensure_ascii=False)
    save_time = time.time() - save_start
    print(f"✅ Saved in {save_time:.2f} seconds\n")

    # Count ground truth embeddings
    def count_ground_truth_embeddings(data: Any) -> int:
        """Count number of ground truth embeddings in data"""
        count = 0
        if isinstance(data, dict):
            if "ground_truth_embedding" in data:
                count += 1
            for value in data.values():
                count += count_ground_truth_embeddings(value)
        elif isinstance(data, list):
            for item in data:
                count += count_ground_truth_embeddings(item)
        return count

    ground_truth_count = count_ground_truth_embeddings(references)
    total_time = time.time() - start_time

    print("=" * 80)
    print("✅ Successfully enhanced law references with ground truth embeddings")
    print("=" * 80)
    print(f"   File: {law_file}")
    print(f"   Ground truth embeddings generated: {ground_truth_count}")
    print(f"   Model: all-MiniLM-L6-v2")
    print(f"   Dimensions: 384")
    print(f"   Parallel workers: {MAX_WORKERS}")
    print(f"   Total time: {total_time:.2f} seconds")
    print(f"   Throughput: {ground_truth_count/total_time:.1f} embeddings/second")
    print("=" * 80)
    print("\n📌 Note: Ground truth embeddings contain full law citations and can be used")
    print("   as authoritative reference for violation-law matching in ML pipeline.")


if __name__ == "__main__":
    main()
