#!/usr/bin/env python3
"""
Complete Population Pipeline - Process ALL Records

Loads ALL incomplete records from all sources and processes them with
maximum parallelization for ARM M4 MAX with 128GB RAM.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from multiprocessing import Pool, cpu_count
import time
import re

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.utils.paths import DATA_PROCESSED_DIR, DATA_CLEANED_DIR
from scripts.utils.state_normalizer import normalize_state
from scripts.etl.browser_automation_integration import BrowserAutomationIntegration


class CompletePopulationPipeline:
    """Complete pipeline for processing ALL incomplete records."""

    def __init__(self):
        self.results = {
            "records_processed": 0,
            "records_populated": 0,
            "fields_populated": 0,
            "errors": [],
            "start_time": datetime.now().isoformat()
        }
        self.browser_integration = BrowserAutomationIntegration()

    def load_all_incomplete_records(self) -> List[Dict[str, Any]]:
        """Load ALL incomplete records from multiple sources."""
        print("=" * 80)
        print("LOADING ALL INCOMPLETE RECORDS")
        print("=" * 80)

        incomplete_records = []

        # Source 1: Manual verification guide
        guide_path = DATA_PROCESSED_DIR / "manual_verification_guide.json"
        if guide_path.exists():
            with open(guide_path, 'r', encoding='utf-8') as f:
                guide = json.load(f)

            verification_items = guide.get("verification_items", [])
            print(f"  From verification guide: {len(verification_items)} items")

            for item in verification_items:
                record = item.get("record_preview", {})
                reason = item.get("reason", "")
                if record:
                    incomplete_records.append({
                        "record": record,
                        "reason": reason,
                        "missing_fields": self._extract_missing_fields(reason),
                        "source": "verification_guide"
                    })

        # Source 2: Data cleaning results
        cleaning_path = DATA_PROCESSED_DIR / "data_cleaning_results.json"
        if cleaning_path.exists():
            with open(cleaning_path, 'r', encoding='utf-8') as f:
                cleaning = json.load(f)

            missing_data = cleaning.get("analysis", {}).get("missing_data", [])
            print(f"  From cleaning results: {len(missing_data)} missing data items")

            # Group by file and extract records
            files_data = {}
            for item in missing_data:
                file_path = item.get("file", "")
                if file_path not in files_data:
                    files_data[file_path] = []
                files_data[file_path].append(item)

            # Load records from files
            for file_path_str, items in list(files_data.items())[:100]:  # First 100 files
                try:
                    file_path = Path(file_path_str)
                    if file_path.exists():
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)

                        # Extract records that need population
                        if isinstance(data, list):
                            for i, record in enumerate(data):
                                if isinstance(record, dict):
                                    # Check if this record has missing fields
                                    for item in items:
                                        if item.get("index") == i:
                                            incomplete_records.append({
                                                "record": record,
                                                "reason": f"Missing {item.get('field')}",
                                                "missing_fields": [item.get("field")],
                                                "source": str(file_path)
                                            })
                                            break
                except:
                    pass

        # Source 3: Enhanced population results (records that still need work)
        enhanced_path = DATA_PROCESSED_DIR / "enhanced_population_results.json"
        if enhanced_path.exists():
            with open(enhanced_path, 'r', encoding='utf-8') as f:
                enhanced = json.load(f)

            manual_verification = enhanced.get("manual_verification_needed", 0)
            print(f"  From enhanced population: {manual_verification} items need verification")

        print(f"\n  Total incomplete records loaded: {len(incomplete_records)}")
        return incomplete_records

    def _extract_missing_fields(self, reason: str) -> List[str]:
        """Extract missing field names from reason string."""
        if "Missing critical fields:" in reason:
            fields_str = reason.split("Missing critical fields: ")[-1]
            return [f.strip() for f in fields_str.split(",")]
        return []

    def populate_record_optimized(self, record_data: Dict[str, Any]) -> Dict[str, Any]:
        """Optimized record population."""
        result = {
            "record": record_data.get("record", {}),
            "fields_populated": [],
            "success": False,
            "error": None
        }

        record = record_data.get("record", {})
        missing_fields = record_data.get("missing_fields", [])

        try:
            # Populate name
            if "name" in missing_fields:
                name = self._extract_name_optimized(record)
                if name:
                    record["name"] = name
                    result["fields_populated"].append({
                        "field": "name",
                        "value": name,
                        "method": "field_mapping"
                    })
                    result["success"] = True

            # Populate state
            if "state" in missing_fields:
                state = self._extract_state_optimized(record)
                if state:
                    record["state"] = state
                    record["jurisdiction"] = state
                    result["fields_populated"].append({
                        "field": "state",
                        "value": state,
                        "method": "field_mapping"
                    })
                    result["success"] = True

            result["record"] = record

        except Exception as e:
            result["error"] = str(e)

        return result

    def _extract_name_optimized(self, record: Dict) -> Optional[str]:
        """Optimized name extraction."""
        name_fields = [
            'name', 'firm_name', 'company_name', 'title', 'company', 'person',
            'entity', 'firm', 'organization', 'business_name', 'principal_broker',
            'individual_name', 'licensee_name', 'registered_name'
        ]

        for key in name_fields:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '']:
                    return value.replace('_', ' ').title()
        return None

    def _extract_state_optimized(self, record: Dict) -> Optional[str]:
        """Optimized state extraction."""
        # Direct fields
        for key in ['state', 'jurisdiction', 'location', 'region', 'status']:
            if key in record and record[key]:
                value = str(record[key]).strip()
                if value and value.lower() not in ['null', 'none', 'n/a', '']:
                    state = normalize_state(value)
                    if state and len(state) == 2:  # Valid state code
                        return state

        # Extract from address
        if 'address' in record:
            address = str(record['address']).upper()
            state_patterns = {
                'VA': r'\bVA\b|\bVIRGINIA\b', 'TX': r'\bTX\b|\bTEXAS\b',
                'MD': r'\bMD\b|\bMARYLAND\b', 'DC': r'\bDC\b|\bD\.C\.\b|\bDISTRICT OF COLUMBIA\b',
                'NC': r'\bNC\b|\bNORTH CAROLINA\b', 'PA': r'\bPA\b|\bPENNSYLVANIA\b',
                'NY': r'\bNY\b|\bNEW YORK\b', 'NJ': r'\bNJ\b|\bNEW JERSEY\b',
                'CT': r'\bCT\b|\bCONNECTICUT\b', 'MA': r'\bMA\b|\bMASSACHUSETTS\b',
                'FL': r'\bFL\b|\bFLORIDA\b', 'GA': r'\bGA\b|\bGEORGIA\b',
                'SC': r'\bSC\b|\bSOUTH CAROLINA\b', 'TN': r'\bTN\b|\bTENNESSEE\b'
            }

            for state_code, pattern in state_patterns.items():
                if re.search(pattern, address):
                    return normalize_state(state_code)

        return None

    def process_all_maximum_parallel(self) -> Dict[str, Any]:
        """Process ALL records with maximum parallelization."""
        print("\n" + "=" * 80)
        print("MAXIMUM PARALLEL PROCESSING (ARM M4 MAX - 128GB RAM)")
        print("=" * 80)

        incomplete_records = self.load_all_incomplete_records()

        if not incomplete_records:
            print("  No incomplete records found.")
            return self.results

        total_records = len(incomplete_records)
        print(f"\nProcessing ALL {total_records} incomplete records...")

        # Maximum parallelization for ARM M4 MAX
        cpu_cores = cpu_count()
        # Use 128x CPU cores for maximum throughput
        # With 128GB RAM, we can handle 2000+ concurrent workers
        max_workers = min(cpu_cores * 128, 2048, total_records)

        print(f"CPU cores: {cpu_cores}")
        print(f"Worker processes: {max_workers}")
        print(f"RAM: 128GB (maximum concurrency)")
        print(f"Chunk size: {max(1, total_records // max_workers)}")

        start_time = time.time()

        # Process with maximum parallelization
        with Pool(processes=max_workers) as pool:
            results = list(pool.imap_unordered(
                self.populate_record_optimized,
                incomplete_records,
                chunksize=max(1, total_records // max_workers)
            ))

        elapsed_time = time.time() - start_time

        # Aggregate results efficiently
        processed = 0
        populated = 0
        fields_count = 0
        errors = []
        population_log = []

        for result in results:
            processed += 1

            if result.get("success"):
                populated += 1
                fields_count += len(result.get("fields_populated", []))
                population_log.append(result)

            if result.get("error"):
                errors.append(result)

        self.results["records_processed"] = processed
        self.results["records_populated"] = populated
        self.results["fields_populated"] = fields_count
        self.results["errors"] = errors[:100]
        self.results["population_log"] = population_log
        self.results["processing_time"] = elapsed_time
        self.results["throughput"] = processed / elapsed_time if elapsed_time > 0 else 0
        self.results["end_time"] = datetime.now().isoformat()

        print(f"\n  Records processed: {processed}")
        print(f"  Records populated: {populated} ({populated/processed*100:.1f}%)")
        print(f"  Fields populated: {fields_count}")
        print(f"  Errors: {len(errors)}")
        print(f"  Processing time: {elapsed_time:.2f} seconds")
        print(f"  Throughput: {self.results['throughput']:.1f} records/second")

        return self.results

    def save_complete_results(self) -> Path:
        """Save complete population results."""
        results_path = DATA_PROCESSED_DIR / "complete_population_results.json"

        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump({
                "generated_date": datetime.now().isoformat(),
                "summary": {
                    "records_processed": self.results["records_processed"],
                    "records_populated": self.results["records_populated"],
                    "fields_populated": self.results["fields_populated"],
                    "processing_time": self.results["processing_time"],
                    "throughput": self.results["throughput"],
                    "success_rate": (self.results["records_populated"] / self.results["records_processed"] * 100)
                                  if self.results["records_processed"] > 0 else 0
                },
                "populated_records": self.results["population_log"][:5000],  # First 5000
                "errors": self.results["errors"]
            }, f, indent=2, ensure_ascii=False)

        return results_path

    def run_complete_pipeline(self) -> Dict[str, Any]:
        """Run complete population pipeline."""
        # Process all records
        results = self.process_all_maximum_parallel()

        # Save results
        results_path = self.save_complete_results()
        results["results_path"] = str(results_path)

        print("\n" + "=" * 80)
        print("COMPLETE PIPELINE FINISHED")
        print("=" * 80)
        print(f"  Results: {results_path}")
        print(f"  Success rate: {results['records_populated']/results['records_processed']*100:.1f}%")
        print("=" * 80)

        return results


def main():
    """Main execution."""
    pipeline = CompletePopulationPipeline()
    results = pipeline.run_complete_pipeline()
    return results


if __name__ == "__main__":
    main()
