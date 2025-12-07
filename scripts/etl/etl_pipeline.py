#!/usr/bin/env python3
"""
ETL/ELT Pipeline for Data Ingestion and Vector Embedding
Processes all data types and creates vector embeddings
"""

import os
import json
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Optional
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from vector_embeddings import VectorEmbeddingSystem

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RESEARCH_DIR = PROJECT_ROOT / "research"
EVIDENCE_DIR = PROJECT_ROOT / "evidence"

class ETLPipeline:
    """ETL Pipeline for processing all data types"""

    def __init__(self):
        self.embedding_system = VectorEmbeddingSystem()
        self.processed_files = set()
        self.load_processed_files()

    def load_processed_files(self):
        """Load list of already processed files"""
        processed_file = DATA_DIR / "vectors" / "processed_files.json"
        if processed_file.exists():
            try:
                with open(processed_file, 'r') as f:
                    self.processed_files = set(json.load(f))
            except:
                self.processed_files = set()

    def save_processed_files(self):
        """Save list of processed files"""
        processed_file = DATA_DIR / "vectors" / "processed_files.json"
        processed_file.parent.mkdir(parents=True, exist_ok=True)
        with open(processed_file, 'w') as f:
            json.dump(list(self.processed_files), f, indent=2)

    def process_csv(self, file_path: Path) -> int:
        """Process CSV file and create embeddings"""
        try:
            df = pd.read_csv(file_path)
            source = f"csv:{file_path.relative_to(PROJECT_ROOT)}"
            content_ids = self.embedding_system.embed_dataframe(df, source)
            print(f"  Processed CSV: {file_path.name} ({len(content_ids)} embeddings)")
            return len(content_ids)
        except Exception as e:
            print(f"  Error processing CSV {file_path.name}: {e}")
            return 0

    def process_json(self, file_path: Path) -> int:
        """Process JSON file and create embeddings"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            source = f"json:{file_path.relative_to(PROJECT_ROOT)}"
            content_ids = self.embedding_system.embed_json(data, source)
            print(f"  Processed JSON: {file_path.name} ({len(content_ids)} embeddings)")
            return len(content_ids)
        except Exception as e:
            print(f"  Error processing JSON {file_path.name}: {e}")
            return 0

    def process_pdf_text(self, file_path: Path) -> int:
        """Process PDF file (text already extracted)"""
        try:
            # Look for extracted PDF text in research directory
            pdf_name = file_path.stem
            extracted_file = RESEARCH_DIR / f"{pdf_name}_extracted.json"

            if extracted_file.exists():
                with open(extracted_file, 'r') as f:
                    pdf_data = json.load(f)

                # Extract text from PDF data structure
                text_content = ""
                if isinstance(pdf_data, dict):
                    text_content = pdf_data.get('text', '')
                    if not text_content and 'pages' in pdf_data:
                        text_content = "\n".join([page.get('text', '') for page in pdf_data['pages']])
                elif isinstance(pdf_data, list):
                    text_content = "\n".join([str(item) for item in pdf_data])

                if text_content:
                    source = f"pdf:{file_path.relative_to(PROJECT_ROOT)}"
                    metadata = {
                        'file_name': file_path.name,
                        'data_type': 'pdf'
                    }
                    content_id = self.embedding_system.embed_text(text_content, source, metadata)
                    print(f"  Processed PDF: {file_path.name} (1 embedding)")
                    return 1 if content_id else 0
            else:
                # Try to read PDF directly if pdftools available
                try:
                    import pdftools
                    text = pdftools.pdf_text(str(file_path))
                    source = f"pdf:{file_path.relative_to(PROJECT_ROOT)}"
                    metadata = {'file_name': file_path.name, 'data_type': 'pdf'}
                    content_id = self.embedding_system.embed_text(text, source, metadata)
                    print(f"  Processed PDF: {file_path.name} (1 embedding)")
                    return 1 if content_id else 0
                except:
                    print(f"  Skipping PDF {file_path.name}: no extracted text found")
                    return 0
        except Exception as e:
            print(f"  Error processing PDF {file_path.name}: {e}")
            return 0

    def process_excel(self, file_path: Path) -> int:
        """Process Excel file and create embeddings"""
        try:
            # Read all sheets
            excel_file = pd.ExcelFile(file_path)
            total_embeddings = 0

            for sheet_name in excel_file.sheet_names:
                df = pd.read_excel(excel_file, sheet_name=sheet_name)
                source = f"excel:{file_path.relative_to(PROJECT_ROOT)}:sheet_{sheet_name}"
                content_ids = self.embedding_system.embed_dataframe(df, source)
                total_embeddings += len(content_ids)

            print(f"  Processed Excel: {file_path.name} ({total_embeddings} embeddings)")
            return total_embeddings
        except Exception as e:
            print(f"  Error processing Excel {file_path.name}: {e}")
            return 0

    def process_file(self, file_path: Path, force: bool = False) -> int:
        """Process a single file"""
        file_str = str(file_path)

        # Check if already processed
        if not force and file_str in self.processed_files:
            return 0

        # Process based on file extension
        suffix = file_path.suffix.lower()

        if suffix == '.csv':
            count = self.process_csv(file_path)
        elif suffix == '.json':
            count = self.process_json(file_path)
        elif suffix == '.pdf':
            count = self.process_pdf_text(file_path)
        elif suffix in ['.xlsx', '.xls']:
            count = self.process_excel(file_path)
        else:
            print(f"  Skipping unsupported file type: {file_path.name}")
            return 0

        # Mark as processed
        if count > 0:
            self.processed_files.add(file_str)

        return count

    def process_directory(self, directory: Path, pattern: str = "**/*", force: bool = False) -> Dict[str, int]:
        """Process all files in a directory"""
        stats = {
            'csv': 0,
            'json': 0,
            'pdf': 0,
            'excel': 0,
            'total_files': 0,
            'total_embeddings': 0
        }

        if not directory.exists():
            print(f"Directory does not exist: {directory}")
            return stats

        # Find all files
        files = list(directory.glob(pattern))

        for file_path in files:
            if file_path.is_file():
                stats['total_files'] += 1
                suffix = file_path.suffix.lower()

                if suffix == '.csv':
                    count = self.process_file(file_path, force)
                    stats['csv'] += 1
                    stats['total_embeddings'] += count
                elif suffix == '.json':
                    count = self.process_file(file_path, force)
                    stats['json'] += 1
                    stats['total_embeddings'] += count
                elif suffix == '.pdf':
                    count = self.process_file(file_path, force)
                    stats['pdf'] += 1
                    stats['total_embeddings'] += count
                elif suffix in ['.xlsx', '.xls']:
                    count = self.process_file(file_path, force)
                    stats['excel'] += 1
                    stats['total_embeddings'] += count

        return stats

    def run_full_pipeline(self, force: bool = False) -> Dict[str, Any]:
        """Run full ETL pipeline on all data sources"""
        print("=" * 60)
        print("ETL Pipeline: Processing All Data Sources")
        print("=" * 60)

        results = {
            'ingress': {},
            'egress': {},
            'source': {},
            'research': {},
            'evidence': {},
            'scraped': {}
        }

        # Process ingress (raw data)
        print("\nProcessing INGRESS (raw data)...")
        raw_dir = DATA_DIR / "raw"
        if raw_dir.exists():
            results['ingress'] = self.process_directory(raw_dir, force=force)

        # Process source data
        print("\nProcessing SOURCE data...")
        source_dir = DATA_DIR / "source"
        if source_dir.exists():
            results['source'] = self.process_directory(source_dir, force=force)

        # Process cleaned data (egress)
        print("\nProcessing EGRESS (cleaned data)...")
        cleaned_dir = DATA_DIR / "cleaned"
        if cleaned_dir.exists():
            results['egress'] = self.process_directory(cleaned_dir, force=force)

        # Process research data
        print("\nProcessing RESEARCH data...")
        if RESEARCH_DIR.exists():
            results['research'] = self.process_directory(RESEARCH_DIR, force=force)

        # Process evidence
        print("\nProcessing EVIDENCE...")
        if EVIDENCE_DIR.exists():
            results['evidence'] = self.process_directory(EVIDENCE_DIR, "**/*.pdf", force=force)

        # Process scraped data
        print("\nProcessing SCRAPED data...")
        scraped_dir = DATA_DIR / "scraped"
        if scraped_dir.exists():
            results['scraped'] = self.process_directory(scraped_dir, force=force)

        # Save everything
        self.save_processed_files()
        self.embedding_system.save()

        # Print summary
        print("\n" + "=" * 60)
        print("ETL Pipeline Complete")
        print("=" * 60)

        total_embeddings = sum(r.get('total_embeddings', 0) for r in results.values())
        total_files = sum(r.get('total_files', 0) for r in results.values())

        print(f"Total files processed: {total_files}")
        print(f"Total embeddings created: {total_embeddings}")

        stats = self.embedding_system.get_stats()
        print(f"\nVector Store Stats:")
        print(f"  Total embeddings: {stats['total_embeddings']}")
        print(f"  Vector store size: {stats['vector_store_size']}")
        print(f"  Model: {stats['model']}")

        results['summary'] = {
            'total_files': total_files,
            'total_embeddings': total_embeddings,
            'vector_store_stats': stats
        }

        return results

def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='ETL Pipeline for Vector Embeddings')
    parser.add_argument('--file', type=str, help='Process a specific file')
    parser.add_argument('--force', action='store_true', help='Force reprocessing of all files')
    parser.add_argument('--dir', type=str, help='Process a specific directory')

    args = parser.parse_args()

    pipeline = ETLPipeline()

    if args.file:
        # Process single file
        file_path = Path(args.file)
        if not file_path.is_absolute():
            file_path = PROJECT_ROOT / file_path
        count = pipeline.process_file(file_path, force=args.force)
        pipeline.save_processed_files()
        pipeline.embedding_system.save()
        print(f"Processed file: {file_path.name} ({count} embeddings)")
    elif args.dir:
        # Process directory
        dir_path = Path(args.dir)
        if not dir_path.is_absolute():
            dir_path = PROJECT_ROOT / dir_path
        results = pipeline.process_directory(dir_path, force=args.force)
        pipeline.save_processed_files()
        pipeline.embedding_system.save()
        print(f"Processed directory: {dir_path}")
        print(f"Total embeddings: {results['total_embeddings']}")
    else:
        # Run full pipeline
        results = pipeline.run_full_pipeline(force=args.force)

        # Save results
        results_file = DATA_DIR / "vectors" / "etl_results.json"
        results_file.parent.mkdir(parents=True, exist_ok=True)
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\nResults saved to: {results_file}")

if __name__ == "__main__":
    main()
